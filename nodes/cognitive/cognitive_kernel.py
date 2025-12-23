"""
CHAMBERS PROTOCOL: COGNITIVE ARCHITECTURE NODE (KERNEL)
Based on 'The Mathematics of Psychological Framework' (INTJ Logic).

PRINCIPLE:
Personality is a calculated output of Neural Hardware, Environmental Training, and Framework Type.
Equation: [Hardware] * [Framework_Type] * [Training_Data] = Cognitive Velocity
"""

import json
from decimal import Decimal, getcontext

getcontext().prec = 10

class CognitiveArchEngine:
    def __init__(self):
        self.version = "1.0.0"
        self.name = "Chambers Cognitive Singularity Engine"

    def _normalize(self, value):
        return max(0.0, min(1.0, float(value)))

    def _determine_type(self, i, n, t, j):
        """Derives the 4-letter Code based on scalar inputs."""
        code = ""
        code += "E" if i > 0.5 else "I"
        code += "N" if n > 0.5 else "S"
        code += "T" if t > 0.5 else "F"
        code += "J" if j > 0.5 else "P"
        return code

    def compute_cognitive_physics(self, inputs: dict) -> dict:
        """
        Executes the Mathematics of Consciousness.
        """
        
        # --- DIMENSION 1: NEURAL HARDWARE (The Processor) ---
        # Derived from: Synapse Fire Rate * Processing Speed * Sensory Inputs
        v_synapse_rate = self._normalize(inputs.get("neural_synapse_fire_rate", 0.9))
        v_processing_speed = self._normalize(inputs.get("processing_speed_ms", 0.85)) # Higher is faster (inverted in reality, but normalized here)
        v_sensory_volume = self._normalize(inputs.get("sensory_input_volume", 0.8))
        
        # Hardware Score
        dim_hardware = v_synapse_rate * v_processing_speed * v_sensory_volume

        # --- DIMENSION 2: FRAMEWORK TYPE (The Operating System) ---
        # Derived from the 4 Dichotomies (Input 0.0 to 1.0)
        # 0.0 = I, S, F, P  |  1.0 = E, N, T, J
        val_ie = self._normalize(inputs.get("orientation_ie", 0.2)) # Low = Introvert
        val_ns = self._normalize(inputs.get("orientation_ns", 0.8)) # High = Intuitive
        val_tf = self._normalize(inputs.get("orientation_tf", 0.9)) # High = Thinking
        val_jp = self._normalize(inputs.get("orientation_jp", 0.8)) # High = Judging
        
        # Determine the Tag (e.g., "INTJ")
        type_code = self._determine_type(val_ie, val_ns, val_tf, val_jp)
        
        # Calculate Framework Efficiency (Alignment of the stack)
        # In this model, we assume extreme clarity (near 0 or near 1) is more efficient than ambiguity (0.5).
        # We use absolute distance from 0.5 to measure "Clarity of Preference"
        clarity_score = (abs(val_ie - 0.5) + abs(val_ns - 0.5) + abs(val_tf - 0.5) + abs(val_jp - 0.5)) / 2
        # Max clarity = 1.0 (if all are 0.0 or 1.0)

        dim_framework = 0.5 + (clarity_score * 0.5) # Base 0.5 + Bonus for clarity

        # --- DIMENSION 3: ENVIRONMENTAL INFLUENCE (Training Data) ---
        # Derived from: Maternal/Paternal Influence * Mentorship * Years
        # Ref: "(Maternal Grandmother 74 GB x Influence)"
        v_parental_imprint = self._normalize(inputs.get("early_influence_coherence", 0.7))
        v_mentorship = self._normalize(inputs.get("mentorship_quality", 0.8))
        v_experience = self._normalize(inputs.get("years_of_experience_index", 0.6))
        
        # Influence Score
        dim_influence = v_parental_imprint * v_mentorship * v_experience

        # --- DIMENSION 4: SITUATIONAL DYNAMICS (The Runtime) ---
        # Equation: (Motivation x Ability) - Situational Constraints
        v_motivation = self._normalize(inputs.get("intrinsic_motivation", 0.9))
        v_ability = self._normalize(inputs.get("skill_competence", 0.8))
        v_constraints = self._normalize(inputs.get("situational_constraints", 0.2)) # Low is good
        
        # Runtime Score
        dim_runtime = (v_motivation * v_ability) - (v_constraints * 0.5)
        dim_runtime = max(0.0, dim_runtime)

        # --- THE SINGULARITY CALCULATION ---
        # Cognitive_Velocity = Hardware * Framework * Influence * Runtime
        
        cognitive_index = (
            dim_hardware * dim_framework * dim_influence * dim_runtime
        ) * 100

        # --- AUDIT & DIAGNOSTICS ---
        vectors = {
            "Neural_Hardware_Speed": dim_hardware,
            "Framework_Clarity": dim_framework,
            "Environmental_Training": dim_influence,
            "Runtime_Dynamics": dim_runtime
        }
        
        bottleneck = min(vectors, key=vectors.get)
        bottleneck_val = vectors[bottleneck]
        
        # Directives based on Type
        directive = "Optimize Current State."
        if type_code == "INTJ":
            directive = "ARCHITECT DETECTED: Leverage systemic vision. Bottleneck is likely 'Social Friction' (Influence)."
        elif type_code == "ENTP":
            directive = "DEBATER DETECTED: High innovation potential. Risk of 'Execution Failure' (Runtime)."
        elif bottleneck == "Neural_Hardware_Speed":
            directive = "COGNITIVE LOAD: System is processing too much sensory data. Reduce inputs (Seclusion)."
        elif bottleneck == "Framework_Clarity":
            directive = "AMBIGUITY ERROR: Decision framework is conflicted (e.g., T vs F). Force a logic protocol."

        return {
            "cognitive_velocity_score": round(cognitive_index, 4),
            "detected_framework_type": type_code,
            "status": "LUCID" if cognitive_index > 50 else "FOGGED",
            "primary_bottleneck": bottleneck,
            "bottleneck_impact": f"Consciousness limited by {bottleneck} at {bottleneck_val:.2f}",
            "strategic_directive": directive,
            "vector_breakdown": vectors,
            "mechanics_source": "The Mathematics of Psychological Framework (Chambers)"
        }

if __name__ == "__main__":
    # Test: The Classic INTJ (Introvert, Intuitive, Thinking, Judging)
    engine = CognitiveArchEngine()
    test_case = {
        "orientation_ie": 0.1,  # Introvert
        "orientation_ns": 0.9,  # Intuitive
        "orientation_tf": 0.9,  # Thinking
        "orientation_jp": 0.9,  # Judging
        "neural_synapse_fire_rate": 0.95,
        "situational_constraints": 0.1
    }
    print(json.dumps(engine.compute_cognitive_physics(test_case), indent=2))