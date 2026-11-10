"""Duplicate-key checks shared by knowledge-pipeline YAML inputs."""

import pytest
import yaml
from strict_yaml import parse_yaml


def test_nested_duplicates_include_both_source_locations() -> None:
    with pytest.raises(yaml.YAMLError, match="duplicate key 'fr'") as error:
        parse_yaml("labels:\n  fr: first\n  en: second\n  fr: third\n", source="concepts.yml")

    message = str(error.value)
    assert '"concepts.yml", line 2' in message
    assert '"concepts.yml", line 4' in message


def test_explicit_override_of_yaml_merge_remains_valid() -> None:
    data = parse_yaml(
        "defaults: &base {fr: Bonjour, en: Hello}\nlabels: {<<: *base, fr: Salut}\n",
        source="example.yml",
    )
    assert data["labels"] == {"fr": "Salut", "en": "Hello"}


def test_duplicate_merge_keys_are_rejected() -> None:
    text = "base: &base {x: 1}\nitem:\n  <<: *base\n  <<: *base\n"
    with pytest.raises(yaml.YAMLError, match="duplicate key '<<'"):
        parse_yaml(text, source="example.yml")


def test_unsafe_yaml_constructors_remain_disabled() -> None:
    with pytest.raises(yaml.YAMLError):
        parse_yaml("!!python/object/apply:os.system ['false']", source="example.yml")


def test_duplicate_yaml_keys_are_reported_by_registry_cli(tmp_path, monkeypatch, capsys) -> None:
    import check_concept_registry
    import check_resource_registry

    invalid = tmp_path / "duplicate.yml"
    invalid.write_text("schema_version: 1\nschema_version: 1\n", encoding="utf-8")
    for module in (check_concept_registry, check_resource_registry):
        monkeypatch.setattr(module, "REGISTRY", invalid)
        assert module.main() == 1
        output = capsys.readouterr().err
        assert "duplicate.yml" in output
        assert "duplicate key 'schema_version'" in output
