# CLAUDE.md

Project-specific instructions for Claude Code working in this repo.

## What this repo is

`dannys-claude` is both:

1. **The development source-of-truth** for four Claude Code plugins (`sprint`, `cai`, `codebase-x-ray`, `explain`).
2. **A curated aggregator marketplace** that re-exports three of those plugins from their standalone mirror repos.

```
workingdanny911/dannys-claude        ← THIS REPO (dev source of truth)
├── plugins/
│   ├── sprint/                      → mirrored to workingdanny911/sprint
│   ├── cai/                         → mirrored to workingdanny911/cai
│   ├── codebase-x-ray/              → mirrored to workingdanny911/codebase-x-ray
│   └── explain/                     (monorepo only, no mirror)
├── .claude-plugin/marketplace.json  (aggregator, points to GitHub sources)
└── scripts/mirror-plugins.sh        (subtree-split + push automation)
```

## Why standalone mirrors exist

Each mirrored plugin lives in its own public GitHub repo so it can be:

- discovered and starred independently
- installed directly: `/plugin marketplace add workingdanny911/<plugin>`
- promoted on its own merits without being buried under the umbrella marketplace

Standalone repos are **read-only mirrors**. Never commit to them directly — the next `mirror-plugins.sh` run uses `--force-with-lease` and will overwrite divergent history.

## Developer workflow

All work happens in this monorepo. The mirror is a one-way push.

### Editing a plugin

```bash
# 1. Edit files under plugins/<plugin>/
# 2. Commit and push to monorepo
git add plugins/cai/
git commit -m "cai: <change>"
git push

# 3. Sync mirror(s)
bash scripts/mirror-plugins.sh           # all three
bash scripts/mirror-plugins.sh cai       # just one
```

`explain` has no mirror — push to monorepo is all you need.

### Releasing a new plugin version

Two files must move together:

1. `plugins/<plugin>/.claude-plugin/plugin.json` → bump `version`
2. `.claude-plugin/marketplace.json` → bump matching entry's `version`

Commit both, push, then mirror:

```bash
git add plugins/cai/.claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "cai v0.3.4: release"
git push
bash scripts/mirror-plugins.sh cai
```

### Adding a new plugin

1. Create `plugins/<new-plugin>/` with a valid `.claude-plugin/plugin.json`.
2. Add an entry to `.claude-plugin/marketplace.json` (use `./plugins/<new-plugin>` as `source` initially).
3. If you want a standalone mirror:
   - Add `<new-plugin>` to the `ALL_PLUGINS` array in `scripts/mirror-plugins.sh`.
   - Create the standalone GitHub repo: `gh repo create workingdanny911/<new-plugin> --public`.
   - Run `bash scripts/mirror-plugins.sh <new-plugin>` to do the initial split + push.
   - Clone the mirror once and add `.claude-plugin/marketplace.json` (self-marketplace), `LICENSE`, `.gitignore`.
   - Switch the monorepo's aggregator entry `source` from `./plugins/<new-plugin>` to `{ "source": "github", "repo": "workingdanny911/<new-plugin>" }`.

## End-user installation (for context)

Users can install either way:

```bash
# Curated marketplace (all plugins)
/plugin marketplace add workingdanny911/dannys-claude
/plugin install sprint@dannys-claude

# Standalone repo (per plugin)
/plugin marketplace add workingdanny911/sprint
/plugin install sprint@sprint
```

Both paths resolve to the same code.

## Constraints

| Rule | Reason |
|---|---|
| Never commit directly to standalone mirror repos | The next mirror push will overwrite the divergent history. |
| Don't rename or move `plugins/<name>/` directories | `git subtree split --prefix=plugins/<name>` is keyed on the path. Renaming breaks mirror history continuity. |
| Don't merge external PRs into mirror repos | Same overwrite risk. Direct contributors to PR against this monorepo. |
| Keep `plugin.json` `version` and aggregator entry `version` in sync | Users see mismatched versions otherwise. |
| `__pycache__/`, `.DS_Store`, build artifacts → never commit | Already in `.gitignore`; keep it that way. |

## Mirror script internals

`scripts/mirror-plugins.sh` does, for each plugin:

```
git subtree split --prefix=plugins/<plugin> -b split/<plugin>
git push https://github.com/workingdanny911/<plugin>.git split/<plugin>:main --force-with-lease
git branch -D split/<plugin>
```

`git subtree split` is deterministic given the same monorepo history — re-running produces identical commit SHAs, so `--force-with-lease` is a no-op when nothing changed.

## Useful one-liners

```bash
# Verify all three mirrors exist and have content
for p in sprint cai codebase-x-ray; do gh repo view workingdanny911/$p --json url,description,pushedAt; done

# Verify aggregator marketplace.json is valid JSON
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && echo OK

# See what subtree split WOULD produce without pushing
git subtree split --prefix=plugins/cai
```
