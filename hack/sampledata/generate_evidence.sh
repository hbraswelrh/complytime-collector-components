#!/bin/bash
# Generate multiple evidence records for testing Grafana dashboards

# Configuration
COLLECTOR_URL="${COLLECTOR_URL:-http://localhost:8088/eventsource/receiver}"
NUM_RECORDS="${NUM_RECORDS:-10}"
BASE_TIME=$(date +%s)000  # Current time in milliseconds

# Policy engines to test
POLICY_ENGINES=("conforma" "opa" "kyverno" "gatekeeper" "falco")

# Policy rules to test
POLICY_RULES=("github_branch_protection" "require_signed_commits" "enforce_mfa" "scan_on_push" "no_secrets_in_code")

# Status values to test
STATUSES=("success" "failure" "not_run" "needs_review" "not_applicable")

# Generate and send evidence records
for i in $(seq 1 $NUM_RECORDS); do
  # Randomly select values
  ENGINE=${POLICY_ENGINES[$RANDOM % ${#POLICY_ENGINES[@]}]}
  RULE=${POLICY_RULES[$RANDOM % ${#POLICY_RULES[@]}]}
  STATUS=${STATUSES[$RANDOM % ${#STATUSES[@]}]}
  
  # Generate timestamp (spread over last 6 hours for time-series visualization)
  HOURS_AGO=$((RANDOM % 6))
  MINUTES_AGO=$((RANDOM % 60))
  TIMESTAMP=$((BASE_TIME - (HOURS_AGO * 3600 * 1000) - (MINUTES_AGO * 60 * 1000)))
  
  # Create evidence JSON
  EVIDENCE=$(cat <<EOF
{
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
    "log_provider": "${ENGINE}",
    "product": {
      "name": "${ENGINE}",
      "vendor_name": "${ENGINE}",
      "version": "v0.8.6"
    },
    "uid": "test-evidence-${i}",
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
  "osint": null,
  "scan": {
    "type_id": 0
  },
  "severity": "unknown",
  "severity_id": 0,
  "status": "${STATUS}",
  "status_id": 2,
  "time": ${TIMESTAMP},
  "type_name": "",
  "type_uid": 60070,
  "policy": {
    "data": "{\"name\":\"Test Policy ${i}\",\"description\":\"Generated test policy\",\"sources\":[{\"name\":\"OSPS-QA-07.01\",\"policy\":[\"github.com/test/policy\"],\"ruleData\":{},\"config\":{\"include\":[\"${RULE}\"]}}]}",
    "desc": "Generated test policy",
    "name": "Test Policy ${i}",
    "uid": "${RULE}"
  },
  "action": "observed",
  "action_id": 3
}
EOF
)
  
  echo "Sending evidence ${i}/${NUM_RECORDS}: engine=${ENGINE}, rule=${RULE}, status=${STATUS}"
  
  # Send to collector
  curl -s -X POST "${COLLECTOR_URL}" \
    -H "Content-Type: application/json" \
    -d "${EVIDENCE}" > /dev/null
  
  # Small delay to avoid overwhelming the collector
  sleep 0.1
done

echo ""
echo "Sent ${NUM_RECORDS} evidence records to ${COLLECTOR_URL}"
echo "Check Grafana dashboard at http://localhost:3000 (default time range: last 6 hours)"

