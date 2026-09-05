# Data Product Strategy

The `productStrategy` object captures the business intent behind a data product and links it to a **single higher-level business KPI** it is primarily accountable for. It defines the objectives, the primary KPI at the business level, and the **product-level KPIs** that measure its direct contribution.

Optionally, it can also include **related KPIs** — secondary or cross-unit measures that:

1. **Capture additional value** — show extra benefits beyond the main KPI, useful for demonstrating broader impact.
2. **Track side effects** — monitor unintended positive or negative impacts on other KPIs.
3. **Highlight cross-department value** — reveal benefits for other business units, strengthening prioritization and funding cases.

Beyond KPIs, `productStrategy` can include:

- **objectives** — natural-language statements describing the business outcomes the product supports.
- **strategicAlignment** — references to corporate initiatives, programs, or policy documents that the product contributes to (e.g., Smart City Vision 2030).

By embedding both primary and related KPI connections directly into the product specification, `productStrategy` ensures that data products remain technically sound, strategically aligned, and transparent in how they deliver value.

## Attributes and options

> Example of catalog object usage:

```yml
schema: https://opendataproducts.org/v4.1/schema/odps.yaml
# JSON schema: https://opendataproducts.org/v4.1/schema/odps.json
version: 4.1
product:
  productStrategy:
    status: Planned
    startDate: 2026-01-12
    endDate: 2026-06-30
    objectives:
      - en: Reduce emergency response time
    strategicAlignment:
      - en: Smart City Vision 2030
    contributesToKPI:
      id: bizkpi-city-response-time
      name: City Emergency Response Time
      description: Average minutes from incident to first responder arrival
      unit: minutes
      target: 5
      direction: at_most
      timeframe: "by Q4"
    relatedKPIs:
      - id: bizkpi-traffic-congestion
        name: Traffic Congestion Index
        unit: percentage
        target: -10
        direction: decrease
    productKPIs:
      - id: kpi-detection-coverage
        name: Event Detection Coverage
        description: '% of reported incidents captured in real time'
        unit: percentage
        target: 95
        direction: at_least
        frequency: hourly
        calculation: detected_events / reported_events

      - id: kpi-time-to-insight
        name: Average Time to Insight
        description: Median time from event occurrence to product update
        unit: seconds
        target: 60
        direction: at_most
        calculation: p50(update_ts - event_ts)

```

| Element | Type | Options | Description |
|---|---|---|---|
| **productStrategy** | object | – | Top‑level block that connects the data product to business goals and KPIs. |
| **objectives** | array of objects | language‑tagged strings | Business objectives the product supports, written in natural language. |
| **contributesToKPI** | object | required | **Single higher‑level business KPI** (from SMART objectives) that this product is accountable for. |
| **id** | string | optional | Identifier of the business KPI (use shared IDs for roll‑ups). |
| **name** | string | required | KPI name. |
| **status** | string | One of: Planned, Active, At Risk, Achieved, Partially Achieved, Cancelled, Expired | Indicates the status of the strategy object. Consider this similar to data product lifecycle status. |
| **startDate** | string (date) | ISO 8601 date (YYYY-MM-DD) | Indicates when the product strategy becomes active. Used for timeline and Gantt chart visualizations. |
| **endDate**   | string (date) | ISO 8601 date (YYYY-MM-DD) | Indicates when the product strategy ends or is planned to end. Used for timeline and Gantt chart visualizations. |
| **description** | string | optional | Human‑readable description. |
| **unit** | string | e.g., `percentage`, `minutes`, `s` | Unit of measurement. |
| **target** | number/string | – | Target value for the KPI. |
| **direction** | enum | `increase`, `decrease`, `at_least`, `at_most`, `equals` | Desired direction of movement. |
| **timeframe** | string | optional | When the target should be met. |
| **frequency** | string | Measurement cadence (e.g., hourly, daily, monthly). |
| **owner** | string | Responsible role/team (optional). |
| **calculation** | string | Human‑readable formula (optional). |
| **productKPIs** | array | optional | KPIs measured **at product level** that influence `contributesToKPI`. Useful for contribution analysis and governance checks. |
| **relatedKPIs** | array | optional | Secondary/cross‑unit KPIs to monitor side‑effects and additional value (informational; not for prioritization). |
| **strategicAlignment** | array | language‑tagged strings | Strategic initiatives, policies, or visions the product aligns with. |


### Governance‑by‑Design checks (Minimum Lovable Gates)

- **Required:** `contributesToKPI.name` present.  
- **Recommended:** ≥1 `productKPIs` with `unit`, `target`, and `calculation`.  
- **Optional:** `relatedKPIs` for secondary/side effects.  
- **Traceability:** use shared KPI `id`s to enable cross‑product roll‑ups against the same business KPI.
