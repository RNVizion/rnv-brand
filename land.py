#!/usr/bin/env python3
"""Land the three rnv-brand commits from a phone: one short command.

    git pull
    python3 land.py
    git push            # only after it prints LANDED

Upload this file to the root of rnv-brand on GitHub the way you uploaded up.py,
up1.py and up2.py, pull in the Codespace, and run it from the repository root.

What it does, in order, stopping at the first thing that is not as expected:
  1. Finds the three landing scripts among the files uploaded on top of
     rnv-brand@aaf34ed, by their contents, not their names, and copies them
     out of the repository to ~/.rnv-land.
  2. Removes every uploaded file (the three scripts and this one) in one
     commit. The repository's tree must then be aaf34ed's again, 4778a03f.
  3. Runs step 1, 2 and 3. After each, `git add -A` and `git write-tree` must
     print that step's result tree, and only then does it commit.

It commits locally and never pushes; `git push` is yours. Run it twice and the
second run says what is already done and changes nothing. If it stops halfway,
running `python3 ~/.rnv-land/land.py` carries on from the last commit it made.
"""
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "aaf34ed"
BASE_TREE = "4778a03fea4a31c2d85371d6e2ab0513799be388"
STEPS = [
    ("6328b83ff2dab4bf78b626eb188395710018a4d069d32f56e1d56e7886e48b6d",
     "730626e5a724b6f8e1224ce5aa80e30ea4dc2460",
     "Ship the brand's five faces in engine/fonts/, with their licenses, a guard and font_faces()"),
    ("eb6f6d46ab1a30b36e66aa03a581d4d037b9609a2956ba3b51820f2101b5642e",
     "b0fec64306b9e0f5a3c1bb2c3935c7fd5e16cab1",
     "Record the apps' one color file; README stops counting PERMANENT; manifest v1.3.5"),
    ("59c0c40eb1c3272c2887c111393611f2571afb31bd755e91a1ff8cb06c5bac59",
     "7a7244a0d840391aa34cb247a5697443fa0ce8f5",
     "American spelling in the registers, the engine's comments, the checker and the docs"),
]
KEEP = Path.home() / ".rnv-land"


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode:
        stop(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def stop(msg):
    sys.exit(f"\nSTOPPED: {msg}\nNothing after this point was done. Send a screenshot.")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    top = git("rev-parse", "--show-toplevel")
    if Path(top).resolve() != Path.cwd().resolve():
        stop(f"run this from the repository root, {top}")
    if not Path("engine/brand.py").is_file():
        stop("this is not an rnv-brand checkout")
    if git("status", "--porcelain"):
        stop("the working tree has uncommitted changes:\n" + git("status", "--short"))
    KEEP.mkdir(exist_ok=True)
    if Path(__file__).resolve() != (KEEP / "land.py").resolve():
        shutil.copyfile(__file__, KEEP / "land.py")   # so a rerun works after the upload is removed
    trees = [BASE_TREE] + [t for _, t, _ in STEPS]
    head = git("rev-parse", "HEAD^{tree}")

    if head not in trees:
        # Expect only uploaded files added on top of aaf34ed.
        if subprocess.run(["git", "merge-base", "--is-ancestor", BASE_COMMIT, "HEAD"]).returncode:
            stop(f"HEAD does not descend from {BASE_COMMIT}")
        changes = [l.split("\t", 1) for l in git("diff", "--name-status", BASE_COMMIT, "HEAD").splitlines()]
        odd = [p for s, p in changes if s != "A" or "/" in p or not p.endswith(".py")]
        if odd:
            stop("since aaf34ed, files other than uploaded scripts changed: " + ", ".join(odd))
        uploaded = [p for _, p in changes]
        by_hash = {sha(p): p for p in uploaded}
        missing = [i + 1 for i, (h, _, _) in enumerate(STEPS) if h not in by_hash]
        if missing:
            stop(f"the uploaded files do not include landing step(s) {missing}; uploaded: {', '.join(uploaded)}")
        for i, (h, _, _) in enumerate(STEPS, 1):
            shutil.copyfile(by_hash[h], KEEP / f"step{i}.py")
        git("rm", "-q", *uploaded)
        git("commit", "-qm", "Remove the landing scripts; they belong outside the repository")
        head = git("rev-parse", "HEAD^{tree}")
        if head != BASE_TREE:
            stop(f"after removing the uploads the tree is {head[:8]}, not aaf34ed's {BASE_TREE[:8]}")
        print(f"removed {len(uploaded)} uploaded files: {', '.join(uploaded)}; tree is aaf34ed's again, {head[:8]}")

    done = trees.index(head)
    if done == len(STEPS):
        print(f"\nLANDED already: tree {head[:8]}. Nothing to do. Push if you have not: git push")
        return
    for i in range(done, len(STEPS)):
        h, result, message = STEPS[i]
        script = KEEP / f"step{i + 1}.py"
        if not script.is_file() or sha(script) != h:
            stop(f"step {i + 1}'s script is not in {KEEP}; upload the three scripts again with this one")
        r = subprocess.run([sys.executable, "-I", str(script)])
        if r.returncode:
            stop(f"step {i + 1} refused (its message is above)")
        git("add", "-A")
        tree = git("write-tree")
        if tree != result:
            stop(f"after step {i + 1} the tree is {tree[:8]}, expected {result[:8]}. Not committed. "
                 f"To undo: git reset -q --hard && git clean -fdq")
        git("commit", "-qm", message)
        print(f"step {i + 1} committed, tree ok {tree[:8]}")
    print("\n" + git("log", "--oneline", "-5"))
    print(f"\nLANDED: tree {git('rev-parse', 'HEAD^{tree}')[:8]}. Now type: git push")


if __name__ == "__main__":
    main()
