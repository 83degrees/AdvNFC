# HOME_ASSISTANT_CONFIG_DEPLOYMENT_STANDARD.md

**Standard:** Home Assistant Configuration Deployment Standard
**Version:** v1.0.0
**Status:** Approved
**Approval tag:** `home-assistant-config-deployment-standard-v1.0.0`
**Approval date:** 2026-10-06
**Lifecycle:** Independent

## 1. Purpose, Scope and Authority

This Standard defines the mandatory authority, identity, transfer-integrity, validation, evidence, rollback and recovery controls for governed Home Assistant configuration deployed through the temporary `operator_selected` mechanism.

It is a **product-applicable Standard** maintained authoritatively at:

`/Standards/Product/HOME_ASSISTANT_CONFIG_DEPLOYMENT_STANDARD.md`

It is projected unchanged into applicable governed product repositories at:

`00_Governance/01_Central/01_Standards/HOME_ASSISTANT_CONFIG_DEPLOYMENT_STANDARD.md`

It applies to a governed deployable unit classified as `haos_config` with deployment mechanism `operator_selected` under the Deployment Architecture Standard.

`CENTRAL_GOVERNANCE.md` remains the higher constitutional authority. The Deployment Architecture Standard remains authoritative for deployable-unit classification and canonical source structure. Product architecture and the Project Profile remain authoritative for product-specific configuration meaning, target-instance identity and environment responsibilities. This Standard supplies only the mechanism-specific controls for operator-managed configuration deployment and must not duplicate or override those authorities.

This Standard does not itself authorise deployment, Beta acceptance, stable promotion, production deployment, rollback or recovery. It does not bypass issue workflow, human review, validation, deployment authority, rollback authority or other required approval gates.

## 2. Mechanism Definition and Boundary

`operator_selected` means that an authorised user or operator performs or directs the deployment and selects the practical file-transfer transport for that deployment.

The transfer method is at the authorised user or operator's discretion. It may use SMB, a file editor, SCP/SFTP, direct file upload or another available manual or tool-assisted route. This Standard does not mandate Windows, SMB, Git on Home Assistant OS, a Home Assistant App, GitHub Actions, an agent-accessible Home Assistant endpoint or any other single transport or operating system.

The selected transport is an execution detail, not an authority source. Its use does not expand scope, alter the governed payload, satisfy a missing deployment authorisation or provide stronger provenance than the evidence it actually produces.

This is a temporary operator-managed route. It does not establish a general automation design, a runtime synchronization service or a transport-specific product dependency.

## 3. Deployment Authority and Preconditions

Before transfer begins, the governing Linear issue or linked deployment evidence must identify:

- the explicit authority to deploy the stated candidate to the stated target instance and environment;
- the authorised operator;
- the exact governed source candidate and source path;
- the exact target instance and deterministic target path;
- the intended transport, where already selected, or that the operator will select it before transfer;
- the required Home Assistant configuration-validation route;
- the immediate prior target state and rollback route; and
- any credentials, availability window, restart, reload or service-impact considerations material to safe execution.

Deployment must not begin when authority, candidate, target or rollback scope is ambiguous. Access to a transport or target does not itself constitute deployment authority.

## 4. Candidate, Source and Target Identity

The deployment record must identify the governed source with the strongest identity reasonably available, normally including:

- source repository;
- exact source commit SHA or other immutable accepted candidate identity;
- deterministic repository-relative source path;
- the file or bounded file-set being deployed; and
- a content hash, complete manifest or equivalent exact-byte identity where practical.

The target identity must include:

- the Home Assistant instance and environment;
- the deterministic Home Assistant configuration path for each deployed item; and
- enough context to distinguish the intended target from another instance, mount, share, editor workspace or similarly named path.

Source and target paths must be mapped explicitly before transfer. Wildcards, an editor's current folder, a recent-file list, a moving branch name or an unlabeled local copy are not sufficient identity where they could select different content.

Manual transfer has honest provenance limits. An operator observation that a copy completed does not independently prove that target bytes derive from a stated Git commit. Git identity may be claimed only where evidence binds the transferred bytes to the governed candidate. Otherwise the evidence must describe the manual source selection, paths and any byte comparison actually performed without overstating provenance.

## 5. Immediate Prior-State Capture

Before any target file is overwritten, removed or replaced, the operator must capture or confirm the immediate prior target state sufficiently to restore the affected configuration.

The capture must:

- cover every target path affected by the deployment;
- preserve file names, relative paths and exact prior bytes where those bytes remain available;
- identify the target instance and capture time;
- be stored separately from the paths being replaced; and
- remain accessible until the deployment has been accepted or recovered.

A current Home Assistant backup may support recovery where it demonstrably contains the affected state and can be restored within the required recovery objective. A backup name or routine schedule alone is not proof that the immediate prior affected files are captured.

If the prior state cannot be captured or a viable recovery route cannot be established, deployment must stop unless the user gives a specific governed exception after the limitation and consequence have been made explicit.

## 6. Transfer and Governed-Byte Preservation

The operator must transfer the accepted governed payload from the recorded source path to the recorded target path without intentional editing, reformatting, line-ending conversion, encoding conversion, merge resolution or content generation during the transfer.

If target-specific transformation is genuinely required, the transformed content must be produced and accepted as governed source before deployment or handled through separately governed work. The deployment step must not become an undocumented editing or templating stage.

The operator must record the transport actually used. Transport-specific logs, copy confirmations or screenshots may support evidence, but they must not be treated as proof of exact payload identity unless they establish it.

After transfer, the operator must establish resulting identity proportionately to risk. Prefer an exact target-side hash or byte-for-byte comparison. Where the selected transport cannot provide that evidence, use the strongest available combination of target read-back, file size, content inspection, manifest comparison and subsequent Home Assistant validation, and record the remaining limitation.

## 7. Home Assistant Configuration Validation

After transfer and before Beta acceptance, the deployed target instance must pass the Home Assistant-supported configuration check against the resulting configuration.

The validation evidence must identify:

- the target instance and environment;
- the validation route used;
- the time of validation;
- the result, including material warnings or errors; and
- the deployed candidate or resulting target state to which the result applies.

A successful file transfer, YAML parse, editor save, restart attempt or absence of an immediate visible fault does not replace the Home Assistant configuration check.

Where the change requires a reload or restart to exercise the accepted candidate, that action occurs only with applicable authority and after the configuration check succeeds. Beta acceptance applies only to the resulting deployed state whose identity and successful validation are sufficiently established.

## 8. Deployment Evidence

The governing issue or linked authoritative evidence must record at minimum:

- deployment authority and operator;
- source repository, candidate identity and source path;
- target instance, environment and exact target path;
- transport actually used;
- immediate prior-state capture identity and location or the authorised exception;
- target-byte verification performed and any unresolved manual-provenance limitation;
- Home Assistant configuration-validation route and result;
- reload or restart result where applicable;
- deployment time and overall outcome; and
- rollback or recovery result where invoked.

Evidence may remain in its authoritative native system where Linear links or references it sufficiently for closure. Credentials, access tokens, backup keys and other secrets must not be placed in Linear, Git or retained evidence.

## 9. Fail-Closed Conditions

Deployment or Beta acceptance must fail closed when any material condition prevents sufficient identification or safe validation of the governed result, including where:

- required deployment authority is absent or ambiguous;
- the source candidate or source path cannot be established;
- the target instance or target path cannot be established;
- the selected payload may differ from the accepted governed content and the difference cannot be resolved;
- the immediate prior state or viable recovery route is unavailable without an authorised exception;
- the transfer result cannot be established sufficiently for the governed change;
- Home Assistant configuration validation fails, cannot run or cannot be bound to the resulting target state; or
- required evidence is missing or contradictory.

Fail closed means stop progression, preserve available evidence and do not represent the candidate as deployed, validated or Beta-accepted. A different transport may be selected and the controlled operation retried against the same authorised candidate where doing so resolves the limitation without changing accepted substance.

## 10. Failure, Rollback and Recovery

If transfer is partial, target identity is uncertain, configuration validation fails or the deployed configuration produces unacceptable behaviour, the operator must stop further progression and assess whether restoration is required.

Rollback normally restores the recorded immediate prior state to the same deterministic target paths using an authorised available transport, then repeats the Home Assistant configuration check against the restored state. Any required reload or restart follows only after successful validation and applicable authority.

Recovery evidence must record the triggering failure, files or paths restored, prior-state identity, transport used, validation result and final target status. A failed candidate must not remain represented as accepted merely because the prior state was restored successfully.

Where safe restoration cannot be completed or verified, the issue remains incomplete and the unresolved target state must be surfaced promptly for governed recovery.

## 11. Completion and Future Mechanisms

Issue completion remains governed by the applicable workflow in `CENTRAL_GOVERNANCE.md`. For a runtime configuration change following `WF-01`, successful configuration validation is a precondition to Beta acceptance, not a substitute for Beta operation or the remaining completion controls.

This Standard governs only the `operator_selected` route. A future automated or transport-specific mechanism requires separately governed authority and must define its own identity, security, validation, rollback and evidence model before replacing this mechanism.
