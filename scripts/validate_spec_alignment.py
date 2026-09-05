#!/usr/bin/env python3
"""Validate ODPS docs, examples, and schema alignment."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
INCLUDES = SOURCE / "includes"
EXAMPLES = SOURCE / "examples"
JSON_SCHEMA_PATH = SOURCE / "schema" / "odps.json"
YAML_SCHEMA_PATH = SOURCE / "schema" / "odps.yaml"

IGNORED_DYNAMIC_KEYS = {
    "$ref",
    "en",
    "default",
    "premium",
    "gold",
    "dataonly",
    "API",
    "Agent",
    "agent",
}

COMPONENT_ROOTS = {
    "contract": ("product", "contract"),
    "details": ("product", "details"),
    "pricingPlans": ("product", "pricingPlans"),
    "SLA": ("product", "SLA"),
    "dataQuality": ("product", "dataQuality"),
    "dataAccess": ("product", "dataAccess"),
    "paymentGateways": ("product", "paymentGateways"),
    "license": ("product", "license"),
    "dataHolder": ("product", "dataHolder"),
}

FORBIDDEN_TEXT_PATTERNS = {
    "legacy outputPorttype spelling": r"\boutputPorttype\b",
    "legacy dataHolder businessId spelling": r"\bbusinessId\b",
    "legacy displayTitle spelling": r"\bdisplayTitle\b",
    "lowercase recurring pricing unit": r"\bunit:\s+recurring\b",
    "short SLA reference path": r"#/product/SLA/(?:default|premium|gold)\b",
    "short dataQuality reference path": r"#/product/dataQuality/(?:default|premium)\b",
}


@dataclass
class Failure:
    check: str
    location: str
    message: str

    def render(self) -> str:
        return f"[{self.check}] {self.location}: {self.message}"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text())


def yaml_blocks(path: Path) -> list[tuple[int, str]]:
    text = path.read_text(errors="ignore")
    pattern = re.compile(r"```(?:ya?ml)\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)
    return [(index, match.group(1)) for index, match in enumerate(pattern.finditer(text), 1)]


def is_v41_document(value: Any) -> bool:
    if not isinstance(value, dict) or "product" not in value:
        return False
    schema = str(value.get("schema", ""))
    return "v4.1/schema/odps" in schema


def has_template_placeholders(value: Any) -> bool:
    return isinstance(value, str) and "{{" in value and "}}" in value


def contains_placeholder(value: Any) -> bool:
    if value is None:
        return True
    if has_template_placeholders(value):
        return True
    if isinstance(value, str) and "selected dimension" in value:
        return True
    if isinstance(value, dict):
        return any(contains_placeholder(child) for child in value.values())
    if isinstance(value, list):
        return any(contains_placeholder(child) for child in value)
    return False


def is_ref_only(value: Any) -> bool:
    return isinstance(value, dict) and set(value) == {"$ref"}


def is_ref_map(value: Any) -> bool:
    return isinstance(value, dict) and bool(value) and all(is_ref_only(child) for child in value.values())


def should_schema_validate(value: Any) -> bool:
    return not contains_placeholder(value) and not is_ref_only(value) and not is_ref_map(value)


def is_complete_v41_document(value: Any) -> bool:
    return (
        is_v41_document(value)
        and isinstance(value.get("product"), dict)
        and "details" in value["product"]
    )


def pointer(schema: dict[str, Any], path: tuple[str, ...]) -> dict[str, Any] | None:
    current: Any = schema
    for part in path:
        if not isinstance(current, dict):
            return None
        current = current.get("properties", {}).get(part)
        if isinstance(current, dict) and "$ref" in current:
            current = resolve_ref(schema, current["$ref"])
    return current if isinstance(current, dict) else None


def resolve_ref(schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"external $ref not supported in validation script: {ref}")
    current: Any = schema
    for part in ref[2:].split("/"):
        current = current[part]
    return current


def validate_instance(
    failures: list[Failure],
    check: str,
    location: str,
    instance: Any,
    schema: dict[str, Any],
) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    for error in errors:
        path = "/" + "/".join(str(part) for part in error.path)
        failures.append(Failure(check, f"{location}{path}", error.message))


def standalone_subschema(root_schema: dict[str, Any], subschema: dict[str, Any]) -> dict[str, Any]:
    result = dict(subschema)
    if "$schema" in root_schema:
        result.setdefault("$schema", root_schema["$schema"])
    if "$defs" in root_schema:
        result.setdefault("$defs", root_schema["$defs"])
    return result


def validate_markdown_yaml_examples(
    failures: list[Failure],
    json_schema: dict[str, Any],
    yaml_schema: dict[str, Any],
) -> None:
    files = sorted(INCLUDES.glob("*.md")) + [SOURCE / "index.html.md"]
    for path in files:
        for index, block in yaml_blocks(path):
            location = f"{path.relative_to(ROOT)} fenced yaml block #{index}"
            try:
                parsed = yaml.safe_load(block)
            except Exception as exc:  # noqa: BLE001 - report parser's exact message
                failures.append(Failure("markdown-yaml-parse", location, str(exc).splitlines()[0]))
                continue

            if parsed is None:
                failures.append(Failure("markdown-yaml-parse", location, "empty YAML block"))
                continue

            if is_complete_v41_document(parsed) and should_schema_validate(parsed):
                validate_instance(failures, "markdown-v41-json-schema", location, parsed, json_schema)
                validate_instance(failures, "markdown-v41-yaml-schema", location, parsed, yaml_schema)
                continue

            if isinstance(parsed, dict) and len(parsed) == 1:
                root_key = next(iter(parsed))
                if root_key in COMPONENT_ROOTS and should_schema_validate(parsed[root_key]):
                    json_subschema = pointer(json_schema, COMPONENT_ROOTS[root_key])
                    yaml_subschema = pointer(yaml_schema, COMPONENT_ROOTS[root_key])
                    if json_subschema:
                        validate_instance(
                            failures,
                            "component-json-schema",
                            location,
                            parsed[root_key],
                            standalone_subschema(json_schema, json_subschema),
                        )
                    if yaml_subschema:
                        validate_instance(
                            failures,
                            "component-yaml-schema",
                            location,
                            parsed[root_key],
                            standalone_subschema(yaml_schema, yaml_subschema),
                        )


def validate_standalone_yaml_examples(
    failures: list[Failure],
    json_schema: dict[str, Any],
    yaml_schema: dict[str, Any],
) -> None:
    for path in sorted(EXAMPLES.rglob("*.yml")):
        location = str(path.relative_to(ROOT))
        try:
            parsed = load_yaml(path)
        except Exception as exc:  # noqa: BLE001 - report parser's exact message
            failures.append(Failure("example-yaml-parse", location, str(exc).splitlines()[0]))
            continue

        if is_complete_v41_document(parsed) and should_schema_validate(parsed):
            validate_instance(failures, "example-v41-json-schema", location, parsed, json_schema)
            validate_instance(failures, "example-v41-yaml-schema", location, parsed, yaml_schema)


def collect_keys(value: Any, keys: set[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key not in IGNORED_DYNAMIC_KEYS:
                keys.add(str(key))
            collect_keys(child, keys)
    elif isinstance(value, list):
        for child in value:
            collect_keys(child, keys)


def validate_hello_world_text_alignment(failures: list[Failure]) -> None:
    path = INCLUDES / "_helloworld.md"
    blocks = yaml_blocks(path)
    if len(blocks) != 1:
        failures.append(Failure("hello-world", str(path.relative_to(ROOT)), "expected exactly one YAML block"))
        return

    try:
        parsed = yaml.safe_load(blocks[0][1])
    except Exception as exc:  # noqa: BLE001
        failures.append(Failure("hello-world-parse", str(path.relative_to(ROOT)), str(exc).splitlines()[0]))
        return

    keys: set[str] = set()
    collect_keys(parsed, keys)
    spec_text = "\n".join(
        file.read_text(errors="ignore")
        for file in sorted(INCLUDES.glob("*.md")) + [SOURCE / "index.html.md"]
        if file.name != "_helloworld.md"
    )
    for key in sorted(keys):
        pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(key)}(?![A-Za-z0-9_])")
        if not pattern.search(spec_text):
            failures.append(
                Failure(
                    "hello-world-text-alignment",
                    f"{path.relative_to(ROOT)} key {key}",
                    "key is used in hello world but not defined or mentioned in the textual spec",
                )
            )

    for ref in find_refs(parsed):
        if ref.startswith("#/") and not internal_pointer_exists(parsed, ref):
            failures.append(
                Failure(
                    "hello-world-ref-resolution",
                    f"{path.relative_to(ROOT)} {ref}",
                    "internal reference does not resolve in the hello world document",
                )
            )


def find_refs(value: Any) -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref" and isinstance(child, str):
                refs.append(child)
            else:
                refs.extend(find_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.extend(find_refs(child))
    return refs


def internal_pointer_exists(document: Any, ref: str) -> bool:
    current = document
    for raw_part in ref[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return False
    return True


def normalize_type(schema_node: dict[str, Any]) -> set[str]:
    value = schema_node.get("type")
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {str(item) for item in value}
    if "oneOf" in schema_node:
        result: set[str] = set()
        for item in schema_node["oneOf"]:
            if isinstance(item, dict):
                result.update(normalize_type(item))
        return result
    return set()


def validate_schema_alignment(
    failures: list[Failure],
    json_schema: dict[str, Any],
    yaml_schema: dict[str, Any],
) -> None:
    Draft202012Validator.check_schema(json_schema)
    Draft202012Validator.check_schema(yaml_schema)

    for path in [(), ("product",)]:
        json_node = pointer(json_schema, path) if path else json_schema
        yaml_node = pointer(yaml_schema, path) if path else yaml_schema
        json_props = set(json_node.get("properties", {}))
        yaml_props = set(yaml_node.get("properties", {}))
        if json_props != yaml_props:
            failures.append(
                Failure(
                    "schema-property-alignment",
                    "/" + "/".join(path) if path else "/",
                    f"JSON-only {sorted(json_props - yaml_props)}; YAML-only {sorted(yaml_props - json_props)}",
                )
            )

    important_paths = [
        ("version",),
        ("product", "details"),
        ("product", "contract"),
        ("product", "SLA"),
        ("product", "dataQuality"),
        ("product", "pricingPlans"),
        ("product", "dataAccess"),
        ("product", "paymentGateways"),
        ("product", "license"),
        ("product", "dataHolder"),
    ]
    for path in important_paths:
        json_node = pointer(json_schema, path)
        yaml_node = pointer(yaml_schema, path)
        if not json_node or not yaml_node:
            failures.append(Failure("schema-node-alignment", "/" + "/".join(path), "missing in one schema"))
            continue
        json_type = normalize_type(json_node)
        yaml_type = normalize_type(yaml_node)
        if json_type and yaml_type and json_type.isdisjoint(yaml_type):
            failures.append(
                Failure(
                    "schema-type-alignment",
                    "/" + "/".join(path),
                    f"JSON type {sorted(json_type)} does not overlap YAML type {sorted(yaml_type)}",
                )
            )

    json_access = resolve_ref(json_schema, "#/$defs/DataAccessItem")
    if "outputPortType" not in json_access.get("properties", {}):
        failures.append(Failure("schema-canonical-field", "#/$defs/DataAccessItem", "missing outputPortType"))

    yaml_access = pointer(yaml_schema, ("product", "dataAccess"))
    yaml_required = yaml_access.get("additionalProperties", {}).get("required", []) if yaml_access else []
    if "outputPortType" not in yaml_required:
        failures.append(Failure("schema-canonical-field", "/product/dataAccess", "outputPortType is not required"))


def validate_forbidden_drift(failures: list[Failure]) -> None:
    files = sorted(INCLUDES.glob("*.md")) + [SOURCE / "index.html.md", JSON_SCHEMA_PATH, YAML_SCHEMA_PATH]
    for path in files:
        text = path.read_text(errors="ignore")
        for label, pattern in FORBIDDEN_TEXT_PATTERNS.items():
            match = re.search(pattern, text)
            if match:
                line = text[: match.start()].count("\n") + 1
                failures.append(Failure("forbidden-drift", f"{path.relative_to(ROOT)}:{line}", label))


def main() -> int:
    failures: list[Failure] = []
    json_schema = load_json(JSON_SCHEMA_PATH)
    yaml_schema = load_yaml(YAML_SCHEMA_PATH)

    try:
        validate_schema_alignment(failures, json_schema, yaml_schema)
    except Exception as exc:  # noqa: BLE001
        failures.append(Failure("schema-load", "source/schema", str(exc)))

    validate_markdown_yaml_examples(failures, json_schema, yaml_schema)
    validate_standalone_yaml_examples(failures, json_schema, yaml_schema)
    validate_hello_world_text_alignment(failures)
    validate_forbidden_drift(failures)

    if failures:
        print(f"Spec alignment validation failed with {len(failures)} issue(s):")
        for failure in failures:
            print(f"- {failure.render()}")
        return 1

    print("Spec alignment validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
