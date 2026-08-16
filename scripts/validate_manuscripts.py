#!/usr/bin/env python3
"""Validate bedtime-Bible manuscripts against the accuracy pipeline."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_ROOT = ROOT / "manuscripts-v2"

REQUIRED_FRONT = ("story_id", "title", "primary_passage", "afr20_quote_check")
ALLOWED_QUOTE = {"pending", "verified", "AFR20_QUOTE_CHECK_REQUIRED"}
AUDIT_KEYS = (
    "primary_passage",
    "passage_read",
    "context_read",
    "required_details",
    "unsupported_details",
    "chronology_check",
    "people_check",
    "numbers_check",
    "theology_check",
    "direct_quotes_verified",
    "afr20_quote_check",
    "audit_status",
)
CLOSING = (
    "Wie was in hierdie verhaal",
    "Wat leer ons",
    "Vers om te onthou",
    "Onthou jy",
)
OPENING = "Een dag, lank, lank gelede"
QUOTE_STATUS = {"passed", "failed", "pending"}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        raise ValueError("missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("unterminated YAML frontmatter")
    raw, body = parts[1], parts[2]
    if yaml is not None:
        data = yaml.safe_load(raw) or {}
    else:
        data = _minimal_yaml(raw)
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data, body


def _minimal_yaml(raw: str) -> dict:
    """Fallback parser for simple key: value frontmatter (no nested structures)."""
    data: dict = {}
    key = None
    for line in raw.splitlines():
        if re.match(r"^\s+-\s+", line) and key:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(re.sub(r"^\s+-\s+", "", line).strip().strip('"'))
            continue
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == "":
            data[key] = []
        elif val.lower() in {"true", "false"}:
            data[key] = val.lower() == "true"
        elif val.lower() in {"null", "~"}:
            data[key] = None
        else:
            data[key] = val.strip('"').strip("'")
    return data


def consecutive_duplicate_paragraphs(body: str) -> list[str]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if len(p.strip()) > 50]
    dupes = []
    for i in range(len(paras) - 1):
        a, b = paras[i], paras[i + 1]
        if a.startswith("![") or a.startswith(">") or a.startswith("#"):
            continue
        if a[:80] == b[:80]:
            dupes.append(a[:80])
    return dupes


def quoted_verses_without_reference(body: str) -> list[str]:
    issues = []
    section = body
    m = re.search(r"### Vers om te onthou\s*(.+?)(?:### |\Z)", section, re.S)
    if not m:
        return ["missing Vers om te onthou section"]
    block = m.group(1)
    if "—" not in block and "-" not in block:
        issues.append("memory verse missing reference separator")
    if re.search(r"[“\"]", block) and not re.search(
        r"\d+:\d+", block
    ):
        issues.append("quoted memory verse missing chapter:verse")
    return issues


def validate_data(data: dict, body: str, *, approved: bool) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_FRONT:
        if key not in data or data[key] in (None, ""):
            errors.append(f"missing frontmatter: {key}")

    status = str(data.get("afr20_quote_check", ""))
    if status and status not in ALLOWED_QUOTE:
        errors.append(f"invalid afr20_quote_check: {status}")

    audit = data.get("scripture_audit")
    if not isinstance(audit, dict):
        errors.append("missing scripture_audit mapping")
        audit = {}
    else:
        for key in AUDIT_KEYS:
            if key not in audit:
                errors.append(f"scripture_audit missing: {key}")

    if OPENING not in body:
        errors.append("missing opening: Een dag, lank, lank gelede")
    for label in CLOSING:
        if label not in body:
            errors.append(f"missing closing: {label}")

    imgs = len(re.findall(r"!\[Beeld", body))
    if imgs < 6:
        errors.append(f"expected 6 image placeholders, found {imgs}")

    dupes = consecutive_duplicate_paragraphs(body)
    if dupes:
        errors.append(f"consecutive duplicate paragraph: {dupes[0]!r}")

    errors.extend(quoted_verses_without_reference(body))

    if approved:
        if not audit:
            errors.append("approved gate requires scripture_audit")
        else:
            for flag in (
                "passage_read",
                "context_read",
                "direct_quotes_verified",
            ):
                if audit.get(flag) is not True:
                    errors.append(f"approved gate: {flag} must be true")
            for check in (
                "chronology_check",
                "people_check",
                "numbers_check",
                "theology_check",
            ):
                if audit.get(check) != "passed":
                    errors.append(f"approved gate: {check} must be passed")
            if audit.get("unsupported_details") not in ([], None):
                errors.append("approved gate: unsupported_details must be empty")
            if data.get("afr20_quote_check") != "verified":
                errors.append("approved gate: afr20_quote_check must be verified")
            if audit.get("afr20_quote_check") != "verified":
                errors.append("approved gate: scripture_audit.afr20_quote_check must be verified")
            if audit.get("audit_status") != "approved":
                errors.append("approved gate: audit_status must be approved")
            details = audit.get("required_details") or []
            if not details:
                errors.append("approved gate: required_details must be non-empty")

    return errors


def validate_file(path: Path, *, approved: bool) -> list[str]:
    text = path.read_text(encoding="utf-8")
    try:
        data, body = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]
    return validate_data(data, body, approved=approved)


def iter_manuscripts(root: Path) -> list[Path]:
    return sorted(root.rglob("*.md"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, help="single manuscript")
    parser.add_argument("--root", type=Path, default=MANUSCRIPT_ROOT)
    parser.add_argument(
        "--approved",
        action="store_true",
        help="strict gate: scripture_audit must be fully passed",
    )
    args = parser.parse_args(argv)

    paths = [args.path] if args.path else iter_manuscripts(args.root)
    failed = 0
    for path in paths:
        if path is None or not path.exists():
            print(f"FAIL {path}: not found")
            failed += 1
            continue
        errors = validate_file(path, approved=args.approved)
        rel = path
        try:
            rel = path.resolve().relative_to(ROOT)
        except ValueError:
            pass
        if errors:
            failed += 1
            print(f"FAIL {rel}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"OK   {rel}")
    print(f"{len(paths) - failed}/{len(paths)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
