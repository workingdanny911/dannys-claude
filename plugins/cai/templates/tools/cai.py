#!/usr/bin/env python3
"""CAI (Context As Infrastructure) CLI — AI-facing context search and analysis tool."""

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict, deque
from datetime import date, datetime
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Core utilities
# ---------------------------------------------------------------------------

def find_project_root() -> Path:
    """Walk up from cwd until we find .claude/ or .git/."""
    current = Path.cwd().resolve()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir() or (parent / ".git").is_dir():
            return parent
    return current


def read_config(project_root: Path) -> dict:
    """Parse configuration from .claude/rules/cai.md."""
    config = {
        "context_dir": "context",
        "source_roots": ["src/"],
    }
    rules_path = project_root / ".claude" / "rules" / "cai.md"
    if not rules_path.is_file():
        return config
    text = rules_path.read_text(encoding="utf-8")
    m = re.search(r"Context directory:\s*(.+)", text)
    if m:
        config["context_dir"] = m.group(1).strip()
    m = re.search(r"Source roots:\s*\[([^\]]*)\]", text)
    if m:
        roots = [r.strip().rstrip("/") + "/" for r in m.group(1).split(",") if r.strip()]
        if roots:
            config["source_roots"] = roots
    return config


def parse_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter between --- markers. Returns empty dict on failure."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}
    end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end < 0:
        return {}
    try:
        fm = yaml.safe_load("\n".join(lines[1:end]))
        return fm if isinstance(fm, dict) else {}
    except yaml.YAMLError:
        return {}


def walk_context_docs(context_dir: Path) -> list:
    """Return list of dicts: {path, rel_path, frontmatter, body_lines} for all .md files."""
    docs = []
    if not context_dir.is_dir():
        return docs
    for md in sorted(context_dir.rglob("*.md")):
        fm = parse_frontmatter(md)
        if not fm:
            continue
        try:
            body = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            body = ""
        body_lines = body.split("\n")
        # skip frontmatter lines for body content
        in_fm = False
        body_start = 0
        for i, line in enumerate(body_lines):
            if i == 0 and line.strip() == "---":
                in_fm = True
                continue
            if in_fm and line.strip() == "---":
                body_start = i + 1
                break
        docs.append({
            "path": md,
            "rel_path": str(md.relative_to(context_dir.parent)),
            "frontmatter": fm,
            "body_lines": body_lines,
            "body_start": body_start,
        })
    return docs


def extract_snippet(body_lines: list, line_start: int, line_end: int, max_chars: int = 200) -> str:
    """Extract snippet text from body lines (0-indexed). Truncate if needed."""
    snippet_lines = body_lines[line_start:line_end + 1]
    text = "\n".join(snippet_lines).strip()
    if len(text) > max_chars:
        text = text[:max_chars] + "..."
    return text


def find_heading_for_line(body_lines: list, line_idx: int) -> str:
    """Find the nearest heading above or at the given line."""
    for i in range(line_idx, -1, -1):
        if body_lines[i].startswith("#"):
            return body_lines[i].strip()
    return ""


def resolve_target(target: str, project_root: Path, config: dict) -> dict:
    """Auto-detect target as file, directory, or module name.

    Returns: {type: file|dir|module, path: str, module: str}
    """
    target_path = Path(target)
    abs_path = (project_root / target_path) if not target_path.is_absolute() else target_path

    if abs_path.is_file():
        module = _extract_module_from_path(str(target), config["source_roots"])
        return {"type": "file", "path": str(target), "module": module}

    if abs_path.is_dir():
        module = _extract_module_from_path(str(target).rstrip("/") + "/", config["source_roots"])
        return {"type": "dir", "path": str(target), "module": module}

    # Check if it's a module name (specs/{name}/_overview.md exists)
    context_dir = project_root / config["context_dir"]
    overview = context_dir / "specs" / target / "_overview.md"
    if overview.is_file():
        return {"type": "module", "path": str(target), "module": target}

    # Fallback: treat as module name even without overview
    return {"type": "module", "path": str(target), "module": target}


def _extract_module_from_path(filepath: str, source_roots: list) -> str:
    """Extract module name from a source file path given source roots."""
    filepath = filepath.replace("\\", "/")
    for root in source_roots:
        root = root.replace("\\", "/")
        if filepath.startswith(root):
            remainder = filepath[len(root):]
            parts = remainder.split("/")
            if parts and parts[0]:
                return parts[0]
    # Heuristic: second path component if path has multiple parts
    parts = filepath.strip("/").split("/")
    if len(parts) >= 2:
        return parts[-2] if len(parts) == 2 else parts[1] if parts[0] in ("src", "lib", "packages") else parts[0]
    return filepath.strip("/").split("/")[0] if parts else ""


def _module_from_spec_path(rel_path: str, context_dir_name: str) -> str:
    """Extract module name from a spec document's relative path."""
    # rel_path like context/specs/auth/_overview.md
    prefix = context_dir_name + "/specs/"
    if prefix in rel_path:
        after = rel_path.split(prefix, 1)[1]
        parts = after.split("/")
        if parts:
            return parts[0]
    return ""


# ---------------------------------------------------------------------------
# Search engine
# ---------------------------------------------------------------------------

def find_by_covers(target_path: str, docs: list) -> list:
    """Find docs whose covers field matches target_path."""
    results = []
    target_norm = target_path.replace("\\", "/")
    for doc in docs:
        covers = doc["frontmatter"].get("covers", [])
        if not isinstance(covers, list):
            continue
        for pattern in covers:
            pattern = str(pattern).replace("\\", "/")
            if _glob_match(target_norm, pattern):
                results.append(doc)
                break
    return results


def _glob_match(path: str, pattern: str) -> bool:
    """Simple glob matching: supports * and **."""
    # Convert glob pattern to regex
    regex = pattern.replace(".", r"\.")
    regex = regex.replace("**/", "(.+/)?")
    regex = regex.replace("**", ".*")
    regex = regex.replace("*", "[^/]*")
    regex = "^" + regex + "$"
    try:
        return bool(re.match(regex, path))
    except re.error:
        return pattern in path


def find_by_convention(target_path: str, source_roots: list, context_dir: Path) -> list:
    """Find spec docs by convention-based mapping: source module -> specs/{module}/."""
    module = _extract_module_from_path(target_path, source_roots)
    if not module:
        return []
    specs_dir = context_dir / "specs" / module
    if not specs_dir.is_dir():
        return []
    results = []
    for md in sorted(specs_dir.rglob("*.md")):
        fm = parse_frontmatter(md)
        if fm:
            try:
                body = md.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                body = ""
            body_lines = body.split("\n")
            body_start = 0
            in_fm = False
            for i, line in enumerate(body_lines):
                if i == 0 and line.strip() == "---":
                    in_fm = True
                    continue
                if in_fm and line.strip() == "---":
                    body_start = i + 1
                    break
            results.append({
                "path": md,
                "rel_path": str(md.relative_to(context_dir.parent)),
                "frontmatter": fm,
                "body_lines": body_lines,
                "body_start": body_start,
            })
    return results


def find_by_tags(keywords: list, docs: list) -> list:
    """Find docs whose tags overlap with keywords."""
    results = []
    kw_lower = [k.lower() for k in keywords]
    for doc in docs:
        tags = doc["frontmatter"].get("tags", [])
        if not isinstance(tags, list):
            continue
        tags_lower = [str(t).lower() for t in tags]
        overlap = sum(1 for k in kw_lower if k in tags_lower)
        if overlap > 0:
            results.append((doc, overlap))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


# Tags that match everything and add noise — exclude from scoring
STOP_TAGS = frozenset(["auto-generated", "auto generated", "generated", "draft"])


def filter_stop_tags(tags: list) -> list:
    """Remove generic/noisy tags from scoring."""
    return [t for t in tags if str(t).lower() not in STOP_TAGS]


def find_by_content(keywords: list, docs: list) -> list:
    """Find docs with keyword matches in headings and body. Returns (doc, score, matches)."""
    results = []
    kw_lower = [k.lower() for k in keywords]
    for doc in docs:
        body_lines = doc["body_lines"]
        body_start = doc.get("body_start", 0)
        score = 0
        matches = []
        for kw in kw_lower:
            # Check tags (weight 3) — excluding stop-tags
            tags = doc["frontmatter"].get("tags", [])
            if isinstance(tags, list):
                for t in filter_stop_tags(tags):
                    if kw in str(t).lower():
                        score += 3
                        break
            # Check headings (weight 2) and body (weight 1)
            heading_matched = False
            body_matched = False
            for i in range(body_start, len(body_lines)):
                line_lower = body_lines[i].lower()
                if kw in line_lower:
                    if body_lines[i].startswith("#"):
                        if not heading_matched:
                            score += 2
                            heading_matched = True
                        matches.append({"line": i, "type": "heading"})
                    else:
                        if not body_matched:
                            score += 1
                            body_matched = True
                        matches.append({"line": i, "type": "body"})
        if score > 0:
            results.append((doc, score, matches))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def calculate_relevance(match_reasons: list) -> str:
    """Determine relevance level from match reasons.

    - high: covers direct match OR 2+ keyword matches
    - medium: convention-based mapping OR 1 keyword match
    - low: tag-only match
    """
    if "covers" in match_reasons:
        return "high"
    reasons_set = set(match_reasons)
    keyword_count = sum(1 for r in match_reasons if r in ("tag", "heading", "body"))
    if keyword_count >= 2:
        return "high"
    if "convention" in reasons_set:
        return "medium"
    if keyword_count == 1:
        return "medium"
    return "low"


def _best_snippet_for_doc(doc: dict, keywords: list = None) -> dict:
    """Extract the most relevant snippet from a document."""
    body_lines = doc["body_lines"]
    body_start = doc.get("body_start", 0)
    if keywords:
        kw_lower = [k.lower() for k in keywords]
        for i in range(body_start, len(body_lines)):
            line_lower = body_lines[i].lower()
            if any(k in line_lower for k in kw_lower):
                start = max(body_start, i - 1)
                end = min(len(body_lines) - 1, i + 3)
                heading = find_heading_for_line(body_lines, i)
                text = extract_snippet(body_lines, start, end)
                return {"lines": f"{start + 1}-{end + 1}", "heading": heading, "text": text}
    # Fallback: first meaningful content after frontmatter
    for i in range(body_start, min(body_start + 30, len(body_lines))):
        if body_lines[i].strip() and not body_lines[i].startswith("---"):
            start = i
            end = min(len(body_lines) - 1, i + 4)
            heading = find_heading_for_line(body_lines, i)
            text = extract_snippet(body_lines, start, end)
            return {"lines": f"{start + 1}-{end + 1}", "heading": heading, "text": text}
    return {"lines": "1-1", "heading": "", "text": "(empty document)"}


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def _format_result_text(result: dict) -> str:
    """Format a single result for text output."""
    fm = result.get("frontmatter", {})
    rel = result["rel_path"]
    doc_type = fm.get("type", "unknown")
    confidence = fm.get("confidence", fm.get("status", ""))
    relevance = result.get("relevance", "med")
    tag = {"high": "high", "medium": "med", "low": "low", "transitive": "trans"}.get(relevance, relevance)
    padding = " " * max(0, 5 - len(tag))
    header = f"[{tag}]{padding} {rel} ({doc_type}"
    if confidence:
        header += f", {confidence}"
    header += ")"
    lines = [header]
    for snippet in result.get("snippets", []):
        line_range = snippet.get("lines", "")
        heading = snippet.get("heading", "")
        text = snippet.get("text", "")
        prefix = f"  L{line_range}: "
        if heading:
            lines.append(f"{prefix}{heading}")
            if text:
                indent = " " * len(prefix)
                # Skip lines that are the heading itself to avoid duplication
                text_lines = [tl for tl in text.split("\n") if tl.strip() != heading.strip()]
                for tl in text_lines[:3]:
                    if tl.strip():
                        lines.append(f"{indent}{tl}")
        elif text:
            first_line, *rest = text.split("\n")
            lines.append(f"{prefix}{first_line}")
            indent = " " * len(prefix)
            for tl in rest[:2]:
                lines.append(f"{indent}{tl}")
    return "\n".join(lines)


def _format_results(results: list, as_json: bool) -> str:
    """Format a list of results for output."""
    if as_json:
        json_results = []
        for r in results:
            fm = r.get("frontmatter", {})
            entry = {
                "path": r["rel_path"],
                "type": fm.get("type", "unknown"),
                "relevance": r.get("relevance", "medium"),
                "snippets": r.get("snippets", []),
            }
            if "confidence" in fm:
                entry["confidence"] = fm["confidence"]
            if "status" in fm:
                entry["status"] = fm["status"]
            if r.get("reason"):
                entry["reason"] = r["reason"]
            json_results.append(entry)
        return json.dumps({"results": json_results, "total": len(json_results)}, indent=2, ensure_ascii=False)

    if not results:
        return "0 documents found."
    lines = []
    for r in results:
        lines.append(_format_result_text(r))
        lines.append("")
    counts = defaultdict(int)
    for r in results:
        counts[r.get("relevance", "medium")] += 1
    summary_parts = []
    for level in ("high", "medium", "low", "transitive"):
        if counts[level]:
            summary_parts.append(f"{counts[level]} {level}")
    lines.append(f"{len(results)} documents found ({', '.join(summary_parts)})")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_suggest(args, project_root, config):
    context_dir = project_root / config["context_dir"]
    if not context_dir.is_dir():
        _error(f"Context directory not found: {context_dir}")

    target_info = resolve_target(args.target, project_root, config)
    module = target_info["module"]
    docs = walk_context_docs(context_dir)
    seen = set()
    results = []

    def _add(doc, relevance, reason, keywords=None):
        key = str(doc["path"])
        if key in seen:
            return
        seen.add(key)
        snippet = _best_snippet_for_doc(doc, keywords)
        results.append({
            **doc,
            "relevance": relevance,
            "reason": reason,
            "snippets": [snippet],
        })

    # 1. covers field matching
    for doc in find_by_covers(target_info["path"], docs):
        _add(doc, "high", f"covers field matches {target_info['path']}")

    # 2. convention-based mapping
    if module:
        for doc in find_by_convention(target_info["path"], config["source_roots"], context_dir):
            _add(doc, "medium", f"convention-based mapping: {module}")

    # 3. tag-based expansion (excluding stop-tags to prevent noise snowball)
    collected_tags = set()
    for r in results:
        tags = r.get("frontmatter", {}).get("tags", [])
        if isinstance(tags, list):
            for t in filter_stop_tags(tags):
                collected_tags.add(str(t).lower())
    if collected_tags:
        tag_kw = list(collected_tags)
        for doc, _overlap in find_by_tags(tag_kw, docs):
            _add(doc, "low", f"tag match: {', '.join(tag_kw)}", tag_kw)

    # 4. If module name is known, also search by module name as keyword
    if module and not results:
        for doc, score, matches in find_by_content([module], docs):
            rel = "medium" if score >= 2 else "low"
            _add(doc, rel, f"content match: {module}", [module])

    print(_format_results(results, args.json))


def cmd_search(args, project_root, config):
    context_dir = project_root / config["context_dir"]
    if not context_dir.is_dir():
        _error(f"Context directory not found: {context_dir}")

    keywords = args.keywords.split()
    if not keywords:
        _error("No keywords provided.")

    docs = walk_context_docs(context_dir)
    scored = find_by_content(keywords, docs)
    results = []
    for doc, score, matches in scored:
        if score < 2:
            continue  # filter out noise
        if score >= 4:
            relevance = "high"
        else:
            relevance = "medium"
        # Find best matching snippet
        snippets = []
        best_lines = set()
        for m in matches[:3]:
            line_idx = m["line"]
            if line_idx in best_lines:
                continue
            best_lines.add(line_idx)
            start = max(0, line_idx - 1)
            end = min(len(doc["body_lines"]) - 1, line_idx + 3)
            heading = find_heading_for_line(doc["body_lines"], line_idx)
            text = extract_snippet(doc["body_lines"], start, end)
            snippets.append({"lines": f"{start + 1}-{end + 1}", "heading": heading, "text": text})
        if not snippets:
            snippets = [_best_snippet_for_doc(doc, keywords)]
        results.append({
            **doc,
            "relevance": relevance,
            "reason": f"keyword match (score: {score})",
            "snippets": snippets[:2],
        })
    print(_format_results(results, args.json))


def cmd_budget(args, project_root, config):
    context_dir = project_root / config["context_dir"]
    if not context_dir.is_dir():
        _error(f"Context directory not found: {context_dir}")

    task_keywords = args.task.lower().split()
    n = args.n
    docs = walk_context_docs(context_dir)

    scored_docs = []
    for doc in docs:
        fm = doc["frontmatter"]
        score = 0

        # 1. Tag overlap (0-5) — excluding stop-tags
        tags = fm.get("tags", [])
        if isinstance(tags, list):
            tags_filtered = filter_stop_tags(tags)
            tags_lower = [str(t).lower() for t in tags_filtered]
            tag_overlap = sum(1 for kw in task_keywords if kw in tags_lower)
            score += min(tag_overlap, 5)

        # 2. Dependency proximity (0-5): if module matches task keywords
        module = _module_from_spec_path(doc["rel_path"], config["context_dir"])
        if module and module.lower() in task_keywords:
            score += 5
        elif module:
            for kw in task_keywords:
                if kw in module.lower():
                    score += 3
                    break

        # 3. Recency (0-3)
        last_synced = fm.get("last_synced")
        if last_synced:
            try:
                if isinstance(last_synced, date):
                    synced_date = last_synced
                else:
                    synced_date = datetime.strptime(str(last_synced), "%Y-%m-%d").date()
                days_ago = (date.today() - synced_date).days
                if days_ago <= 7:
                    score += 3
                elif days_ago <= 30:
                    score += 2
                elif days_ago <= 90:
                    score += 1
            except (ValueError, TypeError):
                pass

        # 4. Confidence (-1 to 5)
        confidence = fm.get("confidence", "")
        confidence_scores = {"verified": 5, "reviewed": 3, "draft": 0, "intent": -1}
        score += confidence_scores.get(str(confidence), 0)

        # 5. Type weight (0-3) — issue and roadmap promoted
        doc_type = fm.get("type", "")
        type_scores = {"spec": 3, "convention": 3, "decision": 2, "issue": 3, "roadmap": 2, "glossary": 1, "project": 1}
        doc_type_score = type_scores.get(str(doc_type), 0)
        if doc_type == "roadmap" and fm.get("status") == "completed":
            doc_type_score = 0
        score += doc_type_score

        # 6. Body content match (0-4)
        body_lines = doc.get("body_lines", [])
        body_start = doc.get("body_start", 0)
        body_text = "\n".join(body_lines[body_start:]).lower()
        body_hits = sum(1 for kw in task_keywords if kw in body_text)
        score += min(body_hits, 4)

        # 7. Draft penalty: reduce noise from unverified docs
        if str(confidence) == "draft":
            score = int(score * 0.6)

        scored_docs.append((doc, score))

    scored_docs.sort(key=lambda x: x[1], reverse=True)
    top_n = scored_docs[:n]

    # Graph expansion: follow depends_on/related_specs from high-relevance docs
    existing_paths = {str(d["rel_path"]) for d, _ in top_n}
    expanded_docs = []
    for doc, score in top_n:
        if score >= 12:
            fm = doc["frontmatter"]
            links = []
            for field in ("depends_on", "related_specs"):
                val = fm.get(field, [])
                if isinstance(val, list):
                    links.extend(str(v) for v in val)
            for link in links:
                if link not in existing_paths:
                    for d in docs:
                        if d["rel_path"] == link or d["rel_path"].endswith(link):
                            expanded_docs.append(d)
                            existing_paths.add(d["rel_path"])
                            break
    for d in expanded_docs:
        top_n.append((d, -1))  # -1 signals transitive relevance

    results = []
    for doc, score in top_n:
        snippet = _best_snippet_for_doc(doc, task_keywords)
        if score == -1:
            relevance = "transitive"
        elif score >= 12:
            relevance = "high"
        elif score >= 6:
            relevance = "medium"
        else:
            relevance = "low"
        results.append({
            **doc,
            "relevance": relevance,
            "reason": f"budget score: {score}" if score >= 0 else "transitive (via depends_on/related_specs)",
            "snippets": [snippet],
        })

    if args.json:
        json_results = []
        for r in results:
            fm = r.get("frontmatter", {})
            entry = {
                "path": r["rel_path"],
                "type": fm.get("type", "unknown"),
                "relevance": r.get("relevance", "medium"),
                "score": next(s for d, s in top_n if str(d["path"]) == str(r["path"])),
                "snippets": r.get("snippets", []),
            }
            if "confidence" in fm:
                entry["confidence"] = fm["confidence"]
            if "status" in fm:
                entry["status"] = fm["status"]
            json_results.append(entry)
        print(json.dumps({"results": json_results, "total": len(json_results), "max_score": top_n[0][1] if top_n else 0}, indent=2, ensure_ascii=False))
    else:
        print(_format_results(results, False))


def cmd_impact(args, project_root, config):
    context_dir = project_root / config["context_dir"]
    if not context_dir.is_dir():
        _error(f"Context directory not found: {context_dir}")

    target_info = resolve_target(args.target, project_root, config)
    module = target_info["module"]
    if not module:
        _error(f"Cannot determine module from target: {args.target}")

    # Build dependency graph
    # 1. Load project-level module_dependencies from specs/_overview.md
    project_overview = context_dir / "specs" / "_overview.md"
    project_deps = {}  # module -> [dependency modules]
    if project_overview.is_file():
        fm = parse_frontmatter(project_overview)
        md = fm.get("module_dependencies", {})
        if isinstance(md, dict):
            project_deps = {str(k): [str(v) for v in vs] if isinstance(vs, list) else [] for k, vs in md.items()}

    # 2. Load per-module depends_on from each module's _overview.md
    specs_dir = context_dir / "specs"
    module_depends_on = {}  # module -> [dependency modules]
    module_exports = {}  # module -> [exports]
    if specs_dir.is_dir():
        for child in sorted(specs_dir.iterdir()):
            if child.is_dir():
                overview = child / "_overview.md"
                if overview.is_file():
                    fm = parse_frontmatter(overview)
                    deps = fm.get("depends_on", [])
                    if isinstance(deps, list):
                        # Extract module names from dependency paths
                        dep_modules = []
                        for d in deps:
                            d_str = str(d)
                            # Handle paths like context/specs/auth/_overview.md
                            m = _module_from_spec_path(d_str, config["context_dir"])
                            if m:
                                dep_modules.append(m)
                            else:
                                # Might be a plain module name
                                dep_modules.append(d_str.split("/")[-1].replace("_overview.md", "").strip("/"))
                        module_depends_on[child.name] = dep_modules
                    exports = fm.get("exports", [])
                    if isinstance(exports, list):
                        module_exports[child.name] = [str(e) for e in exports]

    # Build reverse dependency graph (who depends on whom)
    reverse_graph = defaultdict(set)
    # From project_deps
    for mod, deps in project_deps.items():
        for dep in deps:
            reverse_graph[dep].add(mod)
    # From module depends_on
    for mod, deps in module_depends_on.items():
        for dep in deps:
            reverse_graph[dep].add(mod)

    # BFS from target module to find all downstream (dependents)
    visited = set()
    queue = deque([module])
    visited.add(module)
    layers = []  # [(module, depth)]
    bfs_order = []
    depth_map = {module: 0}
    while queue:
        current = queue.popleft()
        cur_depth = depth_map[current]
        if current != module:
            bfs_order.append((current, cur_depth))
        for dependent in sorted(reverse_graph.get(current, set())):
            if dependent not in visited:
                visited.add(dependent)
                depth_map[dependent] = cur_depth + 1
                queue.append(dependent)

    direct_count = sum(1 for _, d in bfs_order if d == 1)
    indirect_count = sum(1 for _, d in bfs_order if d > 1)

    # Also collect upstream (modules this module depends on) via BFS
    forward_graph = defaultdict(set)
    for mod, deps in project_deps.items():
        for dep in deps:
            forward_graph[mod].add(dep)
    for mod, deps in module_depends_on.items():
        for dep in deps:
            forward_graph[mod].add(dep)

    upstream_visited = set()
    upstream_queue = deque([module])
    upstream_visited.add(module)
    upstream_order = []
    upstream_depth = {module: 0}
    while upstream_queue:
        current = upstream_queue.popleft()
        cur_depth = upstream_depth[current]
        if current != module:
            upstream_order.append((current, cur_depth))
        for dep in sorted(forward_graph.get(current, set())):
            if dep not in upstream_visited:
                upstream_visited.add(dep)
                upstream_depth[dep] = cur_depth + 1
                upstream_queue.append(dep)

    upstream_direct = sum(1 for _, d in upstream_order if d == 1)
    upstream_indirect = sum(1 for _, d in upstream_order if d > 1)

    if args.json:
        downstream_list = []
        for mod, depth in bfs_order:
            entry = {
                "module": mod,
                "depth": depth,
                "type": "direct" if depth == 1 else "indirect",
            }
            if mod in module_exports:
                entry["exports"] = module_exports[mod]
            overview = context_dir / "specs" / mod / "_overview.md"
            if overview.is_file():
                entry["spec"] = str(overview.relative_to(context_dir.parent))
            downstream_list.append(entry)
        upstream_list = []
        for mod, depth in upstream_order:
            entry = {
                "module": mod,
                "depth": depth,
                "type": "direct" if depth == 1 else "indirect",
            }
            if mod in module_exports:
                entry["exports"] = module_exports[mod]
            overview = context_dir / "specs" / mod / "_overview.md"
            if overview.is_file():
                entry["spec"] = str(overview.relative_to(context_dir.parent))
            upstream_list.append(entry)
        output = {
            "target_module": module,
            "downstream": {
                "modules": downstream_list,
                "total": len(bfs_order),
                "direct": direct_count,
                "indirect": indirect_count,
            },
            "upstream": {
                "modules": upstream_list,
                "total": len(upstream_order),
                "direct": upstream_direct,
                "indirect": upstream_indirect,
            },
        }
        if module in module_exports:
            output["target_exports"] = module_exports[module]
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        lines = [f"Module: {module}"]
        if module in module_exports:
            lines.append(f"Exports affected: {', '.join(module_exports[module])}")

        # Downstream
        lines.append("")
        lines.append("Downstream (이 모듈에 의존하는):")
        if bfs_order:
            lines.append(f"  {module}")
            _print_impact_tree(lines, module, reverse_graph, module_exports, context_dir, config, visited_print=set(), depth=1, prefix="  ")
            lines.append(f"  → {len(bfs_order)} modules ({direct_count} direct, {indirect_count} indirect)")
        else:
            lines.append("  (없음)")

        # Upstream
        lines.append("")
        lines.append("Upstream (이 모듈이 의존하는):")
        if upstream_order:
            lines.append(f"  {module}")
            _print_impact_tree(lines, module, forward_graph, module_exports, context_dir, config, visited_print=set(), depth=1, prefix="  ")
            lines.append(f"  → {len(upstream_order)} modules ({upstream_direct} direct, {upstream_indirect} indirect)")
        else:
            lines.append("  (없음)")

        lines.append("")
        total = len(bfs_order) + len(upstream_order)
        lines.append(f"Total impact: {total} modules (downstream {len(bfs_order)}, upstream {len(upstream_order)})")
        print("\n".join(lines))


def _print_impact_tree(lines, current_module, reverse_graph, module_exports, context_dir, config, visited_print, depth, prefix):
    """Recursively print impact tree."""
    dependents = sorted(reverse_graph.get(current_module, set()))
    for i, dep in enumerate(dependents):
        if dep in visited_print:
            continue
        visited_print.add(dep)
        is_last = (i == len(dependents) - 1)
        connector = "\u2514\u2500\u2500 " if is_last else "\u251c\u2500\u2500 "
        # Find why this module depends on current
        dep_info = ""
        overview = context_dir / "specs" / dep / "_overview.md"
        if overview.is_file():
            fm = parse_frontmatter(overview)
            depends = fm.get("depends_on", [])
            if isinstance(depends, list):
                for d in depends:
                    if current_module in str(d):
                        dep_info = f" (depends_on: {current_module})"
                        break

        lines.append(f"{prefix}{connector}{dep}{dep_info}")

        # Show spec snippet if available
        if overview.is_file():
            try:
                body = overview.read_text(encoding="utf-8")
                body_lines = body.split("\n")
                for j, line in enumerate(body_lines):
                    if current_module.lower() in line.lower() and not line.startswith("---"):
                        snippet_text = line.strip()[:80]
                        child_prefix = prefix + ("\u2502   " if not is_last else "    ")
                        # Use 1-indexed line numbers for display
                        lines.append(f"{child_prefix}\u2514\u2500\u2500 {config['context_dir']}/specs/{dep}/_overview.md L{j + 1}: \"{snippet_text}\"")
                        break
            except (OSError, UnicodeDecodeError):
                pass

        child_prefix = prefix + ("    " if is_last else "\u2502   ")
        _print_impact_tree(lines, dep, reverse_graph, module_exports, context_dir, config, visited_print, depth + 1, child_prefix)


def cmd_diff(args, project_root, config):
    context_dir = project_root / config["context_dir"]
    if not context_dir.is_dir():
        _error(f"Context directory not found: {context_dir}")

    target_info = resolve_target(args.target, project_root, config)

    # Find the spec doc(s)
    docs = walk_context_docs(context_dir)
    spec_docs = []

    # If target is a context doc path itself
    target_path = project_root / args.target
    if target_path.is_file() and str(target_path).startswith(str(context_dir)):
        fm = parse_frontmatter(target_path)
        if fm:
            try:
                body = target_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                body = ""
            body_lines = body.split("\n")
            body_start = 0
            in_fm = False
            for i, line in enumerate(body_lines):
                if i == 0 and line.strip() == "---":
                    in_fm = True
                    continue
                if in_fm and line.strip() == "---":
                    body_start = i + 1
                    break
            spec_docs.append({
                "path": target_path,
                "rel_path": str(target_path.relative_to(project_root)),
                "frontmatter": fm,
                "body_lines": body_lines,
                "body_start": body_start,
            })
    else:
        # Find specs for this module
        module = target_info["module"]
        if module:
            for doc in docs:
                doc_module = _module_from_spec_path(doc["rel_path"], config["context_dir"])
                if doc_module == module and doc["frontmatter"].get("type") == "spec":
                    spec_docs.append(doc)

    if not spec_docs:
        _error(f"No spec documents found for target: {args.target}")

    results = []
    for doc in spec_docs:
        fm = doc["frontmatter"]
        last_synced = fm.get("last_synced")
        if not last_synced:
            results.append({
                **doc,
                "relevance": "medium",
                "reason": "no last_synced date",
                "snippets": [{"lines": "-", "heading": "No last_synced", "text": "Cannot determine changes: last_synced not set."}],
                "diff_summary": "N/A (no last_synced)",
            })
            continue

        synced_str = str(last_synced)

        # Determine source files from covers or convention
        covers = fm.get("covers", [])
        source_paths = []
        if isinstance(covers, list) and covers:
            source_paths = [str(c) for c in covers]
        else:
            # Convention-based: source_root/{module}/**
            module = _module_from_spec_path(doc["rel_path"], config["context_dir"])
            if module:
                for root in config["source_roots"]:
                    source_paths.append(f"{root}{module}/")

        if not source_paths:
            results.append({
                **doc,
                "relevance": "low",
                "reason": "no source paths determined",
                "snippets": [{"lines": "-", "heading": "No source mapping", "text": "Cannot determine source files for this spec."}],
                "diff_summary": "N/A",
            })
            continue

        # Run git log
        git_log = ""
        git_diff_stat = ""
        try:
            cmd = ["git", "log", f"--since={synced_str}", "--oneline", "--"]
            cmd.extend(source_paths)
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(project_root), timeout=10)
            git_log = result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            git_log = "(git not available)"

        try:
            cmd = ["git", "diff", f"--stat", f"HEAD@{{'{synced_str}'}}", "--"]
            cmd.extend(source_paths)
            result = subprocess.run(
                ["git", "log", f"--since={synced_str}", "--stat", "--oneline", "--"],
                capture_output=True, text=True, cwd=str(project_root), timeout=10,
            )
            git_diff_stat = result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            git_diff_stat = ""

        if not git_log:
            relevance = "low"
            diff_text = f"No changes since {synced_str}."
        else:
            commit_count = len(git_log.split("\n"))
            relevance = "high" if commit_count >= 5 else "medium"
            diff_text = git_log

        snippets = [{"lines": "-", "heading": f"Changes since {synced_str}", "text": diff_text[:300]}]
        results.append({
            **doc,
            "relevance": relevance,
            "reason": f"diff since {synced_str}",
            "snippets": snippets,
        })

    if args.json:
        json_results = []
        for r in results:
            fm = r.get("frontmatter", {})
            entry = {
                "path": r["rel_path"],
                "type": fm.get("type", "unknown"),
                "last_synced": str(fm.get("last_synced", "")),
                "relevance": r.get("relevance", "medium"),
                "snippets": r.get("snippets", []),
            }
            json_results.append(entry)
        print(json.dumps({"results": json_results, "total": len(json_results)}, indent=2, ensure_ascii=False))
    else:
        for r in results:
            print(_format_result_text(r))
            print()
        print(f"{len(results)} spec(s) checked.")


def cmd_status(args, project_root, config):
    context_dir = project_root / config["context_dir"]
    if not context_dir.is_dir():
        _error(f"Context directory not found: {context_dir}")

    docs = walk_context_docs(context_dir)
    total = len(docs)
    type_counts = defaultdict(int)
    confidence_counts = defaultdict(int)
    status_counts = defaultdict(int)
    stale_count = 0
    latest_synced = None

    for doc in docs:
        fm = doc["frontmatter"]
        doc_type = fm.get("type", "unknown")
        type_counts[doc_type] += 1

        confidence = fm.get("confidence", "")
        if confidence:
            confidence_counts[str(confidence)] += 1

        status = fm.get("status", "")
        if status:
            status_counts[str(status)] += 1

        last_synced = fm.get("last_synced")
        if last_synced:
            try:
                if isinstance(last_synced, date):
                    synced_date = last_synced
                else:
                    synced_date = datetime.strptime(str(last_synced), "%Y-%m-%d").date()
                days_ago = (date.today() - synced_date).days
                if days_ago > 30:
                    stale_count += 1
                if latest_synced is None or synced_date > latest_synced:
                    latest_synced = synced_date
            except (ValueError, TypeError):
                pass

    if args.json:
        output = {
            "total": total,
            "by_type": dict(type_counts),
            "by_confidence": dict(confidence_counts),
            "by_status": dict(status_counts),
            "stale_count": stale_count,
            "latest_synced": str(latest_synced) if latest_synced else None,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        lines = [f"Context Health Summary ({total} documents)"]
        lines.append("")
        lines.append("By type:")
        for t, c in sorted(type_counts.items()):
            lines.append(f"  {t}: {c}")
        if confidence_counts:
            lines.append("")
            lines.append("By confidence:")
            for c, n in sorted(confidence_counts.items()):
                lines.append(f"  {c}: {n}")
        if status_counts:
            lines.append("")
            lines.append("By status:")
            for s, n in sorted(status_counts.items()):
                lines.append(f"  {s}: {n}")
        lines.append("")
        lines.append(f"Stale (>30 days): {stale_count}")
        if latest_synced:
            lines.append(f"Latest sync: {latest_synced}")
        print("\n".join(lines))


def cmd_list(args, project_root, config):
    context_dir = project_root / config["context_dir"]
    if not context_dir.is_dir():
        _error(f"Context directory not found: {context_dir}")

    docs = walk_context_docs(context_dir)
    filtered = []
    for doc in docs:
        fm = doc["frontmatter"]
        if args.type and fm.get("type") != args.type:
            continue
        if args.tag:
            tags = fm.get("tags", [])
            if not isinstance(tags, list):
                continue
            tags_lower = [str(t).lower() for t in tags]
            if args.tag.lower() not in tags_lower:
                continue
        filtered.append(doc)

    if args.json:
        json_results = []
        for doc in filtered:
            fm = doc["frontmatter"]
            entry = {"path": doc["rel_path"], "type": fm.get("type", "unknown"), "tags": fm.get("tags", [])}
            if "confidence" in fm:
                entry["confidence"] = fm["confidence"]
            if "status" in fm:
                entry["status"] = fm["status"]
            if "last_synced" in fm:
                entry["last_synced"] = str(fm["last_synced"])
            json_results.append(entry)
        print(json.dumps({"results": json_results, "total": len(json_results)}, indent=2, ensure_ascii=False))
    else:
        if not filtered:
            print("0 documents found.")
            return
        for doc in filtered:
            fm = doc["frontmatter"]
            doc_type = fm.get("type", "unknown")
            tags = fm.get("tags", [])
            tag_str = ", ".join(str(t) for t in tags) if isinstance(tags, list) else ""
            confidence = fm.get("confidence", fm.get("status", ""))
            meta = f"({doc_type}"
            if confidence:
                meta += f", {confidence}"
            meta += ")"
            line = f"  {doc['rel_path']} {meta}"
            if tag_str:
                line += f" [{tag_str}]"
            print(line)
        print(f"\n{len(filtered)} documents found.")


def cmd_validate(args, project_root, config):
    context_dir = project_root / config["context_dir"]
    if not context_dir.is_dir():
        _error(f"Context directory not found: {context_dir}")

    docs = walk_context_docs(context_dir)
    # Also scan for .md files without valid frontmatter
    all_md = sorted(context_dir.rglob("*.md"))

    errors = []
    warnings = []
    fixed = 0

    # Required fields by type
    common_required = ["type", "tags", "last_synced"]
    type_required = {
        "spec": ["level", "confidence"],
        "decision": ["status"],
        "roadmap": ["status"],
        "issue": ["severity"],
    }
    type_enums = {
        "type": ["decision", "issue", "spec", "convention", "roadmap", "glossary", "project"],
        "level": ["project", "module", "component"],
        "confidence": ["intent", "draft", "reviewed", "verified"],
        "status_decision": ["proposed", "accepted", "deprecated", "superseded"],
        "status_roadmap": ["exploring", "planned", "in-progress", "completed"],
        "severity": ["low", "medium", "high", "critical"],
    }

    for md_path in all_md:
        rel = str(md_path.relative_to(context_dir.parent))
        fm = parse_frontmatter(md_path)
        if not fm:
            # Check if it has --- markers but broken YAML
            try:
                text = md_path.read_text(encoding="utf-8")
                if text.startswith("---"):
                    errors.append(f"{rel}: malformed frontmatter (YAML parse error)")
                # Files without frontmatter at all are skipped silently
            except (OSError, UnicodeDecodeError):
                pass
            continue

        doc_type = fm.get("type", "")

        # Check common required fields
        for field in common_required:
            if field not in fm:
                if args.fix and field == "last_synced":
                    _fix_add_field(md_path, "last_synced", date.today().isoformat())
                    fixed += 1
                    warnings.append(f"{rel}: added missing last_synced (set to today)")
                elif args.fix and field == "tags":
                    _fix_add_field(md_path, "tags", [])
                    fixed += 1
                    warnings.append(f"{rel}: added missing tags (set to [])")
                else:
                    errors.append(f"{rel}: missing required field '{field}'")

        # Check type enum
        if doc_type and doc_type not in type_enums["type"]:
            errors.append(f"{rel}: invalid type '{doc_type}' (expected: {', '.join(type_enums['type'])})")

        # Check type-specific required fields
        if doc_type in type_required:
            for field in type_required[doc_type]:
                if field not in fm:
                    errors.append(f"{rel}: missing required field '{field}' for type '{doc_type}'")

        # Check enum values
        if doc_type == "spec":
            level = fm.get("level", "")
            if level and level not in type_enums["level"]:
                errors.append(f"{rel}: invalid level '{level}'")
            conf = fm.get("confidence", "")
            if conf and conf not in type_enums["confidence"]:
                errors.append(f"{rel}: invalid confidence '{conf}'")
        elif doc_type == "decision":
            status = fm.get("status", "")
            if status and status not in type_enums["status_decision"]:
                errors.append(f"{rel}: invalid status '{status}' for decision")
        elif doc_type == "roadmap":
            status = fm.get("status", "")
            if status and status not in type_enums["status_roadmap"]:
                errors.append(f"{rel}: invalid status '{status}' for roadmap")
        elif doc_type == "issue":
            sev = fm.get("severity", "")
            if sev and sev not in type_enums["severity"]:
                errors.append(f"{rel}: invalid severity '{sev}'")

    if args.json:
        output = {
            "errors": errors,
            "warnings": warnings,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "fixed": fixed,
            "valid": len(errors) == 0,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        if errors:
            print("Errors:")
            for e in errors:
                print(f"  [ERROR] {e}")
        if warnings:
            print("Warnings:")
            for w in warnings:
                print(f"  [WARN]  {w}")
        if not errors and not warnings:
            print("All documents valid.")
        else:
            print(f"\n{len(errors)} errors, {len(warnings)} warnings" + (f", {fixed} auto-fixed" if fixed else ""))

    if errors:
        sys.exit(1)


def _fix_add_field(filepath: Path, field: str, value):
    """Add a missing field to frontmatter."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return
    # Find closing ---
    end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end < 0:
        return
    # Format value
    if isinstance(value, list):
        val_str = f"{field}: []"
    elif isinstance(value, str):
        val_str = f"{field}: {value}"
    else:
        val_str = f"{field}: {value}"
    lines.insert(end, val_str)
    filepath.write_text("\n".join(lines), encoding="utf-8")


def cmd_update_synced(args, project_root, config):
    target_path = Path(args.target)
    if not target_path.is_absolute():
        target_path = project_root / target_path
    if not target_path.is_file():
        _error(f"File not found: {args.target}")

    fm = parse_frontmatter(target_path)
    if not fm:
        _error(f"No valid frontmatter in: {args.target}")

    today_str = date.today().isoformat()
    try:
        text = target_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        _error(f"Cannot read file: {args.target}")

    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        _error(f"No frontmatter found in: {args.target}")

    end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end < 0:
        _error(f"Malformed frontmatter in: {args.target}")

    # Find existing last_synced line and replace, or insert before closing ---
    found = False
    for i in range(1, end):
        if lines[i].startswith("last_synced:"):
            lines[i] = f"last_synced: {today_str}"
            found = True
            break
    if not found:
        lines.insert(end, f"last_synced: {today_str}")

    target_path.write_text("\n".join(lines), encoding="utf-8")

    rel = str(target_path.relative_to(project_root)) if str(target_path).startswith(str(project_root)) else str(target_path)

    if args.json:
        print(json.dumps({"path": rel, "last_synced": today_str, "status": "updated"}, indent=2))
    else:
        print(f"Updated last_synced to {today_str}: {rel}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _error(message: str):
    """Print error and exit with code 1."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Main / argparse
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="cc",
        description="CAI CLI — search and analyze context documents for AI coding agents.",
    )
    parser.add_argument("--json", action="store_true", help="Output in JSON format instead of text")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # suggest
    p_suggest = subparsers.add_parser(
        "suggest",
        help="Find related context documents for a file, directory, or module",
        description="Given a source file path, directory, or module name, find and rank related context documents with snippets.",
    )
    p_suggest.add_argument("target", help="File path, directory path, or module name")

    # search
    p_search = subparsers.add_parser(
        "search",
        help="Keyword-based search across all context documents",
        description="Search context documents by keywords (space-separated, OR logic). More keyword matches = higher relevance.",
    )
    p_search.add_argument("keywords", help="Space-separated keywords to search for (use quotes for multiple)")

    # budget
    p_budget = subparsers.add_parser(
        "budget",
        help="Rank top N most relevant documents for a task",
        description="Given a task description, score and rank context documents by relevance (tag overlap, dependency proximity, recency, confidence, type weight).",
    )
    p_budget.add_argument("--task", required=True, help="Task description (keywords extracted automatically)")
    p_budget.add_argument("-n", type=int, default=10, help="Number of top documents to return (default: 10)")

    # impact
    p_impact = subparsers.add_parser(
        "impact",
        help="Trace downstream modules affected by changes to a target",
        description="Build full dependency graph and BFS-traverse to find all modules affected by changes to the target module.",
    )
    p_impact.add_argument("target", help="File path, directory path, or module name")

    # diff
    p_diff = subparsers.add_parser(
        "diff",
        help="Show source code changes since a spec was last synced",
        description="For a spec document, show git log of source changes since last_synced date.",
    )
    p_diff.add_argument("target", help="Spec file path or module name")

    # status
    p_status = subparsers.add_parser(
        "status",
        help="Show overall context health summary",
        description="Display total document count, distribution by type/confidence/status, stale count, and latest sync date.",
    )

    # list
    p_list = subparsers.add_parser(
        "list",
        help="List context documents with optional filters",
        description="List all context documents, optionally filtered by type and/or tag.",
    )
    p_list.add_argument("--type", help="Filter by document type (spec, decision, convention, issue, roadmap, glossary, project)")
    p_list.add_argument("--tag", help="Filter by tag (case-insensitive)")

    # validate
    p_validate = subparsers.add_parser(
        "validate",
        help="Validate frontmatter schema of all context documents",
        description="Check all context documents for missing required fields, invalid enum values, and malformed frontmatter.",
    )
    p_validate.add_argument("--fix", action="store_true", help="Auto-fix fixable issues (e.g., missing last_synced)")

    # update-synced
    p_update_synced = subparsers.add_parser(
        "update-synced",
        help="Update last_synced date of a document to today",
        description="Set the last_synced field of the specified context document to today's date.",
    )
    p_update_synced.add_argument("target", help="Path to the context document to update")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    project_root = find_project_root()
    config = read_config(project_root)

    commands = {
        "suggest": cmd_suggest,
        "search": cmd_search,
        "budget": cmd_budget,
        "impact": cmd_impact,
        "diff": cmd_diff,
        "status": cmd_status,
        "list": cmd_list,
        "validate": cmd_validate,
        "update-synced": cmd_update_synced,
    }

    handler = commands.get(args.command)
    if handler:
        handler(args, project_root, config)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
