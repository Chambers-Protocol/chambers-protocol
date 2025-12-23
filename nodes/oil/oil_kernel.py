"""
CHAMBERS PROTOCOL: OIL & GAS SINGULARITY NODE (KERNEL)
Based on 'The Oil & Gas Singularity Point Algorithm' Architecture.

PRINCIPLE:
The convergence of Computational Power (Quantum/AI) and Physical Engineering.
Structure: [Computation] * [Engineering] * [Operations] * [Economics]
"""

import json
from decimal import Decimal, getcontext

# High precision for high-value resource extraction
getcontext().prec = 10

class OilSingularityEngine:
    def __init__(self):
        self.version = "1.0.0"
        self.name = "Chambers O&G Singularity Engine"

    def _normalize(self, value):
        """Clamps inputs between 0.0 and 1.0"""
        return max(0.0, min(1.0, float(value)))

    def compute_singularity_index(self, inputs: dict) -> dict:
        """
        Executes the Singularity Point Algorithm.
        """
        
        # --- DIMENSION 1: COMPUTATIONAL FIDELITY (The Brain) ---
        # Derived from: Quantum Computing * AI Apps * HPC
        v_reservoir_sims = self._normalize(inputs.get("reservoir_simulation_accuracy", 0.9))
        v_seismic_data = self._normalize(inputs.get("seismic_clarity", 0.85))
        v_predictive_maint = self._normalize(inputs.get("predictive_maintenance_ai", 0.8))
        
        # Computational_Score = (Sims * Seismic * AI)
        dim_compute = v_reservoir_sims * v_seismic_data * v_predictive_maint

        # --- DIMENSION 2: ENGINEERING & RESEARCH (The Science) ---
        # Derived from: Geology * Drilling Tech * Material Science
        v_geology = self._normalize(inputs.get("geological_certainty", 0.7)) # Often the biggest unknown
        v_drilling_tech = self._normalize(inputs.get("drilling_technology_tier", 0.9))
        v_materials = self._normalize(inputs.get("material_durability", 0.9))
        
        # Engineering_Score = (Geology * Tech * Materials)
        dim_engineering = v_geology * v_drilling_tech * v_materials

        # --- DIMENSION 3: OPERATIONAL EXCELLENCE (The Musk Algorithm) ---
        # Derived from: Safety * Environmental Impact * Process Optimization
        v_safety = self._normalize(inputs.get("safety_protocols", 1.0)) # MUST BE 1.0 or huge risk
        v_environmental = self._normalize(inputs.get("environmental_compliance", 1.0))
        v_process_opt = self._normalize(inputs.get("process_automation", 0.8))
        
        # Operations_Score = (Safety * Env * Process)
        # Note: If Safety or Environmental is < 0.8, we penalize heavily
        dim_operations = v_safety * v_environmental * v_process_opt

        # --- DIMENSION 4: MARKET ECONOMICS (The Value) ---
        # Derived from: TAM * Efficiency Gains * Market Valuation
        v_market_demand = self._normalize(inputs.get("global_demand_index", 0.9))
        v_cost_reduction = self._normalize(inputs.get("opex_reduction_target", 0.8))
        
        # Economics_Score
        dim_economics = v_market_demand * v_cost_reduction

        # --- THE SINGULARITY CALCULATION ---
        # The Final Equation: Compute * Engineering * Operations * Economics
        # This represents the "Probability of Ideal Extraction"
        
        singularity_index = (
            dim_compute * dim_engineering * dim_operations * dim_economics
        ) * 100

        # --- AUDIT & DIAGNOSTICS ---
        vectors = {
            "Computational_Fidelity": dim_compute,
            "Engineering_Integrity": dim_engineering,
            "Operational_Excellence": dim_operations,
            "Economic_Viability": dim_economics
        }
        
        # Identify the Bottleneck
        bottleneck = min(vectors, key=vectors.get)
        
        # Special Logic for "Musk Algorithm" (Delete, Simplify, Accelerate)
        recommendation = "Maintain Course"
        if dim_operations < 0.7:
            recommendation = "APPLY MUSK ALGORITHM: Delete processes. Simplify requirements."
        elif dim_compute < 0.7:
            recommendation = "UPGRADE COMPUTE: Reservoir simulation fidelity is limiting yield."

        return {
            "singularity_index": round(singularity_index, 4),
            "status": "OPTIMAL" if singularity_index > 65 else "SUB-OPTIMAL",
            "primary_bottleneck": bottleneck,
            "bottleneck_value": round(vectors[bottleneck], 4),
            "strategic_directive": recommendation,
            "vector_breakdown": vectors,
            "algorithm_source": "The Oil & Gas Singularity Point Algorithm (Chambers)"
        }

if __name__ == "__main__":
    # Quick Test
    engine = OilSingularityEngine()
    test_case = {
        "reservoir_simulation_accuracy": 0.95, 
        "geological_certainty": 0.4, # Bad geology
        "safety_protocols": 1.0
    }
    print(json.dumps(engine.compute_singularity_index(test_case), indent=2))