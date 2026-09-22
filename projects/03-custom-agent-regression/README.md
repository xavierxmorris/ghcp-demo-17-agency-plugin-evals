# Project 03 — Custom-agent regression

The `change-risk-reviewer` agent reads a synthetic change plan and committed
risk policy, then writes `change-risk-review.md`.

It is deliberately bounded:

- it recommends `GO`, `GO WITH CONTROLS`, or `NO-GO`;
- it cites plan and policy evidence;
- it identifies missing evidence; and
- it never deploys, approves, or changes production.

Run one authored scenario:

```powershell
agency eval-new run `
  --plugin . `
  --task change-risk-reviewer--missing-rollback-evidence `
  --keep-tempdir
```
