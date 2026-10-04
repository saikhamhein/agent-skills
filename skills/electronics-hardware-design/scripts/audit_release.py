#!/usr/bin/env python3
"""Check a hardware release inventory. This does not validate the hardware."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys


class InvalidManifest(ValueError):
    """A manifest is not in the documented format."""


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_manifest(data: object) -> dict:
    if not isinstance(data, dict):
        raise InvalidManifest("Top-level value must be an object")
    keys = {"schema_version", "release_id", "source_revision", "required_roles", "artifacts", "omissions"}
    if set(data) != keys:
        raise InvalidManifest(f"Expected exactly these keys: {', '.join(sorted(keys))}")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise InvalidManifest("schema_version must be integer 1")
    if not nonempty(data["release_id"]):
        raise InvalidManifest("release_id must be nonempty text")
    rev = data["source_revision"]
    if not isinstance(rev, str) or not re.fullmatch(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})", rev):
        raise InvalidManifest("source_revision must be a full 40- or 64-digit hexadecimal identifier")
    roles = data["required_roles"]
    if not isinstance(roles, list) or not roles or not all(nonempty(r) for r in roles):
        raise InvalidManifest("required_roles must be a nonempty list of nonempty strings")
    if len(set(roles)) != len(roles):
        raise InvalidManifest("required_roles contains duplicates")
    artifacts = data["artifacts"]
    if not isinstance(artifacts, list) or not artifacts:
        raise InvalidManifest("artifacts must be a nonempty list")
    paths: set[str] = set()
    for item in artifacts:
        if not isinstance(item, dict) or set(item) != {"path", "role", "sha256"}:
            raise InvalidManifest("Each artifact requires exactly path, role, and sha256")
        raw = item["path"]
        if not nonempty(raw) or "\\" in raw or "\x00" in raw:
            raise InvalidManifest("Artifact paths must be nonempty POSIX-style relative paths")
        path = PurePosixPath(raw)
        if path.is_absolute() or any(p in {".", "..", ""} for p in raw.split("/")):
            raise InvalidManifest(f"Unsafe or noncanonical artifact path: {raw}")
        if raw in paths:
            raise InvalidManifest(f"Duplicate artifact path: {raw}")
        paths.add(raw)
        if not nonempty(item["role"]):
            raise InvalidManifest(f"Artifact role must be nonempty: {raw}")
        digest = item["sha256"]
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            raise InvalidManifest(f"Invalid SHA-256: {raw}")
    omissions = data["omissions"]
    if not isinstance(omissions, dict) or not all(nonempty(k) and nonempty(v) for k, v in omissions.items()):
        raise InvalidManifest("omissions must map role names to nonempty reasons")
    if not set(omissions).issubset(roles):
        raise InvalidManifest("An omission must refer to a required role")
    provided = {a["role"] for a in artifacts}
    if provided.intersection(omissions):
        raise InvalidManifest("A role cannot be both provided and omitted")
    return data


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def audit(manifest_path: Path, *, allow_unlisted: bool = False) -> dict:
    if manifest_path.is_symlink():
        raise InvalidManifest("Manifest must not be a symlink")
    manifest_path = manifest_path.resolve(strict=True)
    data = validate_manifest(json.loads(manifest_path.read_text(encoding="utf-8")))
    root = manifest_path.parent
    errors: list[str] = []
    listed = {a["path"] for a in data["artifacts"]}
    provided = {a["role"] for a in data["artifacts"]}
    for role in data["required_roles"]:
        if role not in provided and role not in data["omissions"]:
            errors.append(f"Required role missing: {role}")
    for item in data["artifacts"]:
        relative = PurePosixPath(item["path"])
        target = root.joinpath(*relative.parts)
        if target == manifest_path:
            errors.append("Manifest cannot inventory itself")
            continue
        cursor = root
        linked = False
        for part in relative.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                linked = True
                break
        if linked:
            errors.append(f"Symlink artifact or parent: {item['path']}")
            continue
        if not target.is_file():
            errors.append(f"Artifact missing or not a regular file: {item['path']}")
            continue
        if target.stat().st_size == 0:
            errors.append(f"Empty artifact: {item['path']}")
        try:
            actual = sha256(target)
        except OSError as exc:
            errors.append(f"Cannot read {item['path']}: {exc}")
            continue
        if actual != item["sha256"].lower():
            errors.append(f"SHA-256 mismatch: {item['path']}")
    discovered: set[str] = set()
    for path in root.rglob("*"):
        if path == manifest_path:
            continue
        if path.is_symlink():
            errors.append(f"Symlink found in release tree: {path.relative_to(root).as_posix()}")
        elif path.is_file():
            discovered.add(path.relative_to(root).as_posix())
    extras = sorted(discovered - listed)
    if extras and not allow_unlisted:
        errors.extend(f"Unlisted file: {p}" for p in extras)
    return {
        "release_id": data["release_id"],
        "source_revision": data["source_revision"],
        "artifact_count": len(data["artifacts"]),
        "inventory_scope": "partial" if allow_unlisted else "complete",
        "errors": errors,
        "unlisted_files": extras,
        "declared_omissions": data["omissions"],
        "limitation": "Inventory and file integrity only. Provenance, engineering validity, waiver approval, and hardware performance are not verified.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--allow-unlisted", action="store_true", help="Check a partial inventory and report extra files without failing for them")
    args = parser.parse_args(argv)
    try:
        result = audit(args.manifest, allow_unlisted=args.allow_unlisted)
    except (InvalidManifest, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
