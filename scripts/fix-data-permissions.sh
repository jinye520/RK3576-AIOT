#!/usr/bin/env sh
set -e

PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$PROJECT_ROOT"

TARGETS="data/wvp data/zlm data/record"

echo "[fix-perms] project root: $PROJECT_ROOT"
echo "[fix-perms] target paths: $TARGETS"

echo "[fix-perms] current ownership:"
ls -ld $TARGETS

echo "[fix-perms] attempting sudo chown -R $(id -un):$(id -gn) $TARGETS"
if sudo -n true 2>/dev/null; then
  sudo chown -R "$(id -un):$(id -gn)" $TARGETS

  echo "[fix-perms] applying directory/file modes"
  find data/wvp data/zlm data/record -type d -exec chmod 755 {} \;
  find data/wvp data/zlm data/record -type f -exec chmod 644 {} \;

  echo "[fix-perms] final ownership:"
  ls -ld $TARGETS

  echo "[fix-perms] done"
else
  echo "[fix-perms] sudo requires an interactive password in this environment."
  echo "[fix-perms] please run manually: sudo chown -R $(id -un):$(id -gn) $TARGETS"
  exit 1
fi
