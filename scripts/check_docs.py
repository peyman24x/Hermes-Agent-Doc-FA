#!/usr/bin/env python3
"""Check the static Persian docs using only the Python standard library.

Page checks default to nav-data.js d:1 entries, with sitewide link checks.
With --pages, structure and source comparisons cover the selected pages;
link and duplicate-ID checks still cover every actual HTML file.
No network access, JavaScript execution, or files written. Markdown headings
are heuristic; fences are compared without trimming their content.
"""

import argparse
from collections import Counter
from dataclasses import dataclass, field
import html
from html.parser import HTMLParser
import os
from pathlib import Path, PurePosixPath
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
VOID = set("area base br col embed hr img input link meta param source track wbr".split())
SKIP_DIRS = {"_source", "tools", "node_modules", "__pycache__"}
EXTERNAL_SCHEMES = {"mailto", "tel", "http", "https", "data", "hermes"}
INDEX_MAPPINGS = {
    "user-guide/messaging/index.md": "user-guide/messaging/index.html",
    "integrations/index.md": "integrations/index.html",
    "developer-guide/plugins/index.md": "developer-guide/plugins.html",
    "user-guide/egress/index.md": "user-guide/egress.html",
    "user-guide/secrets/index.md": "user-guide/secrets.html",
}
MARKER = re.compile(r"^<!--\s*source:\s*website/docs/(.+?\.mdx?)\s*-->\s*$", re.M)
FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})([^\r\n]*)$")
NAV_OBJECT = re.compile(r"\{[^{}]*\}")
NAV_PATH = re.compile(r'''\bp\s*:\s*("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')''')
NAV_DONE = re.compile(r"\bd\s*:\s*([01])\b")


@dataclass
class Report:
    errors: int = 0
    warnings: int = 0
    counts: Counter = field(default_factory=Counter)

    def issue(self, path, message, line=0, warning=False):
        if warning:
            self.warnings += 1
        else:
            self.errors += 1
        location = str(path) + (f":{line}" if line else "")
        print(f"{'WARN' if warning else 'FAIL'} {location}: {message}")


@dataclass
class Block:
    text: str
    line: int


class PageParser(HTMLParser):
    """Explicit nonvoid nesting, not the browser's error-repaired DOM."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.ids = {}
        self.duplicates = []
        self.anchors = set()
        self.tags = Counter()
        self.html_attrs = {}
        self.links = []
        self.stylesheets = []
        self.scripts = []
        self.blocks = []
        self.active_code = None
        self.prose = []
        self.has_base = False
        self.replacements = 0

    def error(self, message):
        self.errors.append((self.getpos()[0], message))

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        values = dict(attrs)
        self.tags[tag] += 1
        if len(values) != len(attrs):
            self.error(f"duplicate attribute on <{tag}>")
        if tag == "html":
            self.html_attrs = values
        if tag == "base":
            self.has_base = True
        ident = values.get("id")
        if ident is not None:
            if ident in self.ids:
                self.duplicates.append((line, ident, self.ids[ident]))
            else:
                self.ids[ident] = line
            self.anchors.add(ident)
        if tag == "a" and values.get("name"):
            self.anchors.add(values["name"])
        for attr in ("href", "src"):
            if attr in values:
                self.links.append((line, tag, attr, values[attr] or ""))
        if tag == "link" and "stylesheet" in (values.get("rel") or "").lower().split():
            self.stylesheets.append(values.get("href") or "")
        if tag == "script" and "src" in values:
            self.scripts.append(values["src"] or "")
        if tag == "code" and any(t == "pre" for t, _ in self.stack):
            if self.active_code is not None:
                self.error("nested <code> inside a pre/code block")
            else:
                self.active_code = Block("", line)
        if tag not in VOID:
            self.stack.append((tag, line))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.error(f"self-closing nonvoid <{tag}/> is not valid HTML")
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            self.error(f"void element </{tag}> must not have an end tag")
            return
        if not self.stack or self.stack[-1][0] != tag:
            expected = f"</{self.stack[-1][0]}>" if self.stack else "no end tag"
            self.error(f"unexpected </{tag}>; expected {expected}")
            # Recover without a cascade of spurious EOF errors.
            matches = [i for i, (name, _) in enumerate(self.stack) if name == tag]
            if not matches:
                return
            removed = self.stack[matches[-1]:]
            del self.stack[matches[-1]:]
        else:
            removed = [self.stack.pop()]
        if self.active_code is not None and any(t == "code" for t, _ in removed):
            self.blocks.append(self.active_code)
            self.active_code = None

    def handle_data(self, data):
        self.replacements += data.count("\ufffd")
        if self.active_code is not None:
            self.active_code.text += data
        if not any(t in {"pre", "code", "script", "style"} for t, _ in self.stack):
            bad = Counter(c for c in data if c in "\u064a\u0643")
            if bad:
                self.prose.append((self.getpos()[0], bad))

    def handle_decl(self, decl):
        if not re.match(r"(?i)^doctype\s+html(?:\s|$)", decl):
            self.error(f"unexpected declaration: {decl!r}")

    def unknown_decl(self, data):
        self.error(f"unexpected marked declaration: {data!r}")

    def finish(self, text):
        try:
            self.feed(text)
            self.close()
        except (ValueError, AssertionError) as exc:
            self.error(f"HTML parsing failed: {exc}")
        for tag, line in self.stack:
            self.errors.append((line, f"unclosed <{tag}>"))
        return self


def read_text(path):
    # Universal newline handling matches HTML/Markdown line-ending semantics.
    # All other whitespace, including the final newline, remains significant.
    return path.read_text(encoding="utf-8")


def actual_html(root):
    for directory, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(files):
            if Path(name).suffix.lower() in {".html", ".htm"}:
                yield (Path(directory) / name).resolve()


def load_nav(root, report):
    path = root / "assets/nav-data.js"
    try:
        text = read_text(path)
    except (OSError, UnicodeError) as exc:
        report.issue("assets/nav-data.js", str(exc))
        return []
    pages = []
    seen = set()
    for obj in NAV_OBJECT.findall(text):
        p, d = NAV_PATH.search(obj), NAV_DONE.search(obj)
        if not p:
            continue
        if not d:
            report.issue("assets/nav-data.js", f"missing d:0/1 for {p.group(1)}")
            continue
        # Navigation is a data literal, never execute it. Current paths are
        # plain relative strings; fail rather than guessing JS escape rules.
        value = p.group(1)[1:-1]
        if "\\" in value or not value.endswith(".html"):
            report.issue("assets/nav-data.js", f"unsupported page path {value!r}")
            continue
        if value in seen:
            report.issue("assets/nav-data.js", f"duplicate page {value}")
        seen.add(value)
        if d.group(1) == "1":
            pages.append(value)
    if not seen:
        report.issue("assets/nav-data.js", "no navigation page records found")
    return pages


def local_target(root, page, value):
    """Return (path, fragment), or None for an accepted nonlocal URL."""
    url = urlsplit(value.strip())
    if url.scheme.lower() in EXTERNAL_SCHEMES or (not url.scheme and url.netloc):
        return None
    if url.scheme:
        raise ValueError(f"unsupported URL scheme {url.scheme!r}")
    decoded = unquote(url.path)
    if "\\" in decoded or "\x00" in decoded:
        raise ValueError("backslash/NUL in local URL")
    target = (root / decoded.lstrip("/") if decoded.startswith("/")
              else page.parent / decoded if decoded else page).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        raise ValueError("local URL escapes site root") from None
    if target.is_dir():
        target = target / "index.html"
    return target, unquote(url.fragment)


def check_links(root, parsed, report, selected=None):
    for path, (_, page) in list(parsed.items()):
        if selected is not None and path not in selected:
            continue
        rel = path.relative_to(root).as_posix()
        if page.has_base:
            report.issue(rel, "<base> URL resolution is unsupported; use explicit relative/root paths")
        for line, tag, attr, value in page.links:
            report.counts["references"] += 1
            try:
                resolved = local_target(root, path, value)
            except ValueError as exc:
                report.issue(rel, f"{tag}[{attr}] {value!r}: {exc}", line)
                continue
            if resolved is None:
                continue
            report.counts["local_references"] += 1
            target, fragment = resolved
            if not target.is_file():
                report.issue(rel, f"missing local {attr} {value!r} -> {target.relative_to(root).as_posix()}", line)
            elif fragment and target.suffix.lower() in {".html", ".htm"}:
                report.counts["fragments"] += 1
                if target not in parsed:
                    try:
                        target_text = read_text(target)
                        parsed[target] = (target_text, PageParser().finish(target_text))
                    except (OSError, UnicodeError) as exc:
                        report.issue(rel, f"cannot read fragment target {value!r}: {exc}", line)
                        continue
                if fragment not in parsed[target][1].anchors:
                    report.issue(rel, f"missing fragment in {attr} {value!r}", line)
            elif fragment:
                report.counts["non_html_fragments"] += 1


def check_page(root, path, text, page, report):
    rel = path.relative_to(root).as_posix()
    for line, message in page.errors:
        report.issue(rel, message, line)
    for tag in ("html", "head", "body", "h1"):
        if page.tags[tag] != 1:
            report.issue(rel, f"expected one <{tag}>, found {page.tags[tag]}")
    depth = len(path.relative_to(root).parent.parts)
    expected = "/".join([".."] * depth) or "."
    for attr, value in (("lang", "fa"), ("dir", "rtl"), ("data-root", expected)):
        actual = page.html_attrs.get(attr)
        if actual != value:
            equivalent = attr == "data-root" and actual == value + "/"
            report.issue(rel, f"<html> {attr} should be {value!r}, got {actual!r}"
                         + (" (equivalent trailing slash)" if equivalent else ""), warning=equivalent)
    for required, references in (("assets/style.css", page.stylesheets),
                                 ("assets/nav-data.js", page.scripts),
                                 ("assets/main.js", page.scripts)):
        found = False
        for ref in references:
            try:
                target = local_target(root, path, ref)
                found |= target is not None and target[0] == root / required
            except ValueError:
                pass  # The sitewide link pass reports malformed URLs.
        if not found:
            report.issue(rel, f"missing required stylesheet/script reference to {required}")
    for number, line in enumerate(text.splitlines(), 1):
        if "\ufffd" in line:
            report.issue(rel, f"U+FFFD replacement character ({line.count(chr(0xfffd))})", number)
        if re.search(r"@@CODE\b|@@CODE[_\d]", line, re.I):
            report.issue(rel, "unreplaced @@CODE placeholder", number)
    if page.replacements > text.count("\ufffd"):
        report.issue(rel, "U+FFFD replacement character encoded as an HTML entity")
    for line, chars in page.prose:
        report.issue(rel, "Arabic yeh/kaf in prose: " + ", ".join(
            f"U+{ord(c):04X} x{n}" for c, n in sorted(chars.items())), line)


def load_sources(root, report):
    # The tracked snapshot is authoritative; temporary downloads are not.
    source = root / "_source/llms-full.txt"
    try:
        text = read_text(source)
    except (OSError, UnicodeError) as exc:
        report.issue(source, f"cannot read source snapshot: {exc}")
        return {}, source
    markers = list(MARKER.finditer(text))
    result = {}
    for i, match in enumerate(markers):
        name = match.group(1)
        route = INDEX_MAPPINGS.get(name, str(PurePosixPath(name).with_suffix(".html")))
        if route in result:
            report.issue(source, f"duplicate source mapping for {route}")
            continue
        end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
        result[route] = (name, text[match.end():end])
    if not markers:
        report.issue(source, "no website/docs .md/.mdx source markers found")
    report.counts["source_markers"] = len(markers)
    return result, source


def markdown_parts(text):
    """Return exact fence contents, outside-fence lines, and unclosed fences.

    Indentation before a delimiter is accepted but never removed from content.
    A closer must use the same character, be at least as long, and have only
    trailing whitespace. Backticks in a backtick opener's info are forbidden.
    """
    blocks, prose, pending = [], [], None
    content = []
    for number, line in enumerate(text.splitlines(keepends=True), 1):
        bare = line.rstrip("\r\n")
        if pending:
            char, length, start = pending
            if re.fullmatch(r"[ \t]*" + re.escape(char) + "{" + str(length) + r",}[ \t]*", bare):
                blocks.append(Block("".join(content), start))
                pending, content = None, []
            else:
                content.append(line)
            # Preserve line positions and prevent headings spanning a fence.
            prose.append("")
            continue
        match = FENCE.match(bare)
        if match and not (match[1][0] == "`" and "`" in match[2]):
            pending = (match[1][0], len(match[1]), number)
            prose.append("")
        else:
            prose.append(bare)
    return blocks, prose, pending


class HeadingHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.explicit = []

    def handle_starttag(self, tag, attrs):
        if re.fullmatch(r"h[1-6]", tag):
            ident = dict(attrs).get("id")
            if ident:
                self.explicit.append(ident)


def heading_slug(text):
    """GitHub/Docusaurus-style approximation, not a Markdown/MDX renderer."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"!?\[([^\]]*)\]\[[^\]]*\]", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"`+([^`]*?)`+", r"\1", text)
    # Remove emphasis delimiters, but retain underscores in identifiers.
    text = re.sub(r"(?<!\w)(_+)(?=\S)(.+?)(?<=\S)\1(?!\w)", r"\2", text)
    text = html.unescape(text).lower().strip()
    text = "".join(c for c in text if c in "_-" or c.isspace()
                   or unicodedata.category(c)[0] in "LNM")
    return re.sub(r"\s", "-", text)


def source_anchors(prose):
    explicit, inferred, used = set(), set(), set()
    for i, line in enumerate(prose):
        atx = re.match(r"^[ \t]{0,3}(#{1,6})[ \t]+(.+?)\s*$", line)
        level, title = 0, ""
        if atx:
            level, title = len(atx[1]), re.sub(r"[ \t]+#+[ \t]*$", "", atx[2])
        elif i + 1 < len(prose) and line.strip() and re.fullmatch(r"[ \t]{0,3}(=+|-+)[ \t]*", prose[i + 1]):
            level, title = (1 if "=" in prose[i + 1] else 2), line.strip()
        if not level:
            continue
        custom = re.search(r"\s*\{#([^}\s]+)\}\s*$", title)
        if custom:
            explicit.add(custom[1])
            used.add(custom[1])
            continue
        # llms-full inserts duplicate page titles; translated h1 need not have
        # an English ID. Explicit h1 IDs above are still required.
        if level == 1:
            continue
        base = heading_slug(title)
        slug, n = base, 0
        while slug in used:
            n += 1
            slug = f"{base}-{n}"
        used.add(slug)
        if slug:
            inferred.add(slug)
    parser = HeadingHTML()
    parser.feed("\n".join(prose))
    parser.close()
    explicit.update(parser.explicit)
    return explicit, inferred


def compare_source(rel, page, source, report):
    name, text = source
    blocks, prose, pending = markdown_parts(text)
    if pending:
        report.issue(rel, f"unclosed source fence in {name} at segment line {pending[2]}")
    report.counts["code_source"] += len(blocks)
    report.counts["code_html"] += len(page.blocks)
    if len(blocks) != len(page.blocks):
        report.issue(rel, f"code block count HTML={len(page.blocks)}, source={len(blocks)} ({name})")
    for i, (original, rendered) in enumerate(zip(blocks, page.blocks), 1):
        if original.text == rendered.text:
            report.counts["code_exact"] += 1
        elif original.text.strip("\n") == rendered.text.strip("\n"):
            # Do not silently discard even a single display-leading newline.
            # Only boundary LF differences are downgraded; spaces/tabs aren't.
            report.counts["code_boundary"] += 1
            def boundaries(value):
                return (len(value) - len(value.lstrip("\n")),
                        len(value) - len(value.rstrip("\n")))
            report.issue(rel, f"code block {i}: boundary newlines only, source={boundaries(original.text)}, HTML={boundaries(rendered.text)} (leading, trailing)", rendered.line, warning=True)
        else:
            report.counts["code_different"] += 1
            a, b = original.text, rendered.text
            offset = next((j for j, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
            report.issue(rel, f"code block {i}: content differs at character {offset + 1}; source {a[max(0, offset-24):offset+56]!r}; HTML {b[max(0, offset-24):offset+56]!r}", rendered.line)
    explicit, inferred = source_anchors(prose)
    missing_explicit = sorted(explicit - page.anchors)
    missing_inferred = sorted(inferred - page.anchors - explicit)
    if missing_explicit:
        report.issue(rel, "missing explicit source anchors: " + ", ".join(missing_explicit))
    if missing_inferred:
        report.issue(rel, f"{len(missing_inferred)} inferred source heading anchors absent (heuristic): "
                     + ", ".join(missing_inferred[:12])
                     + (", ..." if len(missing_inferred) > 12 else ""), warning=True)


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("--pages", nargs="+", metavar="PATH", help="site-relative or absolute HTML paths; enables source fidelity for these pages only")
    args = cli.parse_args(argv)
    root, report = ROOT.resolve(), Report()
    nav = load_nav(root, report)
    selected = []
    for value in args.pages if args.pages is not None else nav:
        path = Path(value)
        path = (path if path.is_absolute() else root / path).resolve()
        try:
            rel = path.relative_to(root)
        except ValueError:
            report.issue(value, "selected page is outside the site root")
            continue
        if any(p in SKIP_DIRS or p.startswith(".") for p in rel.parts) or path.suffix.lower() not in {".html", ".htm"}:
            report.issue(value, "selected path must be a nonexcluded HTML page")
            continue
        if path not in selected:
            selected.append(path)
    parsed = {}
    for path in actual_html(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = read_text(path)
        except (OSError, UnicodeError) as exc:
            report.issue(rel, f"cannot read UTF-8 HTML: {exc}")
            continue
        page = PageParser().finish(text)
        parsed[path] = (text, page)
        for line, ident, first in page.duplicates:
            report.issue(rel, f"duplicate id {ident!r} (first at line {first})", line)
    print(f"Scope: {len(parsed)} actual HTML files for links/IDs; {len(selected)} pages for structure/typography; source fidelity {'explicit pages only' if args.pages else 'off (use --pages)'}.")
    check_links(root, parsed, report)
    sources = {}
    if args.pages is not None:
        sources, snapshot = load_sources(root, report)
        print(f"Source: {snapshot.relative_to(root).as_posix()} ({report.counts['source_markers']} markers)")
    for path in selected:
        rel = path.relative_to(root).as_posix()
        if path not in parsed:
            report.issue(rel, "selected page missing or unreadable")
            continue
        text, page = parsed[path]
        check_page(root, path, text, page, report)
        report.counts["pages_checked"] += 1
        if args.pages is not None:
            if rel not in sources:
                report.issue(rel, "no source marker mapping")
            else:
                compare_source(rel, page, sources[rel], report)
    c = report.counts
    print(f"Checked: {c['pages_checked']} pages; {c['references']} href/src ({c['local_references']} local), {c['fragments']} HTML fragments.")
    if args.pages is not None:
        print(f"Code: {c['code_html']} HTML / {c['code_source']} source blocks; {c['code_exact']} exact, {c['code_boundary']} boundary-newline warnings, {c['code_different']} content failures.")
    if c["non_html_fragments"]:
        print(f"Note: {c['non_html_fragments']} non-HTML fragments not validated (target existence checked).")
    print(f"Result: {report.errors} hard errors, {report.warnings} warnings.")
    return 1 if report.errors else 0


if __name__ == "__main__":
    # Windows terminals may not support source Unicode in diagnostic snippets.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    sys.exit(main())
