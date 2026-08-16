#!/usr/bin/env python3
"""
refresh_profile.py — check every repo in the ecosystem against the identity manifest.

Lives in rnv-brand alongside engine/brand.py. Brand tokens are the machine source
for colour and type; profile.json is the machine source for facts about the person
and the products. Same rule: import it, never hardcode.

WHY THIS EXISTS
Surfaces drift independently, and the drift is invisible from inside the surface
that's wrong. Every miss in the July 2026 alignment was caught by comparing two
surfaces that should have agreed, never by reading one harder:

  · the resume had the Vitalyst roles backwards while LinkedIn had them right
  · the GitHub README said "open identity standard" three days after the site
    was clean
  · a post shipped a retired author bio from a template copy already fixed
  · og-image.png claimed 5,003 tests while the homepage said 5,021

So this is a consistency checker, not a linter. Change a fact in profile.json,
run this, and it names every surface that now disagrees.

EXEMPTIONS ARE BOUNDED, MARKED, AND AUDITED
The corpus describes the machine, and so does the blog. Posts about the eval
suite's own history will legitimately quote retired phrasing, which means the
checker needs somewhere for a true-but-historical string to live. A path skip is
the tempting answer and the wrong one: it is unbounded, it is silent, and it
never dies, so coverage shrinks a file at a time and a green run stops meaning
what it used to mean. Four mechanisms replace it:

  · a bounded exemption, {"path": ..., "max": 1}, keeps the file checked and
    asserts a known quantity; occurrence two fails
  · a "retired-ok" marker on or above the line excuses one occurrence in the
    file where a reader can see why, the same move is_refusal made when it
    stopped matching substrings and started testing structure
  · an exemption ledger prints what fired and warns on any exemption that
    matched nothing, because a dead exemption is coverage lost for no benefit
  · ARCHIVE_EXCLUDE declares whole paths that are historical record by
    definition — dated snapshots whose job is preserving the phrasing of
    their day — and skips retirement checks there wholesale. It differs from
    the path skip condemned above in the two ways that matter: it is a class
    chosen once rather than files excused one retirement at a time, and the
    ledger prints it every sweep, so the boundary stays visible

A bare string in exempt[] still works and still means unbounded; the ledger names
those so they can be tightened rather than forgotten.

WHAT IT REACHES
  --all         every repo in the manifest's repos{} block, fetched as a tarball;
                no local clones needed, which suits a phone-and-Codespace workflow
  --repo NAME   one repo, fetched the same way
  --root PATH   a local checkout
  --docx DIR    a local directory of .docx, read without dependencies by
                unzipping the XML. Opt-in and recordless: no workflow passes
                this, nothing is fetched, nothing is stored
  --manual      the checklist for LinkedIn, Hugging Face, dev.to, MCP registry

USAGE
  python scripts/refresh_profile.py --all
  python scripts/refresh_profile.py --repo rnvizion.github.io
  python scripts/refresh_profile.py --docx ~/Documents/outgoing
  python scripts/refresh_profile.py --root ../rnvizion.github.io
  python scripts/refresh_profile.py --manual

Exit code is non-zero when a surface disagrees, so it works as a CI gate. It never
edits anything: the surfaces are too heterogeneous for safe automatic rewriting,
and a wrong fix is worse than a reported drift.
"""
from __future__ import annotations

import argparse
import fnmatch
import io
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
MANIFEST = REPO_ROOT / "profile.json"
OWNER = "RNVizion"

SKIP_DIRS = {".git", "node_modules", "assets/fonts", "chroma", "__pycache__", ".venv", "dist"}
# .vcf added 2026-08-12: card/rnvizion.vcf is a published surface carrying the
# brand number, an email, and two profile URLs, and the walk was skipping it on
# extension alone -- a public surface that passes every run by never being
# opened. Probed before landing: exactly one .vcf exists across all fourteen
# repos in the manifest, and it produces zero new findings. Any future addition
# here gets the same treatment -- widening the walk without probing the newly
# visible set is how a green run stops meaning anything.
# .astro added 2026-08-15 for the same reason .vcf was: rnv-live's only page is
# an .astro file, the repo carries retired/contact/renames, and all three passed
# on a repo whose actual surface the walk never opened. Probed before landing --
# exactly one .astro exists across the fourteen repos and it produces zero new
# findings from the existing checks. It is also the file the var() guard below
# needs to read.
TEXT_EXT = {".html", ".md", ".py", ".yml", ".yaml", ".json", ".xml", ".txt", ".sh", ".jsonl", ".toml", ".vcf", ".astro"}

# The manifest names every retired phrase, and this file quotes several while
# explaining itself. A checker that measures text must exclude its own text, or
# it reads its own words back and calls them violations. That is the same failure
# the eval scorer hit once the corpus began describing the machine.
SELF_EXCLUDE = {"profile.json", "scripts/refresh_profile.py", "refresh_profile.py"}

# Historical record by definition: dated snapshots whose whole purpose is
# preserving the phrasing of their day. Retirement checks (retired phrases and
# retired product names) skip these wholesale — the June baseline IS a 40-case
# run and must keep saying so, or the archive stops being an archive. Everything
# else still applies: contact, renames, and facts read these files like any
# other, because history is exempt from retirement, not from being read. The
# ledger prints this exclusion every full sweep. Add a path here only when its
# contents are frozen by intent: eval history, changelogs, dated reports.
ARCHIVE_EXCLUDE = ("docs/eval-history/",)


def _archived(rel: str) -> bool:
    return any(rel.startswith(a) for a in ARCHIVE_EXCLUDE)


# Point-of-use marker. "retired-ok" on the line, or the line above, excuses one
# occurrence. Bare form excuses any phrase; "retired-ok: 40-case" excuses only
# that one, which is the form to prefer because it cannot over-excuse later.
MARKER = "retired-ok"


# --------------------------------------------------------------------------
def norm(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&amp;", "&").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", s).strip()


# One walk, one read, reused by every check that scans text. The old shape read
# every file once per retired phrase: twelve passes over fourteen repos, which is
# most of the workflow's twenty-minute budget spent re-reading the same bytes.
# The walk also records what it saw and what it read, because the exemption
# ledger cannot judge a dead exemption without knowing whether the file it
# points at was ever opened.
_FILE_CACHE: dict[str, tuple[list[tuple[str, str]], frozenset, frozenset]] = {}


def _skipped(rel: str) -> bool:
    """Skip-dir test by whole path component, never by prefix. The old test was
    rel.startswith(d), and ".github" starts with ".git": every workflow file in
    every repo was invisible, including the one that runs this checker. Wrapping
    both sides in slashes makes `.git` match only the `.git` segment, and keeps
    multi-segment entries like assets/fonts working."""
    return any(f"/{d}/" in f"/{rel}/" for d in SKIP_DIRS)


def _sniffs_text(p: Path) -> bool:
    """True when an extensionless file reads as UTF-8 text. NOTICE, LICENSE,
    CODEOWNERS, Dockerfile and their kin carry no suffix, and an extension
    whitelist reads right past them — which is how a live exemption spent a week
    reported dead. Sniffing the class closes it instead of enumerating it. A
    trailing multibyte character cut by the sample window is tolerated."""
    try:
        with p.open("rb") as fh:
            head = fh.read(8192)
    except OSError:
        return False
    if b"\x00" in head:
        return False
    for trim in range(4):
        try:
            head[: len(head) - trim].decode("utf-8")
            return True
        except UnicodeDecodeError:
            continue
    return False


def _collect(root: Path):
    key = str(root.resolve())
    cached = _FILE_CACHE.get(key)
    if cached is not None:
        return cached
    files: list[tuple[str, str]] = []
    present: set[str] = set()
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if _skipped(rel):
            continue
        present.add(rel)
        if rel in SELF_EXCLUDE:
            continue
        if not (p.suffix.lower() in TEXT_EXT or (p.suffix == "" and _sniffs_text(p))):
            continue
        files.append((rel, p.read_text(encoding="utf-8", errors="ignore")))
    out = (files, frozenset(present), frozenset(r for r, _ in files))
    _FILE_CACHE[key] = out
    return out


def text_files(root: Path) -> list[tuple[str, str]]:
    """Return [(relative path, body)] for every text file under root, cached."""
    return _collect(root)[0]


def tree_presence(root: Path) -> tuple[frozenset, frozenset]:
    """(files that exist under root, files that were actually read)."""
    _, present, scanned = _collect(root)
    return present, scanned


def clear_file_cache() -> None:
    _FILE_CACHE.clear()


RETRY_DELAY = 2.0   # seconds, once, and only for failures a retry could fix

# Appended to every MISS so the reason code is self-explaining in a public
# issue body, where the reader has no access to this source.
MISS_HINT = ('"gone" means 404 on every branch: renamed, private or deleted, '
             'and the manifest is wrong about what exists')


def fetch_repo(name: str, dest: Path) -> tuple[Path | None, str]:
    """Download a repo tarball and unpack it. No clone, no auth, no local state.

    Returns (root, reason). reason is "" on success, "gone" when GitHub answered
    404 on every branch, and "unreachable" for anything else.

    THE TWO ARE DIFFERENT FINDINGS AND MUST NOT COLLAPSE. A 404 on every branch
    is a fact about the ecosystem: the repo was renamed, made private, or
    deleted, and the manifest is now wrong about what exists. It is stable, it
    will 404 again next Monday, and retrying it only burns twenty seconds.
    Anything else -- timeout, DNS, a 5xx, a reset -- is a statement about this
    run's network and nothing about the ecosystem, which is why it gets one
    retry and why its report reads differently.

    Both stop the sweep from being complete. Only one of them is drift.
    """
    for attempt in (1, 2):
        saw_transient = False
        for branch in ("main", "master"):
            url = f"https://codeload.github.com/{OWNER}/{name}/tar.gz/refs/heads/{branch}"
            try:
                with urllib.request.urlopen(url, timeout=60) as r:
                    if r.status != 200:
                        saw_transient = True
                        continue
                    data = r.read()
            except urllib.error.HTTPError as e:
                # 404 is the answer, not a failure to get one. Anything else is.
                if e.code != 404:
                    saw_transient = True
                continue
            except Exception:
                saw_transient = True
                continue
            out = dest / name
            out.mkdir(parents=True, exist_ok=True)
            with tarfile.open(fileobj=io.BytesIO(data)) as tf:
                members = [m for m in tf.getmembers()
                           if not m.name.startswith("/") and ".." not in m.name]
                tf.extractall(out, members=members)
            inner = next((c for c in out.iterdir() if c.is_dir()), None)
            return (inner or out), ""
        if not saw_transient:
            return None, "gone"
        if attempt == 1:
            time.sleep(RETRY_DELAY)
    return None, "unreachable"


def docx_text(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "replace")
    except Exception:
        return ""
    return norm(re.sub(r"<[^>]+>", " ", re.sub(r"</w:p>", "\n", xml)))


class Report:
    """FAIL breaks the build. WARN is worth reading. NOTE is bookkeeping that
    should be visible without being alarming; the exemption ledger lives there,
    because coverage you cannot see is coverage you cannot trust."""

    def __init__(self):
        self.findings: list[tuple[str, str, str, str]] = []   # sev, scope, surface, msg
        self.checks = 0
        # (phrase, exempt path) -> occurrences it actually covered
        self.exempt_use: dict[tuple[str, str], int] = {}
        # phrase -> occurrences excused by a point-of-use marker
        self.marked: dict[str, int] = {}
        # every file that exists under a scanned root, and every file read.
        # The gap between the two is what lets the ledger tell "the phrase is
        # gone" from "the file was never opened" — advice that differs by 180°.
        self.present: set[str] = set()
        self.scanned_files: set[str] = set()
        # (scope, rel) skipped by ARCHIVE_EXCLUDE, counted for the ledger
        self.archived: set[tuple[str, str]] = set()

    def absorb_tree(self, root: Path):
        present, scanned = tree_presence(root)
        self.present |= present
        self.scanned_files |= scanned

    def mark_archived(self, scope: str, rel: str):
        self.archived.add((scope, rel))

    def fail(self, scope, surface, msg):
        self.findings.append(("FAIL", scope, surface, msg))

    def warn(self, scope, surface, msg):
        self.findings.append(("WARN", scope, surface, msg))

    def note(self, scope, surface, msg):
        self.findings.append(("NOTE", scope, surface, msg))

    def miss(self, scope, surface, msg):
        """A surface that could not be read.

        Deliberately NOT a warning. A warning is something you read and judge; a
        MISS is the run telling you it does not know. Collapsing the two is how
        an unfetchable repo used to exit 0 and close the drift issue while
        claiming every surface agreed -- the report was accurate about what it
        read and silent about what it never opened, and silence read as
        agreement. Its own bucket, its own exit code, its own issue.
        """
        self.findings.append(("MISS", scope, surface, msg))

    @property
    def failures(self):
        return [f for f in self.findings if f[0] == "FAIL"]

    @property
    def warnings(self):
        return [f for f in self.findings if f[0] == "WARN"]

    @property
    def misses(self):
        return [f for f in self.findings if f[0] == "MISS"]


# --------------------------------------------------------------------------
# exemption plumbing
# --------------------------------------------------------------------------
def exempt_entries(entry: dict) -> list[dict]:
    """Normalise exempt[] to dicts. A bare string is the legacy unbounded form;
    it keeps working, and the ledger names it so it can be tightened."""
    out = []
    for e in entry.get("exempt", []):
        if isinstance(e, str):
            out.append({
                "path": e,
                "max": None,
                "reason": entry.get("exempt_reason", ""),
                "added": None,
                "legacy": True,
            })
        else:
            out.append({
                "path": e.get("path", ""),
                "max": e.get("max"),
                "reason": e.get("reason", entry.get("exempt_reason", "")),
                "added": e.get("added"),
                "legacy": False,
            })
    return out


def path_matches(rel: str, pat: str) -> bool:
    """One predicate for both exemption matching and the ledger's presence
    test. If these two used different rules, an exemption could fire against a
    file the ledger swears does not exist."""
    return fnmatch.fnmatch(rel, pat) or rel.endswith(pat)


def exempt_for(entries: list[dict], rel: str) -> dict | None:
    for e in entries:
        if path_matches(rel, e["path"]):
            return e
    return None


def marker_excuses(lines: list[str], idx: int, phrase: str) -> bool:
    """True when a retired-ok marker sits on the line or the one above it."""
    for probe in (idx, idx - 1):
        if probe < 0 or probe >= len(lines):
            continue
        line = lines[probe]
        pos = line.lower().find(MARKER)
        if pos == -1:
            continue
        rest = line[pos + len(MARKER):].lstrip(" :\t")
        for closer in ("-->", "*/", "#}"):
            rest = rest.split(closer)[0]
        rest = rest.strip()
        if not rest or phrase.lower() in rest.lower():
            return True
    return False


# --------------------------------------------------------------------------
# checks — each takes (cfg, root, rep, scope)
# --------------------------------------------------------------------------
def check_retired(cfg, root, rep, scope):
    """Retired phrasing must not appear on a live surface. Occurrences survive
    three filters before they fail: a protected string in context, a bounded
    exemption in the manifest, or a marker at the point of use."""
    protected = cfg.get("protected", {}).get("strings", [])
    phrases = [(e["phrase"], e.get("reason", ""), exempt_entries(e)) for e in cfg["retired"]]

    for rel, body in text_files(root):
        if _archived(rel):
            rep.mark_archived(scope, rel)
            continue
        lower = body.lower()
        # cheap pre-filter; splitting lines for every file times every phrase is
        # the expensive part, and most files contain none of these strings
        if not any(p.lower() in lower for p, _, _ in phrases):
            continue
        lines = body.split("\n")
        for phrase, reason, exempts in phrases:
            ex = exempt_for(exempts, rel)
            live = []
            for m in re.finditer(re.escape(phrase), body, re.I):
                ctx = body[max(0, m.start() - 80):m.end() + 80]
                if any(p.lower() in ctx.lower() for p in protected):
                    continue
                idx = body[:m.start()].count("\n")
                if marker_excuses(lines, idx, phrase):
                    rep.marked[phrase] = rep.marked.get(phrase, 0) + 1
                    continue
                live.append(idx + 1)

            if not live:
                continue
            if ex is None:
                for line in live:
                    rep.fail(scope, f"{rel}:{line}", f'retired "{phrase}" — {reason}')
                continue

            key = (phrase, ex["path"])
            rep.exempt_use[key] = rep.exempt_use.get(key, 0) + len(live)
            cap = ex["max"]
            if cap is not None and len(live) > cap:
                rep.fail(
                    scope, f"{rel}:{live[cap]}",
                    f'retired "{phrase}" appears {len(live)} times; the exemption allows '
                    f'{cap}. Either the new use is live copy, or the bound needs raising '
                    f'deliberately'
                )
    rep.checks += len(phrases)


# --------------------------------------------------------------------------
# phone shapes — added 2026-08-12 with profile.json v1.3.0
#
# The four formats a contact surface actually prints. Narrow on purpose: looser
# patterns start matching version strings, IDs and dates, and a guard that cries
# wolf gets muted, which is worse than not having it. Measured across all
# fourteen repos before landing — eight hits, seven of them real contact numbers
# and one a reserved-fictional placeholder, which is the only exemption.
# --------------------------------------------------------------------------
PHONE_SHAPE = re.compile(
    r"\(\d{3}\)\s?\d{3}-\d{4}"      # (202) 987-9948
    r"|\+1\d{10}"                     # +12029879948
    r"|\b\d{3}-\d{3}-\d{4}\b"        # 202-987-9948
    r"|\b\d{3}\.\d{3}\.\d{4}\b"     # 202.987.9948
)


def permitted_phones(cfg):
    """The only numbers allowed to appear anywhere. None if the manifest has none.

    This is the whole design in one function. The guard is written INSIDE-OUT: it
    never learns the personal cell, because a manifest that names a forbidden
    value publishes it. It knows only what is PERMITTED, so anything else fails —
    including a number it has never seen. That is the difference between a
    tripwire on the key coming back and a blocklist of one string.
    """
    bp = cfg.get("identity", {}).get("brand_phone")
    if not isinstance(bp, dict):
        return None
    vals = {v for k, v in bp.items() if not k.startswith("_") and isinstance(v, str)}
    return vals or None


def _json_strings(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from _json_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for n, v in enumerate(node):
            yield from _json_strings(v, f"{path}[{n}]")
    elif isinstance(node, str):
        yield path, node


def audit_manifest_phones(cfg):
    """Manifest paths carrying a number that is not the brand routing number.

    Separate from the surface walk because profile.json sits in SELF_EXCLUDE and
    is invisible to it. Without this, the one file the whole system is named for
    would be the one file the phone guard could not read.

    NOTE WHAT IS NOT RETURNED: the offending value. This report is catted
    verbatim into a public issue body, a public Actions log, and a 30-day
    artifact. A guard that quoted what it found would republish the number it
    exists to suppress, in three more places than the one it caught.
    """
    allowed = permitted_phones(cfg)
    if allowed is None:
        return ["identity.brand_phone is absent or empty, so there is no "
                "permitted number and this guard has nothing to check against. "
                "Restore it rather than removing the check."]
    bad = sorted({p for p, s in _json_strings(cfg)
                  if (m := PHONE_SHAPE.search(s)) and m.group(0) not in allowed})
    return [f"{path} carries a phone-shaped value that is not the brand routing "
            f"number. The value is withheld from this report on purpose. See "
            f"identity._phone_removed before doing anything else."
            for path in bad]


def check_contact(cfg, root, rep, scope):
    ident = cfg["identity"]
    for rel, body in text_files(root):
        for m in re.finditer(r"linkedin\.com/in/([A-Za-z0-9\-]+)", body):
            if m.group(0) != ident["linkedin"]:
                line = body[:m.start()].count("\n") + 1
                rep.fail(scope, f"{rel}:{line}",
                         f'LinkedIn is "{m.group(0)}", manifest says "{ident["linkedin"]}"')
        for m in re.finditer(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", body):
            a = m.group(0)
            role = {k.lower() for k in ident.get("role_emails", {})
                    if not k.startswith("_")}
            if (a == ident["email"] or a.lower() in role
                    or "example" in a or "noreply" in a or "users.noreply" in a):
                continue
            if "rnvizion" in a.lower() or "vizionary" in a.lower():
                line = body[:m.start()].count("\n") + 1
                rep.warn(scope, f"{rel}:{line}", f'address "{a}" is not {ident["email"]}')
    check_phones_on_surfaces(cfg, root, rep, scope)
    rep.checks += 1


def check_phones_on_surfaces(cfg, root, rep, scope):
    """Any phone-shaped string on a surface must be the brand routing number.

    Deliberately folded into check_contact rather than registered as its own
    CHECKS key. Every one of the fourteen repos names its check groups
    explicitly, so run_repo's `list(CHECKS)` default never applies — a new
    registry key would appear armed in the source and run on exactly zero
    surfaces until fourteen manifest entries opted in. Coverage that depends on
    remembering is the failure mode this file exists to catch.
    """
    allowed = permitted_phones(cfg) or set()
    budget = {ex["path"]: ex.get("max", 0)
              for ex in cfg.get("phone_exemptions", [])
              if isinstance(ex, dict) and ex.get("repo") == scope}
    for rel, body in text_files(root):
        for m in PHONE_SHAPE.finditer(body):
            if m.group(0) in allowed:
                continue
            if budget.get(rel, 0) > 0:
                budget[rel] -= 1
                continue
            line = body[:m.start()].count("\n") + 1
            rep.fail(scope, f"{rel}:{line}",
                     "phone-shaped string that is not the brand routing number; "
                     "the value is withheld from this report on purpose, because "
                     "this text is pasted into a public issue")


def check_renames(cfg, root, rep, scope):
    protected = cfg.get("protected", {}).get("strings", [])
    pats = [(re.compile(r"github\.com/" + OWNER + "/" + re.escape(old) + r"\b"), new)
            for old, new in cfg["renamed_repos"].items() if not old.startswith("_")]
    for rel, body in text_files(root):
        for pat, new in pats:
            for m in pat.finditer(body):
                if any(p in body[max(0, m.start() - 80):m.end() + 80] for p in protected):
                    continue
                line = body[:m.start()].count("\n") + 1
                rep.fail(scope, f"{rel}:{line}", f'old repo name in a link; use "{new}"')
    rep.checks += len(pats)


def check_bio(cfg, root, rep, scope):
    canonical = norm(cfg["bio"]["canonical"])
    for pattern in cfg["bio"]["must_appear_in"]:
        matches = sorted(root.glob(pattern))
        if not matches:
            rep.warn(scope, pattern, "no files matched")
            continue
        for p in matches:
            rel = p.relative_to(root).as_posix()
            if canonical not in norm(p.read_text(encoding="utf-8", errors="ignore")):
                rep.fail(scope, rel, "author bio does not match the canonical text")
            rep.checks += 1


def check_facts(cfg, root, rep, scope):
    for name, spec in cfg["facts"].items():
        if name.startswith("_"):
            continue
        sources = spec.get("sources", [])
        if not sources:
            # A fact with no reachable source is enforced nowhere. That is exactly
            # how "40-case" survived on three surfaces: the number was known and
            # nothing was watching the pages that printed it.
            rep.warn(scope, f"facts.{name}",
                     f"declares no source file; '{spec.get('value')}' is checked on no "
                     f"reachable surface. Add the page that prints it")
            continue
        # 'match' is the literal phrase the page must print; 'value' is the
        # semantic fact. A bare value is a useless needle — "60" matches a CSS
        # font weight — which is how a stale resume PAGE once passed this check with
        # total confidence. Fall back to value when no match is given, so a
        # fact without one keeps working exactly as before.
        needle = spec.get("match") or spec["value"]
        for src in sources:
            p = root / src
            if not p.exists():
                rep.warn(scope, src, f"declared source for '{name}' not found")
                continue
            if needle not in p.read_text(encoding="utf-8", errors="ignore"):
                what = (f"the phrase \u201c{needle}\u201d (match for value {spec['value']})"
                        if needle != spec["value"] else f"{spec['value']}")
                rep.fail(scope, src, f"'{name}' should print {what}; not present")
            rep.checks += 1
    # the stat block and the rendered article count must agree
    idx = root / "index.html"
    if idx.exists():
        body = idx.read_text(encoding="utf-8", errors="ignore")
        rendered = len(re.findall(r'<article class="project">', body))
        claimed = cfg["facts"].get("projects", {}).get("value")
        if claimed and rendered and str(rendered) != str(claimed):
            rep.fail(scope, "index.html",
                     f"stat block claims {claimed} projects; {rendered} articles rendered")
        rep.checks += 1


def check_products(cfg, root, rep, scope):
    """Retired display names must not appear. Declared repo slugs must be the
    ones linked. This is the three-layer naming rule, enforced."""
    retired_names = [(p["retired_display"], p["display"]) for p in cfg["products"]
                     if p.get("retired_display")]
    if not retired_names:
        return
    for rel, body in text_files(root):
        if _archived(rel):
            rep.mark_archived(scope, rel)
            continue
        for old, new in retired_names:
            if old not in body:
                continue
            lines = body.split("\n")
            for m in re.finditer(re.escape(old), body):
                idx = body[:m.start()].count("\n")
                if marker_excuses(lines, idx, old):
                    rep.marked[old] = rep.marked.get(old, 0) + 1
                    continue
                rep.fail(scope, f"{rel}:{idx + 1}",
                         f'retired product name "{old}"; use "{new}"')
    rep.checks += len(retired_names)


def check_thresholds(cfg, root, rep, scope):
    """The gates are declared once and quoted on the web resume at
    resume/index.html. Verify the file still says what the manifest says.
    (Named precisely because two different artifacts share the word
    "resume"; the personal .docx are out of scope entirely.)

    An absent key is a failure, not a skip. thresholds.json is read by the eval
    with data.get(key, default), so a renamed or typo'd gate silently falls back
    to the default; the suite keeps passing and the page keeps quoting a bar
    that nothing enforces. A checker that stays quiet on absence reproduces that
    bug one layer up."""
    spec = cfg.get("eval_thresholds", {})
    p = root / "eval" / "thresholds.json"
    if not p.exists():
        return
    try:
        live = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        rep.warn(scope, "eval/thresholds.json", "could not parse")
        return
    for key in ("retrieval_accuracy", "ooc_refusal_accuracy", "false_refusal_rate"):
        if key not in spec:
            continue
        if key not in live:
            rep.fail(scope, "eval/thresholds.json",
                     f"{key} is absent; the eval falls back to its default, so the "
                     f"manifest's {spec[key]} is enforced by nothing")
        elif float(spec[key]) != float(live[key]):
            rep.fail(scope, "eval/thresholds.json",
                     f"{key} is {live[key]}; manifest says {spec[key]}")
    rep.checks += 1


CHECKS = {
    "retired": check_retired, "contact": check_contact, "renames": check_renames,
    "bio": check_bio, "facts": check_facts, "products": check_products,
    "thresholds": check_thresholds,
}


def lint_documents(cfg, docx_dir, rep):
    """A pre-send lint for local .docx. Opt-in, recordless, and NOT a check.

    Named lint_ rather than check_ on purpose. Every check_* function in this
    file is a CHECKS member that runs per repo, unattended, on a schedule. This
    one runs only when a human types a path to their own local files, so calling
    it a check would put it in a family it does not belong to and imply coverage
    that no schedule provides.

    Renamed 2026-08-12 from check_docx, and its scope label from "resumes" to
    "documents". The manifest stopped modelling the personal resume variants that
    day; the tool kept the vocabulary, which is the same thing one layer down.
    Whatever you point this at is a document, and the lint has no opinion about
    what kind.

    WHAT IT DOES NOT DO, stated rather than absorbed: facts are not verified
    here. Selection ran off `appears_in: "resumes"` and that claim is gone, so
    the old code would now select nothing and quietly do less than its name
    suggested -- the exact failure this file exists to catch. The fact loop was
    deleted rather than left returning an empty list.

    What survives is the half that matters most on paper: retired phrases and
    retired product names. A pushed fix cannot recall a printed page, and this
    is the only guard anywhere on that surface.
    """
    files = sorted(Path(docx_dir).glob("*.docx"))
    if not files:
        rep.warn("documents", str(docx_dir), "no .docx found")
        return
    ident = cfg["identity"]
    print(f"\n  {len(files)} document(s) read locally; nothing recorded. "
          f"Retired phrases, retired product names, email and LinkedIn only — "
          f"facts are not checked here, by decision.")
    for f in files:
        text = docx_text(f)
        if not text:
            rep.warn("documents", f.name, "could not read document text")
            continue
        for entry in cfg["retired"]:
            if re.search(re.escape(entry["phrase"]), text, re.I):
                rep.fail("documents", f.name, f'retired "{entry["phrase"]}"')
        for prod in cfg["products"]:
            old = prod.get("retired_display")
            if old and old in text:
                rep.fail("documents", f.name, f'retired product name "{old}"')
        for label, val in (("email", ident["email"]), ("LinkedIn", ident["linkedin"])):
            if val not in text:
                rep.fail("documents", f.name, f"{label} missing; expected {val}")
        rep.checks += 1


# --------------------------------------------------------------------------
# fact verification — derive what can be derived, bound what cannot
# --------------------------------------------------------------------------
def _iter_py(root: Path):
    for py in root.rglob("*.py"):
        rel = py.relative_to(root).as_posix()
        if _skipped(rel):
            continue
        yield py


def _count_test_functions(root: Path) -> int:
    n = 0
    for py in _iter_py(root):
        body = py.read_text(encoding="utf-8", errors="ignore")
        n += len(re.findall(r"^\s*(?:async\s+)?def test_", body, re.M))
    return n


def _count_parametrized_files(root: Path) -> int:
    n = 0
    for py in _iter_py(root):
        body = py.read_text(encoding="utf-8", errors="ignore")
        if "parametrize" in body:
            n += 1
    return n


# --------------------------------------------------------------------------
# R2 — the type guard
# --------------------------------------------------------------------------

class _MarkFinder(HTMLParser):
    """Elements whose entire text is the mark string, tagged with their class."""

    def __init__(self, mark, selectors):
        super().__init__(convert_charrefs=True)
        self.mark, self.selectors = mark, selectors
        self.stack, self.hits = [], []

    def handle_starttag(self, tag, attrs):
        self.stack.append((tag, dict(attrs).get("class", "")))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        # TWO DISCRIMINATORS, BOTH REQUIRED, and each alone produces false
        # findings on a live surface. THE MARK IS A ROLE, NOT A STRING.
        #
        #   text only  -> the blog byline renders the brand name as an author
        #                 credit in mono on eight files, which the register's
        #                 Labels row explicitly permits ("the tracked long form
        #                 beneath a mark ... footers, captions").
        #   class only -> `.wordmark` is the AIII initiative mark on aiii/ (mono,
        #                 correct by decision) and was the RNVizion brand mark on
        #                 rnv-live. Same class, two roles, one surface each.
        #
        # A check cannot infer "this is the wordmark" from contents, because the
        # contents are the brand name either way. Same argument that makes F13's
        # allowlist honest and an inferred scope a hole.
        if data.strip() != self.mark or not self.stack:
            return
        if self.stack[-1][0] in NON_RENDERING_TAGS:
            return
        for _, cls in reversed(self.stack):
            for c in cls.split():
                if c in self.selectors:
                    return self.hits.append((self.stack[-1][0], cls))


NON_RENDERING_TAGS = {"title", "script", "style", "meta", "option", "textarea"}


def css_declarations(text):
    """selector -> {property: value}, parsed rather than matched.

    DECLARATIONS, NEVER BYTES. `.logo .dot` exists in four different whitespace
    formattings across the files that carry it -- identical declarations,
    identical values, identical order. A byte comparison reports four-way drift
    where nothing drifted, and a guard that false-fails gets loosened, which is
    how the real failure gets through.

    COMMENTS ARE STRIPPED FIRST, and that is not tidiness. A CSS comment can
    carry a colon, and this splits declarations on `:` -- so a rule whose comment
    explains the rule swallows the first real declaration and the property
    vanishes. Found by commenting the mark rule on rnv-live and watching the
    guard report that same mark as undeclared.
    """
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    out = {}
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", text):
        sel = " ".join(m.group(1).split()).split("\n")[-1].strip()
        decls = {}
        for d in m.group(2).split(";"):
            if ":" in d:
                k, v = d.split(":", 1)
                decls[k.strip()] = " ".join(v.split())
        if sel and decls:
            out.setdefault(sel, {}).update(decls)
    return out


def emitted_token_values(engine):
    """token name -> value, from the engine's own emitter.

    A page may declare its tokens inline, as the site does, or receive them from
    a stylesheet generated at deploy time that the page never contains, as
    rnv-live does. Resolving only against the file would report every rnv-live
    token as undeclared -- failing on the surface whose tokens are the MOST
    controlled, precisely because they come from source.
    """
    out = {}
    for surface in ("web", "app", "records"):
        try:
            r = subprocess.run([sys.executable, str(engine), "--css", surface],
                               capture_output=True, text=True, timeout=30)
        except Exception:
            return out
        for m in re.finditer(r"(--rnv-[a-z0-9-]+)\s*:\s*([^;]+);", r.stdout):
            out[m.group(1)] = m.group(2).strip()
    return out


# CSS weight keywords, so a failure can name what it actually saw. `bold` is 700
# and reads as a plausible mark weight to anyone not holding the register; saying
# "bold, which is 700" is more useful than "not 900".
WEIGHT_KEYWORDS = {"normal": 400, "bold": 700, "lighter": 100, "bolder": 900}


def _declared_weight(decls):
    """The numeric weight a rule declares, or None if it declares none.

    None is a FINDING, not a skip. A mark with no declared weight inherits, so
    its weight depends on whatever the page happens to set around it -- which is
    the same class of failure as a token that resolves to nothing, arriving one
    property over.
    """
    raw = (decls or {}).get("font-weight")
    if raw is None:
        return None, None
    v = raw.strip().lower()
    if v.isdigit():
        return int(v), raw
    return WEIGHT_KEYWORDS.get(v), raw


def _rule_for(cls, blocks):
    """The declaration block that carries this element's font-family."""
    for name in cls.split():
        for sel, decls in blocks.items():
            if sel.split()[-1].lstrip(".") == name and "font-family" in decls:
                return decls
    return None


def _resolve_family(cls, blocks, tokens):
    """The font-family declared for a class, with one level of var() resolution."""
    for name in cls.split():
        for sel, decls in blocks.items():
            if sel.split()[-1].lstrip(".") == name and "font-family" in decls:
                fam = decls["font-family"]
                v = re.match(r"var\((--[a-z0-9-]+)\)", fam)
                if v:
                    return tokens.get(v.group(1), v.group(1))
                return fam
    return None


def _requests_family(text, family):
    """Does this file actually LOAD the face, by any of the three mechanisms?

    The site requests through a Google Fonts link, rnv-live through an
    @fontsource npm import, and a self-contained page could use @font-face. All
    three are the same rule wearing different syntax, which is why this asks the
    question rather than looking for one shape.
    """
    f = family.strip().strip('"\'').lower()
    for line in text.splitlines():
        low = line.lower()
        if f not in low:
            continue
        if ("fonts.googleapis.com" in low or "@fontsource" in low
                or "@font-face" in low or "src:" in low):
            return True
    return f in re.sub(r"(?s)<style.*?</style>", " ", text).lower() and (
        "fonts.googleapis.com" in text.lower() or "@fontsource" in text.lower())


def verify_type(cfg, rep, workdir: Path):
    """R2. Every rendering of the mark uses the mark face, and requests it.

    NOT A `CHECKS` MEMBER, for the same two reasons as verify_tokens. Every one
    of the fourteen repos names its check groups explicitly, so a new registry
    key runs on zero surfaces while reading armed in the source. And this is not
    repo-shaped: it compares surfaces against a register and an emitter, which is
    verify_facts' shape rather than run_repo's. **Surfaces are discovered** -- any
    repo that grows an HTML or .astro file is checked from that moment, with no
    list to update and none to forget.

    WHAT IT CATCHES, in the order the register ranks them:

      1. The mark drawn in a face that is not the mark face. This is the failure
         with a live example: rnv-live rendered the brand mark in JetBrains Mono
         at 700 until 2026-08-16, four revisions after decision #15 retired the
         wordmark from mono, and nothing reported it.
      2. The mark face drawn but never requested. **The direction matters and it
         was nearly built backwards.** Loading a face and not drawing it is a
         wasted request that renders fine -- aiii/ does exactly that, kept
         deliberately per decision #18. Drawing a face without loading it puts
         the wordmark in a fallback and is visibly wrong. Arm the second.
      3. The canonical font link drifting on one page out of the set that shares
         it. No stored copy: the set defines itself, so there is nothing to go
         stale. Pages the register exempts are excluded first.
      4. F13 -- any page redefining `--font-body` away from the body face, which
         must fail even on an initiative page permitted to *use* another face in
         its `body` selector. The two conditions read different layers, and a
         token-only check would pass a page while verifying nothing.
    """
    reg = cfg.get("type_register")
    if not reg:
        rep.fail("type", "profile.json",
                 "type_register is absent; the mark face, the mark string and "
                 "the mark-bearing selectors are all unknown, so no surface was "
                 "checked. Restore it rather than removing this check")
        return

    engine = REPO_ROOT / "engine" / "brand.py"
    if not engine.exists():
        rep.fail("type", "engine/brand.py",
                 "not found; token values could not be resolved and no mark was "
                 "verified")
        return

    mark_family = reg["mark_family"]
    mark_weight = reg.get("mark_weight")
    mark_string = reg["mark_string"]
    selectors = set(reg["mark_selectors"]["selectors"])
    body_family = reg["body_family"]
    exempt_link = set(reg.get("no_canonical_link", {}).get("paths", []))
    tokens = emitted_token_values(engine)

    links, checked = {}, 0
    for name in [r for r in cfg["repos"] if not r.startswith("_")]:
        root, why = fetch_repo(name, workdir)
        if root is None:
            rep.miss("type", name,
                     f"could not fetch ({why}); no mark on this surface was "
                     f"verified. {MISS_HINT}")
            continue
        for relpath, body in text_files(root):
            if not relpath.endswith((".html", ".astro")):
                continue
            where = f"{name}/{relpath}"
            blocks = css_declarations(body)
            local = dict(tokens)
            for decls in blocks.values():
                for k, v in decls.items():
                    if k.startswith("--"):
                        local[k] = v

            finder = _MarkFinder(mark_string, selectors)
            try:
                finder.feed(body)
            except Exception:
                rep.warn("type", where, "could not be parsed as markup; no mark "
                                        "on this file was verified")
                continue

            for tag, cls in finder.hits:
                checked += 1
                fam = _resolve_family(cls, blocks, local)
                if fam is None:
                    rep.fail("type", where,
                             f"<{tag} class=\"{cls}\"> renders the mark and no "
                             f"font-family is declared for it, so it inherits "
                             f"whatever the page happens to set")
                elif mark_family.lower() not in fam.lower():
                    rep.fail("type", where,
                             f"<{tag} class=\"{cls}\"> renders the mark in "
                             f"{fam.split(',')[0].strip()} rather than "
                             f"{mark_family}")
                elif (weight := _declared_weight(_rule_for(cls, blocks)))[0] != mark_weight \
                        and mark_weight is not None:
                    found, raw = weight
                    detail = (f"declares no font-weight, so it inherits whatever "
                              f"the page sets" if raw is None else
                              f"is {raw}" + (f", which is {found}" if found and str(found) != raw.strip() else ""))
                    rep.fail("type", where,
                             f"<{tag} class=\"{cls}\"> renders the mark in the "
                             f"right face at the wrong weight: it {detail}, and "
                             f"the register rules {mark_weight}")
                elif not _requests_family(body, mark_family):
                    rep.fail("type", where,
                             f"draws {mark_family} and never requests it, so the "
                             f"mark renders in a fallback face. Loading without "
                             f"drawing is harmless; this is the other direction")

            if relpath not in exempt_link and not any(
                    relpath.endswith(e) for e in exempt_link):
                for m in re.finditer(r"https://fonts\.googleapis\.com/css2\?[^\"'>]+", body):
                    links.setdefault(m.group(0), []).append(where)

            for sel, decls in blocks.items():
                if "--font-body" in decls and body_family.lower() not in decls["--font-body"].lower():
                    rep.fail("type", where,
                             f"redefines --font-body away from {body_family}. "
                             f"An initiative page may USE another face in its "
                             f"body selector; it may not redefine the token")

    if len(links) > 1:
        ranked = sorted(links.items(), key=lambda kv: -len(kv[1]))
        for link, pages in ranked[1:]:
            for pg in pages:
                rep.fail("type", pg,
                         f"font link differs from the {len(ranked[0][1])} pages "
                         f"that share one string; no exemption covers it")
    if checked == 0:
        rep.note("type", "-",
                 "no surface in the ecosystem renders the mark; nothing compared")
    rep.checks += 1


def verify_tokens(cfg, rep, workdir: Path):
    """Every `var(--rnv-*)` on a surface must resolve against what emit_css emits.

    THE GAP THIS CLOSES. `engine/brand.py`'s emit_css derives CSS custom property
    names straight from the WEB dict keys, and rnv-live's deploy.yml pipes that
    into src/styles/tokens.css. Rename a key here and a custom property renames
    in another repository's stylesheet. Its index.astro references those
    properties by name, so a rename landed without its consumer leaves var()
    calls resolving to nothing, a page deploying with no background, and -- until
    today -- no check anywhere reporting it. rnv-live's own guard asserts that
    hex literals live in tokens.css; it never asserts that a var() resolves.

    That is not hypothetical. The ground ramp rename on 2026-08-14 and the serif
    role rename on the 15th were both this exact shape, and both were caught by
    running this comparison BY HAND. This is that comparison, automated.

    NOT A `CHECKS` MEMBER, DELIBERATELY. Every one of the fourteen repos names
    its check groups explicitly, so a new registry key runs on zero surfaces
    while reading armed in the source. This is also not repo-shaped: it compares
    one source file against every consumer of it, which is verify_facts' shape,
    not run_repo's. It therefore runs unconditionally in the facts pass -- the
    same dispatch decided for expiring_surfaces and for the same reason.

    CONSUMERS ARE DISCOVERED, NOT LISTED. A hardcoded consumer list is a
    construct that goes stale silently the first time a new surface adopts
    emit_css. Instead every fetched repo is scanned for `var(--rnv-*)`, so a new
    consumer arms itself. The cost is that this pass fetches repos again; the
    benefit is that there is no list to forget.
    """
    engine = REPO_ROOT / "engine" / "brand.py"
    if not engine.exists():
        # An early return with no finding is a check that reads armed and
        # verifies nothing. Say so instead.
        rep.fail("tokens", "engine/brand.py",
                 "not found; the emitted token set could not be built, so no "
                 "var() reference was verified")
        return

    emitted = set()
    for surface in ("web", "app", "records"):
        try:
            out = subprocess.run(
                [sys.executable, str(engine), "--css", surface],
                capture_output=True, text=True, timeout=30)
        except Exception as exc:
            rep.fail("tokens", "engine/brand.py",
                     f"--css {surface} could not be run ({type(exc).__name__}); "
                     f"no var() reference was verified against it")
            return
        if out.returncode != 0:
            rep.fail("tokens", "engine/brand.py",
                     f"--css {surface} exited {out.returncode}; "
                     f"no var() reference was verified against it")
            return
        emitted |= set(re.findall(r"--rnv-[a-z0-9-]+", out.stdout))

    if not emitted:
        rep.fail("tokens", "engine/brand.py",
                 "emitted no --rnv-* properties at all; a comparison against an "
                 "empty set would pass every surface and verify nothing")
        return

    checked = 0
    for name in [r for r in cfg["repos"] if not r.startswith("_")]:
        root, why = fetch_repo(name, workdir)
        if root is None:
            rep.miss("tokens", name,
                     f"could not fetch ({why}); var() references in this repo "
                     f"were not verified. {MISS_HINT}")
            continue
        for relpath, body in text_files(root):
            used = set(re.findall(r"var\((--rnv-[a-z0-9-]+)", body))
            if not used:
                continue
            checked += 1
            for token in sorted(used - emitted):
                rep.fail("tokens", f"{name}/{relpath}",
                         f"references {token}, which engine/brand.py does not "
                         f"emit. A renamed or removed key leaves this resolving "
                         f"to nothing and the surface renders without it")
    if checked == 0:
        # Zero consuming files is indistinguishable from a broken scan, and the
        # difference matters: one means nothing consumes the tokens, the other
        # means the guard verified nothing while reporting clean.
        rep.note("tokens", "-",
                 f"{len(emitted)} properties emitted and no file in the "
                 f"ecosystem references one; nothing was compared")
    rep.checks += 1


def verify_facts(cfg, rep, workdir: Path):
    """Check the manifest against reality, not just surfaces against the manifest.

    Without this the manifest is a single point of truth that nothing verifies:
    ship a test suite, and the checker faithfully enforces a stale number across
    every surface with total confidence. That is the same failure the eval suite
    had once, a scorecard graded against answers that were asserted rather than
    checked.

    Not every fact is derivable, and the honest move is to say which. Project and
    eval-case counts come out of the files exactly. The test total cannot: source
    counting yields a floor because parametrized tests expand at runtime. So the
    floor is what gets enforced, and the gap is reported rather than hidden.

    One rule governs every branch here: a fetch failure is missing evidence, not
    a finding. An incomplete floor can only understate, so asserting against it
    would report a network blip as a fabricated metric, which is the failure this
    whole file exists to prevent.
    """
    facts = cfg["facts"]

    # ---- eval cases: exact ----
    spec = facts.get("eval_cases", {})
    d = spec.get("derive", {})
    if d.get("method") == "exact" and d.get("repo"):
        root, why = fetch_repo(d["repo"], workdir)
        if root is None:
            rep.miss("verify", d["repo"],
                     f"could not fetch ({why}); eval cases unverified. "
                     f"{MISS_HINT}")
        else:
            f = root / d["file"]
            if not f.exists():
                rep.warn("verify", d["file"], "not found")
            else:
                rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
                actual = len(rows)
                kinds = {}
                for r in rows:
                    kinds[r.get("kind")] = kinds.get(r.get("kind"), 0) + 1
                if str(actual) != str(spec["value"]):
                    rep.fail("verify", d["file"],
                             f"manifest says {spec['value']} eval cases; the file has {actual}")
                else:
                    print(f"    derived  eval_cases = {actual}  {kinds}")
                for k, v in d.get("split", {}).items():
                    if kinds.get(k) != v:
                        rep.fail("verify", d["file"],
                                 f"manifest split says {k}={v}; the file has {kinds.get(k)}")
            rep.checks += 1

    # ---- projects: exact, cross-checked against the rendered page ----
    # products[] is the manifest talking to itself, which is consistency rather
    # than verification. index.html is the surface a reader actually counts, so
    # that is the one that settles it.
    spec = facts.get("projects", {})
    if spec.get("derive", {}).get("method") == "exact":
        declared = str(spec["value"])
        n_products = len([p for p in cfg["products"] if p.get("display")])
        if str(n_products) != declared:
            rep.fail("verify", "profile.json",
                     f"manifest says {declared} projects; products[] lists {n_products}")
        site, why = fetch_repo("rnvizion.github.io", workdir)
        if site is None:
            rep.miss("verify", "rnvizion.github.io",
                     f"could not fetch ({why}); project count checked against "
                     f"products[] only, which is self-consistency and not "
                     f"verification. {MISS_HINT}")
        else:
            idx = site / "index.html"
            if not idx.exists():
                rep.warn("verify", "index.html", "not found")
            else:
                rendered = len(re.findall(r'<article class="project">',
                                          idx.read_text(encoding="utf-8", errors="ignore")))
                if str(rendered) != declared:
                    rep.fail("verify", "index.html",
                             f"manifest says {declared} projects; the page renders {rendered}")
                else:
                    print(f"    derived  projects = {rendered}  (rendered articles; "
                          f"products[] agrees at {n_products})")
        rep.checks += 1

    # ---- tests: floor only ----
    spec = facts.get("tests", {})
    d = spec.get("derive", {})
    if d.get("method") in ("floor", "floor_display"):
        floor, param_files, missing = 0, 0, []
        for name in d.get("repos", []):
            root, why = fetch_repo(name, workdir)
            if root is None:
                missing.append(f"{name} ({why})")
                continue
            floor += _count_test_functions(root)
            param_files += _count_parametrized_files(root)

        if missing:
            # Partial evidence cannot support any of the assertions below: a short
            # floor makes a correct display look inflated, and losing whichever
            # repos hold the parametrized files makes it look impossible.
            rep.miss("verify", "tests",
                     f"could not fetch {', '.join(missing)}; the floor is incomplete at "
                     f"{floor:,}, so the display assertions are skipped rather than run "
                     f"against partial evidence")
            rep.checks += 1
            return

        raw = str(spec["value"]).replace(",", "").replace("+", "")
        declared = int(raw)
        ladder = [int(x.replace(",", "").replace("+", "")) for x in spec.get("ladder", [])]
        is_display = d.get("method") == "floor_display"
        gap = declared - floor
        print(f"    derived  tests floor = {floor:,}  displayed = {spec['value']}  "
              f"gap = {gap:+,}  ({param_files} parametrized file(s))")

        # floor_observed is the manifest's record of the last derivation. Until
        # this check existed it had no reader, so it drifted silently inside the
        # file whose job is preventing silent drift. This checker never edits,
        # by contract, so the finding carries the exact replacement value and a
        # human commits it — the same division of labour as every other check.
        recorded = spec.get("floor_observed")
        if recorded is not None:
            if floor > recorded:
                rep.note("verify", "profile.json",
                         f"floor_observed records {recorded:,} but source now derives "
                         f"{floor:,}; refresh it to {floor} in the next manifest edit")
            elif floor < recorded:
                rep.warn("verify", "profile.json",
                         f"floor_observed records {recorded:,} but source derives only "
                         f"{floor:,} with every repo fetched; tests were removed or a "
                         f"repo shrank, and the recorded floor is no longer supported")
            else:
                print(f"    ok       floor_observed = {recorded:,} matches the derivation")

        if not is_display:
            # an exact claim can never sit below a source floor
            if declared < floor:
                rep.fail("verify", "profile.json",
                         f"declared {declared:,} is BELOW the source floor {floor:,}; "
                         f"a source count can only understate, so the manifest is stale")
        else:
            # a displayed floor fails the other way: by claiming more than source
            # can carry. Below the floor is not an error, it is underselling, and
            # the ladder says when the next rung has been earned.
            if declared > floor and param_files == 0:
                rep.fail("verify", "profile.json",
                         f"display claims {spec['value']} but the source floor is {floor:,} "
                         f"and nothing is parametrized, so nothing can expand at runtime")
            elif declared > floor * 1.25:
                # runtime expansion is real but bounded; a quarter above the source
                # floor is already generous for the number of parametrized files here
                per = gap / param_files if param_files else gap
                rep.fail("verify", "profile.json",
                         f"display claims {spec['value']} against a source floor of {floor:,}. "
                         f"That needs {per:,.0f} extra runtime tests per parametrized file, "
                         f"which is not plausible; read the figure off a CI run")
            elif declared > floor:
                print(f"    note     {spec['value']} sits {gap:,} above the source floor; "
                      f"supported by runtime expansion across {param_files} parametrized "
                      f"file(s), not provable from source alone")
            earned = max([r for r in ladder if r <= floor], default=None)
            if earned and earned > declared:
                rep.warn("verify", "profile.json",
                         f"the source floor {floor:,} has earned the next rung: "
                         f"display says {spec['value']}, {earned:,}+ is now supportable")
        rep.checks += 1


# --------------------------------------------------------------------------
def report_exemptions(cfg, rep):
    """The exemption ledger. Coverage you cannot see is coverage you cannot
    trust, so every skip gets named: what it covered, what it allows, and which
    entries covered nothing at all. A dead exemption is coverage lost for no
    benefit, and it is the one that accumulates quietly."""
    rows, dead, unbounded = [], [], []
    for entry in cfg["retired"]:
        phrase = entry["phrase"]
        for ex in exempt_entries(entry):
            used = rep.exempt_use.get((phrase, ex["path"]), 0)
            cap = "unbounded" if ex["max"] is None else str(ex["max"])
            rows.append((phrase, ex["path"], used, cap))
            if used == 0:
                dead.append((phrase, ex["path"]))
            if ex["max"] is None:
                unbounded.append((phrase, ex["path"]))

    marked_total = sum(rep.marked.values())
    if not rows and not marked_total:
        return

    print("\nEXEMPTION LEDGER")
    print("=" * 70)
    for phrase, path, used, cap in rows:
        print(f"  {used:>3} used / {cap:<9} {path}   \u2190 \"{phrase}\"")
    if marked_total:
        print(f"\n  {marked_total} occurrence(s) excused by a {MARKER} marker at the point of use:")
        for phrase, n in sorted(rep.marked.items(), key=lambda kv: -kv[1]):
            print(f"      {n:>3}  \"{phrase}\"")
    if rep.archived:
        print(f"\n  {len(rep.archived)} file(s) under a declared archive path, excluded "
              f"from retirement checks:")
        for a in ARCHIVE_EXCLUDE:
            n = sum(1 for _, rel in rep.archived if rel.startswith(a))
            print(f"      {n:>3}  {a}**")

    # A dead exemption has three explanations, and only one of them ends in
    # "delete it". The old warning assumed the file was read and knew only the
    # other two; acting on it once nearly removed a live exemption whose file
    # the walk had never opened.
    for phrase, path in dead:
        matched = [r for r in rep.present if path_matches(r, path)]
        if not matched:
            rep.warn("exemptions", path,
                     f'covers nothing, and no file matching "{path}" exists in any '
                     f"scanned repo. The file moved or was deleted; repoint the "
                     f"exemption or delete it")
        elif not any(r in rep.scanned_files for r in matched):
            ex = sorted(matched)[0]
            rep.warn("exemptions", path,
                     f'never tested: "{ex}" exists but was not among the files read. '
                     f"That is a coverage gap in the walk, not a dead exemption — "
                     f"widen collection before judging it, and do not delete")
        else:
            rep.warn("exemptions", path,
                     f'covers nothing; "{phrase}" no longer appears there. The file '
                     f"was read, so deleting is safe — or the content moved and a "
                     f"fresh use now sits somewhere unexempted")
    for phrase, path in unbounded:
        rep.note("exemptions", path,
                 f'unbounded for "{phrase}"; one known use buys infinite uses. Add '
                 f'"max" so occurrence two has to be deliberate')


# profile.json v1.3.0 removed identity.phone: the personal cell does not live in
# a public repository. "phone" therefore leaves this tuple.
#
# This is NOT an open coverage gap, and an earlier draft of this comment wrongly
# called it one. The .docx resume variants are personal documents that carry the
# cell, and by decision of 2026-08-12 they are out of scope for this system
# entirely -- see _resumes_out_of_scope in the manifest. There is no surface left
# whose phone number this could be compared against, so there is nothing to
# check and nothing to reinstate. Do not "close" it by reading the number back
# into the manifest.
MANUAL_IDENTITY_KEYS = ("name", "email", "linkedin", "github", "site")


def print_manual(cfg):
    i, r = cfg["identity"], cfg["role"]
    missing = [k for k in MANUAL_IDENTITY_KEYS if k not in i]
    if missing:
        # An absent key is a manifest defect, not a field to skip. A .get()
        # here would print a blank line that a human reads as "checked, empty."
        print(f"error: identity is missing {', '.join(missing)}; the manual "
              f"checklist prints expected values and a blank one reads as "
              f"verified", file=sys.stderr)
        raise SystemExit(2)
    print("\nMANUAL SURFACES — not reachable from here")
    print("=" * 70)
    print("Expected values, so the comparison is quick:")
    for k in MANUAL_IDENTITY_KEYS:
        print(f"   {k:<10} {i[k]}")
    bp = i.get("brand_phone")
    if bp:
        print(f"   {'phone':<10} {bp['display']}  <- brand routing number only; "
              f"the personal cell is not in this manifest")
    else:
        print(f"   {'phone':<10} (NOT IN MANIFEST — nothing to compare)")
    print(f"   {'role':<10} {r['title']}, {r['employer']}")
    print(f"   {'tagline':<10} {cfg['tagline']['canonical']}")
    print(f"   {'bio':<10} {cfg['bio']['canonical'][:70]}…")
    for s in cfg["manual_surfaces"]:
        print(f"\n  {s['name']}  ({s['url']})")
        for item in s["check"]:
            print(f"     [ ] {item}")


def run_repo(cfg, name, root, rep, only=None):
    groups = cfg["repos"].get(name, {}).get("checks", list(CHECKS))
    for g in groups:
        if only and g not in only:
            continue
        fn = CHECKS.get(g)
        if fn:
            fn(cfg, root, rep, name)


def main():
    ap = argparse.ArgumentParser(description="Check the ecosystem against profile.json.")
    ap.add_argument("--manifest", default=str(MANIFEST))
    ap.add_argument("--all", action="store_true", help="every repo in the manifest")
    ap.add_argument("--repo", help="one repo, fetched remotely")
    ap.add_argument("--root", help="a local checkout")
    ap.add_argument("--docx", help="a local directory of .docx to lint before sending")
    ap.add_argument("--only", help="comma-separated check groups")
    ap.add_argument("--quiet", action="store_true", help="skip the manual checklist")
    ap.add_argument("--manual", action="store_true", help="print only the checklist")
    ap.add_argument("--verify-facts", action="store_true",
                    help="check the manifest against reality, not just surfaces against the manifest")
    args = ap.parse_args()

    mp = Path(args.manifest)
    if not mp.exists():
        print(f"error: manifest not found at {mp}", file=sys.stderr)
        return 2
    cfg = json.loads(mp.read_text(encoding="utf-8"))

    # Refuse to proceed on a manifest carrying a number that is not the brand
    # one. Exit 1, not 2, on purpose: profile-drift.yml only understands 0 and
    # 1, and a 2 falls through the open branch, the close branch AND the
    # fail-the-job branch — a silent green run. 1 opens the drift issue, which
    # is exactly the signal this deserves. (The pre-existing `return 2` for a
    # missing manifest has that same silent-green problem and is not fixed here.)
    phone_problems = audit_manifest_phones(cfg)
    if phone_problems:
        print("MANIFEST PHONE AUDIT FAILED — nothing else ran.", file=sys.stderr)
        for problem in phone_problems:
            print(f"  {problem}", file=sys.stderr)
        return 1

    only = set(args.only.split(",")) if args.only else None

    if args.manual:
        print_manual(cfg)
        return 0

    rep = Report()
    scanned = []
    full_sweep = bool(args.all)

    if args.verify_facts:
        print("\nVERIFYING FACTS against source")
        print("=" * 70)
        with tempfile.TemporaryDirectory() as tmp:
            verify_facts(cfg, rep, Path(tmp))
            # Unconditional, not a CHECKS member. See verify_tokens' docstring.
            verify_tokens(cfg, rep, Path(tmp))
            verify_type(cfg, rep, Path(tmp))
        scanned.append("manifest")

    if args.root:
        root = Path(args.root)
        name = root.resolve().name
        run_repo(cfg, name, root, rep, only)
        rep.absorb_tree(root)
        clear_file_cache()
        scanned.append(name)
    elif args.all or args.repo:
        names = [args.repo] if args.repo else [k for k in cfg["repos"] if not k.startswith("_")]
        with tempfile.TemporaryDirectory() as tmp:
            for name in names:
                root, why = fetch_repo(name, Path(tmp))
                if root is None:
                    rep.miss(name, "-",
                             f"could not fetch ({why}); every check declared for "
                             f"this repo was skipped, not passed. {MISS_HINT}")
                    full_sweep = False   # a partial sweep cannot judge a dead exemption
                    continue
                run_repo(cfg, name, root, rep, only)
                rep.absorb_tree(root)
                clear_file_cache()
                scanned.append(name)
    elif not args.docx and not args.verify_facts:
        ap.error("give --all, --repo, --root, --docx, --verify-facts, or --manual")

    if args.docx:
        lint_documents(cfg, args.docx, rep)
        scanned.append("documents")

    # Only a complete sweep can tell a dead exemption from an unvisited one.
    if full_sweep and (not only or "retired" in only):
        report_exemptions(cfg, rep)

    print(f"\nCHECKED against {mp.name} v{cfg.get('version','?')} "
          f"({rep.checks} checks over {len(scanned)} surface set(s))")
    print("=" * 70)
    if not rep.findings:
        print("  Every surface agrees with the manifest.")
    else:
        last = None
        for sev, scope, surface, msg in rep.findings:
            if scope != last:
                print(f"\n  [{scope}]")
                last = scope
            print(f"    {sev:<5} {surface}")
            print(f"          {msg}")

    print("\n" + "-" * 70)
    print(f"  scanned: {', '.join(scanned) or 'nothing'}")
    notes = (len(rep.findings) - len(rep.failures)
             - len(rep.warnings) - len(rep.misses))
    print(f"  {len(rep.failures)} failure(s), {len(rep.warnings)} warning(s), "
          f"{len(rep.misses)} unread, {notes} note(s)")
    if rep.misses:
        # The line that had to exist. Everything above describes what was read;
        # without this, a report with no failures reads as an all-clear for an
        # ecosystem it only partly opened.
        print(f"  INCOMPLETE SWEEP — {len(rep.misses)} surface set(s) could not be "
              f"read. Nothing above speaks to them, and a clean result here is "
              f"not a clean result for the ecosystem.")

    if not args.quiet:
        print_manual(cfg)

    # 1 = something disagrees. 3 = nothing disagreed but the sweep was
    # incomplete. 0 = complete and clean, which is now the only thing that
    # means what it says.
    #
    # Drift outranks coverage when both are true: exit 1 opens the drift issue
    # and leaves any coverage issue untouched, which is correct, because a run
    # that found drift AND could not read a repo has resolved neither.
    if rep.failures:
        return 1
    if rep.misses:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
