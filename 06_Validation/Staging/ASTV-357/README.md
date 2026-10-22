# ASTV-357 Disposable Staging Fixture

This fixture provisions a one-shot Home Assistant staging instance for the
G4-authorised ASTV-357 isolation phase. The workflow copies AdvNFC only from
immutable tag `v1.6.0-beta.288e3df`, verifies that the tag resolves to
`288e3df5187a5c37e44feda202cc570f9eb539e0`, and runs Home Assistant Core
`2026.9.4` in a container with `--network none` and no published ports.

The fixture deliberately contains:

- a private copy of the observed twelve-record logical mapping baseline;
- a read-only eight-intent ASTV catalogue double;
- an inert file-only gateway spy/sink;
- no MQTT configuration, reader listener automation, production URL,
  credential, device integration, or repository secret; and
- no create, update, delete, Save, reload, or Activate call.

The verification step creates only one staging-local area registry entry,
reads the AdvNFC and ASTV administration surfaces, proves that the reserved UID
`A3570001` is absent, and confirms that the gateway spy was not invoked. The
container is then removed. The complete disposable configuration and evidence
are uploaded as a retained GitHub Actions artifact.

Do not extend this workflow with the write/activation lifecycle until Linear
records a subsequent explicit human approval of that controlled sequence.

