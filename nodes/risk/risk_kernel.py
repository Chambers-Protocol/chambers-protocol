"""
CHAMBERS PROTOCOL: RISK MANAGEMENT NODE (KERNEL)
Based on 'The Optimal Mechanics of Risk Management' Architecture.

PRINCIPLE:
Risk Management is not additive; it is multiplicative. 
If (Liquidity Management) is zero, the Total Safety Score is zero, 
regardless of how good your Trading Algorithm is.
"""

import math
import json
from decimal import Decimal, getcontext

# Set high precision for financial fidelity
getcontext().prec = 10

class RiskMechanicsEngine:
    def __init__(self):
        self.version = "1.0.0"
        self.name = "Chambers Risk Singularity Engine"

    def _normalize(self, value, min_val=0.0, max_val=1.0):
        """Ensures inputs remain within deterministic bounds (0.0 to 1.0)."""
        return max(min_val, min(max_val, float(value)))

    def compute_risk_fidelity(self, inputs: dict) -> dict:
        """
        Executes the Multiplicative Risk Chain.
        
        The Model decomposes Risk into 5 Core Vectors (derived from your Architecture):
        1. Investment_Thesis (Alpha Generation)
        2. Quantitative_Research (Model Integrity)
        3. Trading_Infrastructure (Execution Safety)
        4. Risk_Models (Defensive Geometry)
        5. Regulatory_Compliance (Structural Integrity)
        """
        
        # --- 1. PARSE INPUTS (With Defaults) ---
        # If the user (Claude) doesn't provide a specific score, we assume "Standard Industry Friction" (0.85)
        
        # VECTOR A: Investment Thesis Integrity
        # Logic: (Philosophy * Strategy_Implementation)
        v_philosophy = self._normalize(inputs.get("philosophy_alignment", 0.9))
        v_strategy = self._normalize(inputs.get("strategy_implementation", 0.9))
        
        # VECTOR B: Quantitative Research
        # Logic: (Models * Algorithms * Historical_Data * Signal_Generator)
        v_models = self._normalize(inputs.get("model_robustness", 0.85))
        v_data_cleanliness = self._normalize(inputs.get("data_integrity", 0.9))
        
        # VECTOR C: Trading Infrastructure (The Piping)
        # Logic: (Liquidity * Margin * Clearing * Settlement)
        v_liquidity = self._normalize(inputs.get("liquidity_depth", 0.8))
        v_execution = self._normalize(inputs.get("execution_speed", 0.95))
        
        # VECTOR D: Risk Models (The Shield)
        # Logic: (VaR * Stress_Testing * Scenario_Analysis)
        v_stress_testing = self._normalize(inputs.get("stress_testing_rigor", 0.7)) # Default lower to punish laziness
        v_portfolio_opt = self._normalize(inputs.get("portfolio_optimization", 0.85))
        
        # VECTOR E: Compliance & Ops (The Foundation)
        # Logic: (Regulatory_Adherence * Internal_Policies)
        v_compliance = self._normalize(inputs.get("regulatory_adherence", 1.0)) # Binary: You follow laws or you don't.
        v_ops = self._normalize(inputs.get("operational_resilience", 0.9))

        # --- 2. THE MULTIPLICATIVE CHAINS ---
        
        # "Investment Capital" Integrity
        alpha_integrity = v_philosophy * v_strategy
        
        # "Research & Analysis" Integrity
        research_fidelity = v_models * v_data_cleanliness
        
        # "Trading & Execution" Integrity
        execution_fidelity = v_liquidity * v_execution
        
        # "Risk Management" Integrity
        defense_score = v_stress_testing * v_portfolio_opt
        
        # "Operational" Integrity
        structural_integrity = v_compliance * v_ops
        
        # --- 3. THE SINGULARITY CALCULATION ---
        # Total_Risk_Fidelity = (Alpha * Research * Execution * Defense * Structure)
        # If ANY of these are weak, the whole score collapses.
        
        total_fidelity = (
            alpha_integrity * research_fidelity * execution_fidelity * defense_score * structural_integrity
        ) * 100  # Scale to 0-100

        # --- 4. GENERATE DETERMINISTIC AUDIT ---
        
        # Identify the "Constraint" (The Lowest Value)
        components = {
            "Alpha_Integrity": alpha_integrity,
            "Research_Fidelity": research_fidelity,
            "Execution_Fidelity": execution_fidelity,
            "Defense_Score": defense_score,
            "Structural_Integrity": structural_integrity
        }
        
        # Find the weak link
        constraint_name = min(components, key=components.get)
        constraint_value = components[constraint_name]

        return {
            "risk_fidelity_score": round(total_fidelity, 4),
            "status": "OPTIMAL" if total_fidelity > 80 else "COMPROMISED",
            "critical_constraint_node": constraint_name,
            "constraint_impact": f"The entire risk architecture is capped by {constraint_name} at {constraint_value:.2f}",
            "vector_breakdown": components,
            "mechanics_source": "The Optimal Mechanics of Risk Management (Chambers)"
        }

# --- TESTING BLOCK (Allows you to run 'python risk_kernel.py' to verify) ---
if __name__ == "__main__":
    engine = RiskMechanicsEngine()
    
    # Simulate a Scenario: "High Algo Capability, but Low Stress Testing"
    test_inputs = {
        "model_robustness": 0.99,       # Amazing AI models
        "execution_speed": 0.99,        # Fast execution
        "stress_testing_rigor": 0.40,   # BUT... they ignored tail risks
        "regulatory_adherence": 1.0
    }
    
    result = engine.compute_risk_fidelity(test_inputs)
    print(json.dumps(result, indent=2))