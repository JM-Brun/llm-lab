"""Failure and compatibility checks for generated artifact publication."""

import os
import stat
from pathlib import Path

import pytest
from artifact_writer import write_artifacts


def test_failed_staging_preserves_all_destinations_and_cleans_temporary_files(
    tmp_path: Path,
) -> None:
    first, second = tmp_path / "first.json", tmp_path / "second.json"
    first.write_text("old first", encoding="utf-8")
    second.write_text("old second", encoding="utf-8")

    with pytest.raises(UnicodeEncodeError):
        write_artifacts({first: "new first", second: "\ud800"})

    assert first.read_text(encoding="utf-8") == "old first"
    assert second.read_text(encoding="utf-8") == "old second"
    assert sorted(path.name for path in tmp_path.iterdir()) == ["first.json", "second.json"]


def test_success_preserves_existing_mode_and_uses_normal_creation_mode(tmp_path: Path) -> None:
    existing, new, reference = tmp_path / "existing", tmp_path / "new", tmp_path / "reference"
    existing.write_text("old", encoding="utf-8")
    existing.chmod(0o640)
    reference.write_text("reference", encoding="utf-8")

    write_artifacts({existing: "updated", new: "created"})

    assert existing.read_text(encoding="utf-8") == "updated"
    assert new.read_text(encoding="utf-8") == "created"
    assert stat.S_IMODE(existing.stat().st_mode) == 0o640
    assert stat.S_IMODE(new.stat().st_mode) == stat.S_IMODE(reference.stat().st_mode)


def test_symbolic_link_is_preserved_and_aliases_are_rejected(tmp_path: Path) -> None:
    target, link = tmp_path / "target", tmp_path / "link"
    target.write_text("old", encoding="utf-8")
    link.symlink_to(target.name)

    write_artifacts({link: "new"})

    assert link.is_symlink()
    assert target.read_text(encoding="utf-8") == "new"
    with pytest.raises(ValueError, match="Multiple generated artifacts"):
        write_artifacts({link: "one", target: "two"})
    assert target.read_text(encoding="utf-8") == "new"


def test_replace_failure_cleans_staged_files_but_is_not_a_transaction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import artifact_writer

    first, second = tmp_path / "first", tmp_path / "second"
    first.write_text("old first", encoding="utf-8")
    second.write_text("old second", encoding="utf-8")
    real_replace = os.replace

    def fail_second(source: Path, target: Path) -> None:
        if target == second:
            raise PermissionError("simulated replacement failure")
        real_replace(source, target)

    monkeypatch.setattr(artifact_writer.os, "replace", fail_second)
    with pytest.raises(PermissionError, match="simulated replacement failure") as error:
        write_artifacts({first: "new first", second: "new second"})

    assert any("replacing 1 of 2" in note for note in error.value.__notes__)
    assert any(str(second) in note for note in error.value.__notes__)
    assert first.read_text(encoding="utf-8") == "new first"
    assert second.read_text(encoding="utf-8") == "old second"
    assert sorted(path.name for path in tmp_path.iterdir()) == ["first", "second"]


def test_standalone_export_does_not_truncate_existing_file_on_write_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import export_knowledge_graph

    output = tmp_path / "graph.jsonld"
    output.write_text("old export", encoding="utf-8")
    monkeypatch.setattr(export_knowledge_graph, "build_graph", lambda: {"value": "\ud800"})

    with pytest.raises(UnicodeEncodeError):
        export_knowledge_graph.write_export(output)

    assert output.read_text(encoding="utf-8") == "old export"
    assert list(tmp_path.iterdir()) == [output]


def test_generator_writes_nothing_when_a_later_language_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import build_learning_map

    monkeypatch.setattr(build_learning_map, "SITE", tmp_path)
    monkeypatch.setattr(build_learning_map, "ROOT", tmp_path)

    def prepare(language: str) -> dict[Path, str]:
        if language == "en":
            raise ValueError("invalid English route")
        return {tmp_path / f"learning-map-data-{language}.json": "{}\n"}

    monkeypatch.setattr(build_learning_map, "prepare_build", prepare)

    with pytest.raises(ValueError, match="invalid English route"):
        build_learning_map.main()

    assert list(tmp_path.iterdir()) == []


def test_generator_does_not_write_when_graph_export_is_invalid(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import build_learning_map
    import export_knowledge_graph

    monkeypatch.setattr(build_learning_map, "SITE", tmp_path)
    monkeypatch.setattr(build_learning_map, "ROOT", tmp_path)
    monkeypatch.setattr(
        build_learning_map,
        "prepare_build",
        lambda language: {tmp_path / f"learning-map-data-{language}.json": "{}\n"},
    )

    def invalid_graph() -> dict[str, str]:
        raise ValueError("unresolved page association")

    monkeypatch.setattr(export_knowledge_graph, "build_graph", invalid_graph)

    with pytest.raises(ValueError, match="unresolved page association"):
        build_learning_map.main()

    assert list(tmp_path.iterdir()) == []
