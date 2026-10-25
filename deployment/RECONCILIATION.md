# Live backend reconciliation

Read-only comparison of the running backend JAR against the fork's `52615ac`
backend found exactly four differing class files and no added/removed entries.
`javap -c -p -constants` established:

- `ApplicationConfig`: live adds the `PUBLIC_ORIGIN` environment setting.
- `SecretHitlerServer`: live passes that origin to CORS, falling back to the
  upstream `https://secret-hitler.online` if unset/blank. Other instruction
  differences are constant-pool index shifts, not game logic.
- `SecretHitlerServer$1` and `$2`: disassembly is identical; class-file metadata
  differs (source line positions after the CORS edit).

The fork now preserves configurable `PUBLIC_ORIGIN`, defaults to
`https://secret-hitler.ashayc.com`, validates an exact HTTPS origin, and rejects
other browser origins before HTTP handling **and WebSocket upgrade**. No DEBUG
or wildcard is needed. Missing Origin remains allowed for non-browser clients.
This origin check is not authentication.

Regression `backend/test_origin.py` exercises real HTTP, OPTIONS, WebSocket
upgrades and lobby creation against an isolated backend/Postgres. The original
image fails the allowed-origin assertion; an HTTP-before-only implementation
failed WebSocket rejection, so enforcement uses a servlet filter instead.
CI now gates both image publications on these integration tests and unit tests.

No production containers, Compose, Caddy configuration or live database were
modified. The five existing legacy Firebase/Fly workflows remain retained and
disabled. Deployment is a separate action; pin published images by digest.
