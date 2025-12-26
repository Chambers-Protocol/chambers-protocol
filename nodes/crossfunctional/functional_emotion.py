"""
functional_emotion.py

Chambers Enterprise Grid (CEG) Node:
Functional Emotion Quotient (FEQ)

Purpose
-------
FEQ is a control/modulation node that quantifies how emotional state (fight/flight/freeze)
modulates the Interface Conversion Engine (ICE) without changing the underlying structure
of the Pattern:Reality system.

Core idea
---------
- Baseline Pattern (P)  = 5.1
- Baseline Reality (R)  = 4.9
- Emotional state collapses into (fight, flight, freeze)
- FEQ acts as a gain factor on conversion throughput and a directional bias that can
  distort Pattern-vs-Reality emphasis:
    * Fight  -> pushes toward Pattern dominance (structure/enforcement)
    * Flight -> pushes away from Pattern (avoidance/pivot/entropy)
    * Freeze -> suppresses BOTH (conversion stalls)

This file is intentionally self-contained and built to be easy to extend into:
- telemetry ingestion
- org diagnostics
- dashboards / scoring
- simulations

Author: (codifying Chris Chambers' FEQ / ICE construct)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isclose
from typing import Dict, Tuple


# -----------------------------
# Constants / Baseline Defaults
# -----------------------------

BASE_PATTERN: float = 5.1
BASE_REALITY: float = 4.9


class EmotionalMode(str, Enum):
    FIGHT = "fight"
    FLIGHT = "flight"
    FREEZE = "freeze"
    MIXED = "mixed"  # When state is distributed (not dominant)


# -----------------------------
# Core Data Structures
# -----------------------------

@dataclass(frozen=True)
class EmotionalState:
    """
    Emotional state vector E = (e_f, e_l, e_z) with constraint:
        e_f + e_l + e_z = 1

    - e_f: fight intensity
    - e_l: flight intensity
    - e_z: freeze intensity
    """
    fight: float
    flight: float
    freeze: float

    def normalized(self, tol: float = 1e-9) -> "EmotionalState":
        s = self.fight + self.flight + self.freeze
        if s <= tol:
            # Degenerate: treat as full freeze (stall)
            return EmotionalState(0.0, 0.0, 1.0)
        return EmotionalState(self.fight / s, self.flight / s, self.freeze / s)

    def validate(self, tol: float = 1e-6) -> None:
        nf = self.normalized()
        if nf.fight < -tol or nf.flight < -tol or nf.freeze < -tol:
            raise ValueError("EmotionalState components must be non-negative.")
        if not isclose(nf.fight + nf.flight + nf.freeze, 1.0, abs_tol=tol):
            raise ValueError("EmotionalState must sum to 1 (after normalization).")

    def dominant_mode(self, threshold: float = 0.60) -> EmotionalMode:
        """
        Returns the dominant emotional mode if any component exceeds threshold,
        otherwise returns MIXED.
        """
        nf = self.normalized()
        if nf.fight >= threshold:
            return EmotionalMode.FIGHT
        if nf.flight >= threshold:
            return EmotionalMode.FLIGHT
        if nf.freeze >= threshold:
            return EmotionalMode.FREEZE
        return EmotionalMode.MIXED


@dataclass(frozen=True)
class ICEBaseline:
    """
    Baseline Pattern:Reality equilibrium.

    By default:
      P = 5.1
      R = 4.9
    """
    pattern: float = BASE_PATTERN
    reality: float = BASE_REALITY

    @property
    def ratio(self) -> float:
        """Pattern:Reality ratio (P/R)."""
        if self.reality == 0:
            return float("inf")
        return self.pattern / self.reality

    @property
    def imbalance(self) -> float:
        """Absolute imbalance |P - R|."""
        return abs(self.pattern - self.reality)

    @property
    def throughput(self) -> float:
        """Total conversion capacity proxy (P + R)."""
        return self.pattern + self.reality


@dataclass(frozen=True)
class FEQConfig:
    """
    Configuration for FEQ → ICE modulation.

    These parameters encode the "gain" and "bias" behaviors.

    Intuition:
      - freeze suppresses everything: higher freeze -> lower throughput
      - fight increases Pattern bias (P up relative to R)
      - flight decreases Pattern bias (P down relative to R)
      - A "tiny asymmetry" is healthy; big imbalance is risky
    """
    # How strongly freeze suppresses throughput (0..1 typical)
    freeze_suppression_strength: float = 1.25

    # How strongly fight/flight bias Pattern vs Reality (directional)
    directional_bias_strength: float = 0.35

    # Optional base gain (can represent ambient arousal/energy)
    base_gain: float = 1.0

    # Safety clamps
    min_gain: float = 0.0
    max_gain: float = 2.5

    # If you want latency included later, keep placeholder
    latency: float = 0.0


@dataclass(frozen=True)
class ICEResult:
    """
    Result of applying FEQ modulation to the ICE baseline.

    - effective_pattern / effective_reality: modulated values
    - gain: overall throughput scaling (0..max)
    - bias: directional bias applied (+ => pattern-heavy, - => reality-heavy)
    - stall: True if system is effectively frozen (gain ~ 0)
    - signals: diagnostics for drift (fight-heavy, flight-heavy, freeze)
    """
    effective_pattern: float
    effective_reality: float
    gain: float
    bias: float
    stall: bool
    mode: EmotionalMode
    signals: Dict[str, float]

    @property
    def ratio(self) -> float:
        if self.effective_reality == 0:
            return float("inf")
        return self.effective_pattern / self.effective_reality

    @property
    def imbalance(self) -> float:
        return abs(self.effective_pattern - self.effective_reality)

    @property
    def throughput(self) -> float:
        return self.effective_pattern + self.effective_reality


# -----------------------------
# FEQ Node Implementation
# -----------------------------

class FunctionalEmotionQuotient:
    """
    CEG Node: Functional Emotion Quotient (FEQ)

    FEQ takes:
      - an ICEBaseline (P, R)
      - an EmotionalState (fight/flight/freeze)
      - a FEQConfig (gain/bias strengths)

    and returns an ICEResult describing the modulated conversion engine.
    """

    def __init__(self, baseline: ICEBaseline | None = None, config: FEQConfig | None = None) -> None:
        self.baseline = baseline or ICEBaseline()
        self.config = config or FEQConfig()

    # ---- public API ----

    def apply(self, state: EmotionalState) -> ICEResult:
        """
        Apply FEQ to the ICE baseline and return modulated ICE values + diagnostics.
        """
        state_n = state.normalized()
        state_n.validate()

        mode = state_n.dominant_mode()

        gain = self._compute_gain(state_n)
        bias = self._compute_bias(state_n)

        # Apply gain to total magnitude and bias to redistribute between P and R.
        p0, r0 = self.baseline.pattern, self.baseline.reality
        p_eff, r_eff = self._apply_gain_and_bias(p0, r0, gain, bias)

        stall = gain <= 1e-6 or (p_eff + r_eff) <= 1e-6

        signals = self._compute_signals(state_n, gain, bias, stall)

        return ICEResult(
            effective_pattern=p_eff,
            effective_reality=r_eff,
            gain=gain,
            bias=bias,
            stall=stall,
            mode=mode,
            signals=signals,
        )

    # ---- internals ----

    def _compute_gain(self, state: EmotionalState) -> float:
        """
        Compute overall throughput gain.
        Freeze suppresses throughput most strongly.
        Fight/flight can be treated as "arousal" but we keep it simple:
          gain = base_gain * (1 - k * freeze)
        clamped to [min_gain, max_gain]
        """
        k = self.config.freeze_suppression_strength
        raw = self.config.base_gain * max(0.0, 1.0 - k * state.freeze)
        return self._clamp(raw, self.config.min_gain, self.config.max_gain)

    def _compute_bias(self, state: EmotionalState) -> float:
        """
        Compute directional bias:
          + => Pattern-heavy (fight)
          - => Reality-heavy (flight)
          0 => balanced or freeze-dominant

        bias = s * (fight - flight) * (1 - freeze)
        """
        s = self.config.directional_bias_strength
        raw = s * (state.fight - state.flight) * (1.0 - state.freeze)
        # bias is typically small; no hard clamp needed, but keep sane
        return self._clamp(raw, -1.0, 1.0)

    def _apply_gain_and_bias(self, p0: float, r0: float, gain: float, bias: float) -> Tuple[float, float]:
        """
        Apply:
          1) Gain to both P and R (throughput scaling)
          2) Bias to shift mass from one side to the other without changing total

        We preserve total T = gain*(p0+r0), then allocate:
          p = T * w
          r = T * (1-w)
        where w = base_weight + bias_adjustment
        """
        T0 = p0 + r0
        if T0 <= 0:
            return 0.0, 0.0

        # baseline weight of pattern
        w0 = p0 / T0  # for 5.1:4.9 => 0.51

        # bias shifts w0 by +/- some fraction
        # If bias=+0.1 => w increases; if -0.1 => decreases
        w = self._clamp(w0 + bias, 0.0, 1.0)

        T = gain * T0
        p = T * w
        r = T * (1.0 - w)
        return p, r

    def _compute_signals(self, state: EmotionalState, gain: float, bias: float, stall: bool) -> Dict[str, float]:
        """
        Produce diagnostics signals that can be graphed or thresholded.
        """
        # These are interpretable scalar signals (0..1-ish)
        return {
            "fight_intensity": state.fight,
            "flight_intensity": state.flight,
            "freeze_intensity": state.freeze,
            "throughput_gain": gain,
            "pattern_bias": max(0.0, bias),
            "reality_bias": max(0.0, -bias),
            "stall": 1.0 if stall else 0.0,
        }

    @staticmethod
    def _clamp(x: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, x))


# -----------------------------
# Example / Quick CLI Run
# -----------------------------

def _demo() -> None:
    feq = FunctionalEmotionQuotient()

    examples = {
        "Balanced (mixed)": EmotionalState(fight=0.34, flight=0.33, freeze=0.33),
        "Fight-heavy": EmotionalState(fight=0.75, flight=0.15, freeze=0.10),
        "Flight-heavy": EmotionalState(fight=0.15, flight=0.75, freeze=0.10),
        "Freeze-heavy": EmotionalState(fight=0.05, flight=0.05, freeze=0.90),
        "Near baseline calm": EmotionalState(fight=0.40, flight=0.40, freeze=0.20),
    }

    print("=== Functional Emotion Quotient (FEQ) Demo ===")
    print(f"Baseline P:R = {feq.baseline.pattern}:{feq.baseline.reality} (ratio={feq.baseline.ratio:.4f})")
    print()

    for name, st in examples.items():
        res = feq.apply(st)
        print(f"[{name}] mode={res.mode.value}")
        print(f"  gain={res.gain:.4f} bias={res.bias:+.4f} stall={res.stall}")
        print(f"  effective P={res.effective_pattern:.4f} R={res.effective_reality:.4f} "
              f"(ratio={res.ratio:.4f}, imbalance={res.imbalance:.4f}, throughput={res.throughput:.4f})")
        print(f"  signals={res.signals}")
        print()


if __name__ == "__main__":
    _demo()
