import sys
from fontTools.ttLib import TTFont
from pathlib import Path

"""Utility to set the hhea.lineGap field to zero.

Usage:
    python fix_line_gap.py <font_dir> [<font_dir> ...]
The script searches recursively for TTF, OTF, WOFF, and WOFF2 files
and updates them in place if the lineGap value differs from zero.
"""

def fix_font(path: Path) -> bool:
    try:
        font = TTFont(str(path))
        if "hhea" in font:
            hhea = font["hhea"]
            if hhea.lineGap != 300:
                hhea.lineGap = 300
                font.save(str(path))
                print(f"Processed {path}".ljust(100), end="\r", flush=True)
                return True
    except Exception as e:
        print(f"Failed to process {path}: {e}")
    return False

def main(paths):
    changed = 0
    for dir_path in paths:
        for ext in ("*.ttf", "*.otf"):
            for font_file in Path(dir_path).rglob(ext):
                if fix_font(font_file):
                    changed += 1
    print()
    print(f"Updated {changed} fonts", flush=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_line_gap.py <font_dir> [<font_dir> ...]")
        sys.exit(1)
    main(sys.argv[1:])
