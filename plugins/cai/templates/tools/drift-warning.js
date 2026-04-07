#!/usr/bin/env node
"use strict";

// drift-warning.js — PreToolUse hook for CAI (Context As Infrastructure)
// Checks if a spec related to the file being edited is stale.
// Outputs warning to stderr if stale. Always exits 0.
// Zero npm dependencies — uses only Node.js built-ins.

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

function main() {
  try {
    const input = readStdin();
    const toolInput = JSON.parse(input);

    const filePath = extractFilePath(toolInput);
    if (!filePath) return;

    const projectRoot = findProjectRoot(filePath);
    if (!projectRoot) return;

    const config = readConfig(projectRoot);
    const contextDir = path.join(projectRoot, config.contextDirectory);
    const specsDir = path.join(contextDir, "specs");

    if (!fs.existsSync(specsDir)) return;

    const relativeFile = path.relative(projectRoot, path.resolve(filePath));
    const matchingSpec = findMatchingSpec(specsDir, relativeFile, config.sourceRoots);
    if (!matchingSpec) return;

    const frontmatter = parseFrontmatter(matchingSpec);
    if (!frontmatter.last_synced) return;

    const coveredPaths = getCoveredSourcePaths(matchingSpec, specsDir, config.sourceRoots);
    const isStale = checkStale(coveredPaths, frontmatter.last_synced, projectRoot);
    if (isStale) {
      const specRel = path.relative(projectRoot, matchingSpec);
      process.stderr.write(
        `[cai] Warning: spec "${specRel}" may be stale ` +
        `(last synced: ${frontmatter.last_synced}). ` +
        `Review the spec before relying on it — trust code over outdated spec.\n`
      );
    }
  } catch (_) {
    // Fail silently — never block the operation
  }
}

function readStdin() {
  return fs.readFileSync(0, "utf-8");
}

function extractFilePath(toolInput) {
  // Edit tool: file_path field
  // Write tool: file_path field
  // MultiEdit tool: file_path field
  if (toolInput && typeof toolInput.file_path === "string") {
    return toolInput.file_path;
  }
  // Fallback: check for path field
  if (toolInput && typeof toolInput.path === "string") {
    return toolInput.path;
  }
  return null;
}

function findProjectRoot(filePath) {
  let dir = path.dirname(path.resolve(filePath));
  const root = path.parse(dir).root;
  while (dir !== root) {
    if (fs.existsSync(path.join(dir, ".claude"))) {
      return dir;
    }
    // Also check for context/ directory as a fallback signal
    if (fs.existsSync(path.join(dir, "context", "specs"))) {
      return dir;
    }
    dir = path.dirname(dir);
  }
  return null;
}

function readConfig(projectRoot) {
  const defaults = {
    contextDirectory: "context",
    sourceRoots: ["src/"],
  };

  const rulesPath = path.join(projectRoot, ".claude", "rules", "cai.md");
  if (!fs.existsSync(rulesPath)) return defaults;

  try {
    const content = fs.readFileSync(rulesPath, "utf-8");

    const ctxMatch = content.match(/^Context directory:\s*(.+)$/m);
    if (ctxMatch) {
      defaults.contextDirectory = ctxMatch[1].trim();
    }

    const srcMatch = content.match(/^Source roots:\s*\[([^\]]*)\]$/m);
    if (srcMatch) {
      defaults.sourceRoots = srcMatch[1]
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);
    }
  } catch (_) {
    // Use defaults on any read error
  }

  return defaults;
}

function findMatchingSpec(specsDir, relativeFile, sourceRoots) {
  const specFiles = walkMarkdownFiles(specsDir);

  // Pass 1: Check covers field in frontmatter
  for (const specFile of specFiles) {
    const fm = parseFrontmatter(specFile);
    if (!fm.covers || !Array.isArray(fm.covers)) continue;
    for (const pattern of fm.covers) {
      if (globMatch(relativeFile, pattern)) {
        return specFile;
      }
    }
  }

  // Pass 2: Convention-based mapping using source roots
  // context/specs/{module}/ maps to {source_root}/{module}/
  for (const srcRoot of sourceRoots) {
    if (!relativeFile.startsWith(srcRoot)) continue;
    const afterRoot = relativeFile.slice(srcRoot.length);
    const moduleName = afterRoot.split(path.sep)[0];
    if (!moduleName) continue;

    // Look for module overview first, then any spec in the module dir
    const moduleOverview = path.join(specsDir, moduleName, "_overview.md");
    if (fs.existsSync(moduleOverview)) {
      return moduleOverview;
    }

    const moduleDir = path.join(specsDir, moduleName);
    if (fs.existsSync(moduleDir) && fs.statSync(moduleDir).isDirectory()) {
      const moduleSpecs = walkMarkdownFiles(moduleDir);
      if (moduleSpecs.length > 0) {
        return moduleSpecs[0];
      }
    }
  }

  return null;
}

function walkMarkdownFiles(dir) {
  const results = [];
  if (!fs.existsSync(dir)) return results;

  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        results.push(...walkMarkdownFiles(fullPath));
      } else if (entry.isFile() && entry.name.endsWith(".md")) {
        results.push(fullPath);
      }
    }
  } catch (_) {
    // Skip unreadable directories
  }

  return results;
}

function parseFrontmatter(filePath) {
  try {
    const content = fs.readFileSync(filePath, "utf-8");
    const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!match) return {};

    const yaml = match[1];
    const result = {};

    for (const line of yaml.split("\n")) {
      const kvMatch = line.match(/^(\w[\w_]*)\s*:\s*(.+)$/);
      if (!kvMatch) continue;

      const key = kvMatch[1];
      let value = kvMatch[2].trim();

      // Parse simple arrays: [item1, item2]
      if (value.startsWith("[") && value.endsWith("]")) {
        value = value
          .slice(1, -1)
          .split(",")
          .map((s) => s.trim().replace(/^["']|["']$/g, ""))
          .filter(Boolean);
      } else {
        // Strip surrounding quotes
        value = value.replace(/^["']|["']$/g, "");
      }

      result[key] = value;
    }

    return result;
  } catch (_) {
    return {};
  }
}

function globMatch(filePath, pattern) {
  // Simple glob matching: supports * and **
  // Convert glob to regex
  const regexStr = pattern
    .replace(/\./g, "\\.")
    .replace(/\*\*/g, "{{GLOBSTAR}}")
    .replace(/\*/g, "[^/]*")
    .replace(/\{\{GLOBSTAR\}\}/g, ".*");

  try {
    const regex = new RegExp("^" + regexStr + "$");
    return regex.test(filePath);
  } catch (_) {
    return false;
  }
}

function getCoveredSourcePaths(specPath, specsDir, sourceRoots) {
  // Pass 1: Use explicit covers field from frontmatter
  const fm = parseFrontmatter(specPath);
  if (fm.covers && Array.isArray(fm.covers)) {
    return fm.covers;
  }

  // Pass 2: Convention-based mapping — derive source path from spec path
  // context/specs/{module}/ maps to {source_root}/{module}/
  const relToSpecs = path.relative(specsDir, specPath);
  const moduleName = relToSpecs.split(path.sep)[0];
  if (!moduleName || moduleName.startsWith("_")) {
    return [];
  }

  return sourceRoots.map((root) => path.join(root, moduleName));
}

function checkStale(coveredPaths, lastSynced, projectRoot) {
  if (coveredPaths.length === 0) return false;

  try {
    const pathArgs = coveredPaths.map((p) => `"${p}"`).join(" ");
    const result = execSync(
      `git log --oneline --since="${lastSynced}" -- ${pathArgs}`,
      {
        cwd: projectRoot,
        encoding: "utf-8",
        timeout: 5000,
        stdio: ["pipe", "pipe", "pipe"],
      }
    );
    return result.trim().length > 0;
  } catch (_) {
    // git not available or not a git repo — cannot determine staleness
    return false;
  }
}

main();
