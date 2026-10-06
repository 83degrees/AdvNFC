#!/bin/bash
set -euo pipefail

VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
  echo "Usage: $0 <version> [output-directory]" >&2
  exit 2
fi
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+([+~.-][A-Za-z0-9.+~-]+)?$ ]]; then
  echo "Invalid Debian/package version: $VERSION" >&2
  exit 2
fi

OUT_DIR="${2:-dist}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RPI_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SOURCE_ROOT="$RPI_ROOT/source"
REPO_ROOT="$(cd "$RPI_ROOT/../.." && pwd)"
ARCH="all"
GIT_SHA="${SOURCE_GIT_SHA:-$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || true)}"
if [[ ! "$GIT_SHA" =~ ^[0-9a-f]{40}$ ]]; then
  echo "SOURCE_GIT_SHA or repository HEAD must identify an exact 40-character commit" >&2
  exit 2
fi
PKG="advnfc-reader-agent"
WORK="$(mktemp -d)"
ROOT="$WORK/root"
trap 'rm -rf "$WORK"' EXIT

mkdir -p   "$ROOT/DEBIAN"   "$ROOT/opt/advnfc/reader_agent"   "$ROOT/lib/systemd/system"   "$ROOT/lib/udev/rules.d"   "$ROOT/usr/local/sbin"   "$ROOT/usr/share/advnfc/profiles"   "$ROOT/usr/share/advnfc/secrets"

install -m 0755 "$SOURCE_ROOT/opt/advnfc/reader_agent/advnfc_reader_agent.sh"   "$ROOT/opt/advnfc/reader_agent/advnfc_reader_agent.sh"
install -m 0644 "$SOURCE_ROOT/lib/systemd/system/advnfc-reader-agent.service"   "$ROOT/lib/systemd/system/advnfc-reader-agent.service"
install -m 0644 "$SOURCE_ROOT/lib/udev/rules.d/99-advnfc-acr122u.rules"   "$ROOT/lib/udev/rules.d/99-advnfc-acr122u.rules"
install -m 0755 "$SOURCE_ROOT/usr/local/sbin/advnfc-reader-agent-check"   "$ROOT/usr/local/sbin/advnfc-reader-agent-check"
install -m 0755 "$SOURCE_ROOT/usr/local/sbin/advnfc-reader-agent-init"   "$ROOT/usr/local/sbin/advnfc-reader-agent-init"
install -m 0755 "$SOURCE_ROOT/usr/local/sbin/advnfc-profile"   "$ROOT/usr/local/sbin/advnfc-profile"
install -m 0644 "$SOURCE_ROOT/usr/share/advnfc/profiles/"*.yaml   "$ROOT/usr/share/advnfc/profiles/"
install -m 0640 "$SOURCE_ROOT/usr/share/advnfc/secrets/"*.env.example   "$ROOT/usr/share/advnfc/secrets/"

cat >"$ROOT/opt/advnfc/reader_agent/VERSION" <<EOF
version=$VERSION
git_sha=$GIT_SHA
EOF
chmod 0644 "$ROOT/opt/advnfc/reader_agent/VERSION"

cat >"$ROOT/DEBIAN/control" <<EOF
Package: $PKG
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Depends: bash, coreutils, adduser, util-linux, libnfc-bin, mosquitto-clients, usbutils, udev, systemd, python3, python3-yaml
Maintainer: AdvNFC
Description: Governed AdvNFC Raspberry Pi NFC reader agent
 Installs the AdvNFC reader agent, systemd unit, ACR122U access rule,
 readiness tooling and version metadata. Node-local configuration and
 secrets remain outside the package under /etc/advnfc.
EOF

cat >"$ROOT/DEBIAN/postinst" <<'EOF'
#!/bin/bash
set -e

if ! getent group advnfc >/dev/null; then
  addgroup --system advnfc
fi
if ! id advnfc >/dev/null 2>&1; then
  adduser --system --ingroup advnfc --home /nonexistent --no-create-home --disabled-login advnfc
fi

mkdir -p /etc/advnfc /etc/advnfc/profiles /etc/advnfc/secrets
chown root:advnfc /etc/advnfc /etc/advnfc/profiles /etc/advnfc/secrets
chmod 0750 /etc/advnfc /etc/advnfc/profiles /etc/advnfc/secrets

udevadm control --reload-rules || true
udevadm trigger --subsystem-match=usb || true
systemctl daemon-reload
systemctl enable advnfc-reader-agent.service >/dev/null 2>&1 || true

# Fresh installs do not start the service before a validated active profile exists.
# Upgrades restart only an already-running service.
if systemctl is-active --quiet advnfc-reader-agent.service; then
  systemctl restart advnfc-reader-agent.service
fi
EOF
chmod 0755 "$ROOT/DEBIAN/postinst"

cat >"$ROOT/DEBIAN/prerm" <<'EOF'
#!/bin/bash
set -e
if [[ "${1:-}" == "remove" ]]; then
  systemctl stop advnfc-reader-agent.service >/dev/null 2>&1 || true
  systemctl disable advnfc-reader-agent.service >/dev/null 2>&1 || true
fi
EOF
chmod 0755 "$ROOT/DEBIAN/prerm"

cat >"$ROOT/DEBIAN/postrm" <<'EOF'
#!/bin/bash
set -e
systemctl daemon-reload >/dev/null 2>&1 || true
exit 0
EOF
chmod 0755 "$ROOT/DEBIAN/postrm"

mkdir -p "$OUT_DIR"
OUT="$OUT_DIR/${PKG}_${VERSION}_${ARCH}.deb"
dpkg-deb --build --root-owner-group "$ROOT" "$OUT"
sha256sum "$OUT" >"$OUT.sha256"
echo "$OUT"
