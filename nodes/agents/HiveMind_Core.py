"""
HiveMind_Core.py
Chambers Enterprise Grid Node: HiveMind Core (HMC) with Supabase Persistence.
"""
from __future__ import annotations

import os
import sys
import time
import uuid
import json
from dataclasses import dataclass, field, asdict, is_dataclass
from enum import Enum
from threading import RLock
from typing import Any, Dict, List, Optional, Protocol, Tuple
from dotenv import load_dotenv
from supabase import create_client

# Explicitly load .env from the project root
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- SERIALIZATION HELPER ---
def to_serializable(obj):
    """Recursively converts Enums and Dataclasses to JSON-safe types."""
    if is_dataclass(obj):
        return {k: to_serializable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, list):
        return [to_serializable(i) for i in obj]
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    return obj

# =============================================================================
# Core Types
# =============================================================================

class Role(str, Enum):
    RESEARCHER = "researcher"
    DESIGNER = "designer"
    CODER = "coder"
    TESTER = "tester"
    OPS = "ops"
    SALES = "sales"
    EXEC = "exec"
    GENERAL = "general"

class ArtifactKind(str, Enum):
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
    latency_budget_ms: int = 100

@dataclass
class AgentSession:
    agent_id: str
    capabilities: AgentCapabilities
    connected_at_ms: int = field(default_factory=now_ms)
    last_seen_ms: int = field(default_factory=now_ms)
    metadata: Dict[str, Any] = field(default_factory=dict)

# =============================================================================
# Stigmergy Artifacts
# =============================================================================

@dataclass
class Artifact:
    artifact_id: str
    kind: ArtifactKind
    created_at_ms: int
    updated_at_ms: int
    author_agent_id: Optional[str]
    role_hint: Optional[Role]
    priority: Priority = Priority.MEDIUM
    pheromone_strength: float = 0.0
    confidence: float = 0.5
    ttl_ms: Optional[int] = None
    title: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self, t_ms: Optional[int] = None) -> bool:
        if self.ttl_ms is None:
            return False
        t_ms = t_ms or now_ms()
        return (t_ms - self.created_at_ms) > self.ttl_ms

# =============================================================================
# Persistence Layer (Supabase)
# =============================================================================

class SupabaseStore:
    """
    Persistent CRDT-like store backed by Supabase (PostgreSQL).
    Replaces the volatile InMemoryCRDT.
    """
    def __init__(self) -> None:
        url = os.getenv("CENTRAL_LEDGER_URL")
        key = os.getenv("CENTRAL_LEDGER_SECRET")
        if not url or not key:
            print("WARNING: Supabase credentials missing. HiveMind running in volatile mode.", file=sys.stderr)
            self.client = None
        else:
            try:
                self.client = create_client(url, key)
            except Exception as e:
                print(f"Supabase Init Error: {e}", file=sys.stderr)
                self.client = None
        self.table = "hive_memory"
        self._local_cache = {} 

    def get(self, key: str) -> Any:
        # If no client, use local cache
        if not self.client: return self._local_cache.get(key)
        
        try:
            response = self.client.table(self.table).select("value").eq("key", key).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]["value"]
            return None
        except Exception as e:
            # Fallback to silent fail to not crash Claude
            print(f"DB READ ERROR: {e}", file=sys.stderr)
            return None

    def set(self, key: str, value: Any) -> None:
        # Convert Dataclasses/Enums to raw JSON-safe dicts
        clean_value = to_serializable(value)
        
        if not self.client:
            self._local_cache[key] = clean_value
            return

        data = { "key": key, "value": clean_value, "updated_at": "now()" }
        try:
            self.client.table(self.table).upsert(data, on_conflict="key").execute()
        except Exception as e:
            print(f"DB WRITE ERROR: {e}", file=sys.stderr)

    def keys(self, prefix: str = "") -> List[str]:
        if not self.client:
            return [k for k in self._local_cache.keys() if k.startswith(prefix)]
        try:
            response = self.client.table(self.table).select("key").ilike("key", f"{prefix}%").execute()
            return [row["key"] for row in response.data]
        except Exception as e:
            print(f"DB LIST ERROR: {e}", file=sys.stderr)
            return []

# =============================================================================
# Sub-Components
# =============================================================================

class StigmergyBoard:
    def __init__(self, store: SupabaseStore) -> None:
        self.store = store
        self._index_prefix = "artifact:"
        self._lock = RLock()

    def post(self, artifact: Artifact) -> None:
        key = self._index_prefix + artifact.artifact_id
        artifact.updated_at_ms = now_ms()
        self.store.set(key, artifact)

    def get(self, artifact_id: str) -> Optional[Artifact]:
        key = self._index_prefix + artifact_id
        data = self.store.get(key)
        if isinstance(data, dict):
            # Because data comes back as raw dicts/ints, we need to handle reconstruction loosely
            # For simplicity in this version, we return the object as a reconstructed Artifact 
            # or just rely on the fact that Python is duck-typed enough for read operations.
            # Ideally, we would re-cast Enums here.
            return Artifact(
                artifact_id=data.get("artifact_id"),
                kind=ArtifactKind(data.get("kind")) if data.get("kind") else ArtifactKind.TASK,
                created_at_ms=data.get("created_at_ms"),
                updated_at_ms=data.get("updated_at_ms"),
                author_agent_id=data.get("author_agent_id"),
                role_hint=Role(data.get("role_hint")) if data.get("role_hint") else None,
                priority=Priority(data.get("priority")) if data.get("priority") else Priority.MEDIUM,
                pheromone_strength=data.get("pheromone_strength", 0.0),
                confidence=data.get("confidence", 0.5),
                ttl_ms=data.get("ttl_ms"),
                title=data.get("title", ""),
                payload=data.get("payload", {})
            )
        return None

    def list(self) -> List[Artifact]:
        keys = self.store.keys(self._index_prefix)
        artifacts = []
        for k in keys:
            art = self.get(k.replace(self._index_prefix, ""))
            if art: artifacts.append(art)
        artifacts.sort(key=lambda a: (int(a.priority), a.pheromone_strength), reverse=True)
        return artifacts

    def reinforce(self, artifact_id: str, delta: float, reason: str = "") -> None:
        art = self.get(artifact_id)
        if not art: return
        art.pheromone_strength = max(0.0, art.pheromone_strength + float(delta))
        self.post(art)

@dataclass
class GoalNode:
    goal_id: str
    title: str
    description: str = ""
    parent_goal_id: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: str = "open"
    created_at_ms: int = field(default_factory=now_ms)
    updated_at_ms: int = field(default_factory=now_ms)
    children: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class GoalHierarchy:
    def __init__(self, store: SupabaseStore) -> None:
        self.store = store
        self._prefix = "goal:"

    def create_goal(self, title: str, description: str, priority: Priority) -> GoalNode:
        g = GoalNode(goal_id=new_id("goal"), title=title, description=description, priority=priority)
        self.store.set(self._prefix + g.goal_id, g)
        return g

    def get(self, goal_id: str) -> Optional[GoalNode]:
        data = self.store.get(self._prefix + goal_id)
        if data: 
            return GoalNode(
                goal_id=data.get("goal_id"),
                title=data.get("title"),
                description=data.get("description", ""),
                parent_goal_id=data.get("parent_goal_id"),
                priority=Priority(data.get("priority", 5)),
                status=data.get("status", "open"),
                created_at_ms=data.get("created_at_ms"),
                updated_at_ms=data.get("updated_at_ms"),
                children=data.get("children", []),
                metadata=data.get("metadata", {})
            )
        return None

    def mark(self, goal_id: str, status: str) -> None:
        g = self.get(goal_id)
        if g:
            g.status = status
            self.store.set(self._prefix + g.goal_id, g)

class ConnectionGateway:
    def __init__(self) -> None:
        self._sessions: Dict[str, AgentSession] = {}
    
    def connect(self, agent_id: Optional[str], capabilities: AgentCapabilities) -> AgentSession:
        agent_id = agent_id or new_id("agent")
        s = AgentSession(agent_id=agent_id, capabilities=capabilities)
        self._sessions[agent_id] = s
        return s

    def sessions(self) -> List[AgentSession]:
        return list(self._sessions.values())

class RoleOrchestrator:
    def route(self, task: Artifact, sessions: List[AgentSession]) -> Optional[Any]:
        if not sessions: return None
        return type('Assignment', (), {'assigned_agent_id': sessions[0].agent_id})()

class EmergenceEngine:
    def score_outcome(self, artifact: Artifact) -> Any:
        return type('Score', (), {'score': 1.0, 'reason': 'default'})()

# =============================================================================
# HiveMind Core (Node)
# =============================================================================

class HiveMindCore:
    def __init__(self, store: Optional[Any] = None) -> None:
        self.store = store or SupabaseStore()
        self.gateway = ConnectionGateway()
        self.board = StigmergyBoard(self.store)
        self.goals = GoalHierarchy(self.store)
        self.orchestrator = RoleOrchestrator()
        self.emergence = EmergenceEngine()

    def ingest_goal(self, title: str, description: str, priority: Priority = Priority.HIGH) -> GoalNode:
        return self.goals.create_goal(title, description, priority)

    def decompose_to_task(self, goal: GoalNode, title: str, role_hint: Role) -> Artifact:
        art = Artifact(
            artifact_id=new_id("task"),
            kind=ArtifactKind.TASK,
            created_at_ms=now_ms(),
            updated_at_ms=now_ms(),
            author_agent_id=None,
            role_hint=role_hint,
            title=title
        )
        self.board.post(art)
        return art

    def allocate(self, task_artifact_id: str) -> Optional[Any]:
        task = self.board.get(task_artifact_id)
        if not task: return None
        return self.orchestrator.route(task, self.gateway.sessions())

    def post_result(self, agent_id: str, task_artifact_id: str, kind: ArtifactKind, title: str, payload: Dict) -> Artifact:
        art = Artifact(
            artifact_id=new_id("art"),
            kind=kind,
            created_at_ms=now_ms(),
            updated_at_ms=now_ms(),
            author_agent_id=agent_id,
            role_hint=None,
            title=title,
            payload=payload
        )
        self.board.post(art)
        return art

    def reinforce(self, artifact_id: str) -> Any:
        self.board.reinforce(artifact_id, 1.0)
        return type('Score', (), {'score': 1.0})()

    def converge_goal(self, goal_id: str, threshold: float = 0.5) -> bool:
        return True