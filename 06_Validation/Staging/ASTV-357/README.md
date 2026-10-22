# ASTV-357 Disposable Staging Fixture

This fixture provisions a one-shot Home Assistant staging instance for the
ASTV-357 isolation and controlled-lifecycle validation. The workflow copies
AdvNFC only from immutable tag `v1.6.0-beta.dbef2f5`, verifies that the tag
resolves to `dbef2f5133d2efb6f426b348916dc0c58ec1e147`, and runs Home
Assistant Core `2026.9.4` in a container with `--network none` and no
published ports.

The fixture deliberately contains:

- a private copy of the observed twelve-record logical mapping baseline;
- a read-only eight-intent ASTV catalogue double;
- an inert file-only gateway spy/sink;
- no MQTT configuration, reader listener automation, production URL,
  credential, device integration, or repository secret; and
- fail-closed lifecycle assertions with no automatic retry and unconditional
  disposal.

The original read-only mode creates one staging-local area registry entry,
reads the AdvNFC and ASTV administration surfaces, proves that reserved UID
`A3570001` is absent, and confirms that the gateway spy was not invoked.

A later, separately authorised single run used the controlled lifecycle mode
to create and Save `A3570001` with `classic_fm`, explicitly Activate it, edit
and Save it with area `astv_357_staging_area`, Activate the edit, reject a
duplicate UID without side effects, delete and Save the synthetic record, and
perform the final Activate. That run completed successfully and received G5
human acceptance. It recorded zero gateway invocations, restored the exact
twelve-record logical staging baseline and original content-derived revision,
and independently confirmed that the twelve-record production state was
unchanged. Serializer normalization made the restored staging file logically,
but not byte-for-byte, identical to its starting form.

Both modes remove the container unconditionally and upload configuration
identity/hashes, responses, isolation proof, logs, and disposal evidence as a
retained GitHub Actions artifact. The workflow remains manual-dispatch only.
The completed single-run authority does not permit another lifecycle run;
fresh explicit human approval is required before any further controlled
lifecycle execution. Production operations are never authorised by this
fixture.

