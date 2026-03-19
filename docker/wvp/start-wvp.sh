#!/usr/bin/env sh
set -e

WVP_HOME=${WVP_HOME:-/opt/wvp}
WVP_JAR=${WVP_JAR:-$WVP_HOME/wvp-pro.jar}
WVP_CONFIG=${WVP_CONFIG:-$WVP_HOME/application-docker.yml}
WVP_OVERRIDE_DIR=${WVP_OVERRIDE_DIR:-$WVP_HOME/runtime-override}
WVP_OVERRIDE_STATIC=${WVP_OVERRIDE_STATIC:-$WVP_OVERRIDE_DIR/static}

if [ ! -f "$WVP_JAR" ]; then
  echo "[WVP] Placeholder mode: $WVP_JAR not found"
  echo "[WVP] Put your real WVP jar at data/wvp/wvp-pro.jar and restart the service."
  tail -f /dev/null
  exit 0
fi

mkdir -p "$WVP_OVERRIDE_DIR"
RUNTIME_CONFIGS="$WVP_CONFIG"

if [ -d "$WVP_OVERRIDE_STATIC" ] && [ -f "$WVP_OVERRIDE_STATIC/index.html" ]; then
  cat > "$WVP_OVERRIDE_DIR/application-runtime.yml" <<EOF
spring:
  web:
    resources:
      static-locations: file:${WVP_OVERRIDE_STATIC}/,classpath:/static/,classpath:/public/,classpath:/resources/,classpath:/META-INF/resources/
EOF
  RUNTIME_CONFIGS="$WVP_CONFIG,$WVP_OVERRIDE_DIR/application-runtime.yml"
  echo "[WVP] runtime static override enabled: $WVP_OVERRIDE_STATIC"
fi

echo "[WVP] Starting real package: $WVP_JAR"
exec java -Xms512m -Xmx1024m -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/opt/wvp/ -jar "$WVP_JAR" --spring.config.location="$RUNTIME_CONFIGS"
