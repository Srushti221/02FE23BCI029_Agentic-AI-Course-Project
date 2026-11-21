"""
Lab 11: Agentic SDLC Factory
Simple student version: Autonomous agents build a software feature from requirements to deployment.
Task: Create an Exam Revaluation Fee Calculator (DBMS & CNS)
"""

import sys
import os

# Phase 1: Requirement Agent
def agent_requirement(req_text):
    print("\n[Step 1: Requirement Agent]")
    print(f" -> Requirement Parsed: '{req_text}'")
    return {"base_fee": 300, "discount_rule": "10% off for 3 or more subjects"}

# Phase 2: Design Agent
def agent_design(specs):
    print("\n[Step 2: Design Agent]")
    print(" -> Architecture: Created RevaluationCalculator class with calculate(num_subjects) method.")
    return specs

# Phase 3: Code Generator Agent
def agent_code():
    print("\n[Step 3: Code Generator Agent]")
    code = """
class RevaluationCalculator:
    def calculate(self, count):
        fee = count * 300
        if count >= 3:
            fee *= 0.90
        return int(fee)
"""
    print(" -> Generated Python class RevaluationCalculator dynamically.")
    return code

# Phase 4: Test Agent
def agent_test(code_str):
    print("\n[Step 4: Test Agent]")
    namespace = {}
    exec(code_str, namespace)
    calc = namespace["RevaluationCalculator"]()
    
    t1 = calc.calculate(1) == 300
    t2 = calc.calculate(3) == 810  # 900 - 10%
    print(f" -> Test 1 (1 subject = Rs 300): {'PASSED' if t1 else 'FAILED'}")
    print(f" -> Test 2 (3 subjects = Rs 810 discount): {'PASSED' if t2 else 'FAILED'}")
    return t1 and t2

# Phase 5: Deploy Agent
def agent_deploy(passed):
    print("\n[Step 5: Deployment Agent]")
    if passed:
        print(" -> All tests verified. Feature DEPLOYED to production portal.")
    else:
        print(" -> Tests failed. Deployment BLOCKED.")

if __name__ == "__main__":
    print("=" * 55)
    print("Lab 11: Agentic SDLC Factory (Automated Software Dev)")
    print("=" * 55)

    req = "Charge Rs 300 per subject for revaluation, with 10% discount for 3+ subjects."
    specs = agent_requirement(req)
    agent_design(specs)
    code = agent_code()
    passed = agent_test(code)
    agent_deploy(passed)

    print("\n" + "=" * 55)
    print("Requirement transformed into tested deployed code by Agents!")
    print("=" * 55)
