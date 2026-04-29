"""SKILL.md frontmatter validator のテスト.

Pydantic v2 によるスキーマ検証と、cross-cutting なビジネスルール検証
(name とディレクトリ一致、本文非空) の両方をカバーする。
"""

from pathlib import Path

import pytest

from scripts.validate_skills import (
    SkillFrontmatter,
    SkillValidationError,
    parse_frontmatter,
    validate_skill_file,
)


def test_parse_frontmatter_valid(tmp_path: Path) -> None:
    skill = tmp_path / "SKILL.md"
    skill.write_text(
        "---\n"
        "name: foo\n"
        "description: A description that is at least thirty chars long.\n"
        "---\n"
        "\n"
        "body\n"
    )
    fm = parse_frontmatter(skill.read_text())
    assert fm["name"] == "foo"


def test_parse_frontmatter_missing_opening(tmp_path: Path) -> None:
    skill = tmp_path / "SKILL.md"
    skill.write_text("name: foo\n")
    with pytest.raises(SkillValidationError, match="frontmatter"):
        parse_frontmatter(skill.read_text())


def test_parse_frontmatter_unclosed(tmp_path: Path) -> None:
    skill = tmp_path / "SKILL.md"
    skill.write_text("---\nname: foo\n")
    with pytest.raises(SkillValidationError, match="unclosed"):
        parse_frontmatter(skill.read_text())


def test_parse_frontmatter_malformed_yaml(tmp_path: Path) -> None:
    """不正 YAML は SkillValidationError に変換され、yaml.YAMLError は raw に漏れない."""
    skill = tmp_path / "SKILL.md"
    skill.write_text("---\nname: [unclosed\n---\nbody\n")
    with pytest.raises(SkillValidationError, match="YAML"):
        parse_frontmatter(skill.read_text())


def test_skill_frontmatter_model_accepts_valid_data() -> None:
    fm = SkillFrontmatter.model_validate(
        {
            "name": "my-skill",
            "description": "A sufficiently detailed description for triggering.",
            "license": "MIT",
            "allowed-tools": "Bash, Read",
        }
    )
    assert fm.name == "my-skill"
    assert fm.allowed_tools == "Bash, Read"


def test_skill_frontmatter_model_rejects_short_description() -> None:
    from pydantic import ValidationError as PydanticValidationError

    with pytest.raises(PydanticValidationError):
        SkillFrontmatter.model_validate({"name": "x", "description": "short"})


def test_validate_skill_file_passes(tmp_path: Path) -> None:
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    skill = skill_dir / "SKILL.md"
    skill.write_text(
        "---\n"
        "name: my-skill\n"
        "description: A sufficiently detailed description for triggering purposes.\n"
        "license: MIT\n"
        "allowed-tools: Bash, Read\n"
        "---\n"
        "\n"
        "## Body\n"
    )
    errors = validate_skill_file(skill)
    assert errors == []


def test_validate_skill_file_missing_required_field(tmp_path: Path) -> None:
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    skill = skill_dir / "SKILL.md"
    skill.write_text("---\nname: my-skill\n---\n\nbody\n")
    errors = validate_skill_file(skill)
    assert len(errors) == 1
    assert "description" in errors[0].lower()


def test_validate_skill_file_name_directory_mismatch(tmp_path: Path) -> None:
    skill_dir = tmp_path / "actual-name"
    skill_dir.mkdir()
    skill = skill_dir / "SKILL.md"
    skill.write_text(
        "---\n"
        "name: wrong-name\n"
        "description: A sufficiently detailed description for triggering purposes.\n"
        "---\n"
        "\n"
        "body\n"
    )
    errors = validate_skill_file(skill)
    assert len(errors) == 1
    assert "name" in errors[0] and "directory" in errors[0]


def test_validate_skill_file_short_description(tmp_path: Path) -> None:
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    skill = skill_dir / "SKILL.md"
    skill.write_text("---\nname: my-skill\ndescription: short\n---\n\nbody\n")
    errors = validate_skill_file(skill)
    assert len(errors) == 1
    assert "description" in errors[0].lower()


def test_validate_skill_file_empty_body(tmp_path: Path) -> None:
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    skill = skill_dir / "SKILL.md"
    skill.write_text(
        "---\n"
        "name: my-skill\n"
        "description: A sufficiently detailed description for triggering purposes.\n"
        "---\n"
    )
    errors = validate_skill_file(skill)
    assert len(errors) == 1
    assert "body" in errors[0]


def test_main_returns_error_when_skills_dir_empty(tmp_path: Path) -> None:
    """skills/ が空のときは事故とみなして exit 1."""
    from scripts.validate_skills import main

    empty_dir = tmp_path / "empty-skills"
    empty_dir.mkdir()
    rc = main([str(empty_dir)])
    assert rc == 1
