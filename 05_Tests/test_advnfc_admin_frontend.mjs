import assert from "node:assert/strict";
import test from "node:test";

globalThis.HTMLElement = class {};

const {
  AdvNfcAdapterError,
  AdvNfcProviderAdapter,
  commonErrorCategory,
} = await import("../custom_components/advnfc/frontend/advnfc-administration-panel.mjs");

function hassWith(handler, isAdmin = false) {
  return {
    user: { is_admin: isAdmin },
    callWS: async (message) => handler(message),
  };
}

function capabilities(extra = {}) {
  return {
    ok: true,
    interface_id: "advnfc.tag_mapping.administration",
    interface_version: 3,
    tag_mapping_schema_version: 1,
    supported_action_types: ["astv_intent"],
    operations: ["capabilities", "status", "list", "create", "update", "delete", "activate"],
    ...extra,
  };
}

test("response-only calls use the authenticated Home Assistant WebSocket envelope", async () => {
  let observed;
  const adapter = new AdvNfcProviderAdapter(hassWith(async (message) => {
    observed = message;
    return { context: { id: "ctx" }, response: capabilities() };
  }));

  const response = await adapter.discover();
  assert.equal(response.ok, true);
  assert.deepEqual(observed, {
    type: "call_service",
    domain: "advnfc",
    service: "get_administration_capabilities",
    service_data: {},
    return_response: true,
  });
});

test("capability negotiation rejects the wrong interface major or schema", async () => {
  for (const response of [
    capabilities({ interface_version: 2 }),
    capabilities({ tag_mapping_schema_version: 2 }),
    capabilities({ supported_action_types: [] }),
  ]) {
    const adapter = new AdvNfcProviderAdapter(hassWith(async () => ({ context: {}, response })));
    await assert.rejects(adapter.discover(), (error) => error.kind === "provider");
  }
});

test("Home Assistant permission errors remain separate from provider outcomes", async () => {
  const adapter = new AdvNfcProviderAdapter(hassWith(async () => {
    throw { code: "unauthorized", message: "Unauthorized" };
  }));
  await assert.rejects(
    adapter.discover(),
    (error) => error instanceof AdvNfcAdapterError
      && error.kind === "permission"
      && error.code === "permission_denied",
  );
});

test("timeout is visible and does not become a provider outcome", async () => {
  const adapter = new AdvNfcProviderAdapter(
    hassWith(() => new Promise(() => {})),
    { timeoutMs: 5 },
  );
  await assert.rejects(
    adapter.discover(),
    (error) => error.kind === "timeout" && error.code === "timeout",
  );
});

test("non-admin clients cannot initiate manage operations", async () => {
  let called = false;
  const adapter = new AdvNfcProviderAdapter(hassWith(async () => {
    called = true;
    return {};
  }));
  await assert.rejects(
    adapter.call("create", {}),
    (error) => error.kind === "permission" && error.code === "permission_denied",
  );
  assert.equal(called, false);
});

test("guarded save uses persisted_revision and never retries stale writes", async () => {
  const calls = [];
  let statusReads = 0;
  const adapter = new AdvNfcProviderAdapter(hassWith(async (message) => {
    calls.push(message);
    let response;
    if (message.service === "get_administration_capabilities") response = capabilities();
    else if (message.service === "get_administration_status") {
      statusReads += 1;
      response = { ok: true, persisted_revision: statusReads === 1 ? "persisted-old" : "persisted-new", active_revision: "active", activation_required: true };
    } else if (message.service === "create_tag_mapping") {
      response = { ok: false, error: { code: "stale_revision", message: "Stale" } };
    } else response = { ok: true, mappings: [], active_revision: "active" };
    return { context: {}, response };
  }, true));

  const result = await adapter.guardedMutation("create", { mapping: { uid: "A1" } });
  assert.equal(result.conflict, true);
  const writes = calls.filter((call) => call.service === "create_tag_mapping");
  assert.equal(writes.length, 1);
  assert.equal(writes[0].service_data.expected_revision, "persisted-old");
  assert.equal(result.refreshed_status.persisted_revision, "persisted-new");
});

test("successful save remains activation-required and does not reload", async () => {
  const calls = [];
  const adapter = new AdvNfcProviderAdapter(hassWith(async (message) => {
    calls.push(message);
    const response = message.service === "get_administration_capabilities"
      ? capabilities()
      : message.service === "get_administration_status"
        ? { ok: true, persisted_revision: "persisted-old", active_revision: "active", activation_required: false }
        : { ok: true, persisted_revision: "persisted-new", active_revision: "active", activation_required: true };
    return { context: {}, response };
  }, true));

  const result = await adapter.guardedMutation("update", { mapping: { uid: "A1" } });
  assert.equal(result.activation_required, true);
  assert.equal(result.active_revision, "active");
  assert.equal(result.persisted_revision, "persisted-new");
  assert.equal(calls.some((call) => call.service === "reload_tag_mapping"), false);
});

test("explicit activation is separate, unguarded, and verifies revision equality", async () => {
  const calls = [];
  let statusReads = 0;
  const adapter = new AdvNfcProviderAdapter(hassWith(async (message) => {
    calls.push(message);
    let response;
    if (message.service === "get_administration_capabilities") response = capabilities();
    else if (message.service === "get_administration_status") {
      statusReads += 1;
      response = statusReads === 1
        ? { ok: true, active_revision: "active-old", persisted_revision: "persisted", activation_required: true }
        : { ok: true, active_revision: "persisted", persisted_revision: "persisted", activation_required: false };
    } else response = { ok: true, operation: "activate", active_revision: "persisted", persisted_revision: "persisted", activation_required: false };
    return { context: {}, response };
  }, true));

  const result = await adapter.activate();
  const activation = calls.find((call) => call.service === "reload_tag_mapping");
  assert.deepEqual(activation.service_data, {});
  assert.equal(result.verified, true);
});

test("AdvNFC provider codes normalize through the documented compatibility profile", () => {
  assert.equal(commonErrorCategory("update", "invalid_candidate"), "invalid_request");
  assert.equal(commonErrorCategory("delete", "stale_revision"), "stale_revision");
  assert.equal(commonErrorCategory("create", "atomic_write_failed"), "dependency_unavailable");
  assert.equal(commonErrorCategory("activate", "invalid_candidate"), "activation_failed");
});

test("guarded mutation returns the normalized category with provider detail", async () => {
  const adapter = new AdvNfcProviderAdapter(hassWith(async (message) => ({
    context: {},
    response: message.service === "get_administration_capabilities"
      ? capabilities()
      : message.service === "get_administration_status"
        ? { ok: true, persisted_revision: "persisted", active_revision: "active", activation_required: true }
        : { ok: false, error: { code: "atomic_write_failed", message: "Write failed" } },
  }), true));

  const result = await adapter.guardedMutation("create", { mapping: { uid: "A1" } });
  assert.equal(result.category, "dependency_unavailable");
  assert.equal(result.error.code, "atomic_write_failed");
});

test("optional ASTV intent discovery follows pagination without mixing revisions", async () => {
  const calls = [];
  const adapter = new AdvNfcProviderAdapter(hassWith(async (message) => {
    calls.push(message);
    if (message.service === "get_administration_capabilities") {
      return { context: {}, response: { ok: true, interface_id: "astv.intent_catalogue.administration", interface_version: "1.1.0", capabilities: ["active.list"] } };
    }
    const second = message.service_data.cursor === "page-2";
    return { context: {}, response: {
      ok: true,
      active_revision: "astv-active",
      records: [{ intent_id: second ? "two" : "one", record: { title: second ? "Two" : "One" } }],
      next_cursor: second ? null : "page-2",
    } };
  }));

  const result = await adapter.listAstvIntentTargets();
  assert.equal(result.available, true);
  assert.deepEqual(result.intents.map((entry) => entry.intent_id), ["one", "two"]);
  assert.equal(calls.filter((call) => call.service === "list_intent_records").length, 2);
  assert.equal(calls[1].service_data.limit, 200);
  assert.equal(Object.hasOwn(calls[1].service_data, "view"), false);
});

test("optional ASTV absence or incompatibility does not disable AdvNFC", async () => {
  const unavailable = new AdvNfcProviderAdapter(hassWith(async () => {
    throw { code: "service_not_found", message: "Missing" };
  }));
  assert.deepEqual(await unavailable.listAstvIntentTargets(), {
    available: false,
    state: "unavailable",
    intents: [],
    reason: "provider_unavailable",
  });

  const incompatible = new AdvNfcProviderAdapter(hassWith(async () => ({
    context: {},
    response: { ok: true, interface_id: "other", interface_version: "1.1.0", capabilities: [] },
  })));
  assert.equal((await incompatible.listAstvIntentTargets()).state, "incompatible");
});
