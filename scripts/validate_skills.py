"""SKILL.md frontmatter validator.

設計仕様書 Section 2 で定義された frontmatter 要件を検証する。
スキーマ検証は Pydantic v2、cross-cutting なビジネスルール
(name とディレクトリ一致、本文非空) は外部関数で行う分離設計。

- 必須フィールド: name, description (>=30 chars)
- 推奨フィールド: license, allowed-tools
- ビジネスルール: name はディレクトリ名と一致、本文は非空
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class SkillValidationError(Exception):
    """SKILL.md の検証に関連する例外."""


MIN_DESCRIPTION_LENGTH: int = 30


class SkillFrontmatter(BaseModel):
    """SKILL.md frontmatter のスキーマ.

    gh skill 仕様に準拠。description は発火条件として十分な長さを要求。
    extra="allow" で metadata 等の追加フィールドを許容する
    (gh skill が install 時に自動付与するため)。
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    name: str = Field(min_length=1)
    description: str = Field(min_length=MIN_DESCRIPTION_LENGTH)
    license: str | None = None
    allowed_tools: str | None = Field(default=None, alias="allowed-tools")


@dataclass(frozen=True, slots=True)
class ParsedSkill:
    """SKILL.md をパースした結果. frontmatter (辞書) と body 文字列を保持."""

    frontmatter: dict[str, object]
    body: str


def parse_frontmatter(content: str) -> dict[str, object]:
    """SKILL.md の YAML frontmatter のみを辞書として返す (互換 API).

    フォーマット不正は SkillValidationError を送出する (デフォルト値での継続禁止)。
    """
    return _parse_skill(content).frontmatter


def _parse_skill(content: str) -> ParsedSkill:
    """SKILL.md を frontmatter と body に分離してパースする内部関数.

    終了位置を 1 度だけ計算し、frontmatter 辞書と body 文字列を同時に返す。
    """
    if not content.startswith("---\n"):
        raise SkillValidationError("frontmatter must start with '---\\n'")
    end_index = content.find("\n---\n", 4)
    if end_index == -1:
        raise SkillValidationError("frontmatter is unclosed (no terminating '---')")
    yaml_block = content[4:end_index]
    try:
        parsed = yaml.safe_load(yaml_block)
    except yaml.YAMLError as exc:
        raise SkillValidationError(f"YAML parse error: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SkillValidationError("frontmatter must be a YAML mapping")
    body = content[end_index + 5 :].strip()
    return ParsedSkill(frontmatter=parsed, body=body)


def validate_skill_file(path: Path) -> list[str]:
    """単一の SKILL.md を検証し、エラーメッセージのリストを返す.

    1. YAML frontmatter のパース (失敗時は即座に return)
    2. Pydantic でスキーマ検証 (失敗時はそれだけ返す)
    3. ビジネスルール (name とディレクトリ一致、本文非空)
    """
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")

    try:
        parsed = _parse_skill(content)
    except SkillValidationError as exc:
        return [f"frontmatter: {exc}"]

    try:
        fm = SkillFrontmatter.model_validate(parsed.frontmatter)
    except ValidationError as exc:
        for err in exc.errors():
            loc = ".".join(str(p) for p in err["loc"]) or "<root>"
            errors.append(f"{loc}: {err['msg']}")
        return errors

    if fm.name != path.parent.name:
        errors.append(f"name '{fm.name}' does not match directory '{path.parent.name}'")

    if not parsed.body:
        errors.append("body is empty (frontmatter only)")

    return errors


def main(argv: list[str] | None = None) -> int:
    """skills/ 配下の全 SKILL.md を検証する.

    検証エラーがあれば 1 を返し詳細を stderr に出力。
    """
    if argv is None:
        argv = sys.argv[1:]
    skills_dir = Path(argv[0]) if argv else Path("skills")

    if not skills_dir.is_dir():
        print(f"error: {skills_dir} is not a directory", file=sys.stderr)
        return 1

    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        print(
            f"error: no SKILL.md files found under {skills_dir} "
            "(空ディレクトリは事故とみなしエラー伝播)",
            file=sys.stderr,
        )
        return 1

    has_errors = False
    for skill in skill_files:
        errors = validate_skill_file(skill)
        if errors:
            has_errors = True
            print(f"\n{skill}:", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)

    if has_errors:
        print("\nvalidation failed", file=sys.stderr)
        return 1
    print(f"validated {len(skill_files)} SKILL.md files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
