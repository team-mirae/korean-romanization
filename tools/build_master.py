#!/usr/bin/env python3
"""Merge data/parts/*.tsv into data/master.tsv and build data/glossary.tsv.

See data/CONVENTIONS.md for the column, ID and glossary definitions.
"""
import csv
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = ["korean", "english", "japanese"]
COLUMNS = ["Id", "Tag", "Language", "Text", "Romanization", "Example",
           "Phonemic", "Phonetic", "Notes"]

# Step 1: diacritics removed before comparison.
STRIP = ["̚", "ː", "̥", "̊", "̃"]
# Step 2: mappings, applied in order (multi-character first).
MAP = [
    ("sʰ", "s"), ("ɕʰ", "ɕ"),
    ("ɕ", "ʃ"), ("ʑ", "ʒ"),
    ("ɛ", "e"), ("ɑ", "a"), ("ɐ", "a"), ("ɔ", "o"),
    ("ɸ", "f"), ("ç", "h"), ("ɴ", "ŋ"),
    ("ɡ", "g"),
]


def normalize(ipa: str) -> str:
    s = unicodedata.normalize("NFD", ipa)
    for ch in STRIP:
        s = s.replace(ch, "")
    s = unicodedata.normalize("NFC", s)
    for a, b in MAP:
        s = s.replace(a, b)
    return s


def read_part(name):
    path = ROOT / "data" / "parts" / f"{name}.tsv"
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))
    for r in rows:
        missing = [c for c in COLUMNS if c not in r]
        if missing:
            sys.exit(f"{path}: missing columns {missing}")
    return rows


def main():
    rows = []
    for p in PARTS:
        rows.extend(read_part(p))
    for r in rows:
        r["Id"] = int(r["Id"])
        for c in COLUMNS[1:]:
            r[c] = unicodedata.normalize("NFC", r[c] or "")
    rows.sort(key=lambda r: r["Id"])

    ids = [r["Id"] for r in rows]
    tags = [r["Tag"] for r in rows]
    if len(set(ids)) != len(ids):
        sys.exit("duplicate Id")
    if len(set(tags)) != len(tags):
        dup = sorted({t for t in tags if tags.count(t) > 1})
        sys.exit(f"duplicate Tag: {dup[:20]}")

    with (ROOT / "data" / "master.tsv").open("w", encoding="utf-8", newline="") as f:
        f.write("\t".join(COLUMNS) + "\n")
        for r in rows:
            f.write("\t".join(str(r[c]) for c in COLUMNS) + "\n")

    exact = defaultdict(list)
    func = defaultdict(list)
    for r in rows:
        if r["Phonetic"]:
            exact[r["Phonetic"]].append(r["Tag"])
            func[normalize(r["Phonetic"])].append(r["Tag"])

    with (ROOT / "data" / "glossary.tsv").open("w", encoding="utf-8", newline="") as f:
        f.write("Id\tTag\tPhonetic\tIdenticalTo\tFunctionallyIdenticalTo\n")
        for r in rows:
            ph = r["Phonetic"]
            if ph:
                same = [t for t in exact[ph] if t != r["Tag"]]
                same_set = set(same) | {r["Tag"]}
                near = [t for t in func[normalize(ph)] if t not in same_set]
            else:
                same, near = [], []
            f.write(f'{r["Id"]}\t{r["Tag"]}\t{ph}\t{",".join(same)}\t{",".join(near)}\n')

    by_lang = defaultdict(int)
    for r in rows:
        by_lang[r["Language"]] += 1
    print(f"rows: {len(rows)} {dict(by_lang)}")


if __name__ == "__main__":
    main()
