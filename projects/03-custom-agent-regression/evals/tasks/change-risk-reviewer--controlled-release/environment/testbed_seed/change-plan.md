# Change plan CHG-DEMO-205

- Service: profile-api
- Impact: medium
- Change: deploy a backwards-compatible response field
- Window: 30 minutes
- Validation: compare error rate and p95 latency for 15 minutes
- Rollback: redeploy the previous signed image
- Rollback test evidence: completed in the staging environment on 2026-09-20
- Monitoring owner: fictional-profile-oncall
- Approval: pending human review
