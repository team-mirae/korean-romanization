#!/usr/bin/env python3
"""Generate data/parts/korean.tsv: all 11,172 modern Hangul syllables.

Columns and IPA follow data/CONVENTIONS.md. Standard library only.
"""

import os
import sys
import unicodedata
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "parts", "korean.tsv")

COLUMNS = ["Id", "Tag", "Language", "Text", "Romanization", "Example",
           "Phonemic", "Phonetic", "Notes"]

TENSE = "͈"   # combining double vertical line below
UNREL = "̚"   # combining left angle above (unreleased)

# --- Jamo tables, in Unicode order -----------------------------------------

# 19 initials: ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅅ ㅆ ㅇ ㅈ ㅉ ㅊ ㅋ ㅌ ㅍ ㅎ
L_JAMO = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
L_ROM = ["g", "kk", "n", "d", "tt", "r", "m", "b", "pp", "s", "ss", "",
         "j", "jj", "ch", "k", "t", "p", "h"]
# Phonemic initials: same symbols as phonetic initials, but ㄹ = l, ㅅ = s.
L_PHONEMIC = ["k", "k" + TENSE, "n", "t", "t" + TENSE, "l", "m", "p",
              "p" + TENSE, "s", "s" + TENSE, "", "tɕ", "t" + TENSE + "ɕ",
              "tɕʰ", "kʰ", "tʰ", "pʰ", "h"]
# Phonetic initials (before allophony for ㅅ ㅆ ㅎ).
L_PHONETIC = ["k", "k" + TENSE, "n", "t", "t" + TENSE, "ɾ", "m", "p",
              "p" + TENSE, "sʰ", "s" + TENSE, "", "tɕ", "t" + TENSE + "ɕ",
              "tɕʰ", "kʰ", "tʰ", "pʰ", "h"]
L_SILENT = 11
L_PALATAL = {12, 13, 14}           # ㅈ ㅉ ㅊ
L_S, L_SS, L_H = 9, 10, 18

# 21 vowels: ㅏ ㅐ ㅑ ㅒ ㅓ ㅔ ㅕ ㅖ ㅗ ㅘ ㅙ ㅚ ㅛ ㅜ ㅝ ㅞ ㅟ ㅠ ㅡ ㅢ ㅣ
V_JAMO = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
V_ROM = ["a", "ae", "ya", "yae", "eo", "e", "yeo", "ye", "o", "wa", "wae",
         "oe", "yo", "u", "wo", "we", "wi", "yu", "eu", "ui", "i"]
V_PHONEMIC = ["a", "ɛ", "ja", "jɛ", "ʌ", "e", "jʌ", "je", "o", "wa", "wɛ",
              "ø", "jo", "u", "wʌ", "we", "wi", "ju", "ɯ", "ɰi", "i"]
# Phonetic vowels with the mergers ㅐ=ㅔ, ㅒ=ㅖ, ㅚ=ㅙ=ㅞ applied.
V_PHONETIC = ["a", "e", "ja", "je", "ʌ", "e", "jʌ", "je", "o", "wa", "we",
              "we", "jo", "u", "wʌ", "we", "wi", "ju", "ɯ", "ɰi", "i"]
V_UI = 19

# 28 finals (index 0 = none):
# - ㄱ ㄲ ㄳ ㄴ ㄵ ㄶ ㄷ ㄹ ㄺ ㄻ ㄼ ㄽ ㄾ ㄿ ㅀ ㅁ ㅂ ㅄ ㅅ ㅆ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ
T_JAMO = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ",
          "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ",
          "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
# Transliteration mode: each jamo written with its own letters.
T_ROM = ["", "g", "kk", "gs", "n", "nj", "nh", "d", "l", "lg", "lm", "lb",
         "ls", "lt", "lp", "lh", "m", "b", "bs", "s", "ss", "ng", "j", "ch",
         "k", "t", "p", "h"]
# Phonemic finals: underlying jamo written out in full.
T_PHONEMIC = ["", "k", "k" + TENSE, "ks", "n", "ntɕ", "nh", "t", "l", "lk",
              "lm", "lp", "ls", "ltʰ", "lpʰ", "lh", "m", "p", "ps", "s",
              "s" + TENSE, "ŋ", "tɕ", "tɕʰ", "kʰ", "tʰ", "pʰ", "h"]
K, T_, P = "k" + UNREL, "t" + UNREL, "p" + UNREL
# Phonetic finals in isolation (표준발음법 제9항, 제10항, 제11항).
T_PHONETIC = ["", K, K, K, "n", "n", "n", T_, "l", K, "m", "l", "l", "l",
              P, "l", "m", P, P, T_, T_, "ŋ", T_, T_, K, T_, P, T_]
CLUSTERS = {3, 5, 6, 9, 10, 11, 12, 13, 14, 15, 18}

assert len(L_JAMO) == len(L_ROM) == len(L_PHONEMIC) == len(L_PHONETIC) == 19
assert len(V_JAMO) == len(V_ROM) == len(V_PHONEMIC) == len(V_PHONETIC) == 21
assert len(T_JAMO) == len(T_ROM) == len(T_PHONEMIC) == len(T_PHONETIC) == 28


def build_row(i):
    l, v, t = i // 588, (i % 588) // 28, i % 28
    syllable = chr(0xAC00 + i)
    notes = []

    rom = L_ROM[l] + V_ROM[v] + T_ROM[t]
    tag = "Korean" + rom[0].upper() + rom[1:]

    phonemic = L_PHONEMIC[l] + V_PHONEMIC[v] + T_PHONEMIC[t]

    vowel = V_PHONETIC[v]
    if v == V_UI and l != L_SILENT:
        vowel = "i"
        notes.append("ㅢ→i after consonant")
    if l in L_PALATAL and vowel.startswith("j"):
        vowel = vowel[1:]
        notes.append("glide dropped after palatal")
    onset = L_PHONETIC[l]
    if vowel.startswith(("i", "j")):
        if l == L_S:
            onset = "ɕʰ"
        elif l == L_SS:
            onset = "ɕ" + TENSE
        elif l == L_H:
            onset = "ç"
    phonetic = onset + vowel + T_PHONETIC[t]
    if t in CLUSTERS:
        notes.append("final %s→%s" % (T_JAMO[t], T_PHONETIC[t]))

    row = [str(1000000 + i * 10), tag, "Korean", syllable, rom, "",
           phonemic, phonetic, "; ".join(notes)]
    row = [unicodedata.normalize("NFC", f) for f in row]
    for f in row:
        assert "\t" not in f and "\n" not in f
        assert "͡" not in f and "͜" not in f, "tie bar"
        assert "ɡ" not in f, "non-ASCII g"
    return row


def main():
    rows = [build_row(i) for i in range(11172)]

    by_tag = defaultdict(list)
    for r in rows:
        by_tag[r[1]].append(r[3])
    dups = {k: v for k, v in by_tag.items() if len(v) > 1}
    if dups:
        for k, v in sorted(dups.items()):
            print("tag collision: %s <- %s" % (k, " ".join(v)), file=sys.stderr)
        sys.exit("aborting: %d colliding tags" % len(dups))
    assert len(by_tag) == 11172

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(COLUMNS) + "\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    print("wrote %d rows to %s" % (len(rows), OUT))


if __name__ == "__main__":
    main()
