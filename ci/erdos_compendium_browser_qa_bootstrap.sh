#!/usr/bin/env bash
# Keep browser QA dependencies in a per-user tooling directory, outside project installs.
set -euo pipefail
NODE22="$HOME/.nvm/versions/node/v22.17.1/bin"
if [[ -x "$NODE22/node" && -x "$NODE22/npm" ]]; then
  export PATH="$NODE22:$PATH"
fi
command -v node >/dev/null
command -v npm >/dev/null
TOOL_HOME="$HOME/.local/share/gcl-browser-qa"
mkdir -p "$TOOL_HOME"
npm install --prefix "$TOOL_HOME" --no-audit --no-fund --save-exact playwright-core@1.58.2
if compgen -G "$HOME/.cache/ms-playwright/chromium-*/chrome-linux64/chrome" >/dev/null; then
  echo "CHROMIUM_CACHE_PRESENT"
else
  node "$TOOL_HOME/node_modules/playwright-core/cli.js" install chromium
fi
node -e "const p=require('$TOOL_HOME/node_modules/playwright-core'); if (!p.chromium) process.exit(1); console.log('PLAYWRIGHT_CORE_READY')"
