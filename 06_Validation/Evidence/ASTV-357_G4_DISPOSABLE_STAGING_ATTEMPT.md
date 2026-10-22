# ASTV-357 G4 Disposable Staging Attempt Evidence

**Recorded:** 2026-10-22  
**Authority:** ASTV-357 G4 human authorization recorded in Linear  
**Outcome:** **STOPPED / NEEDS HUMAN REVIEW** — fail-closed before staging verification and before every write or activation lifecycle operation.

## Scope and stop boundary

The authorized preparation assembled a disposable Home Assistant staging configuration and attempted to start it with production connectivity disabled. No create, Save/update, delete, reload, Activate, reader scan, MQTT publication, gateway dispatch, or production configuration mutation was executed. The reserved staging-only tuple remains unexercised:

- UID: `A3570001`
- intent: `classic_fm`

The write/activation lifecycle remains behind the required human approval gate.

## Candidate and environment identity

| Item | Evidence |
|---|---|
| Preparation branch | `gsheldon/astv-357-disposable-staging` |
| Attempt head | `caf951a523915628857df89c02e1754c9a5d1330` |
| Final run | [GitHub Actions run 39753496539](https://github.com/83degrees/AdvNFC/actions/runs/39753496539) |
| Home Assistant image | `ghcr.io/home-assistant/home-assistant:2026.9.4` |
| Image digest | `sha256:3e6710a7ab2a61311d9d899b719f6c3657791c63e8f4942cec4ebc42401d6b76` |
| Accepted AdvNFC tag | `v1.6.0-beta.288e3df` |
| Accepted AdvNFC commit | `288e3df5187a5c37e44feda202cc570f9eb539e0` |
| Accepted component tree | `9dfda2538e4b509ac16ff2846c9f69e51c83c55b` |
| Artifact | `astv-357-disposable-staging-evidence-39753496539`, digest `sha256:51c7c4d5ad4f864c226a64e9ffc03416649f67d999fc252f6c7a7be6e46b7354`, expires 2026-11-21 |

The staged fixture contains the approved normalized 12-record baseline and an eight-intent read-only ASTV catalogue double. Its expected revision is `v1-986df5539173dad03cf231dd5fd094dbdc6024d1786ad721b18b84fe332c4173`. These were assembled and hashed, but they were **not runtime-verified** because Home Assistant stopped during initialization.

## Isolation evidence

The final attempt invoked the container with:

- Docker network mode `none`;
- no published ports;
- all Linux capabilities dropped;
- `no-new-privileges` enabled;
- private runner-temporary `/config` storage;
- no production MQTT endpoint, production reader/device endpoint, production credentials, or production automation listener;
- an inert staging-local gateway sink only;
- no repository or environment secret passed to the job.

Home Assistant exited before opening its local API, with:

```text
Fatal Error: Unable to create library directory /config/deps: [Errno 13] Permission denied: '/config/deps'
```

Consequently, the stage area ID, runtime mapping status, catalogue status, and sink registration were not produced. The verification step was skipped. This is recorded as a failed gate, not as successful staging validation.

## Fail-closed attempts

| Run | Startup result | Lifecycle reached | Disposal |
|---|---|---:|---:|
| `39753034189` | `/run` mounted `noexec`; container initialization stopped | No | Container removed |
| `39753241464` | privileged s6 initialization incompatible with the restricted profile | No | Container removed |
| `39753496539` | direct HA process could not create `/config/deps` on the bind mount | No | `container_removed=true` |

No further retry was triggered. The workflow is now manual-dispatch only to prevent more automatic failure notifications and accidental attempts.

## Production preservation check

A fresh read-only production query after the final disposal reported:

- `state=active`, `ok=true`;
- active count `12`, persisted count `12`;
- active and persisted revision both `v1-986df5539173dad03cf231dd5fd094dbdc6024d1786ad721b18b84fe332c4173`;
- `activation_required=false`;
- `last_activation_error=null`;
- the original 12 UIDs present; `A3570001` absent.

This matches the pre-attempt baseline. Production was not mutated.

## Rollback and disposal

The disposable container was removed by the unconditional cleanup step; retained evidence states `container_removed=true`. The runner-temporary configuration and any transient Home Assistant state are destroyed with the GitHub-hosted runner. The uploaded artifact contains only candidate hashes, the image digest, the fatal startup log, and disposal proof; it contains no `.storage`, token, password, or production credential material.

Because no lifecycle operation ran and no persistent staging service survived, rollback is complete: there is no staged mapping to reverse and no activation to undo. The repository branch is only a reviewable preparation artifact.

## Human decision required

Do **not** approve the write/activation lifecycle yet. A human must first choose or authorize a staging substrate/profile that lets the exact Home Assistant image write its private `/config` while preserving the recorded isolation controls. A subsequent authorized attempt must reproduce the identities above, complete runtime isolation verification, establish the stage area identity, and return again for approval before exercising `A3570001`.
