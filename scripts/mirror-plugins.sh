#!/usr/bin/env bash
# Mirror each plugin under plugins/<name> to its own standalone GitHub repo.
# Idempotent: re-running with no changes is a noop (force-with-lease will succeed without overwrite).
#
# Usage:
#   ./scripts/mirror-plugins.sh            # mirror all configured plugins
#   ./scripts/mirror-plugins.sh sprint     # mirror a single plugin

set -euo pipefail

OWNER="workingdanny911"
ALL_PLUGINS=("sprint" "cai" "codebase-x-ray")

if [[ $# -gt 0 ]]; then
  PLUGINS=("$@")
else
  PLUGINS=("${ALL_PLUGINS[@]}")
fi

cd "$(git rev-parse --show-toplevel)"

for plugin in "${PLUGINS[@]}"; do
  prefix="plugins/${plugin}"
  if [[ ! -d "${prefix}" ]]; then
    echo "ERROR: ${prefix} does not exist"
    exit 1
  fi

  echo "==> Splitting ${prefix}"
  git branch -D "split/${plugin}" 2>/dev/null || true
  git subtree split --prefix="${prefix}" -b "split/${plugin}"

  echo "==> Pushing to ${OWNER}/${plugin}"
  git push "https://github.com/${OWNER}/${plugin}.git" \
    "split/${plugin}:main" --force-with-lease

  git branch -D "split/${plugin}"
done

echo "Mirror complete."
