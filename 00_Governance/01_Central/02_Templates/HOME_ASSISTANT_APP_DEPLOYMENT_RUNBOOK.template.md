# Home Assistant App Custom-Repository Deployment Runbook: <Product>

**Template:** Home Assistant App Deployment Runbook
**Version:** v1.1.1
**Status:** Approved
**Approval tag:** `home-assistant-app-deployment-runbook-template-v1.1.1`
**Approval date:** 2026-10-05

This centrally managed template is an implementation aid for governed Home Assistant App install, update and rollback through a Git custom repository. `HOME_ASSISTANT_APP_DEPLOYMENT_STANDARD.md`, as required by Central Governance Section 18.8, is the detailed authority. This runbook does not grant publication, deployment, rollback or promotion authority.

## 1. Operation identity

- Governing Linear issue: `<ISSUE-ID>`
- Product repository: `<owner/repository>`
- Target Home Assistant environment: `<environment>`
- Operation: `<Beta install | Beta update | stable install | stable update | rollback>`
- Repository source entered in Home Assistant: `<URL[#branch]>`
- Selected branch: `<beta | main | approved release branch>`
- Git candidate SHA: `<full SHA>`
- App slug and version: `<slug> / <version>`
- Prior working source/SHA/version: `<source / SHA / version>`
- Operator: `<person or authorised agent>`

## 2. Required authority

- [ ] The issue is at the applicable governed deployment gate.
- [ ] Human acceptance and required validation remain valid for the exact candidate.
- [ ] Explicit deployment authority identifies the repository, candidate, environment and purpose.
- [ ] If the repository is private and anonymous Supervisor access is required, explicit authority covers the bounded temporary-public window and acknowledges that third-party copies or caches may persist permanently.
- Authorisation reference and time: `<Linear comment/reference and timestamp>`

## 3. Repository and publication preflight

- [ ] Root `repository.yaml` validates.
- [ ] The App package and its `config.yaml` are under canonical `04_Implementation/haos/source/apps/<app>/**`, or under legacy `04_Source/<app>/**` only while an explicit migration issue remains open.
- [ ] No duplicate App package exists at repository root.
- [ ] The complete current tree and reachable Git history were reviewed for secrets, credentials, personal data, sensitive operational evidence and other non-public content.
- [ ] No private dependency or submodule will be exposed, broken or made unusable by anonymous access.
- [ ] Product licence and third-party content permit the authorised publication.
- [ ] Repository source and selected branch resolve to the recorded SHA.
- [ ] App version and required image/build inputs correspond to the candidate and are obtainable.
- [ ] App configuration and App-private data are backed up or have a verified preservation route.
- [ ] The prior working candidate and rollback procedure are usable.
- Preflight evidence: `<links, commands/results or retained evidence references>`

## 4. Public-window boundary, when applicable

- Planned opening condition/time: `<condition / time>`
- Planned closing condition/deadline: `<condition / time>`
- Responsible operator: `<operator>`
- [ ] Only the authorised repository was made public.
- Public visibility verified at: `<timestamp and evidence>`

If visibility cannot be restored and verified by the deadline, stop further deployment activity, notify the user, record the exposure in Linear and treat the repository as public until restoration is proven.

## 5. Install or update

1. In the intended Home Assistant environment, add or repair the exact recorded repository source. Beta normally uses `https://github.com/<owner>/<repository>#beta`.
2. Refresh the App store and verify the repository/source and intended App are present.
3. Install or update only the recorded App version/candidate.
4. Start or restart the App as required by its product deployment authority.
5. Verify the installed version, running state and sufficient deployed content or runtime identity to bind the result to the recorded Git candidate.
6. Perform the product-specific smoke/preflight checks required for the issue.

- Home Assistant repository identity/source observed: `<value>`
- Installed App slug/version observed: `<value>`
- Candidate/deployed-content verification: `<evidence>`
- Runtime checks: `<evidence>`
- Result: `<passed | failed>`

## 6. Close the public window, when applicable

- [ ] Repository visibility was restored to private promptly after the authorised operation.
- Private visibility verified at: `<timestamp and evidence>`
- Public window duration: `<start to end>`
- [ ] Linear records the visibility transition and irreversible-disclosure acknowledgement.

Do not report the operation complete while restored privacy is unverified.

## 7. Failure and rollback

If the operation fails:

1. restore private visibility first if a public window remains open, unless the user explicitly authorises a bounded recovery extension;
2. retain non-secret diagnostic evidence;
3. preserve the existing repository/App identity and App-private data where practical;
4. restore the recorded prior working source/candidate with required authority;
5. verify installed version, running state, data preservation and repository visibility; and
6. record the failure and rollback result against the governing Linear issue.

Do not remove/re-add the repository or reinstall the App as a default rollback when that could detach the App or discard App-private data.

- Failure evidence: `<reference or N/A>`
- Rollback authority: `<reference or N/A>`
- Rollback result and verification: `<reference or N/A>`

## 8. Closure evidence

- [ ] Governing issue, environment, repository source, branch, App slug/version and Git SHA are recorded.
- [ ] Preflight result is recorded.
- [ ] Install/update and running-state verification are recorded.
- [ ] Visibility opening/restoration evidence is recorded where applicable.
- [ ] Rollback result is recorded where applicable.
- [ ] No secret material is retained in the evidence.
- [ ] Any state-changing action after validation received proportionate revalidation.

Closure record: `<Linear comment/link>`
