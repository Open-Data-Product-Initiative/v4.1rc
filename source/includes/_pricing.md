# Data Pricing Plans

> Template structure of Data Pricing Plans array component:

```yml
pricingPlans:
  en:
  - name: Premium subscription 1 year
    unit: Recurring
    priceCurrency: EUR
    price: "50.00"
    billingDuration: year
    
  - name: Premium subcsription 1 month
    unit: Recurring
    priceCurrency: EUR
    price: "8.00"
    billingDuration: month
```


**Standardized data pricing plans are crucial for transparency, scalability, and customer trust.** They ensure that customers can easily understand and compare costs, fostering trust and reducing disputes. For providers, standardized pricing streamlines operations, supports scalability, and simplifies market comparison, allowing for effective competitive positioning. Additionally, it aids in better financial planning and forecasting for both the provider and the customer, ensuring predictable revenue and informed decision-making. Overall, standardized pricing is essential for the sustainable growth and success of data products.

Pricing is the process whereby a business sets the price at which it will sell its products and services. Pricing **OBJECT** contains pricing plans related metadata to be used for example in displaying the items in a marketplace. If needed the standard metadata is converted to marketplace internal format. We encourage all data product owners to enforce usage of this standard to foster global interoperability.  

The 12 pricing plans enabled by ODPS are meticulously defined through an in-depth analysis of pricing models applied across more than 300 data products. We continuously monitor the evolution of pricing plans in the data economy, striving to provide the most comprehensive and up-to-date list of standardized pricing options - yet some gaps might exist.

The Pricing object is general in nature and should be enough for common (80%) use cases. You can make extensions to the standard with "x-" mechanism in order to fulfill any industry specific needs. The ["Specification extensions"](#specification-extensions) section provides details on how to use this feature. 

> In case standardized options are not enough:

```text
You can make extensions to the standard 
with "x-" mechanism in order to fulfill 
any industry specific needs. 

A suggestive example below 

pricingPlans:
  en:
  - name: Premium subscription 1 year
    unit: Recurring
    priceCurrency: EUR
    price: "50.00"
    billingDuration: year
    
  - x-name: Extension plan
    unit: custom
    priceCurrency: EUR
    price: "50.00"
    billingDuration: year
    
```

**Referencing Capability in Pricing Plans** 

ODPS 4.0 introduces a modular referencing system that allows pricing plans to reuse pre-defined components such as data quality profiles, SLA tiers, access methods, and payment gateways. This makes it easy to maintain consistency across multiple data products, reduces duplication, and enables scalable pricing design. Why Use Referencing?

- **DRY Principle**: Define components once, reference them across products.
- **Modularity**: Maintain separate, reusable blocks for SLA, DQ, access, and payment.
- **Flexibility**: Switch plans or upgrade tiers by simply changing references.
- **Auditability**: Easily trace the source of configurations in machine-readable format.

**Example Component Reference Paths**

* SLA: `#/product/SLA/declarative/gold` references gold SLA profile in the SLA component
* Data Quality: `#/product/dataQuality/declarative/default` references default data quality profile in the data quality component
* Access: `#/product/dataAccess/download` references download access profile in the data access component
* Payment Gateway: `#/product/paymentGateways/paypal` references paypal payment profile in the Payment Gateways component

In each of these component groups, you can expect a `default` option to be defined. This default serves as a baseline configuration, ensuring that even when no custom profile is referenced, a reliable and predictable fallback exists. For example, dataQuality.default, SLA.default, and paymentGateways.default can all be used to provide minimum guarantees. 


**Includes the "Pricing Plans as Code" feature.** You can define the necessary actions (CRUP) to set up and use the selected payment gateway, initiating the purchase process. **CRUP** stands for: 

- **C**reate (create pricing plan), 
- **R**etire (delete pricing plan), 
- **U**pdate (update existing pricing plan) and,
- **P**urchase (generate or get link to ignite purchase process in the gateway). 

With this feature, you can translate the pricing plans defined in the declarative part into executable code within payment gateways. 

**Supported payment gateways:**

- Stripe [Docs](https://docs.stripe.com/cli), 
- Checkout [Docs](https://api-reference.checkout.com),
- Square [Docs](https://developer.squareup.com/docs),
- Paypal [Docs](https://developer.paypal.com/api/nvp-soap/payflow/integration-guide/),
- Custom

## ODPS supports 12 standardized pricing models

The _unit_ attribute defines the plan and options for that are fixed unless extended with "x-" mechanism. 

| <div style="width:150px">Pricing plan</div>   | Description | 
|---|---|
| **Recurring time period based** | In the simplest terms, recurring payments (also known as subscription payments, automatic payments, or recurring billing) take place when customers authorize a merchant to charge them repeatedly for goods or services on a prearranged schedule.|
| **One time payments plans** | One Time Fee Revenue Model is a business model that generates revenue through a single payment for perpetual product use or service access. The One Time Fee Revenue Model is a fundamental concept in the world of small businesses and entrepreneurship. |
| **Pay-as-you-go plans** | The Pay As You Go Plan is a flexible alternative to a monthly plan. Instead of paying a recurring monthly charge, you buy credits as needed. |
| **Revenue sharing plans** | Revenue sharing is a performance-based income model that involves sharing business profits or losses among participating partners. Revenue sharing is a profit-sharing system that ensures all parties involved are compensated for their contribution to the business. |
| **Data volume plan** | Volume pricing is a pricing strategy in which an item's price per unit decreases as the purchase quantity increases. |
| **Trial** | A free trial pricing strategy offers target customers a chance to try your product for free for a limited time. It is a sales promotion technique that uses the product to market itself.  |
| **Dynamic pricing** | Dynamic pricing is a pricing strategy that applies variable prices instead of fixed prices. Instead of deciding on a set price for a season, retailers can update their prices multiple times per day to capitalize on the ever-changing market. |
| **Pay what you want plans** |  Also known as PWYW pricing, is a pricing strategy in which buyers pay the desired price for a particular product, commodity, or service. The approach may sometimes lead to the value of zero. Following the buyer's guidance, one can set a suggested price and a minimum price. |
| **Freemium** |  A type of business model that offers basic features of a product or service to users at no cost and charges a premium for supplemental or advanced features. |
| **Open data** | Access to open data is expected to be free of cost, but in some cases it is also possible to collect fees to cover costs of the service.  |
| **Value-based** | Value-based pricing is a strategy of setting prices primarily based on a consumer's perceived value of a product or service. Value-based pricing is customer-focused, meaning companies base their pricing on how much the customer believes a product is worth. Often worth to provide customer a value simulator to see expected value gains and possibly set the price based on that. Pricing would be customized per customer. |
| **On Request** | Access to data product is given only on request. Often provider expects customer to meet provider first. In the discussions conditions, pricing etc are agreed. |


## Pricing Plans optional attributes and elements

> Example of Pricing component usage in english:

```yml

pricingPlans:
  declarative:
    en:
      - name: Standard API subscription 1 month
        priceCurrency: EUR
        price: "50"
        billingDuration: month
        unit: Recurring
        maxTransactionQuantity: 200000
        offering:
          - High Quality Events data
          - High amount of transactions
          - Billed monthly
        paymentGateway:
          $ref: '#/product/paymentGateways/default'
        dataQuality:
          $ref: '#/product/dataQuality/declarative/default'
        SLA:
          $ref: '#/product/SLA/declarative/default'
        access:
          $ref: '#/product/dataAccess/API'
      - name: Premium MCP 1 month
        priceCurrency: EUR
        price: "500"
        billingDuration: month
        unit: Recurring
        maxTransactionQuantity: 0
        offering:
          - High Quality Events data
          - High amount of transactions
          - Billed monthly
        paymentGateway:
          $ref: '#/product/paymentGateways/agent'
        dataQuality:
          $ref: '#/product/dataQuality/declarative/premium'
        SLA:
          $ref: '#/product/SLA/declarative/premium'
        access:
          $ref: '#/product/dataAccess/agent'
          
  executable:
    - name: Premium subscription 1 year
      type: Stripe
      reference: urls to Stripe docs
      create:
        spec:
          - cmd: stripe products create  \
            params: '--name="Premium subscription 1 year"'
          - cmd: stripe prices create  \
            params: '--currency=eur --unit-amount=50 -d "recurring[interval]"=month -d "product_data[name]"="Premium subscription 1 year"'
      read:
        spec:
          - cmd: stripe products get  \
            params: '--name="Premium subscription 1 year"'
      update:
        spec:
          - cmd: stripe products update  \
            params: '--name="Premium subscription 1 year"'
      delete:
        spec:
          - cmd: stripe products delete  \
            params: '--name="Premium subscription 1 year"'
  

```

| <div style="width:150px">Element name</div>   | Type  | Options  | Description  |
|---|---|---|---|
| **pricingPlans** | element | - | Binds the pricing plans related elements and attributes together |
| **en** | element | [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) defined 2-letter codes | **NOTE! This is a dynamic element!** This element binds together other product pricing plan attributes and expresses the langugage used. In the example this is "en", which indicates that pricing plan details are in English. If you would like to use French details, then name the element "fr". The naming of this element follows options (language codes) listed in [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) standard. <br/><br/> You can have product pricing plan details in multiple languages simply by adding similar sets like the example - just change the binding element name to matching language code. <br/><br/> The pattern to implement multilanguage support for data products was adopted from de facto UI translation practices. The attributes inside this element are commonly rendered in the UI for the consumer and providing a simple way to implement that was the driving reasoning. See for example  [JSON - Multi Language](https://simplelocalize.io/docs/file-formats/multi-language-json/) |
| **declarative** | element | - | Grouping element which collects together data product pricing plans with business details |
| **name** | attribute | string | Name of the pricing plan. |
| **priceCurrency** | string  |  Use standard formats: [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) currency format e.g. "USD"; Ticker symbol for cryptocurrencies e.g. "BTC"  |  The primary currency used in pricing. Platforms are assumed to use this as primary currency if currency conversions are used to display product pricing in different locations for various currencies. If the *unit* is revenue-sharing, then this attribute value MUST be percentage.  |
| **price** | string  | -  | The offer price of a product, or of a price component, or revenue-sharing percentage. <br/><br/> If the *unit* of pricing is revenue-sharing, then this *price* attribute value is percentage value. <br/><br/> Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid using these symbols as a readability separator. Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially similiar Unicode symbols. <br/><br/>With *data-volume* the price is for each 1GB of data. |
| **billingDuration** | string  | options: instant, day, week, month, year  | Specifies for how long this price (or price component) will be billed. Can be used, for example, to model the contractual duration of a subscription or payment plan.  |
| **unit** | string | One of: One-time-payment, Pay-per-use, Recurring, Revenue-sharing, Data-volume , Pay-what-you-want, Freemium, Open-data, Value-based, On-request, Trial | One-time-payment is for single time purchase purposes, further purchaces are not intended to continue under same agreement. <br/><br/> *Pay-per-use* is intended for continuous usage and price set is for each successful usage action. <br/><br/> *Recurrring* is intended for continuous time period plans. <br/><br/>*Revenue sharing* is a performance-based income model. An effective revenue sharing deal structure is offering your expertise to a business owner to help them grow their business. In return, you get paid a percentage of the revenue as a royalty fee. <br/><br/> *Freemium* is for free access. Use this option also for open data. <br/><br/> *Data-volume* is for data amount based pricing in which customer pays based on the served data amount. The price is always for 1GB of data. <br/><br/> *Pay-what-you-want*  is a pricing system where buyers pay any desired amount for a given commodity, sometimes including zero. In some cases, a minimum (floor) price may be set, and/or a suggested price may be indicated as guidance for the buyer. The buyer can also select an amount higher than the standard price for the commodity. If the floor price is set, use *minPrice* attribute. <br/><br/> *Open-data*  is an explicit pricing plan category for open data. By default open data should be free, but in some cases it can have a price. <br/><br/> *Value-based* is value-based selling unit. Present the outcome of your story with solid data and a measurable impact with help of *offering* attribute. Example: “We can lower the energy bill in heating by $8-13/square meter in a year. Try out simulator to calculate your value!”. Use optional *valueSimulator* attribute to provide link (URL) to value simulator you have created. In order to set base fee for value-based plan, you can for example set monthly (*billingDuration*) plan with base see with help of *minPrice* attribute. <br/><br/> *On-request* is for plans in which customer is given access to data product after contacting provider. Use provider contact information in providing means to contact data product provider for access permissions request. If the *trial* is used, then trial duration should be defined in the *offering* part. <br/><br/> Read more about the [Pricing plans from ODPS wiki](https://github.com/Open-Data-Product-Initiative/dev/wiki/Pricing-Plans#version-dev)|
| **maxTransactionQuantity** | Integer |  Integer | The maximum transaction quantity for the given billing duration. Use this to define for example monthly (or any other period) request limit to the data product. Note! If you want to set unlimited use, value must be 0 (zero). |
| **offering**  | string | array | The element that contains pricing plan content as array of strings. Think of this as the list of what is included in the pricing plan and what you offer in return to the price asked. Use the language defined in the *plan* |
|  **minPrice** | string  | -  | The lowest price if the price is a range. If dynamic pricing is used with this product, this is the lowest price allowed. In dynamic pricing businesses are able to change prices based on algorithms that take into account competitor pricing, supply and demand, and other external factors in the market. Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid using these symbols as a readability separator. Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially similiar Unicode symbols. |
|  **maxPrice** | string  | -  | The highest price if the price is a range. If dynamic pricing is used with this product, this is the highest price allowed. Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid using these symbols as a readability separator. Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially similiar Unicode symbols. |
| **valueAddedTaxIncluded**  | boolean  | true/false  | Specifies whether the applicable value-added tax (VAT) is included in the price specification or not.  |
| **valueAddedTaxPercentage**  | Integer  | Number percentage value, range 0-100 | Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid using these symbols as a readability separator. Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially similiar Unicode symbols.   |
| **validFrom**  | DateTime  |  A combination of date and time in [ISO 8601](https://www.ionos.com/digitalguide/websites/web-development/iso-8601/) format yyyy-MM-dd'T'HH:mm:ss.SSSZ. | The date when the item becomes valid. |
| **validTo**  | DateTime  | A combination of date and time in [ISO 8601](https://www.ionos.com/digitalguide/websites/web-development/iso-8601/) format yyyy-MM-dd'T'HH:mm:ss.SSSZ.  | The date after when the item is not valid. |
| **additionalPrice**  | string  | -  | This is used to define fees for usage which exceeds the defined max transaction quantity. This value is for each additional transaction. Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid using these symbols as a readability separator. Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially similiar Unicode symbols. |
|  **maxDataQuantity** | Integer  | -  | The maximum amount of data transferred during the billing duration. Unit is GB. |
|  **valueSimulator**  | url | valid url | Intended to be used with *value-based* pricing plan. Provide url to value simulator in which customer can see the value in various cases. In the simulator customer might be able to input own variables to match their exact case and see the gained value. |
| **notes** | string | - | Optional free-text explanatory note associated with the pricing plan. Often used for disclaimers, internal remarks, or elaborating on intent.  |
| **paymentGateway** | reference | path to paymentGateways | Reference to an available payment gateway definition under #/product/paymentGateways/... More details in [Knowledge Base](https://opendataproducts.org/howto/) |
| **dataQuality** | reference | path to dataQuality | Reference to a defined data quality package from #/product/dataQuality/... More details in [Knowledge Base](https://opendataproducts.org/howto/) |
| **SLA** | reference | path to SLA | Reference to a defined SLA specification under #/product/SLA/... More details in [Knowledge Base](https://opendataproducts.org/howto/)|
| **access** | reference | path to dataAccess | Reference to a data access method under #/product/dataAccess/... More details in [Knowledge Base](https://opendataproducts.org/howto/)|
| **executable** | element | - | Grouping element which collects together pricing plans payment gateway management features. You can define the needed action (CRUP) to setup and use the gateway to ignite purchase process. <br/><br/> CRUP stands for: **C**reate, **R**etire, **U**pdate, and **Purchase**.  The actual as code part is added with _spec_ element. |
| **type** | attribute | string, one of: _Stripe_, _Checkout_, _Custom_ | Payment gateway system name. Use one of the predefined options only. With _Custom_ type you can use your in-house solution. |
| **version** | attribute | string | The version of the payment gateway tool used. |
| **reference** | URL | Valid URL | Provide URL pointing to the reference documentation |
| **create** | element | - | Contains the as code part to create pricing plan in the payment gateway |
| **retire** | element | - | Contains the as code part to retire (delete) pricing plan in the payment gateway |
| **update** | element | - | Contains the as code part to update pricing plan in the payment gateway |
| **purchase** | element | - | Contains the as code part to create or get pricing plan purchase igniting link in the payment gateway |
| **spec** | element | YAML/URL/string | The content the as code part for the pricing plan. Content is intended to be in a form that can be injected as is to _type_ defined payment gateway system. Content depends of the system used and reference attribute is expected to provide more information. <br/><br/> **Note!** By default the rules must be provide as valid YAML, either as inline element (YAML) or as valid URL (filesystem or online) pointing to valid YAML content file. String content is allowed and used only if _type_ attribute value is _Custom_. In the custom case your string of course can be YAML too. |

If you see something missing, described inaccurately or plain wrong, or you want to comment the specification, [raise an issue in Github](https://github.com/Open-Data-Product-Initiative/dev/issues)


Join the [ODPS Discord](https://discord.gg/7KfnFxAc) to discuss the ideas and your needs!
