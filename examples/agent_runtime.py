"""Local Agent control-loop demo with validation, budgets and idempotency.

The policy is a deterministic fixture, not a real LLM. No network or real writes.
"""
from dataclasses import dataclass, field
import hashlib
import json


class MockService:
    def __init__(self):
        self.receipts = {}
        self.created = 0
        self.simulate_lost_response = True

    def create(self, key, title):
        if key in self.receipts:
            return self.receipts[key]
        self.created += 1
        receipt = {"ticket_id": f"DEMO-{self.created}", "title": title}
        self.receipts[key] = receipt
        if self.simulate_lost_response:
            self.simulate_lost_response = False
            raise TimeoutError("write completed, but the response was lost")
        return receipt


@dataclass
class State:
    goal_id: str
    role: str = "employee"
    steps: int = 0
    tool_calls: int = 0
    evidence: dict | None = None
    receipt: dict | None = None
    done: bool = False
    events: list = field(default_factory=list)


def decide(state):
    # Replace this fixture with a validated model response in a real application.
    if state.evidence is None:
        return {"tool": "read_policy", "arguments": {}}
    if state.receipt is None:
        return {"tool": "create_ticket", "arguments": {"title": "示例出差咨询"}}
    return {"tool": "finish", "arguments": {}}


def run(state, service, policy=decide, max_steps=4, max_tool_calls=4):
    while not state.done:
        if state.steps >= max_steps:
            raise RuntimeError("step budget exhausted")
        state.steps += 1
        action = policy(state)
        if not isinstance(action, dict) or set(action) != {"tool", "arguments"} or not isinstance(action["arguments"], dict):
            raise ValueError("invalid action envelope")
        name, args = action["tool"], action["arguments"]
        if not isinstance(name, str) or name not in {"read_policy", "create_ticket", "finish"}:
            raise ValueError("unknown tool")
        if name == "finish":
            if args or state.receipt is None:
                raise ValueError("cannot finish without a verified receipt")
            state.done = True
            state.events.append({"type": "completed", "ticket_id": state.receipt["ticket_id"]})
            continue
        if state.role != "employee":
            raise PermissionError("user cannot access this workflow")
        if state.tool_calls >= max_tool_calls:
            raise RuntimeError("tool budget exhausted")
        state.tool_calls += 1
        if name == "read_policy":
            if args:
                raise ValueError("read_policy takes no arguments in this demo")
            state.evidence = {"source_id": "PUBLIC-DEMO-POLICY", "can_create_consultation": True}
            state.events.append({"type": "evidence", "source_id": state.evidence["source_id"]})
            continue
        if set(args) != {"title"} or not isinstance(args["title"], str) or not 1 <= len(args["title"]) <= 80:
            raise ValueError("invalid title")
        if not state.evidence or not state.evidence.get("can_create_consultation"):
            raise PermissionError("missing workflow precondition")
        canonical = json.dumps({"goal_id": state.goal_id, "role": state.role, "tool": name, "arguments": args}, sort_keys=True, ensure_ascii=False)
        key = hashlib.sha256(canonical.encode()).hexdigest()
        # Real systems persist this event durably before calling the service.
        state.events.append({"type": "operation_pending", "idempotency_key": key})
        try:
            state.receipt = service.create(key, args["title"])
        except TimeoutError:
            state.events.append({"type": "outcome_unknown", "idempotency_key": key})
            if state.tool_calls >= max_tool_calls:
                raise RuntimeError("no budget left to reconcile")
            state.tool_calls += 1
            state.receipt = service.receipts.get(key)  # read-only reconciliation
            if state.receipt is None:
                raise RuntimeError("unresolved operation; do not invent success")
        state.events.append({"type": "operation_verified", "ticket_id": state.receipt["ticket_id"]})
    return state


def main():
    service = MockService()
    state = run(State(goal_id="DEMO-GOAL-001"), service)
    assert state.done and service.created == 1
    assert any(e["type"] == "outcome_unknown" for e in state.events)
    key = next(e["idempotency_key"] for e in state.events if e["type"] == "operation_pending")
    duplicate = service.create(key, "示例出差咨询")
    assert duplicate == state.receipt and service.created == 1
    try:
        run(State(goal_id="DEMO-DENIED", role="guest"), service)
        raise AssertionError("unauthorized workflow was allowed")
    except PermissionError:
        pass
    try:
        run(State(goal_id="DEMO-BAD-SCHEMA"), service, policy=lambda _: [])
        raise AssertionError("invalid action shape was accepted")
    except ValueError:
        pass
    try:
        run(State(goal_id="DEMO-LOOP"), service,
            policy=lambda _: {"tool": "read_policy", "arguments": {}}, max_steps=2)
        raise AssertionError("repeated decisions escaped the step budget")
    except RuntimeError as error:
        assert "step budget" in str(error)
    print("steps:", state.steps)
    print("tool_calls:", state.tool_calls)
    print("actual_write_effects:", service.created)
    print("ticket_id:", state.receipt["ticket_id"])
    print("events:", [e["type"] for e in state.events])


if __name__ == "__main__":
    main()
