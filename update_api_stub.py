with open("api/analyze.py", "r") as f:
    content = f.read()

import re

correct_stub = """
    return {
        "status": "success",
        "insolvency_probability": 84,
        "projected_bleed_value": "₹ 4,20,00,000",
        "statutory_violations": [
            {
                "violation_type": "Uncapped Indemnification",
                "statute": "Section 73, Indian Contract Act",
                "risk_description": "Indemnity clause lacks financial cap, exposing enterprise to infinite liability."
            },
            {
                "violation_type": "Asymmetrical Termination",
                "statute": "Section 39, Indian Contract Act",
                "risk_description": "Supplier cannot terminate, while Buyer can terminate for convenience in 3 days."
            }
        ]
    }
"""

content = re.sub(r'    return \{\n.*?"status": "success",.*?"raw_content_preview":.*?\n    \}', correct_stub, content, flags=re.DOTALL)

with open("api/analyze.py", "w") as f:
    f.write(content)
