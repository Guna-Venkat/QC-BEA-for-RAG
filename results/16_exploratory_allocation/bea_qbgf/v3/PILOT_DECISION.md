# BEA-QBGF pilot decision

POST_W12_EXPLORATORY; not confirmation.

```json
{
  "label": "POST_W12_EXPLORATORY",
  "decision": "PROMISING",
  "conditions": {
    "not_clearly_degraded_in_most_cells": true,
    "meaningful_dimension_present": true,
    "different_from_fixed": true,
    "escalation_active": true,
    "not_degenerate_empty": true
  },
  "clearly_degraded_cells": [
    [
      "QASPER",
      256
    ],
    [
      "QASPER",
      1024
    ]
  ],
  "meaningful_dimensions": [
    {
      "dataset": "SciFact",
      "budget": 1024,
      "dimension": "efficiency/coverage/redundancy",
      "comparator": "FIXED_SENTENCE",
      "token_reduction": 0.31809542470853336,
      "redundancy_reduction": 0.08405074373557164,
      "coverage_change": -0.015372023511552091,
      "note": "quality point estimates competitive; not proven statistical noninferiority"
    },
    {
      "dataset": "SciFact",
      "budget": 1024,
      "dimension": "efficiency/coverage/redundancy",
      "comparator": "QBGF_FULL",
      "token_reduction": 0.31677006439453437,
      "redundancy_reduction": 0.04009281454090119,
      "coverage_change": -0.009585728308041719,
      "note": "quality point estimates competitive; not proven statistical noninferiority"
    }
  ],
  "different_context_fraction": 1.0,
  "upgrade_cell_fraction": 0.11333333333333333,
  "empty_cell_fraction": 0.0,
  "interpretation": "Global preregistered exploratory gate; no dataset-specific promotion, no proof of noninferiority, no final-method replacement"
}
```

Expansion requires both PROMISING and a separate manual notebook flag. No final W12 method changes.
