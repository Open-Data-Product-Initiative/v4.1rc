# Inline Pattern

The objects are not defined inline, but instead references a reusable definition in the components section using a $ref path.

> Example:

```yml

schema: https://opendataproducts.org/v4.1/schema/odps.yaml
version: 4.1
product:
  details:
    en:
      name: Pets of the year
      productID: 123456are
      valueProposition: Design a customised petstore using pet preference data.
      description: This is an inline example of a petstore data product.
      visibility: private
      status: draft
      productVersion: '0.1.0'
      type: derived data
    
  serviceLevel:
    slas:
      - dimension: uptime
        objective: 99
        unit: percent

  access:
    format: REST
    specification: OAS 3.0
    specsURL: https://urbanpulse.ai/spec.json

  dataQuality:
    metrics:
      - dimension: completeness
        objective: 95
        code:
          language: SQL
          logic: |
            SELECT ...;
```
