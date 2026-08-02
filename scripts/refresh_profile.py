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
what it used to mean. Three mechanisms replace it:

  · a bounded exemption, {"path": ..., "max": 1}, keeps the file checked and
    asserts a known quantity; occurrence two fails
  · a "retired-ok" marker on or above the line excuses one occurrence in the
    file where a reader can see why, the same move is_refusal made when it
    stopped matching substrings and started testing structure
  · an exemption ledger prints what fired and warns on any exemption that
    matched nothing, because a dead exemption is coverage lost for no benefit

A bare string in exempt[] still works and still means unbounded; the ledger names
those so they can be tightened rather than forgotten.

WHAT IT REACHES
  --all         every repo in the manifest's repos{} block, fetched as a tarball;
                no local clones needed, which suits a phone-and-Codespace workflow
  --repo NAME   one repo, fetched the same way
  --root PATH   a local checkout
  --docx DIR    resume .docx, read without dependencies by unzipping the XML
  --manual      the checklist for LinkedIn, Hugging Face, dev.to, MCP registry

USAGE
  python scripts/refresh_profile.py --all
  python scripts/refresh_profile.py --repo rnvizion.github.io --docx ~/resumes
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
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
MANIFEST = REPO_ROOT / "profile.json"
OWNER = "RNVizion"

SKIP_DIRS = {".git", "node_modules", "assets/fonts", "chroma", "__pycache__", ".venv", "dist"}
TEXT_EXT = {".html", ".md", ".py", ".yml", ".yaml", ".json", ".xml", ".txt", ".sh", ".jsonl", ".toml"}

# The manifest names every retired phrase, and this file quotes several while
# explaining itself. A checker that measures text must exclude its own text, or
# it reads its own words back and calls them violations. That is the same failure
# the eval scorer hit once the corpus began describing the machine.
SELF_EXCLUDE = {"profile.json", "scripts/refresh_profile.py", "refresh_profile.py"}

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
_FILE_CACHE: dict[str, list[tuple[str, str]]] = {}


def text_files(root: Path) -> list[tuple[str, str]]:
    """Return [(relative path, body)] for every text file under root, cached."""
    key = str(root.resolve())
    cached = _FILE_CACHE.get(key)
    if cached is not None:
        return cached
    out: list[tuple[str, str]] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in TEXT_EXT:
            continue
        rel = p.relative_to(root).as_posix()
        if rel in SELF_EXCLUDE:
            continue
        if any(rel.startswith(d) or f"/{d}/" in f"/{rel}" for d in SKIP_DIRS):
            continue
        out.append((rel, p.read_text(encoding="utf-8", errors="ignore")))
    _FILE_CACHE[key] = out
    return out


def clear_file_cache() -> None:
    _FILE_CACHE.clear()


def fetch_repo(name: str, dest: Path) -> Path | None:
    """Download a repo tarball and unpack it. No clone, no auth, no local state."""
    for branch in ("main", "master"):
        url = f"https://codeload.github.com/{OWNER}/{name}/tar.gz/refs/heads/{branch}"
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                if r.status != 200:
                    continue
                data = r.read()
        except Exception:
            continue
        out = dest / name
        out.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            members = [m for m in tf.getmembers() if not m.name.startswith("/") and ".." not in m.name]
            tf.extractall(out, members=members)
        inner = next((c for c in out.iterdir() if c.is_dir()), None)
        return inner or out
    return None


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

    def fail(self, scope, surface, msg):
        self.findings.append(("FAIL", scope, surface, msg))

    def warn(self, scope, surface, msg):
        self.findings.append(("WARN", scope, surface, msg))

    def note(self, scope, surface, msg):
        self.findings.append(("NOTE", scope, surface, msg))

    @property
    def failures(self):
        return [f for f in self.findings if f[0] == "FAIL"]

    @property
    def warnings(self):
        return [f for f in self.findings if f[0] == "WARN"]


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


def exempt_for(entries: list[dict], rel: str) -> dict | None:
    for e in entries:
        pat = e["path"]
        if fnmatch.fnmatch(rel, pat) or rel.endswith(pat):
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
            if a == ident["email"] or "example" in a or "noreply" in a or "users.noreply" in a:
                continue
            if "rnvizion" in a.lower() or "vizionary" in a.lower():
                line = body[:m.start()].count("\n") + 1
                rep.warn(scope, f"{rel}:{line}", f'address "{a}" is not {ident["email"]}')
    rep.checks += 1


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
        for src in sources:
            p = root / src
            if not p.exists():
                rep.warn(scope, src, f"declared source for '{name}' not found")
                continue
            if spec["value"] not in p.read_text(encoding="utf-8", errors="ignore"):
                rep.fail(scope, src, f"'{name}' should read {spec['value']}; not present")
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
    """The gates are declared once and quoted on the resume. Verify the file
    still says what the manifest says.

    An absent key is a failure, not a skip. thresholds.json is read by the eval
    with data.get(key, default), so a renamed or typo'd gate silently falls back
    to the default; the suite keeps passing and the resume keeps quoting a bar
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


def check_docx(cfg, docx_dir, rep):
    files = sorted(Path(docx_dir).glob("*.docx"))
    if not files:
        rep.warn("resumes", str(docx_dir), "no .docx found")
        return
    ident = cfg["identity"]
    fact_specs = [(n, s) for n, s in cfg["facts"].items()
                  if not n.startswith("_") and "resumes" in s.get("appears_in", [])]
    for f in files:
        text = docx_text(f)
        if not text:
            rep.warn("resumes", f.name, "could not read document text")
            continue
        for entry in cfg["retired"]:
            if re.search(re.escape(entry["phrase"]), text, re.I):
                rep.fail("resumes", f.name, f'retired "{entry["phrase"]}"')
        for prod in cfg["products"]:
            old = prod.get("retired_display")
            if old and old in text:
                rep.fail("resumes", f.name, f'retired product name "{old}"')
        for label, val in (("email", ident["email"]), ("LinkedIn", ident["linkedin"])):
            if val not in text:
                rep.fail("resumes", f.name, f"{label} missing; expected {val}")
        # Facts that claim to appear on the resumes get checked there. Absence is
        # the finding; a stray match elsewhere in the document can mask it, which
        # is the known limit of substring checking against prose.
        for name, spec in fact_specs:
            if spec["value"] not in text:
                rep.fail("resumes", f.name,
                         f"'{name}' should read {spec['value']}; not present")
        rep.checks += 1


# --------------------------------------------------------------------------
# fact verification — derive what can be derived, bound what cannot
# --------------------------------------------------------------------------
def _iter_py(root: Path):
    for py in root.rglob("*.py"):
        rel = py.relative_to(root).as_posix()
        if any(rel.startswith(d) or f"/{d}/" in f"/{rel}" for d in SKIP_DIRS):
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
        root = fetch_repo(d["repo"], workdir)
        if root is None:
            rep.warn("verify", d["repo"], "could not fetch; eval cases unverified")
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
        site = fetch_repo("rnvizion.github.io", workdir)
        if site is None:
            rep.warn("verify", "rnvizion.github.io",
                     "could not fetch; project count checked against products[] only, "
                     "which is self-consistency and not verification")
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
            root = fetch_repo(name, workdir)
            if root is None:
                missing.append(name)
                continue
            floor += _count_test_functions(root)
            param_files += _count_parametrized_files(root)

        if missing:
            # Partial evidence cannot support any of the assertions below: a short
            # floor makes a correct display look inflated, and losing whichever
            # repos hold the parametrized files makes it look impossible.
            rep.warn("verify", "tests",
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
    for phrase, path in dead:
        rep.warn("exemptions", path,
                 f'covers nothing; "{phrase}" no longer appears there. Delete it, or the '
                 f"file moved and the exemption is now hiding a different one")
    for phrase, path in unbounded:
        rep.note("exemptions", path,
                 f'unbounded for "{phrase}"; one known use buys infinite uses. Add '
                 f'"max" so occurrence two has to be deliberate')


def print_manual(cfg):
    i, r = cfg["identity"], cfg["role"]
    print("\nMANUAL SURFACES — not reachable from here")
    print("=" * 70)
    print("Expected values, so the comparison is quick:")
    for k in ("name", "email", "phone", "linkedin", "github", "site"):
        print(f"   {k:<10} {i[k]}")
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
    ap.add_argument("--docx", help="directory of resume .docx")
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
        scanned.append("manifest")

    if args.root:
        root = Path(args.root)
        name = root.resolve().name
        run_repo(cfg, name, root, rep, only)
        clear_file_cache()
        scanned.append(name)
    elif args.all or args.repo:
        names = [args.repo] if args.repo else [k for k in cfg["repos"] if not k.startswith("_")]
        with tempfile.TemporaryDirectory() as tmp:
            for name in names:
                root = fetch_repo(name, Path(tmp))
                if root is None:
                    rep.warn(name, "-", "could not fetch (private, empty, or renamed)")
                    full_sweep = False   # a partial sweep cannot judge a dead exemption
                    continue
                run_repo(cfg, name, root, rep, only)
                clear_file_cache()
                scanned.append(name)
    elif not args.docx and not args.verify_facts:
        ap.error("give --all, --repo, --root, --docx, --verify-facts, or --manual")

    if args.docx:
        check_docx(cfg, args.docx, rep)
        scanned.append("resumes")

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
    notes = len(rep.findings) - len(rep.failures) - len(rep.warnings)
    print(f"  {len(rep.failures)} failure(s), {len(rep.warnings)} warning(s), {notes} note(s)")

    if not args.quiet:
        print_manual(cfg)
    return 1 if rep.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
