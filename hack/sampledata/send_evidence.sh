#!/bin/bash
# Send all evidence JSON files to the collector

COLLECTOR_URL="${COLLECTOR_URL:-http://localhost:8088/eventsource/receiver}"
EVIDENCE_DIR="${EVIDENCE_DIR:-$(dirname "$0")}"

echo "Sending evidence files to ${COLLECTOR_URL}..."
echo ""

count=0
failed=0

for file in "${EVIDENCE_DIR}"/evidence-*.json; do
  if [ -f "$file" ]; then
    filename=$(basename "$file")
    if curl -s -X POST "${COLLECTOR_URL}" \
      -H "Content-Type: application/json" \
      -d @"${file}" > /dev/null; then
      echo "✓ Sent: ${filename}"
      ((count++))
    else
      echo "✗ Failed: ${filename}"
      ((failed++))
    fi
    sleep 0.1
  fi
done

echo ""
echo "Summary: ${count} sent successfully"
if [ $failed -gt 0 ]; then
  echo "         ${failed} failed"
fi
echo ""
echo "Check Grafana dashboard at http://localhost:3000"

