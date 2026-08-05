python3 - <<'EOF'
import sys, tempfile, subprocess
from pathlib import Path
sys.path.insert(0,'scripts')
from refresh_profile import fetch_repo
root = fetch_repo('rnvizion.github.io', Path(tempfile.mkdtemp()))
r = root/'resume'/'index.html'
r.write_text(r.read_text().replace('60-case evaluation suite','58-case evaluation suite'))
sys.exit(subprocess.run(['python3','scripts/refresh_profile.py','--root',str(root),'--only','facts','--quiet']).returncode)
EOF
echo "exit $? (1 = guard failed the bad surface = armed)"
