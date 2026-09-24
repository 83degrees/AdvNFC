#!/bin/bash
set -euo pipefail
# AdvNFC reader agent
#
# Environment-specific, non-secret configuration comes from the selected
# AdvNFC profile. The referenced MQTT password remains in a protected
# node-local secret file.

eval "$(/usr/local/sbin/advnfc-profile runtime-shell)"

READER="${READER_OVERRIDE:-$(hostname -s)}"
MQTT_TOPIC="${MQTT_TOPIC_PATTERN//\{reader\}/$READER}"
POLL_S="${POLL_S:-0.20}"
DEBOUNCE_S="${DEBOUNCE_S:-0.80}"
EMPTY_RESET_LOOPS="${EMPTY_RESET_LOOPS:-8}"

prev=""
empty_count=0

echo "AdvNFC reader agent | profile=$ADVNFC_PROFILE | reader=$READER | MQTT=$MQTT_HOST:$MQTT_PORT | topic=$MQTT_TOPIC"

while true; do
  uid=$(nfc-list 2>/dev/null | awk '/UID \(NFCID1\):/{for(i=4;i<=NF;i++) printf toupper($i)}')

  if [[ -n "$uid" ]]; then
    empty_count=0
    if [[ "$uid" != "$prev" ]]; then
      echo "SEND: $uid (reader=$READER)"

      /usr/bin/mosquitto_pub -h "$MQTT_HOST" -p "$MQTT_PORT" \
        -u "$MQTT_USER" -P "$MQTT_PASS" \
        -t "$MQTT_TOPIC" -r \
        -m "$uid"

      prev="$uid"
      sleep "$DEBOUNCE_S"
    fi
  else
    ((++empty_count))
    if (( empty_count >= EMPTY_RESET_LOOPS )); then
      prev=""
      empty_count=0
    fi
  fi

  sleep "$POLL_S"
done
