"""
HiveMind_Core.py

Chambers Enterprise Grid Node:
HiveMind Core (HMC) — a centralized, external “swarm brain” (MCP-style server) that enables
stigmergic coordination across many lightweight agents.

Design intent
-------------
- Agents are lightweight, ephemeral, and mostly stateless (short-term context only).
- All coordination occurs via HMC: a shared substrate (stigmergy board + collective memory +
  goal hierarchy + emergence engine).
- This replaces per-agent long-term memory with persistent collective state.
- Emergent “swarm intelligence” arises from concurrent read/write, reinforcement, and routing.

This module is a functional architectural skeleton meant to be:
- uploaded to VS Code,
- extended into an actual service (FastAPI/gRPC/WebSocket),
- backed by real CRDT storage, vector DB, hypergraph store, and event streaming.

No external dependencies required for the skeleton.

Author: Codified from Chris Chambers' HiveMind Core overview.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from threading import RLock
from typing import Any, Dict, List, Optional, Protocol, Tuple


# =============================================================================
# Core Types
# =============================================================================

class Role(str, Enum):
    """Example role registry. Extend freely."""
    RESEARCHER = "researcher"
    DESIGNER = "designer"
    CODER = "coder"
    TESTER = "tester"
    OPS = "ops"
    SALES = "sales"
    EXEC = "exec"
    GENERAL = "general"


class ArtifactKind(str, Enum):
    """Artifacts written to stigmergy board / memory."""
    TASK = "task"
    PROPOSAL = "proposal"
    EVIDENCE = "evidence"
    RESULT = "result"
    VOTE = "vote"
    OBSERVATION = "observation"
    TRAIL = "trail"


class Priority(int, Enum):
    LOW = 1
    MEDIUM = 5
    HIGH = 9
    CRITICAL = 10


def now_ms() -> int:
    return int(time.time() * 1000)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


# =============================================================================
# Agent Connection & Capability Model
# =============================================================================

@dataclass(frozen=True)
class AgentCapabilities:
    roles: Tuple[Role, ...] = (Role.GENERAL,)
    tags: Tuple[str, ...] = ()
    max_concurrency: int = 1
    latency_budget_ms: int = 100  # target sub-100ms consistency at scale (implementation-specific)


@dataclass
class AgentSession:
    agent_id: str
    capabilities: AgentCapabilities
    connected_at_ms: int = field(default_factory=now_ms)
    last_seen_ms: int = field(default_factory=now_ms)
    # optional: auth claims, rate limits, etc.
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# Stigmergy Artifacts (Shared Blackboard Entries)
# =============================================================================

@dataclass
class Artifact:
    artifact_id: str
    kind: ArtifactKind
    created_at_ms: int
    updated_at_ms: int
    author_agent_id: Optional[str]
    role_hint: Optional[Role]

    # Coordination fields
    priority: Priority = Priority.MEDIUM
    pheromone_strength: float = 0.0      # reinforcement signal (stigmergy)
    confidence: float = 0.5              # how sure is the writer (0..1)
    ttl_ms: Optional[int] = None         # ephemeral artifacts can expire

    # Content fields
    title: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self, t_ms: Optional[int] = None) -> bool:
        if self.ttl_ms is None:
            return False
        t_ms = t_ms or now_ms()
        return (t_ms - self.created_at_ms) > self.ttl_ms


# =============================================================================
# CRDT / Consensus Abstractions (Placeholders)
# =============================================================================

class CRDTStore(Protocol):
    """
    Abstract interface for a CRDT-backed store (or equivalent).
    In a real implementation, this might be Redis CRDT, AntidoteDB, Yjs, etc.
    """
    def get(self, key: str) -> Any: ...
    def set(self, key: str, value: Any) -> None: ...
    def merge(self, key: str, delta: Any) -> None: ...
    def keys(self, prefix: str = "") -> List[str]: ...


class InMemoryCRDT:
    """
    Minimal in-memory store for prototyping.
    Not a real CRDT—just a thread-safe dict.
    """
    def __init__(self) -> None:
        self._lock = RLock()
        self._data: Dict[str, Any] = {}

    def get(self, key: str) -> Any:
        with self._lock:
            return self._data.get(key)

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._data[key] = value

    def merge(self, key: str, delta: Any) -> None:
        # placeholder: implement CRDT merge semantics
        with self._lock:
            current = self._data.get(key)
            if isinstance(current, dict) and isinstance(delta, dict):
                merged = dict(current)
                merged.update(delta)
                self._data[key] = merged
            else:
                self._data[key] = delta

    def keys(self, prefix: str = "") -> List[str]:
        with self._lock:
            if not prefix:
                return list(self._data.keys())
            return [k for k in self._data.keys() if k.startswith(prefix)]


# =============================================================================
# Stigmergy Board (Shared Blackboard)
# =============================================================================

class StigmergyBoard:
    """
    Shared blackboard where agents post observations, partial results, bids, proposals.

    Natural analogy: pheromone trails + stigmergy.
    Implementation detail targets:
      - CRDT KV store for artifacts
      - vector store for semantic retrieval (future)
      - fields for pheromone reinforcement & voting
    """

    def __init__(self, store: CRDTStore) -> None:
        self.store = store
        self._index_prefix = "artifact:"
        self._lock = RLock()

    def post(self, artifact: Artifact) -> None:
        key = self._index_prefix + artifact.artifact_id
        artifact.updated_at_ms = now_ms()
        self.store.set(key, artifact)

    def get(self, artifact_id: str) -> Optional[Artifact]:
        key = self._index_prefix + artifact_id
        art = self.store.get(key)
        if isinstance(art, Artifact):
            if art.is_expired():
                return None
            return art
        return None

    def list(self, kind: Optional[ArtifactKind] = None, role_hint: Optional[Role] = None) -> List[Artifact]:
        artifacts: List[Artifact] = []
        for k in self.store.keys(self._index_prefix):
            art = self.store.get(k)
            if not isinstance(art, Artifact):
                continue
            if art.is_expired():
                continue
            if kind and art.kind != kind:
                continue
            if role_hint and art.role_hint != role_hint:
                continue
            artifacts.append(art)
        # sort by priority, pheromone, updated time
        artifacts.sort(key=lambda a: (int(a.priority), a.pheromone_strength, a.updated_at_ms), reverse=True)
        return artifacts

    def reinforce(self, artifact_id: str, delta: float, reason: str = "") -> None:
        """
        Increase (or decrease) pheromone strength.
        Positive delta reinforces successful coordination paths.
        """
        with self._lock:
            art = self.get(artifact_id)
            if not art:
                return
            art.pheromone_strength = max(0.0, art.pheromone_strength + float(delta))
            art.payload.setdefault("reinforcement_log", []).append(
                {"t_ms": now_ms(), "delta": delta, "reason": reason}
            )
            self.post(art)


# =============================================================================
# Goal Hierarchy (Persistent Objectives -> Subgoals)
# =============================================================================

@dataclass
class GoalNode:
    goal_id: str
    title: str
    description: str = ""
    parent_goal_id: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: str = "open"  # open | in_progress | blocked | done
    created_at_ms: int = field(default_factory=now_ms)
    updated_at_ms: int = field(default_factory=now_ms)
    children: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class GoalHierarchy:
    """Hierarchical goal tree (colony drives)."""

    def __init__(self, store: CRDTStore) -> None:
        self.store = store
        self._prefix = "goal:"
        self._lock = RLock()

    def create_goal(self, title: str, description: str = "", parent_goal_id: Optional[str] = None,
                    priority: Priority = Priority.MEDIUM) -> GoalNode:
        g = GoalNode(goal_id=new_id("goal"), title=title, description=description,
                     parent_goal_id=parent_goal_id, priority=priority)
        self._set(g)
        if parent_goal_id:
            self._append_child(parent_goal_id, g.goal_id)
        return g

    def get(self, goal_id: str) -> Optional[GoalNode]:
        g = self.store.get(self._prefix + goal_id)
        return g if isinstance(g, GoalNode) else None

    def mark(self, goal_id: str, status: str) -> None:
        with self._lock:
            g = self.get(goal_id)
            if not g:
                return
            g.status = status
            g.updated_at_ms = now_ms()
            self._set(g)

    def _set(self, goal: GoalNode) -> None:
        self.store.set(self._prefix + goal.goal_id, goal)

    def _append_child(self, parent_goal_id: str, child_goal_id: str) -> None:
        parent = self.get(parent_goal_id)
        if not parent:
            return
        if child_goal_id not in parent.children:
            parent.children.append(child_goal_id)
            parent.updated_at_ms = now_ms()
            self._set(parent)


# =============================================================================
# Observation Bus (External world feedback)
# =============================================================================

@dataclass
class ObservationEvent:
    event_id: str
    t_ms: int
    topic: str
    payload: Dict[str, Any]
    role_targets: Tuple[Role, ...] = (Role.GENERAL,)


class ObservationBus:
    """
    Real-time feedback from external world: APIs, sensors, human input.

    In production: Kafka/NATS/Redis Streams/etc.
    Here: simple in-memory queue per role.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._queues: Dict[Role, List[ObservationEvent]] = {r: [] for r in Role}

    def publish(self, topic: str, payload: Dict[str, Any], role_targets: Tuple[Role, ...] = (Role.GENERAL,)) -> str:
        evt = ObservationEvent(event_id=new_id("obs"), t_ms=now_ms(), topic=topic,
                               payload=payload, role_targets=role_targets)
        with self._lock:
            for r in role_targets:
                self._queues.setdefault(r, []).append(evt)
        return evt.event_id

    def poll(self, role: Role, max_events: int = 25) -> List[ObservationEvent]:
        with self._lock:
            q = self._queues.get(role, [])
            events = q[:max_events]
            self._queues[role] = q[max_events:]
        return events


# =============================================================================
# Collective Memory (Persistent shared LTM)
# =============================================================================

class CollectiveMemory:
    """
    Eternal shared memory that replaces per-agent LTM.

    Target architecture (future):
      - raw immutable archive (object storage)
      - hypergraph store (entities, relations, provenance)
      - distillation lattice (summaries, embeddings, canonical truths)
    """

    def __init__(self, store: CRDTStore) -> None:
        self.store = store
        self._prefix = "memory:"
        self._lock = RLock()

    def write(self, namespace: str, key: str, value: Any, provenance: Optional[Dict[str, Any]] = None) -> None:
        """
        Write a memory item. In production this would also index embeddings and graph links.
        """
        with self._lock:
            record = {
                "t_ms": now_ms(),
                "namespace": namespace,
                "key": key,
                "value": value,
                "provenance": provenance or {},
            }
            self.store.set(self._prefix + f"{namespace}:{key}", record)

    def read(self, namespace: str, key: str) -> Optional[Dict[str, Any]]:
        v = self.store.get(self._prefix + f"{namespace}:{key}")
        return v if isinstance(v, dict) else None

    def query_prefix(self, namespace: str) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        prefix = self._prefix + f"{namespace}:"
        for k in self.store.keys(prefix):
            v = self.store.get(k)
            if isinstance(v, dict):
                results.append(v)
        results.sort(key=lambda r: r.get("t_ms", 0), reverse=True)
        return results


# =============================================================================
# Role Orchestrator (Routing / Allocation / Deadlock handling)
# =============================================================================

@dataclass
class TaskAssignment:
    task_artifact_id: str
    assigned_agent_id: str
    assigned_role: Role
    assigned_at_ms: int = field(default_factory=now_ms)
    status: str = "assigned"  # assigned|accepted|in_progress|done|failed
    metadata: Dict[str, Any] = field(default_factory=dict)


class RoleOrchestrator:
    """
    Routes tasks to suitable agents, resolves overlaps, escalates deadlocks.

    Natural analogy: task allocation / queen signal.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._assignments: Dict[str, TaskAssignment] = {}  # by task_artifact_id

    def route(self, task: Artifact, sessions: List[AgentSession]) -> Optional[TaskAssignment]:
        """
        Simple routing:
          - match role_hint if present
          - choose the most recently seen eligible agent
        Replace with rule engine / optimization / LLM router later.
        """
        if task.kind != ArtifactKind.TASK:
            return None

        role_hint = task.role_hint or Role.GENERAL
        candidates = [s for s in sessions if role_hint in s.capabilities.roles]
        if not candidates:
            candidates = [s for s in sessions if Role.GENERAL in s.capabilities.roles]
        if not candidates:
            return None

        candidates.sort(key=lambda s: s.last_seen_ms, reverse=True)
        chosen = candidates[0]

        assignment = TaskAssignment(
            task_artifact_id=task.artifact_id,
            assigned_agent_id=chosen.agent_id,
            assigned_role=role_hint
        )
        with self._lock:
            self._assignments[task.artifact_id] = assignment
        return assignment

    def get_assignment(self, task_artifact_id: str) -> Optional[TaskAssignment]:
        with self._lock:
            return self._assignments.get(task_artifact_id)

    def mark(self, task_artifact_id: str, status: str) -> None:
        with self._lock:
            a = self._assignments.get(task_artifact_id)
            if not a:
                return
            a.status = status


# =============================================================================
# Emergence Engine (Reinforcement / Pruning / What-if replay)
# =============================================================================

@dataclass
class EmergenceScore:
    artifact_id: str
    score: float
    reason: str
    t_ms: int = field(default_factory=now_ms)


class EmergenceEngine:
    """
    Actively reinforces successful coordination patterns and prunes dead ends.

    Natural analogy: positive feedback in pheromone trail laying.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._scores: List[EmergenceScore] = []

    def score_outcome(self, artifact: Artifact) -> EmergenceScore:
        """
        Placeholder scoring heuristic:
          - reward artifacts with explicit success marker
          - reward higher confidence and evidence completeness
        """
        base = 0.0
        if artifact.payload.get("success") is True:
            base += 1.0
        base += float(artifact.confidence) * 0.5
        base += min(1.0, len(artifact.payload.get("evidence", [])) / 5.0) * 0.5

        score = base
        reason = artifact.payload.get("score_reason", "heuristic_score")
        es = EmergenceScore(artifact_id=artifact.artifact_id, score=score, reason=reason)
        with self._lock:
            self._scores.append(es)
        return es

    def recent_scores(self, limit: int = 50) -> List[EmergenceScore]:
        with self._lock:
            return list(self._scores[-limit:])


# =============================================================================
# Connection Gateway (Auth, role registry, rate limits)
# =============================================================================

class ConnectionGateway:
    """
    Agents authenticate, declare roles/capabilities.

    Natural analogy: ants entering/exiting the nest.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._sessions: Dict[str, AgentSession] = {}

    def connect(self, agent_id: Optional[str], capabilities: AgentCapabilities,
                metadata: Optional[Dict[str, Any]] = None) -> AgentSession:
        agent_id = agent_id or new_id("agent")
        s = AgentSession(agent_id=agent_id, capabilities=capabilities, metadata=metadata or {})
        with self._lock:
            self._sessions[agent_id] = s
        return s

    def heartbeat(self, agent_id: str) -> None:
        with self._lock:
            s = self._sessions.get(agent_id)
            if s:
                s.last_seen_ms = now_ms()

    def disconnect(self, agent_id: str) -> None:
        with self._lock:
            self._sessions.pop(agent_id, None)

    def sessions(self) -> List[AgentSession]:
        with self._lock:
            return list(self._sessions.values())


# =============================================================================
# HiveMind Core (Node)
# =============================================================================

class HiveMindCore:
    """
    HiveMind Core (HMC):
    Centralized stigmergy + orchestration + emergence + memory + goals + observation.

    Primary responsibilities:
    - Provide a shared blackboard (StigmergyBoard)
    - Route tasks by role (RoleOrchestrator)
    - Maintain persistent collective memory (CollectiveMemory)
    - Maintain goal hierarchy (GoalHierarchy)
    - Reinforce/prune paths (EmergenceEngine)
    - Provide real-time observation stream (ObservationBus)
    - Support large concurrent swarm engagement (implementation detail)
    """

    def __init__(self, store: Optional[CRDTStore] = None) -> None:
        self.store = store or InMemoryCRDT()

        # Layers
        self.gateway = ConnectionGateway()
        self.board = StigmergyBoard(self.store)
        self.goals = GoalHierarchy(self.store)
        self.memory = CollectiveMemory(self.store)
        self.observations = ObservationBus()
        self.orchestrator = RoleOrchestrator()
        self.emergence = EmergenceEngine()

    # -------------------------------------------------------------------------
    # Swarm Cycle Primitives
    # -------------------------------------------------------------------------

    def ingest_goal(self, title: str, description: str = "", priority: Priority = Priority.HIGH) -> GoalNode:
        """
        Task Ingestion: Human/upstream posts a high-level goal to HMC.
        """
        goal = self.goals.create_goal(title=title, description=description, priority=priority)
        return goal

    def decompose_to_task(self, goal: GoalNode, title: str, role_hint: Role,
                          payload: Optional[Dict[str, Any]] = None,
                          priority: Priority = Priority.HIGH) -> Artifact:
        """
        Decomposition & posting to stigmergy board as a TASK artifact.
        """
        art = Artifact(
            artifact_id=new_id("task"),
            kind=ArtifactKind.TASK,
            created_at_ms=now_ms(),
            updated_at_ms=now_ms(),
            author_agent_id=None,
            role_hint=role_hint,
            priority=priority,
            pheromone_strength=0.1,  # initial trail
            confidence=0.6,
            title=title,
            payload={"goal_id": goal.goal_id, **(payload or {})},
        )
        self.board.post(art)
        return art

    def allocate(self, task_artifact_id: str) -> Optional[TaskAssignment]:
        """
        Role Orchestrator routes task to suitable agent.
        """
        task = self.board.get(task_artifact_id)
        if not task:
            return None
        assignment = self.orchestrator.route(task, self.gateway.sessions())
        if assignment:
            # Post an assignment artifact (optional)
            self.board.post(Artifact(
                artifact_id=new_id("assign"),
                kind=ArtifactKind.TRAIL,
                created_at_ms=now_ms(),
                updated_at_ms=now_ms(),
                author_agent_id=None,
                role_hint=assignment.assigned_role,
                priority=task.priority,
                pheromone_strength=task.pheromone_strength,
                confidence=0.7,
                title=f"Assignment for {task.artifact_id}",
                payload={"task_artifact_id": task.artifact_id, "assigned_agent_id": assignment.assigned_agent_id,
                         "assigned_role": assignment.assigned_role.value},
                ttl_ms=60_000,
            ))
        return assignment

    def post_result(self, agent_id: str, task_artifact_id: str, kind: ArtifactKind,
                    title: str, payload: Dict[str, Any],
                    confidence: float = 0.7) -> Artifact:
        """
        Agents execute locally and post results/artifacts back (short-term context only).
        """
        self.gateway.heartbeat(agent_id)

        task = self.board.get(task_artifact_id)
        role_hint = task.role_hint if task else None
        prio = task.priority if task else Priority.MEDIUM

        art = Artifact(
            artifact_id=new_id("art"),
            kind=kind,
            created_at_ms=now_ms(),
            updated_at_ms=now_ms(),
            author_agent_id=agent_id,
            role_hint=role_hint,
            priority=prio,
            pheromone_strength=0.1,
            confidence=confidence,
            title=title,
            payload={"task_artifact_id": task_artifact_id, **payload},
        )
        self.board.post(art)
        return art

    def reinforce(self, artifact_id: str) -> EmergenceScore:
        """
        Emergence Engine scores outcomes and reinforces trails.
        """
        art = self.board.get(artifact_id)
        if not art:
            return EmergenceScore(artifact_id=artifact_id, score=0.0, reason="artifact_not_found")

        score = self.emergence.score_outcome(art)
        # Translate score to pheromone delta (simple mapping)
        delta = max(0.0, score.score) * 0.25
        self.board.reinforce(artifact_id, delta=delta, reason=score.reason)
        return score

    def converge_goal(self, goal_id: str, threshold: float = 2.0) -> bool:
        """
        Completion: when goal convergence threshold hit, notify completion.
        Placeholder: sums reinforcement on artifacts linked to goal_id.
        """
        # Collect artifacts with goal_id reference
        total = 0.0
        for art in self.board.list():
            if art.payload.get("goal_id") == goal_id:
                total += art.pheromone_strength

        if total >= threshold:
            self.goals.mark(goal_id, "done")
            return True
        return False


# =============================================================================
# Minimal Demo (Swarm Cycle Example)
# =============================================================================

def _demo_swarm_cycle() -> None:
    """
    Example: building a software product (termite mound analogy)
    - researchers deposit market data trails
    - designers propose UI
    - coders implement
    - testers prune weak branches
    """
    hmc = HiveMindCore()

    # Connect four lightweight agents (stateless in principle)
    a_research = hmc.gateway.connect(None, AgentCapabilities(roles=(Role.RESEARCHER,)))
    a_design = hmc.gateway.connect(None, AgentCapabilities(roles=(Role.DESIGNER,)))
    a_code = hmc.gateway.connect(None, AgentCapabilities(roles=(Role.CODER,)))
    a_test = hmc.gateway.connect(None, AgentCapabilities(roles=(Role.TESTER,)))

    # Ingest high-level goal
    goal = hmc.ingest_goal("Build MVP product", "Ship a thin slice with validated demand.", Priority.CRITICAL)

    # Decompose into tasks
    t1 = hmc.decompose_to_task(goal, "Collect market evidence for MVP", Role.RESEARCHER, {"deliverable": "market_brief"})
    t2 = hmc.decompose_to_task(goal, "Draft UI proposal", Role.DESIGNER, {"deliverable": "ui_mock"})
    t3 = hmc.decompose_to_task(goal, "Implement core endpoint", Role.CODER, {"deliverable": "api_endpoint"})
    t4 = hmc.decompose_to_task(goal, "Test workflow end-to-end", Role.TESTER, {"deliverable": "test_report"})

    # Allocate tasks (router chooses appropriate agent by role)
    hmc.allocate(t1.artifact_id)
    hmc.allocate(t2.artifact_id)
    hmc.allocate(t3.artifact_id)
    hmc.allocate(t4.artifact_id)

    # Agents post results
    r1 = hmc.post_result(a_research.agent_id, t1.artifact_id, ArtifactKind.EVIDENCE,
                         "Market brief", {"success": True, "evidence": ["TAM", "ICP", "competitors"]}, confidence=0.8)
    r2 = hmc.post_result(a_design.agent_id, t2.artifact_id, ArtifactKind.PROPOSAL,
                         "UI mock proposal", {"success": True, "evidence": ["flows", "wireframes"]}, confidence=0.75)
    r3 = hmc.post_result(a_code.agent_id, t3.artifact_id, ArtifactKind.RESULT,
                         "API endpoint implemented", {"success": True, "evidence": ["PR#123", "docs"]}, confidence=0.85)
    r4 = hmc.post_result(a_test.agent_id, t4.artifact_id, ArtifactKind.RESULT,
                         "E2E test report", {"success": True, "evidence": ["passed", "bugs:0"]}, confidence=0.8)

    # Reinforce successful paths
    for r in (r1, r2, r3, r4):
        hmc.reinforce(r.artifact_id)

    # Converge / complete goal
    done = hmc.converge_goal(goal.goal_id, threshold=0.5)
    print("Goal done?", done, "| status:", hmc.goals.get(goal.goal_id).status)

    # Show top artifacts by pheromone strength
    top = hmc.board.list()[:6]
    print("\nTop stigmergy artifacts:")
    for a in top:
        print(f"- {a.kind.value:<8} {a.artifact_id} pheromone={a.pheromone_strength:.3f} title={a.title}")


if __name__ == "__main__":
    _demo_swarm_cycle()
