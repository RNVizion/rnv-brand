python3 -m py_compile scripts/refresh_profile.py \
 && python3 scripts/refresh_profile.py --verify-facts --quiet \
 && python3 scripts/refresh_profile.py --all --quiet
