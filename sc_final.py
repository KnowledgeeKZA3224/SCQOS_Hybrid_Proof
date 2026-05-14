from braket.circuits import Circuit
from braket.devices import LocalSimulator
from datetime import datetime, timezone
import json, hashlib

SHOTS = 1024

def sc_audit(gates, label):
    failed = [k for k,v in gates.items() if v is not True]
    audit = {
        "label": label,
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failed else "DENIED",
        "failed_gates": failed,
        "audit_hash": hashlib.sha256(json.dumps(gates, sort_keys=True).encode()).hexdigest()
    }
    print(json.dumps(audit, indent=2))
    return not failed

def circuit():
    c = Circuit()
    c.h(0)
    c.cnot(0,1)
    c.cnot(1,2)
    c.cnot(2,3)
    c.rx(0, 0.5)
    c.ry(1, 1.0)
    c.rz(2, 1.5)
    c.rx(3, 2.0)
    return c

PASS = dict(time=True, continuity=True, alignment=True, genesis=True, boundary=True, reference=True, causality=True, consciousness=True, coherence=True)
FAIL = PASS.copy()
FAIL["boundary"] = False

device = LocalSimulator()

print("=== SC PASS TEST ===")
if sc_audit(PASS, "SC_AWS_PASS"):
    result = device.run(circuit(), shots=SHOTS).result()
    print("✅ SC APPROVED → EXECUTION CREATED")
    print(result.measurement_counts)

print("\n=== SC FAIL TEST ===")
if sc_audit(FAIL, "SC_AWS_FAIL"):
    result = device.run(circuit(), shots=SHOTS).result()
else:
    print("❌ SC DENIED → NO EXECUTION CREATED")
    print("SHOTS SENT: 0")
