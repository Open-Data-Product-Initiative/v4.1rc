# Data SLA

> Template structure of SLA array component:

```yml
SLA:
  declarative:
    - dimension: selected dimension
      displaytitle:
      description:
      objective: 
      unit:
  executable:
    - dimension: selected dimension
      type:  
      version: 
      reference: 
      spec:
```

Data Service Level Agreement (SLA) **Object** contains attributes which define the desired and promised quality of the data product. 

A Data Service Level Agreement (SLA) is a contractual agreement between a data service provider and its customers that defines the expected level of service quality, performance, and availability for the data services provided. SLAs outline specific metrics, targets, and responsibilities that both parties agree to adhere to, ensuring accountability and transparency in the delivery of data services.

Defining Data SLAs in a machine-readable format enhances automation, facilitates monitoring, enables real-time compliance tracking, and supports seamless integration with monitoring and alerting systems.

**Structure notes:** The SLA object is divided into 2 parts: declarative and executable. 

* Declarative part defines the dimensions and aimed/intended SLA levels in defined unit. 
* Executable part contains the machine-readable "as code" rules to validate SLA dimensions. The code inside _spec_ element is intended to be injected as in supporting SLA monitoring platforms in their defined format and structure.  

The SLA object is general in nature and should be enough for common (80%) use cases. Note that you can make extensions to the standard with "x-" mechanism in order to fulfill any industry specific needs. The ["Specification extensions"](#specification-extensions) section provides details on how to use this feature.

> In case standardized options are not enough:

```text
The SLA object is general in nature and should 
be enough for common (80%) use cases. 

You can make extensions to the standard 
with "x-" mechanism in order to fulfill 
any industry specific needs. 

A suggestive example below 

SLA:
  declarative:
    default:
      x-dimension: custom
      displaytitle:
        en: Custom SLA
      objective: 99
      unit: percent

```


## SLA can be defined with 11 standardized dimensions with decoupled Everything as Code monitoring

> Example of SLA component usage:

```yml

SLA:
  declarative:
    default:
      dimensions:
        - dimension: uptime
          displaytitle:
            en: Uptime
          objective: 99
          unit: percent
          weight: 50
        - dimension: responseTime
          objective: 200
          unit: milliseconds
          weight: 30

```

| <div style="width:150px">SLA Dimension</div>   | Description | 
|---|---|
| **latency** | minimal amount of time before getting any response. |
| **uptime** | Uptime is a measure of system reliability, expressed as the percentage of time a machine, typically a computer, has been working and available. See more https://uptime.is/. |
| **responseTime** | amount of time to process external request. |
| **errorRate** | Maximum tolerated errors in data, percentage. |
| **endOfSupport** | The date at which your product will not have support anymore. |
| **endOfLife** | The date at which your product will not be available anymore. No support, no access. |
| **updateFrequency** | how often data is updates. |
| **timeToDetect** | How fast can you detect a problem? |
| **timeToNotify** | Once you see a problem, how much time do you need to notify your users? |
| **timeToRepair** | How long do you need to fix the issue once it is detected? |
| **emailResponseTime** | How long do you need to respond to email support requests? |

No mandatory attributes at the moment. Optional attributes are listed in own table and an example is given in the right column. 

## Optional attributes and elements

> Example of SLA component usage:

```yml

SLA:
  declarative:
    default:
      name: 
        en: The Basic SLA
      description: 
        en: The basic SLA package
      dimensions:
        - dimension: uptime
          displaytitle:
            en: Uptime
          objective: 90
          unit: percent
          weight: 50
        - dimension: responseTime
          objective: 200
          unit: milliseconds
          weight: 30
        - dimension: updateFrequency
          objective: 30
          unit: minutes
          weight: 20
    premium:
      name: 
        en: The Premium SLA
      description: 
        en: The Premium SLA package
      dimensions:
        - dimension: uptime
          displaytitle:
            en: Uptime
          objective: 99
          unit: percent
          weight: 70
        - dimension: responseTime
          objective: 100
          unit: milliseconds
          weight: 20
        - dimension: updateFrequency
          objective: 5
          unit: minutes
          weight: 10
  executable:
    - dimension: uptime
      type: prometheus
      reference: 'https://prometheus.io/docs/prometheus/latest/querying/basics/'
      spec: |-
        avg_over_time(
          (
            sum without() (up{job="prometheus"})
              or
            (0 * sum_over_time(up{job="prometheus"}[7d]))
          )[7d:5m]
        )   
    - dimension: responseTime
      type: prometheus
      reference: 'https://prometheus.io/docs/prometheus/latest/querying/basics/'
      spec: |-
        rate(http_server_requests_seconds_sum[$__rate_interval]) /
        rate(http_server_requests_seconds_count[$__rate_interval])

  support:
    phoneNumber: '+971508976456'
    phoneServiceHours: Mon-Fri 8am-4pm (GMT)
    email: support@opendataproducts.org
    emailServiceHours: Mon-Fri 8am-4pm (GMT)
    documentationURL: ''

```
> Example of SLA external profiles usage:

```yml

SLA: # the below file contains the same content as above
  $ref: 'https://example.org/slas/all-packages.yaml'

```

> Example of SLA external profiles for each profile usage:

```yml

SLA:
  declarative:
    default:
      $ref: 'https://example.org/slas/basic.yaml'
    premium:
      $ref: 'https://example.org/slas/premium.yaml'


```

| <div style="width:150px">Element name</div>   | Type  | Options  | Description  |
|---|---|---|---|
| **SLA** | element | - | Binds the SLA-related elements and attributes together. |
| **$ref** | filepath or valid URL | - | Define the SLA in external file for reuse purposes, example  `$ref: 'https://example.org/slas/all-packages.yaml'` See example. This makes it easy to keep related profiles (e.g. default, premium, gold) together, apply versioning and validation once, and publish all variants from a single repo or source. <br/><br/>The same pattern can be used in individual SLA profiles instead of doing it inline. See example. This gives finer control if each SLA is owned or updated by a different team, but increases the number of files to track and host.|
| **default** | object | - | This object must always be present and named exactly `default` if SLA object is used. It acts as the fallback or baseline SLA profile. <br/><br/>Users are free to define additional named profiles such as `premium`, `gold`, etc., in parallel to the default. <br/><br/>In the example above, both `default` and `premium` profiles are included. These variants can be referenced from pricing plans or other objects. <br/><br/>**Example reference usage:** <br/> `SLA: $ref: '#/product/SLA/declarative/default'` |
| **dimensions** | array | - | Contains one or more SLA dimension objects. Each defines a measurable SLA metric such as uptime or responseTime. |
| **dimension** | attribute | string, one of: *latency, uptime, responseTime, errorRate, endOfSupport, endOfLife, updateFrequency, timeToDetect, timeToNotify, timeToRepair, emailResponseTime* | Defines the SLA dimension. |
| **objective** | attribute | integer | Target level to be achieved for the dimension (e.g., 99). |
| **unit** | attribute | Options: percent, milliseconds, seconds, minutes, days, weeks, months, years, never, date, null | Measurement unit for the SLA objective. If "date" is used, format should be dd/mm/yyyy. |
| **weight** | attribute | integer | Optional. Relative importance as percentage of the SLA dimension when calculating the product's overall SLA score. Must be an integer (no decimals). User-editable. |
| **displaytitle** | object | - | Dimension title to be shown in UIs. Localized per language. |
| **description** | object | - | Description of the SLA package or specific dimension, localized per language. |
| **executable** | element | - | Grouping element for SLA monitoring logic. Monitoring definitions are provided as code in the `spec` field for each dimension. |
| **type** | attribute | string | Name of the monitoring system (e.g., Prometheus). Must support SLA-as-code. |
| **spec** | element | YAML/URL/string | Monitoring logic for the defined dimension. Can be inline YAML, plain string, or URL to code file. |
| **reference** | URL | Valid URL | Link to documentation about the monitoring system used. |
| **support** | element | - | Describes how users can get help with usage, billing, or other issues. |
| **phoneNumber** | string | valid phone number | The phone number for support (e.g., +971508976456). Should follow [E.164](https://www.itu.int/rec/T-REC-E.164/en) format. |
| **phoneServiceHours** | string | - | Description of phone support hours, e.g., "Mon–Fri 8am–4pm (GMT)". |
| **email** | string | valid email address | Email address for support requests. Must follow [RFC2822](https://datatracker.ietf.org/doc/html/rfc2822). |
| **emailServiceHours** | string | - | Description of email support hours. |
| **documentationURL** | URL | Valid URL | Link to documentation describing the support process or SLA handling. |




If you see something missing, described inaccurately or plain wrong, or you want to comment the specification, [raise an issue in Github](https://github.com/Open-Data-Product-Initiative/v4.0/issues)

Or join the [ODPS Discord](https://discord.gg/7KfnFxAc) to discuss the ideas and your needs! 
