git rm -r --cached scripts/__pycache__ && git commit -m "untrack compiled checker"

git add profile.json scripts/refresh_profile.py .gitignore
git commit -m "v1.3.0: remove personal number, add brand_phone, widen walk to .vcf"
git push

