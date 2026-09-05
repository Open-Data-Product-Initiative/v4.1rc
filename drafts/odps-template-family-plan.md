# ODPS Template Family Plan

## Purpose

ODPS v4.1 is broad enough to describe many kinds of data products. A single full-schema example is too large for adoption. A small set of applied templates helps users start from the right pattern without learning the full schema first.

This plan defines an ODPS template family that can be added to the ODPS specification, documentation, examples, and SDK tooling.

The templates should be treated as application skeletons. They do not require new schema fields. They reuse the existing ODPS v4.1 schema areas.

## Design principles

1. Avoid maturity labels such as Bronze, Silver, Gold.
   These names imply quality tiers but do not explain the purpose of the template.

2. Avoid the word Dataset in template names.
   It pulls users back to legacy catalog thinking. The template can still support ODPS product types such as `raw data`, `derived data`, and `dataset`, but the template name should focus on reuse and product thinking.

3. Separate product templates from access patterns.
   API, SQL, file, MCP, GraphQL, gRPC, and AI are access channels. They are not product templates by themselves.

4. Make Product Profile the universal minimum.
   Every ODPS data product should be able to start from a Product Profile.

5. Add richer templates by product intent.
   The template should answer what kind of product is being described, not how mature it is.

## Recommended template family

| Template | Purpose | Best for | Main ODPS schema areas | Typical ODPS product types |
|---|---|---|---|---|
| ODPS Product Profile | Describe any data product at minimum level | Cataloging, portfolio inventory, discovery, basic ownership | `product.details`, `product.dataHolder`, `product.dataAccess` | Any product type |
| ODPS Reusable Data Product | Package reusable data for trusted consumption | Shared data assets, reference data, open data, internal reuse, source-aligned or derived data products | `product.details`, `product.dataHolder`, `product.dataAccess`, `product.dataQuality`, `product.SLA` | `raw data`, `derived data`, `dataset` |
| ODPS Analytical Product | Deliver insight, reporting, and decision support | Reports, analytical views, dashboards, indicators, decision-support products | `product.details`, `product.productStrategy`, `product.dataQuality`, `product.SLA`, `product.dataAccess` | `reports`, `analytic view`, `decision support` |
| ODPS Agentic Product | Serve AI agents, AI workflows, and automation | MCP, AI output ports, algorithms, automated decision-making, bi-directional workflows | `product.details`, `product.productStrategy`, `product.dataAccess`, `product.SLA`, `product.dataQuality`, `product.contract`, `product.license` | `algorithm`, `automated decision-making`, `data-driven service`, `bi-directional` |
| ODPS Marketplace Product | Package a data product for controlled or priced consumption | Marketplaces, pricing plans, licensing, contracts, payment gateways, partner sharing, internal chargeback | `product.details`, `product.productStrategy`, `product.pricingPlans`, `product.license`, `product.contract`, `product.paymentGateways`, `product.dataAccess`, `product.SLA`, `product.dataQuality` | Any product with controlled, priced, or contractual consumption |

## Access patterns

Access patterns should be modeled inside `product.dataAccess`. A single product can have several access channels.

| Access pattern | ODPS schema usage | Use when |
|---|---|---|
| File access | `product.dataAccess[].outputPortType: file` | Consumers download files such as CSV, Excel, JSON, XML, zip, or plain text |
| SQL access | `product.dataAccess[].outputPortType: SQL` | Consumers query the product through a database or query layer |
| API access | `product.dataAccess[].outputPortType: API` | Applications, platforms, or services consume the product through an API |
| GraphQL access | `product.dataAccess[].format: GraphQL` | Consumers need flexible query-based access |
| AI access | `product.dataAccess[].outputPortType: AI` | AI systems consume the product directly |
| MCP access | `product.dataAccess[].format: MCP` or `product.dataAccess[].specification: MCP` | AI agents consume tools, context, or actions through MCP |
| gRPC access | `product.dataAccess[].outputPortType: gRPC` | Low-latency system-to-system consumption is needed |
| sFTP access | `product.dataAccess[].outputPortType: sFTP` | Controlled batch transfer is needed |

## Template 1: ODPS Product Profile

### Intent

Use this as the minimum ODPS starting point for any data product.

It answers:

- What is this product?
- Who holds or owns it?
- How is it accessed?
- What is its status and visibility?

### YAML skeleton

```yaml
schema: https://opendataproducts.org/v4.1/schema/odps.yaml
version: "v4.1"

product:
  details:
    en:
      name: "{{name}}"
      productID: "{{productID}}"
      visibility: "organisation" # private | invitation | organisation | dataspace | public
      status: "draft" # announcement | draft | development | testing | acceptance | production | sunset | retired
      type: "dataset" # use one allowed ODPS product type
      description: "{{description}}"
      valueProposition: "{{valueProposition}}"
      productVersion: "v1.0.0"
      portfolioPriority: "medium" # critical | high | medium | low
      governanceProfile: "structured" # structured | enforced | automated | audit_ready
      categories:
        - "{{category}}"
      tags:
        - "{{tag}}"

  dataHolder:
    legalName: "{{legalName}}"
    businessDomain: "{{businessDomain}}"
    contactName: "{{contactName}}"
    email: "{{email}}"
    URL: "{{holderUrl}}"

  dataAccess:
    - name:
        en: "{{accessName}}"
      description:
        en: "{{accessDescription}}"
      outputPortType: "file" # file | API | SQL | AI | gRPC | sFTP
      format: "CSV" # TOON | JSON | XML | CSV | Excel | zip | plain text | GraphQL | MCP
      authenticationMethod: "none" # OAuth | Token | API key | HTTP Basic | none
      accessURL: "{{accessUrl}}"
      documentationURL: "{{documentationUrl}}"
```

## Template 2: ODPS Reusable Data Product

### Intent

Use this when the product packages reusable data for trusted consumption.

It answers:

- What reusable data is provided?
- How good must the data be?
- How fresh or available must it be?
- How can consumers access it?

### YAML skeleton

```yaml
schema: https://opendataproducts.org/v4.1/schema/odps.yaml
version: "v4.1"

product:
  details:
    en:
      name: "{{name}}"
      productID: "{{productID}}"
      visibility: "organisation"
      status: "production"
      type: "derived data" # raw data | derived data | dataset
      description: "{{description}}"
      valueProposition: "{{valueProposition}}"
      productVersion: "v1.0.0"
      portfolioPriority: "high"
      governanceProfile: "enforced"
      created: "2026-01-01"
      updated: "2026-01-01"
      outputFileFormats:
        - "CSV"
        - "JSON"
      categories:
        - "{{category}}"
      tags:
        - "{{tag}}"

  dataHolder:
    legalName: "{{legalName}}"
    businessDomain: "{{businessDomain}}"
    contactName: "{{contactName}}"
    email: "{{email}}"

  dataQuality:
    declarative:
      - displayTitle:
          - en: "Trusted data quality targets"
        description: "Quality targets for trusted reuse."
        dimensions:
          - dimension: "completeness"
            objective: 95
            weight: 40
            unit: "percentage"
            description: "Expected completeness level."
          - dimension: "timeliness"
            objective: 95
            weight: 30
            unit: "percentage"
            description: "Expected timeliness level."
          - dimension: "validity"
            objective: 95
            weight: 30
            unit: "percentage"
            description: "Expected validity level."

  SLA:
    declarative:
      - name:
          en: "Reusable data SLA"
        description:
          en: "Service expectations for reusable data consumption."
        dimensions:
          - dimension: "updateFrequency"
            objective: "1"
            weight: 50
            unit: "days"
            description: "Expected update interval."
          - dimension: "uptime"
            objective: "99"
            weight: 50
            unit: "percent"
            description: "Expected access availability."

  dataAccess:
    - name:
        en: "File download"
      description:
        en: "Downloadable reusable data file."
      outputPortType: "file"
      format: "CSV"
      authenticationMethod: "none"
      accessURL: "{{fileAccessUrl}}"
      documentationURL: "{{documentationUrl}}"
    - name:
        en: "API access"
      description:
        en: "API access to the same reusable data product."
      outputPortType: "API"
      format: "JSON"
      authenticationMethod: "API key"
      specification: "OAS"
      specsURL: "{{openApiSpecUrl}}"
      accessURL: "{{apiAccessUrl}}"
      documentationURL: "{{apiDocumentationUrl}}"
```

## Template 3: ODPS Analytical Product

### Intent

Use this when the product delivers insight, reporting, indicators, or decision support.

It answers:

- What business objective does this analytical product support?
- Which KPI does it contribute to?
- What product-level KPIs track its usefulness?
- What quality and SLA expectations apply?

### YAML skeleton

```yaml
schema: https://opendataproducts.org/v4.1/schema/odps.yaml
version: "v4.1"

product:
  details:
    en:
      name: "{{name}}"
      productID: "{{productID}}"
      visibility: "organisation"
      status: "production"
      type: "analytic view" # reports | analytic view | decision support
      description: "{{description}}"
      valueProposition: "{{valueProposition}}"
      productVersion: "v1.0.0"
      portfolioPriority: "high"
      governanceProfile: "enforced"
      useCases:
        - useCase:
            useCaseTitle: "{{useCaseTitle}}"
            useCaseDescription: "{{useCaseDescription}}"
            useCaseURL: "{{useCaseUrl}}"

  productStrategy:
    status: "Active"
    startDate: "2026-01-01"
    endDate: "2026-12-31"
    objectives:
      - en: "{{businessObjective}}"
    contributesToKPI:
      id: "{{businessKpiId}}"
      name: "{{businessKpiName}}"
      unit: "{{businessKpiUnit}}"
      target: "{{businessKpiTarget}}"
      direction: "increase" # increase | decrease | at_least | at_most | equals
      timeframe: "{{timeframe}}"
      frequency: "monthly"
      owner: "{{owner}}"
      calculation: "{{calculation}}"
    productKPIs:
      - id: "{{productKpiId}}"
        name: "{{productKpiName}}"
        unit: "{{productKpiUnit}}"
        target: "{{productKpiTarget}}"
        calculation: "{{productKpiCalculation}}"
        direction: "increase"
        frequency: "monthly"
        owner: "{{owner}}"

  dataQuality:
    declarative:
      - displayTitle:
          - en: "Analytical quality targets"
        description: "Quality expectations for analytical use."
        dimensions:
          - dimension: "accuracy"
            objective: 95
            weight: 40
            unit: "percentage"
            description: "Expected analytical accuracy."
          - dimension: "consistency"
            objective: 95
            weight: 30
            unit: "percentage"
            description: "Expected consistency across reporting periods."
          - dimension: "timeliness"
            objective: 95
            weight: 30
            unit: "percentage"
            description: "Expected freshness for analytical use."

  SLA:
    declarative:
      - name:
          en: "Analytical product SLA"
        description:
          en: "Service expectations for analytical product consumption."
        dimensions:
          - dimension: "updateFrequency"
            objective: "1"
            weight: 60
            unit: "days"
            description: "Expected refresh interval."
          - dimension: "emailResponseTime"
            objective: "2"
            weight: 40
            unit: "days"
            description: "Expected response time for support by email."

  dataAccess:
    - name:
        en: "Analytical view"
      description:
        en: "Access to the analytical view or report."
      outputPortType: "API"
      format: "JSON"
      authenticationMethod: "OAuth"
      specification: "OAS"
      specsURL: "{{specsUrl}}"
      accessURL: "{{accessUrl}}"
      documentationURL: "{{documentationUrl}}"
```

## Template 4: ODPS Agentic Product

### Intent

Use this when the product is consumed by AI agents, AI applications, workflows, automation, or machine-to-machine processes.

It answers:

- What can the agent or system consume?
- What access protocol is used?
- What operational promises apply?
- What contract or license terms guide automated consumption?

### YAML skeleton

```yaml
schema: https://opendataproducts.org/v4.1/schema/odps.yaml
version: "v4.1"

product:
  details:
    en:
      name: "{{name}}"
      productID: "{{productID}}"
      visibility: "organisation"
      status: "production"
      type: "data-driven service" # algorithm | automated decision-making | data-driven service | bi-directional
      description: "{{description}}"
      valueProposition: "{{valueProposition}}"
      productVersion: "v1.0.0"
      portfolioPriority: "critical"
      governanceProfile: "automated"
      standards:
        - "{{standard}}"
      tags:
        - "agent-ready"
        - "MCP"

  productStrategy:
    status: "Active"
    objectives:
      - en: "{{businessObjective}}"
    contributesToKPI:
      id: "{{businessKpiId}}"
      name: "{{businessKpiName}}"
      unit: "{{businessKpiUnit}}"
      target: "{{businessKpiTarget}}"
      direction: "increase"
      timeframe: "{{timeframe}}"
      frequency: "monthly"
      owner: "{{owner}}"
      calculation: "{{calculation}}"
    productKPIs:
      - id: "{{productKpiId}}"
        name: "{{productKpiName}}"
        unit: "{{productKpiUnit}}"
        target: "{{productKpiTarget}}"
        calculation: "{{productKpiCalculation}}"

  dataQuality:
    declarative:
      - displayTitle:
          - en: "Agentic quality targets"
        description: "Quality expectations for AI and automated consumption."
        dimensions:
          - dimension: "validity"
            objective: 98
            weight: 35
            unit: "percentage"
            description: "Expected validity for machine consumption."
          - dimension: "timeliness"
            objective: 98
            weight: 35
            unit: "percentage"
            description: "Expected freshness for agentic use."
          - dimension: "consistency"
            objective: 98
            weight: 30
            unit: "percentage"
            description: "Expected consistency for automated workflows."

  SLA:
    declarative:
      - name:
          en: "Agentic product SLA"
        description:
          en: "Service expectations for agentic and automated consumption."
        dimensions:
          - dimension: "latency"
            objective: "500"
            weight: 35
            unit: "milliseconds"
            description: "Expected response latency."
          - dimension: "uptime"
            objective: "99"
            weight: 35
            unit: "percent"
            description: "Expected service availability."
          - dimension: "errorRate"
            objective: "1"
            weight: 30
            unit: "percent"
            description: "Maximum expected error rate."

  contract:
    id: "{{contractId}}"
    type: "ODCS" # ODCS | DCS
    contractVersion: "{{contractVersion}}"
    contractURL: "{{contractUrl}}"

  license:
    scope:
      definition: "{{licenseDefinition}}"
      restrictions: "{{licenseRestrictions}}"
      permanent: false
      exclusive: false
      rights:
        - "Reproduction"
        - "Display"
    governance:
      ownership: "{{licenseOwnership}}"
      audit: "{{auditTerms}}"
      confidentiality: "{{confidentiality}}"
      applicableLaws: "{{applicableLaws}}"

  dataAccess:
    - name:
        en: "MCP access"
      description:
        en: "MCP access for AI agents and tools."
      outputPortType: "AI"
      format: "MCP"
      authenticationMethod: "Token"
      specification: "MCP"
      specsURL: "{{mcpSpecUrl}}"
      accessURL: "{{mcpAccessUrl}}"
      documentationURL: "{{documentationUrl}}"
    - name:
        en: "API access"
      description:
        en: "API access for applications and automated workflows."
      outputPortType: "API"
      format: "JSON"
      authenticationMethod: "OAuth"
      specification: "OAS"
      specsURL: "{{openApiSpecUrl}}"
      accessURL: "{{apiAccessUrl}}"
      documentationURL: "{{apiDocumentationUrl}}"
```

## Template 5: ODPS Marketplace Product

### Intent

Use this when the product is offered under controlled, priced, licensed, contractual, or marketplace terms.

It answers:

- What is being offered?
- What pricing applies?
- What license rights and restrictions apply?
- What contract applies?
- What payment gateway applies?
- What SLA and quality terms are attached to the offer?

### YAML skeleton

```yaml
schema: https://opendataproducts.org/v4.1/schema/odps.yaml
version: "v4.1"

product:
  details:
    en:
      name: "{{name}}"
      productID: "{{productID}}"
      visibility: "dataspace" # private | invitation | organisation | dataspace | public
      status: "production"
      type: "data-enhanced product"
      description: "{{description}}"
      valueProposition: "{{valueProposition}}"
      productVersion: "v1.0.0"
      portfolioPriority: "high"
      governanceProfile: "audit_ready"
      categories:
        - "{{category}}"
      tags:
        - "marketplace"
        - "controlled-consumption"

  productStrategy:
    status: "Active"
    objectives:
      - en: "{{businessObjective}}"
    contributesToKPI:
      id: "{{businessKpiId}}"
      name: "{{businessKpiName}}"
      unit: "{{businessKpiUnit}}"
      target: "{{businessKpiTarget}}"
      direction: "increase"
      timeframe: "{{timeframe}}"
      frequency: "monthly"
      owner: "{{owner}}"
      calculation: "{{calculation}}"
    productKPIs:
      - id: "{{productKpiId}}"
        name: "{{productKpiName}}"
        unit: "{{productKpiUnit}}"
        target: "{{productKpiTarget}}"
        calculation: "{{productKpiCalculation}}"

  pricingPlans:
    declarative:
      en:
        - name: "{{pricingPlanName}}"
          priceCurrency: "USD"
          price: "{{price}}"
          billingDuration: "month" # instant | day | week | month | year
          unit: "Recurring" # One-time-payment | Pay-per-use | Recurring | Revenue-sharing | Data-volume | Pay-what-you-want | Freemium | Open-data | Value-based | On-request | Trial
          maxTransactionQuantity: 0
          offering:
            - "{{offeringItem}}"
          valueAddedTaxIncluded: false
          valueAddedTaxPercentage: 0
          notes: "{{pricingNotes}}"

  license:
    scope:
      definition: "{{licenseDefinition}}"
      restrictions: "{{licenseRestrictions}}"
      geographicalArea:
        - "{{geographicalArea}}"
      permanent: false
      exclusive: false
      rights:
        - "Reproduction"
        - "Display"
        - "Distribution"
    termination:
      noticePeriod: 30
      terminationConditions: "{{terminationConditions}}"
      continuityConditions: "{{continuityConditions}}"
    governance:
      ownership: "{{licenseOwnership}}"
      audit: "{{auditTerms}}"
      warranties: "{{warranties}}"
      confidentiality: "{{confidentiality}}"
      applicableLaws: "{{applicableLaws}}"

  contract:
    id: "{{contractId}}"
    type: "ODCS" # ODCS | DCS
    contractVersion: "{{contractVersion}}"
    contractURL: "{{contractUrl}}"

  paymentGateways:
    - description:
        en: "{{paymentGatewayDescription}}"
      type: "Stripe" # Stripe | Axio | Checkout | Custom
      version: "{{paymentGatewayVersion}}"
      reference: "{{paymentGatewayReferenceUrl}}"
      spec: {}

  dataQuality:
    declarative:
      - displayTitle:
          - en: "Marketplace quality targets"
        description: "Quality targets attached to the marketplace offer."
        dimensions:
          - dimension: "completeness"
            objective: 95
            weight: 30
            unit: "percentage"
            description: "Expected completeness level."
          - dimension: "accuracy"
            objective: 95
            weight: 40
            unit: "percentage"
            description: "Expected accuracy level."
          - dimension: "timeliness"
            objective: 95
            weight: 30
            unit: "percentage"
            description: "Expected timeliness level."

  SLA:
    declarative:
      - name:
          en: "Marketplace product SLA"
        description:
          en: "Service expectations attached to the marketplace offer."
        support:
          email: "{{supportEmail}}"
          emailServiceHours: "{{emailServiceHours}}"
          documentationURL: "{{supportDocumentationUrl}}"
        dimensions:
          - dimension: "uptime"
            objective: "99"
            weight: 40
            unit: "percent"
            description: "Expected service availability."
          - dimension: "responseTime"
            objective: "2"
            weight: 30
            unit: "seconds"
            description: "Expected technical response time."
          - dimension: "emailResponseTime"
            objective: "1"
            weight: 30
            unit: "days"
            description: "Expected support response time."

  dataAccess:
    - name:
        en: "Marketplace API access"
      description:
        en: "Controlled API access to the product."
      outputPortType: "API"
      format: "JSON"
      authenticationMethod: "Token"
      specification: "OAS"
      specsURL: "{{specsUrl}}"
      accessURL: "{{accessUrl}}"
      documentationURL: "{{documentationUrl}}"
```

