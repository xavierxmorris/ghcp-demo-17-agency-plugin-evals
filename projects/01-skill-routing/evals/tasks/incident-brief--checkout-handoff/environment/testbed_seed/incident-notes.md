# Checkout incident notes

- Incident ID: INC-DEMO-1042
- Declared severity: SEV2
- Service: checkout-api
- Start: 2026-09-21 08:42 UTC
- Observed impact: some checkout requests exceed 30 seconds and time out
- Confirmed evidence: application instances are healthy; dependency latency rose
- Working hypothesis: the database connection pool may be saturated
- Mitigation attempted: increased one canary instance from 20 to 30 connections
- Result: no confirmed recovery yet
- Missing: affected-region breakdown and failed-request percentage
