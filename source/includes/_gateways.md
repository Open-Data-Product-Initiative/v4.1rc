# Payment Gateways

The `paymentGateways` object in ODPS defines how **transactions are handled** when pricing plans require financial exchanges—whether from humans or AI agents. It allows you to describe and configure multiple named gateway setups (e.g., `default`, `Agent`, `PremiumStripe`) that can be **referenced from pricing plans**.

Each gateway definition provides a structured way to:

- Describe the payment system (e.g., Stripe, Axio, Custom)
- Point to relevant documentation (`reference`)
- Include executable or declarative configuration under `spec`

This component enables flexible monetization strategies, including differentiated billing models for human users vs. machine users, and support for both traditional and agent-native payment protocols.

**Referencing Payment Gateways:**
Named gateway definitions (e.g., `default`, `Agent`) can be **reused across pricing plans** using `$ref`. This ensures consistent payment logic, minimizes duplication, and allows you to tie multiple plans to a single gateway configuration. More details in the [Knowledge Base](https://opendataproducts.org/howto/).

**Benefits of Referencing:**

- **Centralization**: Maintain payment logic in one place and link to it from many pricing plans.
- **Consistency**: Ensure all monetized components use the same gateway logic, version, and authentication flow.
- **Flexibility**: Easily create alternative gateways for specific user segments (e.g., AI agents vs. humans).
- **Transparency**: Documented specs help consumers understand how billing works—and let machines integrate autonomously.

> referencing examples:

```text
  $ref: '#/Product/paymentGateways/default'

  ...

  $ref: '#/Product/dataQuality/agent'
```

**The Role of `default`:**
Whenever the `paymentGateways` object is used, a gateway named `default` is **expected and required**. It serves as the **primary or fallback payment method** and enables compatibility even in simpler configurations that only need one payment integration.

Use the `default` gateway when:

- You want to offer a single, unified payment method (e.g., Stripe for API consumption)
- You’re not using tiered monetization or segmentation
- You want to future-proof your YAML to support pricing plan evolution

Other named gateways (e.g., `Agent`, `premiumStripe`) can be added freely as needed.

## Optional attributes and elements

> Example of Payment Gateways object usage:

```yml

paymentGateways:
  default:
    description:
      en: API consumption payment gateway for humans
    type: Stripe
    version: '1'
    reference: 'https://docs.stripe.com/'
    spec: |
      // Replace this with your actual implementation or link
      stripe.createCheckoutSession({
        amount: 100, // in cents
        currency: 'usd',
        success_url: 'https://your-platform.com/success',
        cancel_url: 'https://your-platform.com/cancel'
      });

  Agent:
    description:
      en: Payment gateway for AI agents
    type: Axio
    version: '1'
    reference: 'https://www.x402.org/'
    spec: |
      paymentMiddleware("0xYourAddress", {"/your-endpoint": "$0.01"});
```

> Example of Payment Gateways external profiles usage:

```yml

paymentGateways: # the below file contains the same content as above
  $ref: 'https://example.org/gateways/all-packages.yaml'

```

> Example of extenal Payment Gateway for each profile usage:

```yml

paymentGateways:
    default:
      $ref: 'https://example.org/gateways/basic.yaml'
    premium:
      $ref: 'https://example.org/gateways/premium.yaml'
```

| <div style="width:150px">Element name</div>   | Type  | Options  | Description  |
|---|---|---|---|
| **paymentGateways** | object | - | Object containing all defined payment gateway configurations. Each key is a named reference (e.g. `default`, `agent`) that can be reused in pricing plans. |
| **$ref** | filepath or valid URL | - | Define the Payment Gateway profiles in external file for reuse purposes, example  `$ref: 'https://example.org/gateways/all-packages.yaml'` See example. This makes it easy to keep related profiles (e.g. default, API, agent) together, apply versioning and validation once, and publish all variants from a single repo or source. <br/><br/>The same pattern can be used in individual Payment Gateway profiles instead of doing it inline. See example. This gives finer control if each Payment Gateway is owned or updated by a different team, but increases the number of files to track and host.|
| **default** | object | - | Named default payment gateway used. If you use paymentGateways object, this default is expected to be first option and is defined always. Can be referenced using `$ref: '#/paymentGateways/default'`. <br/> <br/> In the example, _agent_ payment gateway as an example of freely named gateway which can be referenced using `$ref: '#/paymentGateways/agent'`. You can follow the same pattern and create more |
| **description** | object | string [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) | Multilingual descriptions of the payment gateway. Enables UI rendering in multiple languages. |
| **type** | string | Stripe, Axio, Checkout, Custom | Defines the payment system or protocol used. Use predefined values. `Custom` allows custom or internal solutions. |
| **version** | string | Free-form version label | Indicates the version of the payment gateway specification, SDK, or integration logic. |
| **reference** | URL | Valid URL | Points to documentation or developer reference for the payment gateway system. |
| **spec** | string / YAML / URL | - | Contains the executable or declarative logic for the payment gateway integration. Can be inline YAML, stringified logic, or link to external file. |
