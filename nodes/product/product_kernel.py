"""
CHAMBERS PROTOCOL: PRODUCT STRATEGY & MARKETING NODE (KERNEL)
Based on 'The Product Strategy, Management, and Marketing Decision Model'.

PRINCIPLE:
Value Creation is step-wise:
1. Strategy (50% Impact)
2. Management/Execution (30% Impact)
3. Marketing/Launch (20% Impact)
4. Result = (Base Score) * (Speed_Multiplier)
"""

import json
from decimal import Decimal, getcontext

getcontext().prec = 10

class ProductEngine:
    def __init__(self):
        self.version = "1.0.0"
        self.name = "Chambers Product Singularity Engine"

    def _normalize(self, value):
        return max(0.0, min(1.0, float(value)))

    def compute_product_viability(self, inputs: dict) -> dict:
        """
        Executes the Product Decision Model.
        """
        
        # --- PHASE 1: PRODUCT STRATEGY (Max 50 Points) ---
        # "Early Stage Product Concept = 50% Total Profit Impact"
        v_landscape = self._normalize(inputs.get("competitive_landscape", 0.8))
        v_assets = self._normalize(inputs.get("existing_assets_leverage", 0.7))
        v_market_fit = self._normalize(inputs.get("product_market_fit", 0.6))
        
        # Calculation: (15 pts) + (15 pts) + (20 pts)
        score_strategy = (v_landscape * 15) + (v_assets * 15) + (v_market_fit * 20)

        # --- PHASE 2: PRODUCT MANAGEMENT (Max 30 Points) ---
        # "Mid-Stage Product = 30% Profit Impact"
        v_backlog = self._normalize(inputs.get("backlog_prioritization", 0.8))
        v_buy_build = self._normalize(inputs.get("buy_build_partner_decision", 0.9))
        v_biz_plan = self._normalize(inputs.get("business_plan_validity", 0.8))
        
        # Calculation: (15 pts) + (10 pts) + (5 pts)
        score_management = (v_backlog * 15) + (v_buy_build * 10) + (v_biz_plan * 5)

        # --- PHASE 3: PRODUCT MARKETING (Max 20 Points) ---
        # Derived from Target Market, Brand Awareness, and Outreach
        v_target_market = self._normalize(inputs.get("target_market_clarity", 0.7))
        v_brand = self._normalize(inputs.get("brand_awareness", 0.6))
        v_outreach = self._normalize(inputs.get("outreach_tactics", 0.7))
        
        # Calculation: (10 pts) + (5 pts) + (5 pts)
        score_marketing = (v_target_market * 10) + (v_brand * 5) + (v_outreach * 5)

        # --- PHASE 4: THE WINDOW OF OPPORTUNITY (Multiplier) ---
        # "Window of Opportunity Profitability"
        # Speed to Market and Ops Alignment act as the force multiplier.
        v_speed = self._normalize(inputs.get("speed_to_market", 0.7))
        v_ops_alignment = self._normalize(inputs.get("operational_alignment", 0.8))
        
        # If speed is low, the window closes (multiplier < 1.0)
        # If speed is high, we capture full value.
        multiplier = (v_speed * 0.6) + (v_ops_alignment * 0.4) 
        # Range approx 0.0 to 1.0

        # --- THE SINGULARITY CALCULATION ---
        # Base Potential (0-100)
        base_profit_impact = score_strategy + score_management + score_marketing
        
        # Realized Pipeline Value (The Outcome)
        pipeline_score = base_profit_impact * multiplier

        # --- AUDIT & DIAGNOSTICS ---
        vectors = {
            "Strategy_Foundation (Max 50)": score_strategy,
            "Management_Execution (Max 30)": score_management,
            "Marketing_Activation (Max 20)": score_marketing,
            "Speed_Multiplier": multiplier
        }
        
        bottleneck = "None"
        if score_strategy < 25:
            bottleneck = "Strategy_Gap"
        elif score_management < 15:
            bottleneck = "Execution_Gap"
        elif score_marketing < 10:
            bottleneck = "Marketing_Gap"
        elif multiplier < 0.6:
            bottleneck = "Speed_to_Market"
            
        # Directives
        directive = "Launch & Scale."
        if bottleneck == "Strategy_Gap":
            directive = "HALT DEVELOPMENT: Product Market Fit or Asset Leverage is missing. Do not build yet."
        elif bottleneck == "Execution_Gap":
            directive = "PROCESS FAILURE: Backlog is messy or Build/Buy decision is wrong. Fix the roadmap."
        elif bottleneck == "Speed_to_Market":
            directive = "WINDOW CLOSING: Product is good, but you are too slow. Simplify MVP immediately."

        return {
            "product_pipeline_score": round(pipeline_score, 4),
            "base_profit_potential": round(base_profit_impact, 2),
            "status": "MARKET_READY" if pipeline_score > 60 else "NEEDS_REVISION",
            "primary_bottleneck": bottleneck,
            "strategic_directive": directive,
            "vector_breakdown": vectors,
            "mechanics_source": "The Mechanics of Product Strategy & Marketing (Chambers)"
        }

if __name__ == "__main__":
    # Test: Great Strategy, Slow Execution
    engine = ProductEngine()
    test_case = {
        "product_market_fit": 0.95,
        "backlog_prioritization": 0.9,
        "speed_to_market": 0.3 # Too slow
    }
    print(json.dumps(engine.compute_product_viability(test_case), indent=2))