# Sample Evidence Data

This directory contains sample evidence data and tools for testing the compliance evidence dashboard.

## Files

- `evidence.json` - Base OCSF format evidence example
- `evidence-01.json` through `evidence-10.json` - Pre-generated test evidence with different variations
- `osps.yaml` - OSPS (Open Security Policy Standard) catalog configuration
- `evaluations/plan.yml` - Evaluation plan configuration

## Quick Start: Send Test Evidence

### Send All Evidence Files

**Using the send script:**
```bash
# Send all evidence-*.json files to the collector
./send_evidence.sh

# Or specify a custom collector URL
COLLECTOR_URL=http://localhost:8088/eventsource/receiver ./send_evidence.sh
```

**Send files manually:**
```bash
# Send a single file
curl -X POST http://localhost:8088/eventsource/receiver \
  -H "Content-Type: application/json" \
  -d @evidence-01.json

# Send all evidence files
for f in evidence-*.json; do
  curl -X POST http://localhost:8088/eventsource/receiver \
    -H "Content-Type: application/json" \
    -d @"$f"
  sleep 0.1
done
```

## Evidence File Variations

The pre-generated evidence files (`evidence-01.json` through `evidence-10.json`) include:

- **Different Policy Engines**: conforma, opa, kyverno, gatekeeper, falco, checkov
- **Different Policy Rules**: github_branch_protection, require_signed_commits, enforce_mfa, scan_on_push, no_secrets_in_code, etc.
- **Different Statuses**: success, failure, not_run, needs_review, not_applicable
- **Different Timestamps**: Spread over the last few hours for time-series visualization
- **Different Severities**: low, medium, high, critical

### Manual Evidence Creation

You can create custom evidence files following the OCSF format. Key fields:

```json
{
  "metadata": {
    "product": {
      "name": "conforma"  // Policy engine name (becomes policy_engine_name label)
    }
  },
  "policy": {
    "uid": "github_branch_protection"  // Policy rule ID (becomes policy_rule_id label)
  },
  "status": "success"  // Evaluation result: "success", "failure", "not_run", "needs_review", "not_applicable"
}
```

### Sending Evidence Manually

**Via HTTP Webhook:**
```bash
curl -X POST http://localhost:8088/eventsource/receiver \
  -H "Content-Type: application/json" \
  -d @evidence.json
```

**Send multiple files:**
```bash
for f in evidence_samples/*.json; do
  curl -X POST http://localhost:8088/eventsource/receiver \
    -H "Content-Type: application/json" \
    -d @"$f"
  sleep 0.1
done
```

## Evidence Status Mapping

The collector's transform processor maps OCSF status values to Compass evaluation results:

| OCSF Status | Compass Result | Color in Dashboard |
|------------|----------------|-------------------|
| `success` | `Passed` | Green |
| `failure` | `Failed` | Red |
| `not_run` | `Not Run` | Blue |
| `needs_review` | `Needs Review` | Yellow |
| `not_applicable` | `Not Applicable` | Gray |
| `unknown`, `error`, `timeout` | `Unknown` | Orange |

## Testing Different Scenarios

### Test Different Policy Engines
The pre-generated files include multiple engines. To add more, create new JSON files following the same format and change `metadata.product.name`.

### Test Different Time Ranges
The evidence files have timestamps spread over time. To test different ranges, modify the `time` field (milliseconds since epoch) in the JSON files.

### Test Different Evaluation Results
The evidence files include all status values. To test specific results, modify the `status` field in the JSON files:
- `"success"` → Passed (green)
- `"failure"` → Failed (red)
- `"not_run"` → Not Run (blue)
- `"needs_review"` → Needs Review (yellow)
- `"not_applicable"` → Not Applicable (gray)

## Viewing Results

1. **Access Grafana**: http://localhost:3000
2. **Navigate to Dashboard**: Compliance Evidence Dashboard
3. **Adjust Time Range**: Use the time picker (default: last 6 hours)
4. **Refresh**: Click refresh or wait for auto-refresh

## Troubleshooting

### Evidence Not Appearing

1. **Check collector is running:**
   ```bash
   docker compose ps collector
   docker compose logs collector
   ```

2. **Verify evidence format:**
   - Check JSON is valid
   - Ensure required fields are present
   - Verify status values match expected mappings

3. **Check time range:**
   - Evidence timestamps must be within Grafana's selected time range
   - Default dashboard shows last 6 hours

4. **Check Loki:**
   ```bash
   docker compose logs loki
   ```

### Labels Not Appearing in Queries

- Loki converts OpenTelemetry attribute dots to underscores
- Use `policy_engine_name` not `policy.engine.name` in LogQL queries
- Ensure attributes are set as log record attributes (not resource attributes)

## Example Evidence Variations

See `evidence.json` or any `evidence-*.json` file for the format. To create new evidence files:

1. **Copy an existing file:**
   ```bash
   cp evidence-01.json evidence-11.json
   ```

2. **Edit the new file and change:**
   - `metadata.product.name` - Policy engine name (e.g., "opa", "kyverno", "gatekeeper")
   - `metadata.uid` - Unique identifier for this evidence
   - `policy.uid` - Policy rule identifier (e.g., "github_branch_protection")
   - `status` - Evaluation result ("success", "failure", "not_run", "needs_review", "not_applicable")
   - `severity` - Severity level ("low", "medium", "high", "critical", "unknown")
   - `time` - Timestamp in milliseconds since epoch (use `date +%s%3N` to get current time)

3. **Send the new file:**
   ```bash
   curl -X POST http://localhost:8088/eventsource/receiver \
     -H "Content-Type: application/json" \
     -d @evidence-11.json
   ```

