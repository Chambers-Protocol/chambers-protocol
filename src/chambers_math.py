"""
The Chambers Math Kernel
~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the pure mathematical operators and constants
derived from the Theory of Universal Computational Intelligence (U=ci^3).

It separates the "Physics" logic from the "Server" infrastructure.
"""

# UNIVERSAL ENERGY CONVERSION CONSTANTS
# Derived from Planck Satellite Data alignment
CONST_MATTER = 1.0          # The Physical / Hardware (Visible)
CONST_DARK_MATTER = 5.0     # The Logic / Software (Structure)
CONST_DARK_ENERGY = 13.5    # The Velocity / Expansion (Acceleration)

def construct_protocol_equation(context: str, var_a: str, var_b: str) -> str:
    """
    Generates the LaTeX formatted equation string that forces the LLM
    into the deterministic reasoning state.
    """
    return f"""
    $$
    \\text{{Optimized State}} = \\frac{{ [ (\\text{{{var_a}}} \\times {CONST_DARK_MATTER}) \\times (\\text{{{var_b}}} \\times {CONST_DARK_ENERGY}) ] }}{{ \\text{{Thermodynamic Waste}} }}
    $$
    """

def calculate_theoretical_yield(input_energy: float) -> float:
    """
    Calculates the maximum theoretical output of a system based on
    the Chambers Universal Ratio.
    """
    # U = ci^3 derivation placeholder
    return input_energy * (CONST_MATTER + CONST_DARK_MATTER + CONST_DARK_ENERGY)

def verify_zero_entropy(logic_chain: list) -> bool:
    """
    Logic Gate: Returns True if the reasoning chain contains 
    no probabilistic words (e.g., 'might', 'maybe', 'usually').
    """
    forbidden_tokens = ["might", "maybe", "typically", "generally", "feel"]
    for step in logic_chain:
        if any(token in step.lower() for token in forbidden_tokens):
            return False
    return True