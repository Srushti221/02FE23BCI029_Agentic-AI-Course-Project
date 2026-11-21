"""
TOOL 4: Proctoring Signal Tool (Suggested Technology: Proctoring signals)
Role:
  Parses raw sensor & browser telemetry signals (tab switches, audio spikes, face detection)
  and computes an integrity anomaly score.
"""

def analyze_proctoring_signals(telemetry_events: list = None) -> dict:
    """
    Evaluates real-time exam telemetry.
    Input format: [{'type': 'tab_switch', 'duration_sec': 2}, ...]
    Returns integrity status, risk score (0-100), and infraction details.
    """
    telemetry_events = telemetry_events or []
    infractions = []
    penalty_score = 0

    for ev in telemetry_events:
        event_type = ev.get("type")
        if event_type == "tab_switch":
            duration = ev.get("duration_sec", 1)
            infractions.append(f"Browser tab unfocused for {duration}s")
            penalty_score += 20 * duration
        elif event_type == "multiple_faces":
            infractions.append("Secondary person detected by webcam")
            penalty_score += 50
        elif event_type == "audio_spike":
            db = ev.get("db", 75)
            infractions.append(f"Unusual voice / ambient noise ({db} dB)")
            penalty_score += 25
        elif event_type == "face_missing":
            infractions.append("Candidate face not visible in camera frame")
            penalty_score += 30

    risk_score = min(penalty_score, 100)

    if risk_score == 0:
        integrity_status = "CLEAN"
        advisory = "No behavioral anomalies detected."
    elif risk_score <= 30:
        integrity_status = "WARNING"
        advisory = "Minor anomaly recorded. Approved with logged flag."
    else:
        integrity_status = "MALPRACTICE_FLAGGED"
        advisory = "Serious infraction detected. Withhold marks for committee review."

    return {
        "status": integrity_status,
        "risk_score": risk_score,
        "infractions_count": len(infractions),
        "details": infractions,
        "advisory": advisory
    }
