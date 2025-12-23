"""
CHAMBERS PROTOCOL: VENTURE ARCHITECTURE NODE (KERNEL)
Based on 'The Mechanics of Venture Architecture'.

PRINCIPLE:
Venture Value = (Foundation_Base_Score) * (Execution_Multiplier) * (Market_Velocity)
1. Foundation is ADDITIVE (Max 50% Impact).
2. Execution/Growth is MULTIPLICATIVE (The Scale Factor).
"""

import json
from decimal import Decimal, getcontext

getcontext().prec = 10

class VentureArchEngine:
    def __init__(self):
        self.version = "1.0.0"
        self.name = "Chambers Venture Singularity Engine"

    def _normalize(self, value):
        return max(0.0, min(1.0, float(value)))

    def compute_venture_valuation(self, inputs: dict) -> dict:
        """
        Executes the Venture Architecture Mechanics.
        """
        
        # --- PHASE 1: THE FOUNDATION (Additive - Max 50 Points) ---
        # "Early Stage Product Concept = 50% Profit Impact"
        # Derived from: Competitive Landscape + Existing Assets + Market Fit
        
        v_landscape = self._normalize(inputs.get("competitive_landscape_clarity", 0.8))
        v_assets = self._normalize(inputs.get("existing_assets_leverage", 0.7))
        v_market_fit = self._normalize(inputs.get("product_market_fit", 0.6)) # The hardest part
        
        # Logic: (15% + 15% + 20%) = 50% Total
        score_foundation = (v_landscape * 15) + (v_assets * 15) + (v_market_fit * 20)
        # Max here is 50.0

        # --- PHASE 2: EXECUTION MECHANICS (Multiplicative) ---
        # Derived from: Backlog * Business Plan * Speed to Market
        # If execution is poor (0.5), it halves the value of the foundation.
        
        v_backlog = self._normalize(inputs.get("backlog_prioritization", 0.8))
        v_biz_plan = self._normalize(inputs.get("business_plan_solidity", 0.9))
        v_speed = self._normalize(inputs.get("speed_to_market", 0.7))
        
        # Execution Multiplier (0.0 to 1.0)
        mult_execution = v_backlog * v_biz_plan * v_speed

        # --- PHASE 3: MARKET VELOCITY (Multiplicative) ---
        # Derived from: Marketing Strategy * Sales Pipeline * Retention
        
        v_marketing = self._normalize(inputs.get("marketing_strategy_efficacy", 0.7))
        v_sales = self._normalize(inputs.get("sales_pipeline_velocity", 0.6))
        v_retention = self._normalize(inputs.get("customer_retention_rate", 0.8))
        
        # Growth Multiplier (0.0 to 1.0)
        mult_growth = v_marketing * v_sales * v_retention

        # --- PHASE 4: VALUATION DRIVERS (The Exponents) ---
        # Derived from: Revenue/Employee * Win Rate * Total Addressable Market (TAM)
        
        v_rev_per_employee = self._normalize(inputs.get("revenue_per_employee_efficiency", 0.5))
        v_win_rate = self._normalize(inputs.get("competitive_win_rate", 0.5))
        v_tam_access = self._normalize(inputs.get("tam_accessibility", 0.8))
        
        # Valuation Multiplier
        mult_valuation = v_rev_per_employee * v_win_rate * v_tam_access

        # --- THE SINGULARITY CALCULATION ---
        # Venture_Score = (Foundation) * (Execution * Growth * Valuation) * Scaling_Factor
        
        # We start with the Foundation (0-50).
        # We multiply by the others. 
        # Since multipliers < 1.0 reduce the score, we assume "Standard Performance" is 1.0
        # To make the score intuitive (0-100), we map the multipliers effectively.
        
        # "Perfect Execution" would keep the score intact. "Super-Performance" could boost it.
        # Here, we treat them as efficiency constraints.
        
        efficiency_index = mult_execution * mult_growth * mult_valuation
        
        # We calculate the probability of "Unicorn Status" (High Valuation)
        # Formula: (Foundation Score * 2) * (Efficiency Index ^ 0.3)
        # (The ^0.3 softens the blow of multiplying three decimals together)
        
        venture_score = (score_foundation * 2) * (efficiency_index ** 0.33)

        # --- AUDIT & DIAGNOSTICS ---
        vectors = {
            "Foundation_Strength (Max 50)": score_foundation,
            "Execution_Efficiency": mult_execution,
            "Market_Velocity": mult_growth,
            "Valuation_Potential": mult_valuation
        }
        
        # Bottleneck Analysis
        bottleneck = "None"
        min_val = 1.0
        
        if mult_execution < min_val: 
            bottleneck = "Execution_Mechanics"
            min_val = mult_execution
        if mult_growth < min_val:
            bottleneck = "Market_Velocity"
            min_val = mult_growth
        if mult_valuation < min_val:
            bottleneck = "Valuation_Drivers"
            min_val = mult_valuation
            
        # Strategic Directives
        directive = "Scale Aggressively."
        if score_foundation < 25:
            directive = "PIVOT REQUIRED: Product Market Fit or Asset Leverage is too weak (<50%). Do not scale."
        elif bottleneck == "Execution_Mechanics":
            directive = "OPERATIONAL DRAG: Fix backlog prioritization and speed to market before increasing ad spend."
        elif bottleneck == "Market_Velocity":
            directive = "FUNNEL LEAK: Sales pipeline or retention is destroying value. Halt hiring, fix churn."

        return {
            "venture_viability_score": round(venture_score, 4),
            "status": "INVESTABLE" if venture_score > 60 else "HIGH RISK",
            "primary_bottleneck": bottleneck,
            "bottleneck_impact": f"Valuation multiplier constrained by {bottleneck} at {min_val:.2f}",
            "strategic_directive": directive,
            "vector_breakdown": vectors,
            "mechanics_source": "The Mechanics of Venture Architecture (Chambers)"
        }

if __name__ == "__main__":
    # Test: Great Idea, Terrible Execution
    engine = VentureArchEngine()
    test_case = {
        "product_market_fit": 0.9,      # Great idea
        "speed_to_market": 0.2,         # Too slow
        "sales_pipeline_velocity": 0.3  # Can't sell it
    }
    print(json.dumps(engine.compute_venture_valuation(test_case), indent=2))