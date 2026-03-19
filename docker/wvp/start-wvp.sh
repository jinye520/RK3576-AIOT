#!/usr/bin/env sh
set -e

WVP_HOME=${WVP_HOME:-/opt/wvp}
WVP_JAR=${WVP_JAR:-$WVP_HOME/wvp-pro.jar}
WVP_CONFIG=${WVP_CONFIG:-$WVP_HOME/application-docker.yml}

if [ ! -f "$WVP_JAR" ]; then
  echo "[WVP] Placeholder mode: $WVP_JAR not found"
  echo "[WVP] Put your real WVP jar at data/wvp/wvp-pro.jar and restart the service."
  tail -f /dev/null
  exit 0
fi

echo "[WVP] Starting real package: $WVP_JAR"
exec java -jar "$WVP_JAR" --spring.config.location="$WVP_CONFIG"
