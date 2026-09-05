# Mandatory-only example

Example data product with just the mandatory elements and attributes. This is the minimal representation of a data product metadata that is expected to be found from every data product following ODPS standard. This bare minimum can be expanded with other elements and attributes defined in the specification. Also the possibilty to use extensions exists if local additions are needed. 

> Example of mandatory-only elements and attributes Open Data Product specification instance:

```yml

schema: https://opendataproducts.org/v4.1/schema/odps.yaml
version: 4.1
product:
  details:
    en:
      name: Pets of the year
      productID: 123456are
      valueProposition: Design a customised petstore using pet preference data.
      description: This is a minimal example of a petstore data product.
      visibility: private
      status: draft
      productVersion: '0.1.0'
      type: derived data

```
