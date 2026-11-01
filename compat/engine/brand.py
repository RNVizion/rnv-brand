"""engine.brand: the same module as rnv_brand.brand, under its old name.

Not a copy. Imported, this module puts rnv_brand.brand in its own place in
sys.modules, so `import engine.brand`, `from engine.brand import WEB` and
`rnv_brand.brand` all reach one object, and fonts_dir() names one folder.
Run as `python -m engine.brand`, it runs rnv_brand.brand instead.

It exists so the consumers that import engine.brand keep working until each
moves to rnv_brand at its next pin move. Remove it, and `engine` from
pyproject.toml, once none does: README.md, "Importing it".
"""
import sys

if __name__ == "__main__":
    import runpy

    runpy.run_module("rnv_brand.brand", run_name="__main__", alter_sys=True)
else:
    import rnv_brand.brand as _brand

    sys.modules[__name__] = _brand
