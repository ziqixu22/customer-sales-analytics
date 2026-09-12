# E-commerce Product Analytics & Experimentation Platform

A reproducible Product Data Science portfolio project built around two public datasets:

- **UCI Online Retail II** for real transaction-level product analytics, customer cohorts, retention, revenue, and cancellation behavior.
- **Criteo Uplift** for randomized incrementality experiments with treatment assignment and conversion/visit outcomes.

The project mirrors an industry Product Data Scientist workflow:

`raw transactions -> validated analytics tables -> SQL product metrics -> cohort/retention analysis -> experiment QA -> treatment-effect estimation -> heterogeneous-effect analysis -> business recommendation`

## Business questions

### Product analytics
- How much revenue is generated and how does it change over time?
- What share of orders are cancellations/returns?
- Which countries, products, and customers drive revenue concentration?
- How do customer cohorts retain and generate revenue over time?
- How do repeat-purchase behavior and order frequency evolve?

### Experimentation
- Is treatment allocation balanced?
- What are treatment effects on visit and conversion?
- What are absolute lift, relative lift, confidence intervals, and statistical significance?
- How large would a future experiment need to be?
- Does treatment impact vary across user segments/features?
- Would the result justify launch, targeted rollout, or another experiment?

## Why two datasets?

Online Retail II is observational commerce data and is excellent for product-health analysis, but it has no randomized treatment assignment. Criteo Uplift contains real randomized incrementality-test data but anonymizes product context. Keeping these workstreams separate avoids pretending observational differences are causal.

## Architecture

```text
UCI Online Retail II                    Criteo Uplift
        |                                    |
        v                                    v
transaction validation                 experiment QA
        |                                    |
        v                                    v
DuckDB analytics layer                 ATE / confidence intervals
        |                                    |
        v                                    v
SQL marts: revenue, cohort,            regression adjustment
retention, repeat purchase                  |
        |                                    v
        |                               heterogeneous effects
        \____________________________________/
                         |
                         v
                 decision-oriented README
```

## Repository structure

```text
.
├── README.md
├── pyproject.toml
├── scripts/
│   └── download_data.py
├── sql/
│   ├── product_metrics.sql
│   └── cohort_retention.sql
├── src/product_ds/
│   ├── data.py
│   ├── metrics.py
│   ├── experiment.py
│   └── run_experiment.py
├── tests/
│   ├── test_metrics.py
│   └── test_experiment.py
└── docs/
    ├── architecture.md
    └── interview_guide.md
```

## Data sources

### UCI Online Retail II
Source: UCI Machine Learning Repository, dataset ID 502.

The dataset contains two years of transactions from a UK-based non-store online retailer. Typical fields include:

- Invoice
- StockCode
- Description
- Quantity
- InvoiceDate
- Price
- Customer ID
- Country

The project derives revenue, cancellations, repeat purchases, cohort month, and retention from these raw transactions.

### Criteo Uplift
Source: Hugging Face dataset `criteo/criteo-uplift`.

Expected columns include anonymized features `f0`-`f11`, `treatment`, `conversion`, `visit`, and `exposure`.

Raw data is intentionally not committed to Git.

## Core methods

**SQL / analytics**
- CTEs and window functions
- monthly revenue and order volume
- cancellation rate
- repeat-purchase rate
- cohort assignment and retention matrix
- customer revenue concentration

**Experimentation / statistics**
- sample-ratio-mismatch checks
- two-sample proportion tests
- absolute and relative lift
- confidence intervals
- power / minimum sample size
- regression-adjusted treatment effect
- segment-level treatment-effect analysis

## Testing

The statistical core is unit tested. The current test suite verifies treatment-effect direction, sample-size calculation, sample-ratio checks, and product-metric logic.

Run:

```bash
PYTHONPATH=src pytest -q
```

## Reproducibility

The code never silently generates synthetic data when a public source is unavailable. Data-download scripts point to the original sources, and all derived metrics are computed from downloaded raw files.

## Resume-safe description

Before running full raw data, the project can truthfully be described as:

> Built a reproducible e-commerce product analytics and experimentation platform using real retail transactions and randomized incrementality-test data, with SQL cohort/retention analysis and Python treatment-effect estimation.

After running the full pipeline, replace generic wording with verified row counts, retention values, lift estimates, confidence intervals, and runtimes.

## Why this is not a toy project

The project separates observational analytics from randomized causal measurement, uses reproducible public data, modular code and tests rather than notebook-only analysis, explicitly checks experimental validity, and is designed around business decisions rather than a single model score.