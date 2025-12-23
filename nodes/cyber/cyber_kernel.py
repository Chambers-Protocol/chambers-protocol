"""
CHAMBERS PROTOCOL: CYBERSECURITY NODE (KERNEL)
Based on 'The Optimal Mechanics of Cybersecurity' Architecture.

PRINCIPLE:
Security is a 'Weakest Link' equation. 
If (Human_Awareness) is 0, the firewall doesn't matter.
Equation: [IAM] * [Detection] * [Data_Protection] * [Human_Factor] * [Governance]
"""

import json
from decimal import Decimal, getcontext

getcontext().prec = 10

class CyberSecEngine:
    def __init__(self):
        self.version = "1.0.0"
        self.name = "Chambers Cyber Singularity Engine"

    def _normalize(self, value):
        return max(0.0, min(1.0, float(value)))

    def compute_security_posture(self, inputs: dict) -> dict:
        """
        Executes the Cybersecurity Mechanics.
        """
        
        # --- LAYER 1: IDENTITY & ACCESS (The Gate) ---
        # Derived from: MFA * RBAC * PAM (Privileged Access)
        v_mfa = self._normalize(inputs.get("mfa_coverage", 1.0)) # MUST be 1.0
        v_rbac = self._normalize(inputs.get("least_privilege_enforcement", 0.9))
        v_pam = self._normalize(inputs.get("privileged_access_mgmt", 0.8))
        
        # Identity Score
        dim_iam = v_mfa * v_rbac * v_pam

        # --- LAYER 2: THREAT DETECTION (The Eyes) ---
        # Derived from: SIEM * EDR * Incident Response
        v_siem = self._normalize(inputs.get("siem_coverage", 0.8))
        v_edr = self._normalize(inputs.get("endpoint_detection", 0.9))
        v_ir_plan = self._normalize(inputs.get("incident_response_readiness", 0.7))
        
        # Detection Score
        dim_detection = v_siem * v_edr * v_ir_plan

        # --- LAYER 3: DATA PROTECTION (The Vault) ---
        # Derived from: Encryption * DLP * Backups (Immutable)
        v_encryption = self._normalize(inputs.get("encryption_at_rest", 1.0))
        v_dlp = self._normalize(inputs.get("data_loss_prevention", 0.7))
        v_backups = self._normalize(inputs.get("immutable_backups", 0.9))
        
        # Data Score
        dim_data = v_encryption * v_dlp * v_backups

        # --- LAYER 4: THE HUMAN FACTOR (The Weakest Link) ---
        # Derived from: Phishing Sims * Training * Culture
        v_phishing = self._normalize(inputs.get("phishing_resilience", 0.6)) # Humans usually suck here
        v_training = self._normalize(inputs.get("security_awareness_training", 0.8))
        
        # Human Score
        dim_human = v_phishing * v_training

        # --- LAYER 5: GOVERNANCE (The Law) ---
        # Derived from: Policy * Audit * 3rd Party Risk
        v_policy = self._normalize(inputs.get("policy_enforcement", 0.9))
        v_audit = self._normalize(inputs.get("audit_frequency", 0.8))
        v_vendor = self._normalize(inputs.get("vendor_risk_mgmt", 0.7))
        
        # Governance Score
        dim_governance = v_policy * v_audit * v_vendor

        # --- THE SINGULARITY CALCULATION ---
        # Total_Security_Posture = (IAM * Detection * Data * Human * Governance)
        # Note: If any layer is weak, the multiplier destroys the score.
        
        cyber_index = (
            dim_iam * dim_detection * dim_data * dim_human * dim_governance
        ) * 100

        # --- AUDIT & DIAGNOSTICS ---
        vectors = {
            "Identity_Access_IAM": dim_iam,
            "Threat_Detection": dim_detection,
            "Data_Protection": dim_data,
            "Human_Factor": dim_human,
            "Governance_GRC": dim_governance
        }
        
        bottleneck = min(vectors, key=vectors.get)
        bottleneck_val = vectors[bottleneck]
        
        # Strategic Directives
        directive = "Maintain Defense-in-Depth."
        if bottleneck == "Human_Factor" and bottleneck_val < 0.5:
            directive = "CRITICAL VULNERABILITY: Staff represent an Insider Threat. Mandate immediate Phishing Simulations."
        elif bottleneck == "Identity_Access_IAM" and bottleneck_val < 0.8:
            directive = "IDENTITY CRISIS: Enforce MFA and remove Admin Rights immediately."
        elif bottleneck == "Data_Protection" and bottleneck_val < 0.7:
            directive = "RANSOMWARE RISK: Verify immutable backups. Data is exposed."

        return {
            "cyber_fidelity_score": round(cyber_index, 4),
            "status": "SECURE" if cyber_index > 75 else "VULNERABLE",
            "primary_vulnerability": bottleneck,
            "vulnerability_impact": f"Security posture capped by {bottleneck} at {bottleneck_val:.2f}",
            "strategic_directive": directive,
            "vector_breakdown": vectors,
            "mechanics_source": "The Optimal Mechanics of Cybersecurity (Chambers)"
        }

if __name__ == "__main__":
    # Test: Great Firewall, Stupid Users
    engine = CyberSecEngine()
    test_case = {
        "mfa_coverage": 1.0,
        "encryption_at_rest": 1.0,
        "phishing_resilience": 0.2, # User clicked the link
        "security_awareness_training": 0.5
    }
    print(json.dumps(engine.compute_security_posture(test_case), indent=2))