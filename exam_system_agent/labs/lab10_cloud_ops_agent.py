"""
Lab 10: Cloud Operations Agent
Simple student version: Check server response time, detect slowdowns, and fix by restarting service.
Subjects: Exam Portal (ML, CNS, Agentic AI)
"""

import sys
import os

# Simulated portal state
class ExamPortal:
    def __init__(self):
        self.latency_ms = 40
        self.status = "Normal"

    def cause_overload(self):
        print("\n[Event] 500 students logged in to submit Machine Learning (ML303) exam!")
        self.latency_ms = 950
        self.status = "Slow / Overloaded"

    def restart_service(self):
        print("[Fix] Restarting server workers and clearing memory...")
        self.latency_ms = 45
        self.status = "Normal"

def monitor_and_heal(portal):
    print(f"\nChecking server... Latency: {portal.latency_ms}ms (Status: {portal.status})")
    
    # Threshold check
    if portal.latency_ms > 200:
        print("Alert: Server is too slow! Triggering automatic fix...")
        portal.restart_service()
        print(f"Check after fix: Latency is now {portal.latency_ms}ms (Status: {portal.status})")
    else:
        print("Server health is OK.")

if __name__ == "__main__":
    print("=" * 55)
    print("Lab 10: Cloud Operations Agent")
    print("=" * 55)

    server = ExamPortal()
    
    # 1. Normal state
    monitor_and_heal(server)

    # 2. Overload event happens
    server.cause_overload()

    # 3. Cloud agent monitors and heals
    monitor_and_heal(server)
