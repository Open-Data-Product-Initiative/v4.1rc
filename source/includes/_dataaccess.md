# Data Access

The `dataAccess` object defines how users—or machines—can technically access the data product. It allows publishers to describe **multiple, named access methods** tailored to different consumer needs: from simple file downloads and APIs to AI agent integration via protocols like **MCP**.

Each entry under `dataAccess` (such as `default`, `API`, or `Agent`) represents a distinct access interface with its own metadata, authentication requirements, and documentation references. This structure makes it possible to:

- Offer **flexible access modes** for various user personas (analysts, developers, AI agents, etc.)
- Support **multilingual UI presentation** through localized `name` and `description` fields
- Clearly declare **security expectations** using `authenticationMethod`
- Link to both **machine-readable specs** (`specsURL`) and **human-readable guides** (`documentationURL`)
- Promote **reusability** by referencing these interfaces throughout the ODPS YAML using `$ref`

Including an AI agent-specific access interface (`outputPortType: AI`) supports MCP-based agent interactions, aligning your product with **AI-native data delivery patterns**.

#### Referencing Examples

For example in your `access` section in Pricing, you can reuse any defined method from `dataAccess` like this: _$ref: '#/Product/dataAccess/default'_


## Optional attributes and elements

> Example of Data Access object usage:

```yml

dataAccess:
  default:
    name:
      en: Access to zipped package
    description: 
      en: Latest Dataset and Resources
    outputPortType: file
    format: zip
    accessURL: url to file as zip
  dataonly:
    name:
      en: Access to latest dataset
    description: 
      en: Latest Dataset
    outputPortType: file
    format: CSV
    accessURL: url to file as CSV
  API:
    name:
      en: Access to API
    description: 
      en: API Access to the Latest Dataset
    outputPortType: API
    authenticationMethod: OAuth
    specification: OAS
    format: JSON
    accessURL: >-
      https://data.cms.gov/data-api/v1/dataset/2/data
    specsURL: >-
      https://data.cms.gov/provr-enrollment/api-docs
    documentationURL: >- 
      https://data.cms.gov/provr-enrollment/docs
  agent: 
    name:
      en: AI Agent access to the data product
    description: 
      en: MCP interface for structured data access and agent interaction.
    outputPortType: AI
    authenticationMethod: Token
    specification: MCP
    format: MCP
    specsURL: https://urbanpulse.ai/llms.txt
    documentationURL: https://urbanpulse.ai/llms-full.txt
```

> Example of Data Access external profiles usage:

```yml

dataAccess: # the below file contains the same content as above
  $ref: 'https://example.org/dataAccess/all-packages.yaml'

```

> Example of extenal Data Access for each profile usage:

```yml

dataAccess:
    default:
      $ref: 'https://example.org/dataAccess/basic.yaml'
    API:
      $ref: 'https://example.org/dataAccess/api.yaml'
    agent:
      $ref: 'https://example.org/dataAccess/agent.yaml'
```

| <div style="width:150px">Element name</div>   | Type  | Options  | Description  |
|---|---|---|---|
| **dataAccess** | object | - | Root-level object containing named access configurations. Each key (e.g., `default`, `API`, `Agent`) defines an access method that can be reused across the ODPS YAML. |
| **$ref** | filepath or valid URL | - | Define the Data Access in external file for reuse purposes, example  `$ref: 'https://example.org/dataAccess/all-packages.yaml'` See example. This makes it easy to keep related profiles (e.g. default, API, agent) together, apply versioning and validation once, and publish all variants from a single repo or source. <br/><br/>The same pattern can be used in individual Data Access profiles instead of doing it inline. See example. This gives finer control if each Data Access is owned or updated by a different team, but increases the number of files to track and host.|
| **default** | object | - | This object defines the default access interface and must always be present if dataAccess object is used. The name `default` is fixed and used as the fallback or primary access method. <br/><br/> In the example, you will see additional user-defined access methods (`dataonly`, `API`, `Agent`) demonstrating how various access interfaces can be added beyond the required `default`. <br/><br/> **Example reference usage:** <br/> `access: $ref: '#/dataAccess/default'`|
| **name** | object | ISO 639-1 language codes (e.g., `en`) | Multilingual name for the access interface. Can be shown in UIs. |
| **description** | object | ISO 639-1 language codes (e.g., `en`) | Multilingual description for the access interface. Supports user understanding. |
| **outputPortType** | string | file, API, SQL, AI, gRPC, sFTP, etc. | Describes the technical method for delivering data (e.g., `file` for file downloads, `API` for web services). |
| **format** | string | TOON, JSON, XML, CSV, Excel, zip, plain text, GraphQL, MCP | Specifies the data format made available through this access channel. |
| **authenticationMethod** | string | OAuth, Token, API key, HTTP Basic, none | Security model required to access the data. |
| **specification** | string | OAS, RAML, Slate, MCP | Defines the type of API or protocol specification used to describe access (e.g., OpenAPI, RAML, or a custom protocol like MCP). |
| **specsURL** | URL | Valid URL | Points to the machine-readable technical documentation (e.g., OpenAPI YAML). |
| **accessURL** | URL | Valid URL | The direct access point to retrieve the data – can be for example an API endpoint or a file link. |
| **documentationURL** | URL | Valid URL | A human-readable documentation or guide for access setup, authentication steps, or onboarding. |
| **hashType** | string | SHA-1, SHA-2, SHA-256, MD5, etc. | (Optional) Defines hash algorithm used when providing file integrity verification. |
| **checksum** | string | any string | (Optional) File hash/checksum value, useful for verifying data integrity after download. |
