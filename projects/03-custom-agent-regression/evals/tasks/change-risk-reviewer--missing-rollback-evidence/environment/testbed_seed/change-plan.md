# Change plan CHG-DEMO-204

- Service: orders-db
- Impact: high
- Change: migrate the primary orders table to a new partition key
- Window: 60 minutes
- Validation: compare row counts after migration
- Rollback: restore from backup if required
- Rollback test evidence: not supplied
- Approval: pending human review
