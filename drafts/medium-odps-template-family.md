# ODPS Template Family: Smaller Starting Points for Real Data Products

ODPS v4.1 can describe a broad range of data products. That is the point of a standard: it must be complete enough for different organizations, products, access patterns, contracts, governance needs, and operational models.

But completeness creates a practical adoption problem.

Most teams do not begin with a complete data product description. They usually begin with a name, an owner, a rough purpose, and a few known facts. Later they add access methods, quality expectations, service levels, licensing, pricing, or agent-facing interfaces.

If the first example a user sees is the full schema, the standard can look heavier than it really is. The problem is not the schema. The problem is the starting point.

That is why ODPS now introduces a template family.

## Templates, not new schema types

The ODPS template family is not a new schema layer. It does not introduce a mandatory `template`, `profile`, or `maturityLevel` field.

The templates are reusable YAML skeletons built from the existing ODPS schema areas. A user or tool can copy a skeleton, replace typed placeholders, validate the completed file with the normal ODPS schema, and extend it with additional ODPS components when needed.

This distinction matters.

Templates should help people start faster without fragmenting the standard. They should guide adoption without creating competing dialects of ODPS.

## Two ways to choose a template

There are two common situations when describing a data product.

The first is about product intent:

- Is this a reusable data product?
- Is it an analytical product?
- Is it consumed by AI agents or automation?
- Is it sold, licensed, contracted, or offered through a marketplace?

The second is about description maturity:

- Do we only know the basic product identity?
- Do we know ownership, use cases, and business context?
- Do we also know access, quality, service expectations, and support?

These are different questions. A useful template family should support both.

## Templates by product purpose

The first group helps users choose a skeleton based on what kind of product they are describing.

| Template | Use when |
|---|---|
| ODPS Product Profile | Any data product needs a minimal description with identity, holder, status, and visibility. |
| ODPS Reusable Data Product | The product packages reusable data for trusted consumption. |
| ODPS Analytical Product | The product delivers insight, reporting, indicators, or decision support. |
| ODPS Agentic Product | The product is consumed by AI agents, AI applications, workflows, automation, or machine-to-machine processes. |
| ODPS Marketplace Product | The product is offered under controlled, priced, licensed, contractual, or marketplace terms. |

This group keeps the naming close to the purpose of the product.

It also avoids a common mistake: treating access methods as product templates. API, SQL, file, MCP, GraphQL, gRPC, and AI are access patterns. In ODPS, they belong inside `product.dataAccess`. A single product can have several access methods, and those access methods can change without changing what the product is.

## Templates by description maturity

The second group supports a staged path. It is for cases where the product description becomes richer over time.

| Template | Use when |
|---|---|
| ODPS Product Brief | Only basic identity, value proposition, lifecycle state, and product type are known. |
| ODPS Product Definition | Ownership, business context, categories, tags, and use cases are known, but operational access and service terms are not complete. |
| ODPS Product Operating Model | Operational access, quality expectations, SLA expectations, and support metadata are known. |

This is a maturity path for the description, not a quality ranking for the product.

That difference is important. Labels such as Bronze, Silver, and Gold can imply perceived quality, internal platform tiers, or organization-specific governance stages. They are useful in some internal operating models, but they are poor names for portable standard templates.

In ODPS, a product can start as a brief and later become a definition or operating model as more facts become known. That progression does not change the product's purpose. It only makes the product description more complete.

## Typed placeholders make skeletons tool-friendly

The skeleton files use typed placeholders such as:

```yaml
name: "{{string}}"
productID: "{{string}}"
visibility: "{{enum: private | invitation | organisation | dataspace | public}}"
objective: "{{integer}}"
email: "{{string: email}}"
```

The goal is to make the skeleton useful for both humans and tools.

A human can immediately see what kind of value is expected. A tool can use the placeholder type to generate forms, validate input, or guide completion before the final ODPS file is validated against the schema.

The placeholders are not intended to be final values. They are scaffolding.

## Purpose templates and maturity templates can work together

The two groups are not competing taxonomies.

For example, a team might start with an ODPS Product Brief because only a small amount of information is known. Later, when the product becomes clearer, the team might choose the ODPS Reusable Data Product template because the product packages reusable data with quality expectations and defined access.

Another team might start directly with the ODPS Agentic Product template because the product is already known to serve AI workflows through MCP and API access.

The practical rule is simple:

Start with what you know.

If you know the product purpose, choose a purpose template. If you only know the amount of information available, choose a description maturity template. In both cases, the completed file remains an ODPS document.

## Why this matters for adoption

Standards fail when they require too much ceremony before users see value.

The ODPS template family gives teams a smaller first step. It makes the standard easier to approach without reducing what the standard can express.

It also creates better entry points for tooling:

- Catalog tools can offer the Product Profile or Product Brief as the first registration flow.
- Data product platforms can package reusable, analytical, agentic, and marketplace skeletons as guided creation paths.
- Governance tooling can move products from brief to operating model as the required metadata becomes available.
- SDKs and generators can use typed placeholders to create valid, schema-aligned drafts.

The result is a more practical adoption path.

Teams do not need to learn the whole ODPS schema before writing their first product description. They can start with a focused skeleton, then grow the description as the product matures.

## The principle

The template family follows one principle:

Do not make users choose between simplicity and correctness.

The first ODPS file should be small enough to write. The later ODPS file should be complete enough to operate, govern, contract, automate, and reuse.

Templates make that path visible.

---

Suggested tags: `Data Products`, `Open Data Product Specification`, `Data Governance`, `Data Mesh`, `AI Agents`
