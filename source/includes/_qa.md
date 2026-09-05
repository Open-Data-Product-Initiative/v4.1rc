# Data Quality

> Template structure of Data Quality array component:

```yml
dataQuality:
  declarative:
    default:
      dimensions:
        - dimension: accuracy
          displaytitle:
            en: Data Accuracy (percent)
          objective: 90
          unit: percentage
          weight: 60
        - dimension: completeness
          displaytitle:
            en: Data Completeness (percent)
          objective: 90
          unit: percentage
          weight: 40
  executable:
    - dimension: selected dimension
      type:  
      version: 
      reference: 
      spec:
```
Data quality is essential for one main reason: You give customers the best experience when you make decisions using accurate data. A great customer experience leads to happy customers, brand loyalty, and higher revenue for your business. Information is only valuable if it is of high quality.  

By adhering to defined quality characteristics, organizations can maximize the value of their data assets, improve decision-making, enhance operational efficiency, and maintain trust and confidence in their data-driven processes and systems. ODPS is compatible with EDM Council data quality model.

The `dataQuality` component in ODPS provides a structured and machine-readable way to **declare and monitor the quality characteristics** of a data product. It helps align technical validation with business expectations and supports both human understanding and automated tooling.

**Structure Overview:**
The `dataQuality` object consists of two parts:

- **`declarative`**: Captures target levels for defined quality dimensions like `accuracy`, `completeness`, or `timeliness`. These values represent your **intended** or **promised** quality levels.
- **`executive`**: Allows integration with supported *Everything as Code* tools (e.g., SodaCL, DQOps, MonteCarlo, OpenMetadata) to define **verifiable** and **executable** rules that check whether those targets are met in practice.

This structure ensures that both expectations and enforcement logic are documented and machine-actionable in the same place.

## Referencing Capability
One of the key features of ODPS is the ability to **reuse** named data quality profiles via references. For example, quality profiles such as `default`, `premium`, or `gold` can be defined once under `dataQuality.declarative` and referenced elsewhere in the YAML—such as in SLA definitions, pricing plans, or tiered service offerings.

**Benefits of Referencing:**

- **DRY Principle**: Avoid repetition. Define once, reference many times.
- **Clarity**: Consumers of your data product can easily see which quality profile is associated with a particular service tier or access plan.
- **Scalability**: You can support multiple audiences or markets with varying quality expectations.
- **Auditability**: Clearly link machine-readable checks to business commitments.

> referencing examples:

```text
  $ref: '#/product/dataQuality/declarative/default'

  ...

  $ref: '#/product/dataQuality/declarative/premium'
```

**Referencing Examples:**
To reference a defined quality profile from another part of your YAML (e.g., pricing plan): `$ref: '#/product/dataQuality/declarative/default'`. Or reference a named premium quality package: `$ref: '#/product/dataQuality/declarative/premium'` Use this component to clearly communicate both intentions and verifiable guarantees about data quality—whether you're reporting to stakeholders, building trust with customers, or enabling automated validation through modern DQ tools. 


**The Role of `default`**

The `default` quality profile is **mandatory** whenever the `dataQuality` object is used. It acts as the **baseline** definition, ensuring there is always a clear and predictable quality configuration, even when no referencing is used.

You should use the `default` profile when:

- You want to describe core quality expectations for the product.
- You don’t yet need pricing or SLA-specific variations.
- You want to ensure future compatibility with advanced features such as AI agents, data marketplaces, or automated governance.

This makes the `default` profile both a **minimum requirement** and a **best practice** for clarity and interoperability.

The QA object is general in nature and should be enough for common (80%) use cases. You can make extensions to the standard with "x-" mechanism in order to fulfill 
any industry specific needs. 

## ODPS offers 8 standardized options to define and measure data quality with Everything as Code monitoring 

| <div style="width:150px">Data Quality Dimension</div>   | Description | 
|---|---|
| **accuracy** | The measurement of the veracity of data to its authoritative source |
| **completeness** | Data is required to be populated with a value (aka not null, not nullable). Completeness checks if all necessary data attributes are present in the dataset. |
| **conformity** | Data content must align with required standards, syntax (format, type, range), or permissible domain values. Conformity assesses how closely data adheres to standards, whether internal, external, or industry-wide. |
| **consistency** | Data should retain consistent content across data stores. Consistency ensures that data values, formats, and definitions in one group match those in another group. |
| **coverage** | All records are contained in a data store or data source. Coverage relates to the extent and availability of data present but absent from a dataset. |
| **timeliness** | The data must represent current conditions; the data is available and can be used when needed.  |
| **validity** | Validity refers to the extent to which the data accurately and appropriately represents the real-world object or concept it is supposed to describe. |
| **uniqueness** | Uniqueness means each record and attribute should be one-of-a-kind, aiming for a single, unique data entry |



## Optional attributes and elements

> Example of Data Quality component with some of the data quality dimensions:

```yml
dataQuality:
  declarative:
    default:
      displaytitle: 
        en: The Basic Data Quality
      description: 
        en: The basic quality package
      dimensions:
        - dimension: accuracy
          displaytitle:
            en: Data Accuracy (percent)
          description:
            en: >
              Data Accuracy ensures the data product reflects the real-world
              entities or events it represents, minimizing errors and providing
              reliable insights.
          objective: 90
          unit: percentage
          weight: 60
        - dimension: completeness
          displaytitle:
            en: Data Completeness (percent)
          objective: 90
          unit: percentage
          weight: 40


    premium:
      displaytitle: 
        en: The Premium Data Quality
      description: 
        en: The Preimum quality package
      dimensions:
        - dimension: accuracy
          displaytitle:
            en: Data Accuracy (percent)
          description:
            en: >
              Data Accuracy ensures the data product reflects the real-world
              entities or events it represents, minimizing errors and providing
              reliable insights.
          objective: 98
          unit: percentage
          weight: 70
        - dimension: completeness
          displaytitle:
            en: Data Completeness (percent)
          objective: 99
          unit: percentage
          weight: 30

  executable:
    - dimension: accuracy
      type: SodaCL
      reference: https://docs.soda.io/soda-cl/soda-cl-overview.html
      spec:
        checks:
          - require_unique(member_id)
          - require_range(age_band, 18, 100)
    - dimension: completeness
      type: DQOps
      version: 1.6.0 
      reference: https://dqops.com/docs/dqo-concepts/running-data-quality-checks/
      spec:
        columns:
          target_column:
            profiling_checks: 
              nulls: 
                profile_nulls_percent: 
                  warning: 
                    max_percent: 8.0
                  error: 
                    max_percent: 10.0
                  fatal: 
                    max_percent: 11.0      
```
> Example of DQ external profiles usage:

```yml

dataQuality: # the below file contains the same content as above
  $ref: 'https://example.org/DQ/all-packages.yaml'

```

> Example of DQ external profiles for each profile usage:

```yml

dataQuality:
  declarative:
    default:
      $ref: 'https://example.org/DQ/basic.yaml'
    premium:
      $ref: 'https://example.org/DQ/premium.yaml'
```


| <div style="width:150px">Element name</div>   | Type  | Options  | Description  |
|---|---|---|---|
| **dataQuality** | element | - | Contains array of data quality dimensions with optional computational monitoring object. Under this element Data Quality is divided into declarative and executable parts. |
| **$ref** | filepath or valid URL | - | Define the Data quality profiles in external file for reuse purposes, example  `$ref: 'https://example.org/DQ/all-packages.yaml'` See example. This makes it easy to keep related profiles (e.g. default, premium, gold) together, apply versioning and validation once, and publish all variants from a single repo or source. <br/><br/>The same pattern can be used in individual data quality profiles instead of doing it inline. See example. This gives finer control if each Data quality is owned or updated by a different team, but increases the number of files to track and host.|
| **default** | object | - | This object must always be present and named exactly `default` if dataQuality object is used. It acts as the fallback or primary data quality profile. <br/><br/>Users are free to define additional named profiles such as `premium`, `gold`, etc., in parallel to the default. <br/><br/>In the example, `default` and `premium` are both included. These variants can be referred to from other components like pricing plans. <br/><br/>**Example reference usage:** <br/> `dataQuality: $ref: '#/product/dataQuality/declarative/default'` |
| **dimension** | attribute | string, one of: *accuracy, completeness, conformity, consistency, coverage, timeliness, validity, or uniqueness.* | Defines the data quality dimension. |
| **objective** | attribute | integer | Defines the target value for the data quality dimension |
| **unit** | attribute | string. One of: *percentage, number* | Defines the unit used in stating the target quality level. |
| **weight** | attribute | integer | Optional. Relative importance as percentage of the dimension when calculating the product's overall Data Quality score. Must be an integer (no decimals). |
| **executable** | element | - | Grouping element that collects together data quality monitoring rules. You can define monitoring patterns as code under this element for each dimension. The actual as-code part is defined in the `spec` element. |
| **displaytitle** | object | - | Dimension title to be shown in various UIs. Object contains title(s) in desired language(s). |
| **en** | attribute | [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) defined 2-letter codes | Binds the text elements together in a given language. Multilanguage support is implemented by duplicating content under other ISO language codes. |
| **description** | object | - | Describe the dimension so that it can be used for example in info boxes in UI. Object contains descriptions in desired language(s). |
| **type** | attribute | string, one of: [SodaCL](https://docs.soda.io/soda-cl/soda-cl-overview.html), [Montecarlo](https://docs.getmontecarlo.com/docs/monitors-as-code), [DQOps](https://dqops.com/docs/),  [Great Expectations](https://docs.greatexpectations.io/docs/reference/learn/data_quality_use_cases/dq_use_cases_lp), [OpenMetadata](https://docs.open-metadata.org/v1.12.x/how-to-guides/data-quality-observability/quality/data-quality-as-code), Custom | Data Quality Monitoring as code system name. Use one of the predefined options only. With _Custom_ type you can use your in-house solution. |
| **version** | attribute | string | The version of DQ monitoring tool used. |
| **reference** | URL | Valid URL | Provide URL pointing to the reference documentation. |
| **spec** | element | YAML/URL/string | The content for Data Quality monitoring expressed as code. Accepted as inline YAML, a valid URL pointing to YAML, or a plain string if `type` is `Custom`. |


If you see something missing, described inaccurately or plain wrong, or you want to comment the specification, [raise an issue in Github](https://github.com/Open-Data-Product-Initiative/dev/issues)

Or join the [ODPS Discord](https://discord.gg/7KfnFxAc) to discuss the ideas and your needs!
