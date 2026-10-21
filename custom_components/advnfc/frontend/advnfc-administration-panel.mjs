const ADVNFC_DOMAIN = "advnfc";
const ADVNFC_INTERFACE_ID = "advnfc.tag_mapping.administration";
const ASTV_DOMAIN = "astv_intent_catalogue";
const ASTV_INTERFACE_ID = "astv.intent_catalogue.administration";

const OPERATIONS = Object.freeze({
  capabilities: "get_administration_capabilities",
  status: "get_administration_status",
  list: "list_tag_mappings",
  get: "get_tag_mapping",
  validateRecord: "validate_tag_mapping_record",
  validateCandidate: "validate_tag_mapping",
  create: "create_tag_mapping",
  update: "update_tag_mapping",
  delete: "delete_tag_mapping",
  activate: "reload_tag_mapping",
});

const OPERATION_IDS = Object.freeze({
  capabilities: "capabilities",
  status: "status",
  list: "list",
  get: "get",
  validateRecord: "validate_record",
  validateCandidate: "validate_document",
  create: "create",
  update: "update",
  delete: "delete",
  activate: "activate",
});

const MANAGE_OPERATIONS = new Set([
  "validateRecord",
  "validateCandidate",
  "create",
  "update",
  "delete",
  "activate",
]);

const PROVIDER_UNAVAILABLE_CODES = new Set([
  "not_found",
  "service_not_found",
  "unknown_command",
  "dependency_unavailable",
]);

export class AdvNfcAdapterError extends Error {
  constructor(kind, code, message, cause = undefined) {
    super(message);
    this.name = "AdvNfcAdapterError";
    this.kind = kind;
    this.code = code;
    this.cause = cause;
  }
}

function nativeCode(error) {
  return String(error?.code ?? error?.error?.code ?? "unknown_error");
}

function nativeMessage(error) {
  return String(error?.message ?? error?.error?.message ?? "Home Assistant request failed");
}

function majorVersion(value) {
  return String(value ?? "").split(".")[0];
}

export function commonErrorCategory(operation, providerCode) {
  if (operation === "activate") return "activation_failed";
  return {
    invalid_query: "invalid_request",
    invalid_candidate: "invalid_request",
    duplicate_uid: "invalid_request",
    not_found: "not_found",
    already_exists: "invalid_request",
    stale_revision: "stale_revision",
    persisted_state_unavailable: "dependency_unavailable",
    atomic_write_failed: "dependency_unavailable",
  }[providerCode] ?? "provider_failed";
}

export class AdvNfcProviderAdapter {
  constructor(hass, { timeoutMs = 15000 } = {}) {
    this.hass = hass;
    this.timeoutMs = timeoutMs;
    this.capabilities = null;
  }

  setHass(hass) {
    this.hass = hass;
  }

  get canManage() {
    return this.hass?.user?.is_admin === true;
  }

  async callService(domain, service, serviceData = {}) {
    if (!this.hass?.callWS) {
      throw new AdvNfcAdapterError("client", "connection_unavailable", "Home Assistant WebSocket is unavailable.");
    }

    let timer;
    const timeout = new Promise((_, reject) => {
      timer = globalThis.setTimeout(
        () => reject(new AdvNfcAdapterError("timeout", "timeout", `Timed out calling ${domain}.${service}.`)),
        this.timeoutMs,
      );
    });

    try {
      const result = await Promise.race([
        this.hass.callWS({
          type: "call_service",
          domain,
          service,
          service_data: serviceData,
          return_response: true,
        }),
        timeout,
      ]);
      if (!result || typeof result.response !== "object" || result.response === null) {
        throw new AdvNfcAdapterError("transport", "invalid_response", `${domain}.${service} returned no response payload.`);
      }
      return result.response;
    } catch (error) {
      if (error instanceof AdvNfcAdapterError) throw error;
      const code = nativeCode(error);
      const kind = ["unauthorized", "permission_denied"].includes(code) ? "permission" : "transport";
      throw new AdvNfcAdapterError(kind, kind === "permission" ? "permission_denied" : code, nativeMessage(error), error);
    } finally {
      globalThis.clearTimeout(timer);
    }
  }

  async call(operation, serviceData = {}) {
    const service = OPERATIONS[operation];
    if (!service) {
      throw new AdvNfcAdapterError("client", "unsupported_operation", `Unsupported operation: ${operation}`);
    }
    if (MANAGE_OPERATIONS.has(operation) && !this.canManage) {
      throw new AdvNfcAdapterError("permission", "permission_denied", "Administrator access is required.");
    }
    return this.callService(ADVNFC_DOMAIN, service, serviceData);
  }

  async discover() {
    const response = await this.call("capabilities");
    if (!response.ok || response.interface_id !== ADVNFC_INTERFACE_ID || majorVersion(response.interface_version) !== "3" || response.tag_mapping_schema_version !== 1) {
      throw new AdvNfcAdapterError("provider", "incompatible_interface", "The installed AdvNFC administration interface is not compatible.");
    }
    if (!Array.isArray(response.supported_action_types) || !response.supported_action_types.includes("astv_intent")) {
      throw new AdvNfcAdapterError("provider", "incompatible_schema", "The installed provider does not advertise the schema-v1 astv_intent action.");
    }
    this.capabilities = response;
    return response;
  }

  async requireOperation(operation) {
    const discovery = this.capabilities ?? await this.discover();
    const operationId = OPERATION_IDS[operation];
    if (!Array.isArray(discovery.operations) || !discovery.operations.includes(operationId)) {
      throw new AdvNfcAdapterError("provider", "unsupported_operation", `The installed provider does not advertise ${operationId}.`);
    }
    return discovery;
  }

  async status() {
    await this.requireOperation("status");
    return this.call("status");
  }

  async list() {
    await this.requireOperation("list");
    return this.call("list");
  }

  async guardedMutation(operation, payload = {}) {
    if (!["create", "update", "delete"].includes(operation)) {
      throw new AdvNfcAdapterError("client", "unsupported_mutation", `Not a revision-guarded mutation: ${operation}`);
    }
    await this.requireOperation(operation);
    const before = await this.status();
    if (!before.ok || !before.persisted_revision) return before;

    try {
      const result = await this.call(operation, {
        ...payload,
        expected_revision: before.persisted_revision,
      });
      if (result?.ok !== false) return result;
      if (result?.error?.code !== "stale_revision") {
        return { ...result, category: commonErrorCategory(operation, result.error?.code) };
      }
      return {
        ok: false,
        conflict: true,
        category: "stale_revision",
        result,
        refreshed_status: await this.status(),
        refreshed_active: await this.list(),
      };
    } catch (error) {
      if (!(error instanceof AdvNfcAdapterError) || error.kind !== "timeout") throw error;
      return {
        ok: false,
        uncertain: true,
        error: { code: error.code, message: error.message },
        refreshed_status: await this.status(),
        refreshed_active: await this.list(),
      };
    }
  }

  async activate() {
    await this.requireOperation("activate");
    const before = await this.status();
    if (!before.ok || !before.activation_required) {
      return { ok: false, error: { code: "activation_not_required", message: "Persisted and active revisions already match." }, status: before };
    }

    try {
      const result = await this.call("activate");
      if (!result.ok) {
        return { ...result, category: commonErrorCategory("activate", result.error?.code) };
      }
      const verifiedStatus = await this.status();
      return {
        ...result,
        verified_status: verifiedStatus,
        verified: verifiedStatus.ok === true
          && verifiedStatus.activation_required === false
          && verifiedStatus.active_revision === verifiedStatus.persisted_revision,
      };
    } catch (error) {
      if (!(error instanceof AdvNfcAdapterError) || error.kind !== "timeout") throw error;
      return {
        ok: false,
        uncertain: true,
        category: "activation_failed",
        error: { code: error.code, message: error.message },
        refreshed_status: await this.status(),
        refreshed_active: await this.list(),
      };
    }
  }

  async listAstvIntentTargets() {
    let discovery;
    try {
      discovery = await this.callService(ASTV_DOMAIN, "get_administration_capabilities");
    } catch (error) {
      if (error instanceof AdvNfcAdapterError && PROVIDER_UNAVAILABLE_CODES.has(error.code)) {
        return { available: false, state: "unavailable", intents: [], reason: "provider_unavailable" };
      }
      throw error;
    }
    if (!discovery.ok) {
      const state = PROVIDER_UNAVAILABLE_CODES.has(discovery.error?.code) ? "unavailable" : "error";
      return { available: false, state, intents: [], response: discovery };
    }
    if (discovery.interface_id !== ASTV_INTERFACE_ID || majorVersion(discovery.interface_version) !== "1" || !discovery.capabilities?.includes("active.list")) {
      return { available: false, state: "incompatible", intents: [], reason: "incompatible_provider" };
    }

    const intents = [];
    let cursor;
    let activeRevision;
    do {
      // Omitted view is active for both ASTV interface v1.0 and v1.1.
      const serviceData = { limit: 200 };
      if (cursor) serviceData.cursor = cursor;
      const page = await this.callService(ASTV_DOMAIN, "list_intent_records", serviceData);
      if (!page.ok) {
        const state = PROVIDER_UNAVAILABLE_CODES.has(page.error?.code) ? "unavailable" : "error";
        return { available: false, state, intents: [], response: page };
      }
      if (activeRevision !== undefined && page.active_revision !== activeRevision) {
        return { available: false, state: "stale", intents: [], reason: "revision_changed_during_pagination" };
      }
      activeRevision = page.active_revision;
      intents.push(...(Array.isArray(page.records) ? page.records : []));
      cursor = page.next_cursor ?? null;
    } while (cursor);
    return { available: true, state: "available", active_revision: activeRevision, intents };
  }
}

export class AdvNfcAdministrationPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.adapter = null;
    this.busy = false;
  }

  set hass(value) {
    this._hass = value;
    if (!this.adapter) this.adapter = new AdvNfcProviderAdapter(value);
    else this.adapter.setHass(value);
    if (!this.shadowRoot.childElementCount) this.render();
    const permission = this.shadowRoot.querySelector(".permission");
    if (permission) permission.textContent = `Read access: available · Manage access: ${this.adapter.canManage ? "administrator" : "read only"}`;
  }

  set panel(value) {
    this._panel = value;
  }

  async run(operation) {
    if (this.busy) return;
    this.busy = true;
    this.renderStatus("Loading…", "loading");
    this.toggleButtons(true);
    try {
      const response = operation === "capabilities"
        ? await this.adapter.discover()
        : operation === "status"
          ? await this.adapter.status()
          : operation === "mappings"
            ? await this.adapter.list()
            : await this.adapter.listAstvIntentTargets();
      const success = response.ok === true || response.available === true;
      this.renderStatus(JSON.stringify(response, null, 2), success ? "success" : "error");
    } catch (error) {
      this.renderStatus(`${error.code ?? "error"}: ${error.message}`, "error");
    } finally {
      this.busy = false;
      this.toggleButtons(false);
    }
  }

  toggleButtons(disabled) {
    this.shadowRoot.querySelectorAll("button").forEach((button) => { button.disabled = disabled; });
  }

  renderStatus(text, state = "idle") {
    const output = this.shadowRoot.querySelector("pre");
    if (!output) return;
    output.textContent = text;
    output.dataset.state = state;
  }

  render() {
    if (!this.shadowRoot || !this._hass || this.shadowRoot.childElementCount) return;
    this.shadowRoot.innerHTML = `
      <style>
        :host { display: block; min-height: 100%; color: var(--primary-text-color); background: var(--primary-background-color); }
        main { box-sizing: border-box; max-width: 62rem; margin: 0 auto; padding: max(1rem, env(safe-area-inset-top)) max(1rem, env(safe-area-inset-right)) max(1rem, env(safe-area-inset-bottom)) max(1rem, env(safe-area-inset-left)); }
        h1 { font-size: clamp(1.35rem, 5vw, 2rem); margin: 0 0 .35rem; }
        p { line-height: 1.45; }
        .permission { color: var(--secondary-text-color); }
        .actions { display: grid; grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr)); gap: .75rem; margin: 1rem 0; }
        button { min-height: 2.75rem; border: 0; border-radius: .4rem; padding: .65rem .85rem; color: var(--text-primary-color, white); background: var(--primary-color); font: inherit; cursor: pointer; }
        button:disabled { opacity: .55; cursor: progress; }
        pre { min-height: 10rem; overflow: auto; white-space: pre-wrap; overflow-wrap: anywhere; padding: 1rem; border-radius: .5rem; background: var(--card-background-color); box-shadow: var(--ha-card-box-shadow, none); }
        pre[data-state="error"] { border-inline-start: .3rem solid var(--error-color); }
        pre[data-state="success"] { border-inline-start: .3rem solid var(--success-color, #2e7d32); }
        @media (max-width: 420px) { main { padding-inline: .75rem; } .actions { grid-template-columns: 1fr 1fr; } }
      </style>
      <main>
        <h1>AdvNFC Administration</h1>
        <p>Read-only transport proof for provider state, active tag mappings, and optional ASTV intent discovery. It cannot save or activate mappings.</p>
        <p class="permission">Read access: available · Manage access: ${this.adapter.canManage ? "administrator" : "read only"}</p>
        <div class="actions">
          <button data-operation="capabilities">Capabilities</button>
          <button data-operation="status">Status</button>
          <button data-operation="mappings">Active mappings</button>
          <button data-operation="intents">ASTV targets</button>
        </div>
        <pre aria-live="polite">Choose a proof operation.</pre>
      </main>`;
    this.shadowRoot.querySelectorAll("button").forEach((button) => {
      button.addEventListener("click", () => this.run(button.dataset.operation));
    });
  }
}

if (globalThis.customElements && !globalThis.customElements.get("advnfc-administration-panel")) {
  globalThis.customElements.define("advnfc-administration-panel", AdvNfcAdministrationPanel);
}
