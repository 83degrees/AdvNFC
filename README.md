# AdvNFC

AdvNFC provides the governed Home Assistant NFC tag-mapping integration,
operator-selected Home Assistant configuration, and the Raspberry Pi NFC
reader agent.

Install the custom integration by adding `83degrees/AdvNFC` to HACS as an
Integration repository. HACS is the normal installation and update route for
`custom_components/advnfc`; do not routinely copy that directory into Home
Assistant by hand.

The Home Assistant package and tag mapping remain operator-managed because
they are separate configuration payloads. See `08_Deployment/` for the HACS,
Home Assistant configuration, and Debian package runbooks.
