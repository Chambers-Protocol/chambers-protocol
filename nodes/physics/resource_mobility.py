"""
resource_mobility.py
Chambers Enterprise Grid Node: Resource Mobility Index (RMI) v2.0
Physics Engine for Corporate Longevity & Capital Flow.
NOW FEATURING: The Meltdown Coefficient (GE Correction)
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
    classification: str     # Elite, Durable, Fragile, Meltdown
    narrative: str
    meltdown_risk: str      # Low, Medium, Critical

class ResourceMobilityEngine:
    """
    Implements the Chambers/Grok derivation for Resource Mobility.
    
    Formula v2 (The GE Correction):
    LS_Base = 50 + (15 * RMI^1.5)
    Penalty = 70 * (max(0, RMI - 6.0))^3
    LS_Final = LS_Base - Penalty + Epsilon
    
    Logic: Mobility adds value exponentially until RMI 6.0.
    Beyond 6.0, "Centrifugal Force" tears the organization apart faster than it grows.
    """
    
    def calculate(self, inputs: MobilityInputs) -> MobilityOutput:
        # 1. Clamp inputs
        ss = max(1.0, min(5.0, inputs.structure_score))
        sc = max(1.0, min(10.0, float(inputs.segment_count)))
        ar = max(1.0, min(10.0, inputs.adaptation_rate))
        
        # 2. Calculate Weighted RMI (The "Temperature")
        rmi = (ss * 0.5) + (sc * 0.2) + (ar * 0.3)
        
        # 3. Calculate Base Longevity (The "Fusion Energy")
        base_survival = 50.0
        amplification = 15.0 * math.pow(rmi, 1.5)
        ls_base = base_survival + amplification
        
        # 4. Calculate Meltdown Penalty (The "Centrifugal Force")
        # Threshold: 6.0. Penalty grows cubically (explosively) after this point.
        meltdown_threshold = 6.0
        penalty = 0.0
        meltdown_risk = "LOW"
        
        if rmi > meltdown_threshold:
            excess = rmi - meltdown_threshold
            penalty = 70.0 * math.pow(excess, 3) # Cubic penalty explains the sudden collapse
            meltdown_risk = "CRITICAL" if rmi > 7.0 else "MEDIUM"
            
        # 5. Final Calculations
        ls_final = ls_base - penalty + inputs.epsilon
        
        # Derivative (Complex now due to penalty)
        # d(Base)/dRMI = 22.5 * RMI^0.5
        # d(Penalty)/dRMI = 210 * (RMI-6)^2
        d_base = 22.5 * math.pow(rmi, 0.5)
        d_penalty = 0.0
        if rmi > meltdown_threshold:
            d_penalty = 210.0 * math.pow(rmi - meltdown_threshold, 2)
            
        net_derivative = d_base - d_penalty
        
        # 6. Classification Logic
        narrative = ""
        tier = ""
        
        if penalty > 100:
            tier = "MELTDOWN IMPMINENT (GE Paradox)"
            narrative = f"Organization is hyper-fluid. Capital moves so fast it breaks structural bonds. Predicted collapse matches GE timeline (~120 years vs 350 theoretical)."
        elif ls_final > 250:
            tier = "ELITE (70+ Year Club)"
            narrative = "Perfect balance of structure and fluidity. The 'Golden Mean' of corporate physics."
        elif ls_final > 150:
            tier = "DURABLE (Fortune 500 Avg)"
            narrative = "Strong survival instincts, healthy adaptation."
        else:
            tier = "FRAGILE (Stagnant)"
            narrative = "Structure is too rigid. Entropy will overtake growth."
            
        return MobilityOutput(
            rmi_score=round(rmi, 2),
            longevity_score=round(max(0, ls_final), 1), # Floor at 0 years
            marginal_return=round(net_derivative, 2),
            classification=tier,
            narrative=narrative,
            meltdown_risk=meltdown_risk
        )