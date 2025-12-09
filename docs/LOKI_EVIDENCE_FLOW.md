# How Loki Logs Populate Grafana Dashboards with Evidence

## Overview

This document explains how compliance evidence flows through the system to populate Grafana dashboards via Loki logs.

## Data Flow Architecture

```
Evidence (OCSF/Gemara JSON) 
  → OpenTelemetry Collector (OTLP/Webhook Receiver)
  → Transform Processor (extracts attributes from JSON)
  → Truthbeam Processor (enriches with compliance data from Compass)
  → Loki (via OTLP HTTP exporter)
  → Grafana Dashboards (queries via LogQL)
```

## Step-by-Step Flow

### 1. Evidence Input

Evidence can be sent to the collector in two formats:

#### OCSF Format (Current Sample)
- Location: `hack/sampledata/evidence.json`
- Format: OCSF (Open Cybersecurity Schema Framework) ScanActivity
- Required fields:
  - `policy.uid` - Policy rule identifier
  - `metadata.product.name` - Policy engine name
  - `status` - Evaluation result ("success", "failure", "not_run", etc.)

#### Gemara Format
- Format: Gemara Layer 4 AssessmentLog
- Required fields:
  - `procedure.entry_id` - Policy rule identifier
  - `author.name` - Policy engine name
  - `result` - Evaluation result (Passed, Failed, etc.)

### 2. OpenTelemetry Collector Processing

The collector (`hack/demo/demo-config.yaml`) processes evidence through this pipeline:

#### Receivers
- **OTLP Receiver** (port 4317): Accepts OpenTelemetry Protocol logs
- **Webhook Receiver** (port 8088): Accepts HTTP POST requests at `/eventsource/receiver`

#### Processors

**Transform Processor (`transform/ocsf`):**
- Extracts attributes from JSON body:
  - `policy.rule.id` ← `policy.uid`
  - `policy.engine.name` ← `metadata.product.name`
  - `policy.evaluation.result` ← `status` (mapped to: Passed/Failed/Not Run/Needs Review/Not Applicable/Unknown)

**Truthbeam Processor:**
- Enriches logs with compliance context from Compass service
- Adds attributes like:
  - `compliance.control.id`
  - `compliance.control.category`
  - `compliance.frameworks`
  - `compliance.requirements`
  - `compliance.enrichment.status`

#### Exporter
- **OTLP HTTP Exporter**: Sends logs to Loki at `http://loki:3100/otlp`

### 3. Loki Label Mapping

Loki's OTLP receiver automatically converts OpenTelemetry attributes to labels:

**Attribute Name → Loki Label:**
- `policy.engine.name` → `policy_engine_name`
- `policy.evaluation.result` → `policy_evaluation_result`
- `policy.rule.id` → `policy_rule_id`
- Resource attributes (like `service.name`) → `service_name`

**Note:** Dots in OpenTelemetry attribute names are converted to underscores in Loki labels.

### 4. Grafana Dashboard Queries

The dashboard (`hack/demo/grafana/dashboards/compliance-evidence.json`) uses LogQL queries:

**Example Queries:**
```logql
# Total evidence count
sum(count_over_time({service_name=~".+"} [$__range]))

# Group by evaluation result
sum by (policy_evaluation_result) (count_over_time({service_name=~".+"} [$__range]))

# Group by policy engine
sum by (policy_engine_name) (count_over_time({service_name=~".+"} [$__range]))

# Group by policy rule
sum by (policy_rule_id) (count_over_time({service_name=~".+"} [$__range]))

# Raw logs with JSON parsing
{service_name=~".+"} | json | line_format "{{.policy_rule_id}}|{{.policy_engine_name}}|{{.policy_evaluation_result}}|{{.status}}|{{.severity}}"
```

## Dashboard Panels

The dashboard includes:

1. **Total Evidence Records** - Count of all evidence in time range
2. **Policy Evaluation Results** - Pie chart showing Passed/Failed/Unknown distribution
3. **Evaluation Results Summary** - Table with counts per result type
4. **Evaluation of Control Status Over Time** - Time series showing trends
5. **Policy Engine Usage** - Distribution of evidence by policy engine
6. **Policy Rule Evidence Representation** - Distribution by policy rule ID
7. **Recent Evidence Records** - Table of recent evidence with parsed fields
8. **Evidence Logs (Raw)** - Raw log viewer showing full JSON

## Testing with More Evidence

### Method 1: Send Evidence via HTTP Webhook

Send POST requests to the collector's webhook endpoint:

```bash
curl -X POST http://localhost:8088/eventsource/receiver \
  -H "Content-Type: application/json" \
  -d @hack/sampledata/evidence.json
```

### Method 2: Send Evidence via OTLP

Use an OpenTelemetry client to send logs via OTLP (gRPC port 4317 or HTTP port 4318).

### Method 3: Create Multiple Evidence Files

Create additional evidence files with different:
- Policy engines (`metadata.product.name`)
- Policy rules (`policy.uid`)
- Evaluation results (`status`: "success", "failure", "not_run", "needs_review", "not_applicable")
- Timestamps (spread across time for time-series visualization)

### Sample Evidence Variations

See `hack/sampledata/evidence.json` for the base format. Key fields to vary:

```json
{
  "metadata": {
    "product": {
      "name": "conforma"  // Change to: "opa", "kyverno", "gatekeeper", etc.
    }
  },
  "policy": {
    "uid": "github_branch_protection"  // Change to different rule IDs
  },
  "status": "failure"  // Change to: "success", "not_run", "needs_review", etc.
}
```

## Troubleshooting

### Evidence Not Appearing in Dashboard

1. **Check Collector Logs:**
   ```bash
   docker compose logs collector
   ```

2. **Check Loki Logs:**
   ```bash
   docker compose logs loki
   ```

3. **Verify Evidence Format:**
   - Ensure required fields are present
   - Check JSON is valid
   - Verify status values match expected mappings

4. **Check Label Names:**
   - Loki labels use underscores, not dots
   - Query using `policy_engine_name` not `policy.engine.name`

5. **Time Range:**
   - Ensure evidence timestamps are within Grafana's time range
   - Default dashboard shows last 6 hours

### Labels Not Appearing

- Ensure attributes are set as log record attributes (not resource attributes)
- Check that the transform processor is extracting attributes correctly
- Verify the OTLP exporter is configured correctly

## Configuration Files

- **Collector Config**: `hack/demo/demo-config.yaml`
- **Loki Config**: `hack/demo/loki-config.yaml`
- **Grafana Dashboard**: `hack/demo/grafana/dashboards/compliance-evidence.json`
- **Docker Compose**: `compose.yaml`

