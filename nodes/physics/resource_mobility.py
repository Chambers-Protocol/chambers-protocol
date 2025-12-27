"""
resource_mobility.py
Chambers Enterprise Grid Node: Resource Mobility Index (RMI)
Physics Engine for Corporate Longevity & Capital Flow.
"""
import math
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class MobilityInputs:
    structure_score: float  # Ss: 1-5 (5 = Boundaryless/Hybrid, 1 = Siloed)
    segment_count: int      # Sc: 1-10 (Diversification scale)
    adaptation_rate: float  # Ar: 1-10 (M&A, Spinoffs, Reorg velocity)
    epsilon: float = 0.0    # Random market luck (-20 to +20)

@dataclass
class MobilityOutput:
    rmi_score: float        # The Weighted Index
    longevity_score: float  # Predicted Survival (Years/Strength)
    marginal_return: float  # The Derivative (Speed of benefit accumulation)
    classification: str     # Elite, Durable, Fragile
    narrative: str

class ResourceMobilityEngine:
    """
    Implements the Chambers/Grok derivation for Resource Mobility.
    Formula: LS = 50 + (15 * RMI^1.5) + epsilon
    Derivative: d(LS)/d(RMI) = 22.5 * RMI^0.5
    """
    
    def calculate(self, inputs: MobilityInputs) -> MobilityOutput:
        # 1. Calculate Weighted RMI
        # Weights: Structure (50%), Adaptation (30%), Segments (20%)
        # Note: We normalize inputs to ensure the math holds at scale
        
        # Clamp inputs to valid ranges for safety
        ss = max(1.0, min(5.0, inputs.structure_score))
        sc = max(1.0, min(10.0, float(inputs.segment_count)))
        ar = max(1.0, min(10.0, inputs.adaptation_rate))
        
        # The Core Equation
        rmi = (ss * 0.5) + (sc * 0.2) + (ar * 0.3)
        
        # 2. Calculate Longevity Score (Non-linear amplification)
        # LS = 50 + (15 * RMI^1.5) + E
        base_survival = 50.0
        amplification = 15.0 * math.pow(rmi, 1.5)
        ls = base_survival + amplification + inputs.epsilon
        
        # 3. Calculate the Derivative (The "Lurking" Advantage)
        # d(LS)/d(RMI) = 15 * 1.5 * RMI^0.5 = 22.5 * RMI^0.5
        marginal_return = 22.5 * math.pow(rmi, 0.5)
        
        # 4. Classification Logic
        if ls > 300:
            tier = "ELITE (70+ Year Club)"
            narrative = "Resource mobility is compounding exponentially. Structure enables fluid capital movement."
        elif ls > 200:
            tier = "DURABLE (Fortune 500 Avg)"
            narrative = "Strong survival instincts, but structure may be limiting max adaptation speed."
        else:
            tier = "FRAGILE (Risk of Stagnation)"
            narrative = "Linear resource flow. Lack of cross-functional sharing prevents compounding returns."
            
        return MobilityOutput(
            rmi_score=round(rmi, 2),
            longevity_score=round(ls, 1),
            marginal_return=round(marginal_return, 2),
            classification=tier,
            narrative=narrative
        )

# Quick Test
if __name__ == "__main__":
    # P&G Example from notes
    engine = ResourceMobilityEngine()
    result = engine.calculate(MobilityInputs(5, 10, 8))
    print(f"P&G Test: RMI={result.rmi_score}, LS={result.longevity_score} ({result.classification})")