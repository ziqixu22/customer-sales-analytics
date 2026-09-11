# Customer Sales Analytics Dashboard

An interactive Tableau business-intelligence project that converts transaction-level retail data into a decision-oriented view of revenue, customer segments, geography, demographics, discounts, and purchasing behavior.

## 1. Business Goal

The practical question is:

> How can transaction-level sales data be summarized so that a business user can quickly understand where revenue comes from, which customer segments matter, and how purchasing patterns vary across time and geography?

The dashboard is designed to support exploratory business analysis rather than statistical prediction. It emphasizes interpretable KPIs and segment comparisons that can be used to identify revenue concentration, customer patterns, and possible areas for deeper investigation.

## 2. Data

The Tableau workbook connects to a transaction-level dataset containing fields such as:

- order ID and order date
- order status
- SKU / item ID
- quantity ordered
- unit price and transaction value
- discount amount and discount percentage
- total revenue
- product category
- payment method
- customer ID
- age and gender
- city, county, state, ZIP code, and region
- customer tenure fields

The workbook schema also contains identifying fields that are not analytically necessary for the portfolio presentation. The analysis therefore focuses on aggregated business metrics rather than exposing person-level information.

## 3. Data Preparation and Feature Engineering

### Age Binning

The Tableau workbook creates 10-year age bins and labels ranges such as `<20`, `20-30`, `30-40`, and so on.

Conceptually, for customer age $a_i$, the segment assignment is

$$
B(a_i)=\left\lfloor\frac{a_i}{10}\right\rfloor.
$$

Binning is useful here because comparing every exact age would create a noisy visualization; grouped ranges make demographic differences easier to interpret.

### Gender-Specific Revenue

The workbook defines calculated fields equivalent to

$$
R_i^{(F)}=
\begin{cases}
\text{Total}_i,&\text{Gender}_i=F,\\
0,&\text{otherwise},
\end{cases}
$$

and

$$
R_i^{(M)}=
\begin{cases}
\text{Total}_i,&\text{Gender}_i=M,\\
0,&\text{otherwise}.
\end{cases}
$$

This allows male and female revenue to be compared across product categories in a common view.

## 4. Core KPI Definitions

### Total Revenue

For transaction-level totals $T_i$,

$$
R_{\text{total}}=\sum_{i=1}^{N}T_i.
$$

This is the headline measure shown in the dashboard.

### Monthly Revenue

For month $m$,

$$
R_m=\sum_{i:\,\text{month}(i)=m}T_i.
$$

The workbook includes a `Month-Wise Revenue` view so that seasonality and revenue changes over time can be inspected visually.

### Segment Revenue

For any segment $g$—for example category, region, state, age group, or gender—

$$
R_g=\sum_{i\in g}T_i.
$$

### Revenue Share

A segment's contribution to overall revenue can be interpreted as

$$
\text{RevenueShare}_g=
\frac{R_g}{\sum_h R_h}.
$$

This is useful because absolute revenue and relative importance answer different questions: a large segment may lead in dollars but still be shrinking in share.

## 5. Dashboard Views

The workbook contains several named analyses, including:

- **Total Revenue** — top-line KPI
- **Month-Wise Revenue** — revenue trend over time
- **Age-Wise Sales Analysis** — revenue patterns across age bands
- **Gender-Wise Sales Analysis** — gender-level comparison by category
- **Quantity - Discount Correlation** — relationship between quantity ordered and discount percentage
- **Region-Wise Revenue Share (%)** — contribution of geographic regions
- **Revenue per State** — geographic map view

## 6. Why These Methods Fit the Problem

This is a BI problem, not a supervised-learning problem. A predictive model would answer a different question such as "what will a customer buy next?" or "what will future revenue be?" The goal here is descriptive and diagnostic:

- aggregate raw transactions into interpretable KPIs
- segment revenue by business-relevant dimensions
- expose temporal and geographic structure
- allow interactive filtering rather than force one fixed statistical model

Tableau is therefore appropriate because the main deliverable is a reusable exploratory interface for non-technical stakeholders.

## 7. Analytical Checks / Evaluation

There is no train/test RMSE or classification accuracy because the project does not fit a predictive model. Instead, dashboard quality should be evaluated through KPI consistency and reconciliation.

Useful checks include:

$$
R_{\text{total}}=\sum_m R_m,
$$

and, for mutually exclusive segment groups,

$$
R_{\text{total}}=\sum_g R_g.
$$

Revenue shares should satisfy

$$
0\le \text{RevenueShare}_g\le1,
\qquad
\sum_g\text{RevenueShare}_g=1.
$$

The geographic, demographic, and time-based views should all reconcile to the same filtered transaction population.

## 8. Results and Interpretation

The workbook verifies that the project was implemented as a multi-view customer and sales dashboard and that it includes dedicated analyses for revenue, age, gender, region, state, month, and the relationship between discount percentage and quantity ordered.

The repository does not currently contain a plain-text export of the final dashboard KPI values, so this README intentionally does not invent exact revenue totals or segment percentages. The interactive Tableau workbook should be treated as the source of truth for those displayed values.

The main analytical takeaway is that transaction data becomes more useful when decomposed into three complementary perspectives:

1. **How much?** — total and monthly revenue
2. **Who / what contributes?** — demographic, category, and regional segmentation
3. **What relationships deserve deeper analysis?** — e.g. quantity ordered versus discount percentage

## 9. Repository Contents

```text
.
├── README.md
├── CustomerAnalysis.twb
└── sales_06_FY2020-21.csv.zip
```

## 10. Tableau Dashboard

[View the interactive Tableau dashboard](https://public.tableau.com/views/Wisesalescustomeranalysis/CustomerAnalysis?:language=zh-CN&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## 11. Tools & Skills

Tableau · Business Intelligence · KPI Design · Customer Segmentation · Sales Analytics · Geographic Visualization · Exploratory Data Analysis · Data Storytelling

## 12. Limitations

- This is descriptive analytics, not causal analysis.
- Segment differences should not be interpreted as causal effects of demographic or geographic variables.
- The workbook contains a local source-file path in its metadata; Tableau Public is the most portable way to review the completed dashboard.
- Exact KPI values are not duplicated in text here unless they can be verified directly from repository artifacts.