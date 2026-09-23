#!/bin/bash
# AdvNFC reader agent
#
# Behavior-preserving extraction of the pi-nfc-02 runtime baseline captured
# under ASTV-246. Deployment-specific configuration is supplied by systemd
# through /etc/advnfc/reader-agent.env. Secrets must not be stored here.

HA_BASE_URL="${HA_BASE_URL:-http://ha-starburst.little-dory.ts.net:8123}"
WEBHOOK_ID="${WEBHOOK_ID:-assistive_card_scan}"
WEBHOOK_URL="$HA_BASE_URL/api/webhook/$WEBHOOK_ID"

MQTT_HOST="${MQTT_HOST:-ha-starburst.little-dory.ts.net}"
MQTT_PORT="${MQTT_PORT:-1883}"
MQTT_USER="${MQTT_USER:-ha_mqtt}"
: "${MQTT_PASS:?MQTT_PASS must be supplied through the deployment environment}"

READER="${READER:-$(hostname -s)}"
POLL_S="${POLL_S:-0.20}"
DEBOUNCE_S="${DEBOUNCE_S:-0.80}"
EMPTY_RESET_LOOPS="${EMPTY_RESET_LOOPS:-8}"

prev=""
empty_count=0

echo "AdvNFC reader agent | reader=$READER | MQTT=$MQTT_HOST:$MQTT_PORT | webhook=$WEBHOOK_ID"

while true; do
  uid=$(nfc-list 2>/dev/null | awk '/UID \(NFCID1\):/{for(i=4;i<=NF;i++) printf toupper($i)}')

  if [[ -n "$uid" ]]; then
    empty_count=0
    if [[ "$uid" != "$prev" ]]; then
      ts=$(date -Is)
      echo "SEND: $uid (reader=$READER @ $ts)"

      # Existing Home Assistant webhook output retained during initial migration.
      curl -sS --max-time 2 -H "Content-Type: application/json" \
        -d "{\"uid\":\"$uid\",\"reader\":\"$READER\"}" \
        "$WEBHOOK_URL" >/dev/null || echo "curl failed"

      # Existing non-retained MQTT event output retained during initial migration.
      /usr/bin/mosquitto_pub -h "$MQTT_HOST" -p "$MQTT_PORT" \
        -u "$MQTT_USER" -P "$MQTT_PASS" \
        -t "assistive/nfc/event" \
        -m "{\"uid\":\"$uid\",\"reader\":\"$READER\",\"ts\":\"$ts\"}"

      # Existing retained per-reader state consumed by Home Assistant.
      /usr/bin/mosquitto_pub -h "$MQTT_HOST" -p "$MQTT_PORT" \
        -u "$MQTT_USER" -P "$MQTT_PASS" \
        -t "assistive/nfc/$READER/last_uid" -r \
        -m "$uid"

      prev="$uid"
      sleep "$DEBOUNCE_S"
    fi
  else
    ((empty_count++))
    if (( empty_count >= EMPTY_RESET_LOOPS )); then
      prev=""
      empty_count=0
    fi
  fi

  sleep "$POLL_S"
done
