# AdvNFC

AdvNFC provides the governed Home Assistant NFC tag-mapping integration and
its operator-selected Home Assistant configuration. It consumes reader events
published by the separately governed AdvNFC Reader Agent product.

Install the custom integration by adding `83degrees/AdvNFC` to HACS as an
Integration repository. HACS is the normal installation and update route for
`custom_components/advnfc`; do not routinely copy that directory into Home
Assistant by hand.

The Home Assistant package and tag mapping remain operator-managed because
they are separate configuration payloads. See `08_Deployment/` for the HACS
and Home Assistant configuration runbooks.
