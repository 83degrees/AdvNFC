# AdvNFC Disposable Home Assistant Validation

This maintained validation tool assembles a one-run Home Assistant instance for
AdvNFC baseline and administration-schema checks. It is product-owned
validation tooling, not deployable product runtime.

The manual workflow exposes only two non-mutating modes:

- `baseline_read_only` verifies the synthetic two-record mapping, read-only
  ASTV catalogue double, inert sink and provider status.
- `schema_non_mutating` preserves the unique ASTV-360 probe. It verifies five
  administration service schemas, rejects extra and malformed fields, exercises
  create/update/delete only with a deliberately stale revision, and proves the
  active and persisted state is byte-for-byte unchanged.

`scripts/execute_lifecycle.py` is retained as reviewed source because it proves
the Save/Activate boundary, but the workflow has no lifecycle mode and does not
copy that script into the stage. Running it requires fresh action-specific human
authority and a separately reviewed invocation change. Prior ASTV-357 authority
does not authorize another run.

## Isolation and credential controls

The workflow is manual-dispatch only, has read-only repository permission, and
uses no repository secrets. Home Assistant runs with network mode `none`, no
published ports, all Linux capabilities dropped, `no-new-privileges`, private
config/evidence mounts and an inert file-only gateway sink. The fixture contains
only synthetic UIDs, labels, intents and records.

The workflow generates a random onboarding password for each run. The verifier
reads it from a private file and immediately removes that file; the access token
exists only in process memory. Neither value is written to evidence or logs.
Evidence is written to the runner-temporary `/evidence` mount, outside this tool
source tree, and uploaded after unconditional container disposal.

Immutable dependency pins:

- Home Assistant `2026.9.4` OCI digest:
  `sha256:3e6710a7ab2a61311d9d899b719f6c3657791c63e8f4942cec4ebc42401d6b76`
- `actions/checkout` v4 resolved commit:
  `11d5960a326750d5838078e36cf38b85af677262`
- `actions/upload-artifact` v4 resolved commit:
  `ea165f8d65b6e75b540449e92b4886f43607fa02`

## Source provenance

ASTV-366 curated the tool from these immutable repository states:

- AdvNFC `main`: `2f31c99c1a98bd816261932ee69146d92a2fff19`
- ASTV-357 retained branch:
  `352df6a74ca6cb048a403acc80764c087d8bb188`
- ASTV-360 retained branch:
  `2e58b73ed6c7f463d7eb771b398a04e634111c08`

The following old-path Git blobs supplied the maintained source. Main and the
ASTV-357 branch have the same blob for each listed shared source path.

| Maintained destination | Source path | Source blob |
| --- | --- | --- |
| `.github/workflows/advnfc-disposable-validation.yml` | `.github/workflows/astv-357-disposable-staging.yml` | `a66deb48e66186329454513df0283ee39147dd0d` |
| `README.md` | `06_Validation/Staging/ASTV-357/README.md` | `03ba7147db8274a6bf0262fb6184900fd3d1eaee` |
| `config/AdvNFC/advnfc_tag_mapping.yaml` | `06_Validation/Staging/ASTV-357/config/AdvNFC/advnfc_tag_mapping.yaml` | `ced705049c5a4dcc0b0451ad5b880061753d3b82` |
| `config/configuration.yaml` | `06_Validation/Staging/ASTV-357/config/configuration.yaml` | `f0c17461b7bd456a6f7ec2d593d720a197ecf744` |
| `config/custom_components/astv_intent_catalogue/__init__.py` | `06_Validation/Staging/ASTV-357/config/custom_components/astv_intent_catalogue/__init__.py` | `e0afb0af0ca79b1f1a3ae453f87f1f1407e11026` |
| `config/custom_components/astv_intent_catalogue/manifest.json` | `06_Validation/Staging/ASTV-357/config/custom_components/astv_intent_catalogue/manifest.json` | `22a5a572e8612237a801cf99cb281d1178aefa92` |
| `config/custom_components/astv_staging_sink/__init__.py` | `06_Validation/Staging/ASTV-357/config/custom_components/astv_staging_sink/__init__.py` | `3b9c9b71fed11190321481a1a233089006fc1ed8` |
| `config/custom_components/astv_staging_sink/manifest.json` | `06_Validation/Staging/ASTV-357/config/custom_components/astv_staging_sink/manifest.json` | `89f2e25e010f92ec94d896fe70ed470902f8d50c` |
| `config/packages/advnfc_stage.yaml` | `06_Validation/Staging/ASTV-357/config/packages/advnfc_stage.yaml` | `dd9e3520a2bf476251e163cbf05966406d953cc2` |
| `scripts/verify_baseline.py` | `06_Validation/Staging/ASTV-357/config/staging/verify_stage.py` | `362a20ef32ee044bd2ae4cf4dbe20efc0b3e4ffd` |
| `scripts/execute_lifecycle.py` | `06_Validation/Staging/ASTV-357/config/staging/execute_lifecycle.py` | `22a7725d96c2e840c4695024a2af3b104ab0a558` |
| `scripts/verify_admin_schemas.py` | `06_Validation/Staging/ASTV-357/config/staging/verify_astv360_schema.py` on ASTV-360 | `ab94c2a40fc6e4fdac340a415b962e9d6696a7bc` |

The ASTV-360 workflow, README and baseline verifier variants were divergent
blobs (`c9859497344c3560d31a508901f1cc52b43b422f`,
`27cd1f46b3c6799708a260615322c66e9936c3da`, and
`2da54412cc752116bd61a381de600f104d46c585`) and are not copied wholesale.
Their schema-mode intent is preserved by `verify_admin_schemas.py`; their push
trigger and issue-specific presentation are deliberately retired.

Historical evidence remains under `06_Validation/Evidence/**` and in the
governed Linear attachments. It is not duplicated into this tool directory.

## Permitted source checks

Without starting Home Assistant or dispatching the workflow, maintainers can
run the repository test suites plus:

```text
python -m compileall -q 06_Validation/Tools/advnfc_disposable_ha
python -c "import pathlib,yaml; yaml.safe_load(pathlib.Path('.github/workflows/advnfc-disposable-validation.yml').read_text())"
python -c "import pathlib,yaml; [yaml.safe_load(p.read_text()) for p in pathlib.Path('06_Validation/Tools/advnfc_disposable_ha/config').rglob('*.yaml')]"
```

These checks do not validate the container lifecycle. Workflow dispatch,
staging execution, deployment and production use require separate authority.
