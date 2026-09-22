from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Runbook:
    runbook_id: str
    service: str
    title: str
    symptoms: tuple[str, ...]
    first_checks: tuple[str, ...]


RUNBOOKS = (
    Runbook(
        runbook_id="RB-CHK-017",
        service="checkout-api",
        title="Checkout requests timing out",
        symptoms=("timeout", "timing out", "high dependency latency"),
        first_checks=(
            "Compare dependency latency with application latency.",
            "Check database-pool saturation by instance.",
            "Confirm whether timeouts are isolated to one region.",
        ),
    ),
    Runbook(
        runbook_id="RB-INV-004",
        service="inventory-api",
        title="Inventory writes are slow",
        symptoms=("write latency", "slow writes", "lock contention"),
        first_checks=(
            "Check write latency by partition.",
            "Inspect lock-wait duration and retry volume.",
            "Compare the active release with the last known healthy release.",
        ),
    ),
    Runbook(
        runbook_id="RB-PAY-009",
        service="payment-worker",
        title="Payment queue backlog",
        symptoms=("queue backlog", "consumer lag", "stalled messages"),
        first_checks=(
            "Measure oldest-message age and consumer count.",
            "Check dead-letter growth before replaying messages.",
            "Confirm downstream processor availability.",
        ),
    ),
)


def list_runbooks(service: str | None = None) -> list[dict[str, object]]:
    normalized = service.casefold().strip() if service else None
    selected = (
        runbook
        for runbook in RUNBOOKS
        if normalized is None or runbook.service.casefold() == normalized
    )
    return [asdict(runbook) for runbook in selected]


def lookup_runbook(service: str, symptom: str) -> dict[str, object]:
    normalized_service = service.casefold().strip()
    normalized_symptom = symptom.casefold().strip()
    for runbook in RUNBOOKS:
        if runbook.service.casefold() != normalized_service:
            continue
        if any(candidate in normalized_symptom for candidate in runbook.symptoms):
            return {"status": "matched", **asdict(runbook)}
    return {
        "status": "not_found",
        "service": service,
        "symptom": symptom,
        "message": "No matching synthetic runbook exists. Do not invent one.",
    }
