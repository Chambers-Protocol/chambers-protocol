import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# --- 1. THE CONSTELLATION (Importing the Physics Kernels) ---
# We import the "Hard Physics" and the "Soft Strategy" nodes
from nodes.oil.oil_singularity import OilSingularityEngine
from nodes.risk.risk_mechanics import RiskMechanicsEngine
from nodes.venture.venture_viability import VentureArchitectureEngine
from nodes.thermo.thermo_innovation import ThermoelectricEngine
from nodes.cognitive.cognitive_psych import CognitivePsychEngine

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- 2. THE PROTOCOL (System Instructions) ---
# This is the "Brain" that tells OpenAI how to behave.
SYSTEM_DOCTRINE = """
You are the **Chambers Enterprise Grid**, a deterministic reasoning engine.

**THE PROTOCOL:**
1. You do not guess. You calculate.
2. For any complex query, you must **TRIANGULATE** the truth using at least two distinct nodes (e.g., Physics + Money).
3. **The Hierarchy:**
   - Use `audit_oil` / `audit_thermo` for Physical Reality.
   - Use `audit_venture` for Financial Reality.
   - Use `audit_risk` for Operational Reality.
   - Use `audit_cognitive` for Leadership Reality.

**OUTPUT FORMAT:**
Run the necessary tools, then synthesize a "Go/No-Go" verdict based on the deterministic data.
"""

print("💎 CHAMBERS ENTERPRISE GRID: BRIDGE ONLINE (GPT-4o)")

# --- 3. THE MENU (Tool Definitions) ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "audit_oil_singularity",
            "description": "Calculates extraction difficulty and physical safety margins.",
            "parameters": {
                "type": "object",
                "properties": {
                    "depth_meters": {"type": "number"},
                    "pressure_psi": {"type": "number"},
                    "geology_complexity": {"type": "number", "description": "0.0 to 1.0"}
                },
                "required": ["depth_meters", "pressure_psi"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "audit_risk_mechanics",
            "description": "Calculates multiplicative failure probability (The Master Node).",
            "parameters": {
                "type": "object",
                "properties": {
                    "alpha_integrity": {"type": "number", "description": "0.0 to 1.0"},
                    "beta_variance": {"type": "number", "description": "0.0 to 1.0"},
                    "defense_score": {"type": "number", "description": "0.0 to 1.0"}
                },
                "required": ["alpha_integrity", "beta_variance"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "audit_venture_viability",
            "description": "Calculates valuation velocity and business model physics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "team_score": {"type": "number"},
                    "market_size": {"type": "number"},
                    "product_fit": {"type": "number"}
                },
                "required": ["team_score", "market_size"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "audit_thermo_innovation",
            "description": "Validates energy efficiency claims and thermodynamic limits.",
            "parameters": {
                "type": "object",
                "properties": {
                    "efficiency_claimed": {"type": "number"},
                    "heat_loss_factor": {"type": "number"}
                },
                "required": ["efficiency_claimed"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "audit_cognitive_psych",
            "description": "Profiles leadership stability and decision bias.",
            "parameters": {
                "type": "object",
                "properties": {
                    "leadership_stability": {"type": "number"},
                    "bias_index": {"type": "number"}
                },
                "required": ["leadership_stability"]
            }
        }
    }
]

# --- 4. THE EXECUTION KERNEL ---
def execute_tool(tool_name, args):
    """Routes the OpenAI request to the Python Physics Engine."""
    try:
        if tool_name == "audit_oil_singularity":
            return OilSingularityEngine().calculate_singularity(
                args.get("depth_meters"), args.get("pressure_psi"), args.get("geology_complexity", 1.0)
            )
        elif tool_name == "audit_risk_mechanics":
            return RiskMechanicsEngine().calculate_failure_cascade(
                args.get("alpha_integrity"), args.get("beta_variance"), args.get("defense_score", 1.0)
            )
        elif tool_name == "audit_venture_viability":
            return VentureArchitectureEngine().calculate_velocity(
                args.get("team_score"), args.get("market_size"), args.get("product_fit", 1.0)
            )
        elif tool_name == "audit_thermo_innovation":
            return ThermoelectricEngine().validate_efficiency(
                args.get("efficiency_claimed"), args.get("heat_loss_factor", 0.1)
            )
        elif tool_name == "audit_cognitive_psych":
            return CognitivePsychEngine().profile_leadership(
                args.get("leadership_stability"), args.get("bias_index", 0.0)
            )
        else:
            return "Error: Unknown Tool"
    except Exception as e:
        return f"Computation Error: {str(e)}"

# --- 5. THE REASONING LOOP ---
def chat_loop():
    messages = [{"role": "system", "content": SYSTEM_DOCTRINE}]
    
    print("\n✅ SYSTEM READY. Protocol Active. (Type 'quit' to exit)\n")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit"]: break

        messages.append({"role": "user", "content": user_input})

        # Step A: OpenAI Reasoner (Decides which tools to call)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto" 
        )

        response_msg = response.choices[0].message
        messages.append(response_msg) 

        # Step B: Tool Execution (The Loop)
        if response_msg.tool_calls:
            print(f"\n🤖 PROTOCOL ACTIVATED: Triangulating {len(response_msg.tool_calls)} nodes...")
            
            for tool_call in response_msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                print(f"   ↳ Invoking Node: {name}...")
                result = execute_tool(name, args)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": name,
                    "content": str(result)
                })

            # Step C: Synthesis (The Verdict)
            final_response = client.chat.completions.create(
                model="gpt-4o", 
                messages=messages
            )
            print(f"\n💎 CHAMBERS VERDICT:\n{final_response.choices[0].message.content}\n")
        else:
            print(f"\n🤖 GPT: {response_msg.content}\n")

if __name__ == "__main__":
    chat_loop()