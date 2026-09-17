#!/usr/bin/env python3
"""Synchronize local extracts from the saved dump, without fetching or executing docs.

Usage: python scripts/sync_sources.py [--baseline HEAD]
Hashes cover UTF-8 bodies with normalized newlines and outer whitespace removed.
The baseline is always a git snapshot, never the mutable working-tree extracts.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DUMP = "_source/llms-full.txt"
PREFIX = "website/docs/"
MARKER = re.compile(r"^<!-- source: (website/docs/[^\r\n]+\.mdx?) -->\n", re.MULTILINE)
LOCAL_OVERRIDES = {
    "user-guide/egress/index": "user-guide/egress.html",
    "user-guide/secrets/index": "user-guide/secrets.html",
    "developer-guide/plugins/index": "developer-guide/plugins.html",
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def normalize(body):
    return body.replace("\r\n", "\n").replace("\r", "\n").strip()


def source_key(source):
    """Match md/mdx variants by their docs-relative, extension-free identity."""
    relative = PurePosixPath(source.removeprefix(PREFIX))
    if not source.startswith(PREFIX) or relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Unsafe source path: {source}")
    return str(relative.with_suffix(""))


def extract_path(source):
    name = source.removeprefix(PREFIX).replace("/", "__")
    if name.endswith(".mdx"):
        name += ".md"
    return "_source/pages/" + name


def parse_snapshot(data):
    text = data.decode("utf-8").replace("\r\n", "\n")
    markers = list(MARKER.finditer(text))
    if not markers:
        raise ValueError("No anchored source markers found")
    if len(markers) != len(re.findall(r"^<!-- source:", text, re.MULTILINE)):
        raise ValueError("Unrecognized source marker")
    pages = {}
    for index, marker in enumerate(markers):
        source = marker.group(1)
        key = source_key(source)
        if key in pages:
            raise ValueError(f"Duplicate normalized source key: {key}")
        final = index + 1 == len(markers)
        end = len(text) if final else markers[index + 1].start()
        body = text[marker.end():end]
        # Both saved dumps use exactly this synthetic delimiter. Remove only
        # one suffix, including the final dump delimiter; retain internal rules,
        # frontmatter, headings, code fences, and any genuine trailing rule.
        suffix = "\n---\n" if final else "\n---\n\n"
        if not body.endswith(suffix):
            raise ValueError(f"Unexpected dump boundary after {source}")
        body = normalize(body[:-len(suffix)])
        pages[key] = {
            "source_path": source,
            "body": body,
            "source_sha256": sha256(body.encode("utf-8")),
        }
    paths = [extract_path(page["source_path"]) for page in pages.values()]
    if len(paths) != len(set(paths)):
        raise ValueError("Extract filename collision")
    return pages


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def write_if_different(relative, data):
    path = ROOT / relative
    if path.is_file() and path.read_bytes() == data:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def synchronize(baseline):
    # Resolve once so a moving ref cannot change the baseline mid-run.
    commit = git("rev-parse", "--verify", f"{baseline}^{{commit}}").decode().strip()
    previous_bytes = git("show", f"{commit}:{DUMP}")
    snapshot_bytes = (ROOT / DUMP).read_bytes()
    previous = parse_snapshot(previous_bytes)
    current = parse_snapshot(snapshot_bytes)

    # Read ALL existing extracts before any writes. These normalized hashes
    # detect stale files but must NOT determine historical source_change: the
    # 20 already-present untracked extracts are still added relative to HEAD.
    old_extracts = {
        path.relative_to(ROOT).as_posix(): normalize(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "_source/pages").glob("*")) if path.is_file()
    }
    old_extract_hashes = {
        path: sha256(body.encode("utf-8")) for path, body in old_extracts.items()
    }
    old_extract_comparison = {}
    entries = []
    outputs = {}
    for key, page in sorted(current.items()):
        prior = previous.get(key)
        change = "added" if prior is None else (
            "unchanged" if prior["body"] == page["body"] else "changed"
        )
        relative = extract_path(page["source_path"])
        old_extract_comparison[relative] = (
            "added" if relative not in old_extract_hashes else
            "unchanged" if old_extract_hashes[relative] == page["source_sha256"]
            else "changed"
        )
        route = key.removesuffix("/index") if key != "index" else ""
        local_route = LOCAL_OVERRIDES.get(key, key + ".html")
        entries.append({
            "source_path": page["source_path"],
            "extract_path": relative,
            "canonical_route": "/docs" + ("/" + route if route else ""),
            "local_route": local_route,
            "local_file_exists": (ROOT / local_route).is_file(),
            "source_sha256": page["source_sha256"],
            "previous_source_sha256": prior["source_sha256"] if prior else None,
            "source_change": change,
        })
        outputs[relative] = (page["body"] + "\n").encode("utf-8")

    removed = [previous[key]["source_path"] for key in sorted(previous.keys() - current.keys())]
    counts = {name: sum(entry["source_change"] == name for entry in entries)
              for name in ("added", "changed", "unchanged")}
    counts["removed"] = len(removed)
    # Only obsolete extracts explicitly identified by the git baseline may be
    # removed. Unknown files abort the run rather than being silently deleted.
    obsolete = {extract_path(page["source_path"]) for page in previous.values()} - outputs.keys()
    unexpected = old_extracts.keys() - outputs.keys() - obsolete
    if unexpected:
        raise ValueError(f"Unexpected extracts (not overwritten/deleted): {sorted(unexpected)}")

    manifest = {
        "schema_version": 1,
        "snapshot_path": DUMP,
        "snapshot_sha256": sha256(snapshot_bytes),
        "baseline_commit": commit,
        "baseline_snapshot_sha256": sha256(previous_bytes),
        "baseline_section_count": len(previous),
        "section_count": len(entries),
        "hash_normalization": "UTF-8 source body; LF newlines; outer whitespace stripped; one synthetic dump suffix removed",
        "translation_status": "Local file existence only; translation freshness has not been reviewed.",
        "counts": counts,
        "removed_sources": removed,
        "pages": entries,
    }
    report = [
        "# Source synchronization report", "",
        f"- Snapshot: `{DUMP}` (preserved; no network fetch performed).",
        f"- Snapshot SHA256: `{manifest['snapshot_sha256']}`",
        f"- Baseline: git commit `{commit}`, `{DUMP}`.",
        f"- Baseline snapshot SHA256: `{manifest['baseline_snapshot_sha256']}`",
        f"- Source sections: **{len(entries)}**; baseline normalized keys: **{len(previous)}**.",
        f"- Added: **{counts['added']}**; changed: **{counts['changed']}**; unchanged: **{counts['unchanged']}**; removed: **{counts['removed']}**.",
        "", "## Comparison rules", "",
        "Comparisons and previous hashes use the git baseline dump, not existing extracts. "
        "Already-present untracked extracts remain added if absent from that baseline. "
        "Existing extract bodies and their SHA256 hashes are read before any overwrite; "
        "working-tree repair results are not persisted so reruns remain stable.",
        "", "Source identities normalize `.md`/`.mdx` extensions. Bodies normalize newlines "
        "and outer whitespace after removing exactly one synthetic dump suffix. "
        "Internal separators and document content are preserved. SHA256 source hashes "
        "cover those normalized UTF-8 bodies; snapshot hashes cover the original bytes.",
        "", "No fetch date is inferred. Local HTML existence is recorded only as "
        "`local_file_exists`; translation freshness has not been reviewed.",
        "", "## Changed pages", "",
        "| Source path | Extract path |", "| --- | --- |",
    ]
    report.extend(f"| `{e['source_path']}` | `{e['extract_path']}` |"
                  for e in entries if e["source_change"] == "changed")
    report.extend(["", "## Added pages", ""])
    report.extend(f"- `{e['source_path']}` → `{e['extract_path']}`"
                  for e in entries if e["source_change"] == "added")
    report.extend(["", "## Removed pages", ""])
    report.extend([f"- `{source}`" for source in removed] or ["None."])
    outputs["_source/manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    outputs["_source/SYNC_REPORT.md"] = ("\n".join(report) + "\n").encode("utf-8")

    # Every classification, old-file read, and output is prepared before writes.
    for relative, data in outputs.items():
        write_if_different(relative, data)
    for relative in sorted(obsolete):
        (ROOT / relative).unlink(missing_ok=True)
    actual = {path.relative_to(ROOT).as_posix()
              for path in (ROOT / "_source/pages").iterdir() if path.is_file()}
    expected = {entry["extract_path"] for entry in entries}
    if actual != expected:
        raise ValueError("Extract inventory does not match manifest")
    if (ROOT / DUMP).read_bytes() != snapshot_bytes:
        raise ValueError("Snapshot changed during synchronization")
    print(f"{len(entries)} sections; baseline {len(previous)}; "
          + ", ".join(f"{name}={count}" for name, count in counts.items()))
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default="HEAD", help="Git baseline revision (default: HEAD)")
    synchronize(parser.parse_args().baseline)
