#!/usr/bin/env python3
"""
Generate multiple evidence records for testing Grafana dashboards.

Usage:
    python generate_evidence.py --count 20 --output-dir ./evidence_samples
    python generate_evidence.py --send --count 10 --url http://localhost:8088/eventsource/receiver
"""

import argparse
import json
import random
import time
from datetime import datetime, timedelta
from pathlib import Path
import requests


# Policy engines to test
POLICY_ENGINES = ["conforma", "opa", "kyverno", "gatekeeper", "falco", "checkov", "tfsec"]

# Policy rules to test
POLICY_RULES = [
    "github_branch_protection",
    "require_signed_commits",
    "enforce_mfa",
    "scan_on_push",
    "no_secrets_in_code",
    "require_code_review",
    "enforce_security_scan",
    "block_force_push",
    "require_status_checks",
    "enforce_branch_naming"
]

# Status values and their mappings
STATUSES = ["success", "failure", "not_run", "needs_review", "not_applicable", "unknown"]

# Severity levels
SEVERITIES = ["low", "medium", "high", "critical", "unknown"]


def generate_evidence(
    engine: str,
    rule: str,
    status: str,
    timestamp: int,
    severity: str = "unknown",
    evidence_id: int = 1
) -> dict:
    """Generate a single evidence record in OCSF format."""
    return {
        "activity_id": 0,
        "activity_name": "",
        "category_name": "Application Activity",
        "category_uid": 6,
        "class_name": "Scan Activity",
        "class_uid": 6007,
        "cloud": {
            "provider": ""
        },
        "event_day": 0,
        "metadata": {
            "log_provider": engine,
            "product": {
                "name": engine,
                "vendor_name": engine,
                "version": "v0.8.6"
            },
            "uid": f"test-evidence-{evidence_id}",
            "version": "v0.8.6"
        },
        "num_files": 1,
        "observables": [
            {
                "name": "evidence.json",
                "type": "File Name",
                "type_id": 7
            }
        ],
        "osint": None,
        "scan": {
            "type_id": 0
        },
        "severity": severity,
        "severity_id": 0,
        "status": status,
        "status_id": 2 if status == "failure" else 1,
        "time": timestamp,
        "type_name": "",
        "type_uid": 60070,
        "policy": {
            "data": json.dumps({
                "name": f"Test Policy {evidence_id}",
                "description": f"Generated test policy for {rule}",
                "sources": [{
                    "name": f"OSPS-QA-{random.randint(1, 20):02d}.{random.randint(1, 10):02d}",
                    "policy": [f"github.com/test/policy"],
                    "ruleData": {},
                    "config": {
                        "include": [rule]
                    }
                }]
            }),
            "desc": f"Generated test policy for {rule}",
            "name": f"Test Policy {evidence_id}",
            "uid": rule
        },
        "action": "observed",
        "action_id": 3
    }


def generate_timestamp(hours_ago: int = None) -> int:
    """Generate a timestamp in milliseconds."""
    if hours_ago is None:
        hours_ago = random.randint(0, 6)
    minutes_ago = random.randint(0, 59)
    dt = datetime.now() - timedelta(hours=hours_ago, minutes=minutes_ago)
    return int(dt.timestamp() * 1000)


def main():
    parser = argparse.ArgumentParser(description="Generate evidence records for testing")
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of evidence records to generate (default: 10)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./evidence_samples",
        help="Directory to save evidence files (default: ./evidence_samples)"
    )
    parser.add_argument(
        "--send",
        action="store_true",
        help="Send evidence directly to collector instead of saving to files"
    )
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8088/eventsource/receiver",
        help="Collector webhook URL (default: http://localhost:8088/eventsource/receiver)"
    )
    parser.add_argument(
        "--spread-hours",
        type=int,
        default=6,
        help="Spread evidence over last N hours (default: 6)"
    )
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    if not args.send:
        output_dir.mkdir(exist_ok=True)
    
    print(f"Generating {args.count} evidence records...")
    print(f"Policy engines: {', '.join(POLICY_ENGINES)}")
    print(f"Policy rules: {', '.join(POLICY_RULES[:5])}...")
    print(f"Statuses: {', '.join(STATUSES)}")
    print()
    
    sent_count = 0
    failed_count = 0
    
    for i in range(1, args.count + 1):
        # Randomly select values
        engine = random.choice(POLICY_ENGINES)
        rule = random.choice(POLICY_RULES)
        status = random.choice(STATUSES)
        severity = random.choice(SEVERITIES)
        
        # Generate timestamp spread over specified hours
        hours_ago = random.randint(0, args.spread_hours)
        timestamp = generate_timestamp(hours_ago)
        
        evidence = generate_evidence(engine, rule, status, timestamp, severity, i)
        
        if args.send:
            try:
                response = requests.post(
                    args.url,
                    json=evidence,
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                response.raise_for_status()
                sent_count += 1
                print(f"✓ Sent evidence {i}/{args.count}: engine={engine}, rule={rule}, status={status}")
            except Exception as e:
                failed_count += 1
                print(f"✗ Failed to send evidence {i}: {e}")
        else:
            # Save to file
            filename = output_dir / f"evidence_{i:04d}.json"
            with open(filename, 'w') as f:
                json.dump(evidence, f, indent=2)
            print(f"✓ Generated evidence {i}/{args.count}: {filename.name}")
    
    print()
    if args.send:
        print(f"Summary: {sent_count} sent successfully, {failed_count} failed")
        print(f"Check Grafana dashboard at http://localhost:3000")
        print(f"Default time range: last {args.spread_hours} hours")
    else:
        print(f"Generated {args.count} evidence files in {output_dir}")
        print(f"To send them to the collector, use:")
        print(f"  for f in {output_dir}/*.json; do curl -X POST {args.url} -H 'Content-Type: application/json' -d @$f; done")


if __name__ == "__main__":
    main()

