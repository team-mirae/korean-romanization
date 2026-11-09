#!/usr/bin/env python3
"""Generate data/parts/japanese.tsv: the Japanese kana entries of the KRAMS master table.

Spec: data/CONVENTIONS.md. Standard library only; all data is written out below.

Each table row is (kana, romanization, phonemic, phonetic, notes[, tag]).
- kana: hiragana for kana that exist in both scripts (the katakana form is
  derived by the fixed U+0060 offset), or katakana alone for katakana-only forms.
- romanization: modified Hepburn, lowercase.
- phonemic: standard Japanese phonemic analysis (vowels a i ɯ e o).
- phonetic: Tokyo citation form.
- tag: explicit tag, only where the collision rules below override
  "Japanese" + PascalCase(romanization).

Tag collision rules:
- ぢ -> JapaneseDi, づ -> JapaneseDu, ぢゃ ぢゅ ぢょ -> JapaneseDya/Dyu/Dyo
  (Nihon-shiki), を -> JapaneseWo. Their Romanization stays Hepburn.
- ん -> JapaneseN, っ -> JapaneseSokuon, ー -> JapaneseChoon.
- Obsolete kana take the suffix "Old" (JapaneseWiOld, JapaneseWeOld).
- An extended-katakana form whose tag collides with an earlier tag takes
  the suffix "Ext" (ウォ -> JapaneseWoExt, ディ -> JapaneseDiExt, ...).
"""

import os
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "parts", "japanese.tsv")

COLUMNS = ["Id", "Tag", "Language", "Text", "Romanization", "Example",
           "Phonemic", "Phonetic", "Notes"]

NOTE_YOTSUGANA = "Merged with {0} in the standard language (yotsugana); "
NOTE_V = ("Usual Tokyo realization is [b]; [v] occurs only in careful or "
          "foreign-influenced speech. Phonemic /v/ is a marginal loanword phoneme")
NOTE_LOAN = ("Loanword stratum; phonemic value written as realized because the "
             "native analysis has no slot for it")

# 1. Plain gojūon (3000000). ん is in the special morae block.
GOJUON = [
    ("あ", "a", "a", "a", ""),
    ("い", "i", "i", "i", ""),
    ("う", "u", "ɯ", "ɯ", ""),
    ("え", "e", "e", "e", ""),
    ("お", "o", "o", "o", ""),
    ("か", "ka", "ka", "ka", ""),
    ("き", "ki", "ki", "ki", ""),
    ("く", "ku", "kɯ", "kɯ", ""),
    ("け", "ke", "ke", "ke", ""),
    ("こ", "ko", "ko", "ko", ""),
    ("さ", "sa", "sa", "sa", ""),
    ("し", "shi", "si", "ɕi", ""),
    ("す", "su", "sɯ", "sɯ", ""),
    ("せ", "se", "se", "se", ""),
    ("そ", "so", "so", "so", ""),
    ("た", "ta", "ta", "ta", ""),
    ("ち", "chi", "ti", "tɕi", ""),
    ("つ", "tsu", "tɯ", "tsɯ", ""),
    ("て", "te", "te", "te", ""),
    ("と", "to", "to", "to", ""),
    ("な", "na", "na", "na", ""),
    ("に", "ni", "ni", "ni", ""),
    ("ぬ", "nu", "nɯ", "nɯ", ""),
    ("ね", "ne", "ne", "ne", ""),
    ("の", "no", "no", "no", ""),
    ("は", "ha", "ha", "ha", "Particle は is read wa"),
    ("ひ", "hi", "hi", "çi", ""),
    ("ふ", "fu", "hɯ", "ɸɯ", ""),
    ("へ", "he", "he", "he", "Particle へ is read e"),
    ("ほ", "ho", "ho", "ho", ""),
    ("ま", "ma", "ma", "ma", ""),
    ("み", "mi", "mi", "mi", ""),
    ("む", "mu", "mɯ", "mɯ", ""),
    ("め", "me", "me", "me", ""),
    ("も", "mo", "mo", "mo", ""),
    ("や", "ya", "ja", "ja", ""),
    ("ゆ", "yu", "jɯ", "jɯ", ""),
    ("よ", "yo", "jo", "jo", ""),
    ("ら", "ra", "ɾa", "ɾa", ""),
    ("り", "ri", "ɾi", "ɾi", ""),
    ("る", "ru", "ɾɯ", "ɾɯ", ""),
    ("れ", "re", "ɾe", "ɾe", ""),
    ("ろ", "ro", "ɾo", "ɾo", ""),
    ("わ", "wa", "wa", "wa", ""),
    ("を", "o", "o", "o",
     "Tag JapaneseWo (collision with お JapaneseO); Hepburn o, traditional Hepburn wo; "
     "some speakers say [wo]", "JapaneseWo"),
]

# 2. Dakuten and handakuten (3100000).
DAKUTEN = [
    ("が", "ga", "ga", "ga", "Word-medially often [ŋa] in conservative Tokyo speech"),
    ("ぎ", "gi", "gi", "gi", ""),
    ("ぐ", "gu", "gɯ", "gɯ", ""),
    ("げ", "ge", "ge", "ge", ""),
    ("ご", "go", "go", "go", ""),
    ("ざ", "za", "za", "dza", "Initial [dz], intervocalic [z]"),
    ("じ", "ji", "zi", "dʑi", "Initial [dʑ], intervocalic [ʑ]"),
    ("ず", "zu", "zɯ", "dzɯ", ""),
    ("ぜ", "ze", "ze", "dze", ""),
    ("ぞ", "zo", "zo", "dzo", ""),
    ("だ", "da", "da", "da", ""),
    ("ぢ", "ji", "zi", "dʑi",
     NOTE_YOTSUGANA.format("じ") + "tag JapaneseDi (Nihon-shiki) to avoid collision with じ",
     "JapaneseDi"),
    ("づ", "zu", "zɯ", "dzɯ",
     NOTE_YOTSUGANA.format("ず") + "tag JapaneseDu (Nihon-shiki) to avoid collision with ず",
     "JapaneseDu"),
    ("で", "de", "de", "de", ""),
    ("ど", "do", "do", "do", ""),
    ("ば", "ba", "ba", "ba", ""),
    ("び", "bi", "bi", "bi", ""),
    ("ぶ", "bu", "bɯ", "bɯ", ""),
    ("べ", "be", "be", "be", ""),
    ("ぼ", "bo", "bo", "bo", ""),
    ("ぱ", "pa", "pa", "pa", ""),
    ("ぴ", "pi", "pi", "pi", ""),
    ("ぷ", "pu", "pɯ", "pɯ", ""),
    ("ぺ", "pe", "pe", "pe", ""),
    ("ぽ", "po", "po", "po", ""),
    ("ゔ", "vu", "vɯ", "bɯ", NOTE_V),
]

# 3. Yōon (3200000).
YOON = [
    ("きゃ", "kya", "kja", "kja", ""),
    ("きゅ", "kyu", "kjɯ", "kjɯ", ""),
    ("きょ", "kyo", "kjo", "kjo", ""),
    ("しゃ", "sha", "sja", "ɕa", ""),
    ("しゅ", "shu", "sjɯ", "ɕɯ", ""),
    ("しょ", "sho", "sjo", "ɕo", ""),
    ("ちゃ", "cha", "tja", "tɕa", ""),
    ("ちゅ", "chu", "tjɯ", "tɕɯ", ""),
    ("ちょ", "cho", "tjo", "tɕo", ""),
    ("にゃ", "nya", "nja", "nja", ""),
    ("にゅ", "nyu", "njɯ", "njɯ", ""),
    ("にょ", "nyo", "njo", "njo", ""),
    ("ひゃ", "hya", "hja", "ça", ""),
    ("ひゅ", "hyu", "hjɯ", "çɯ", ""),
    ("ひょ", "hyo", "hjo", "ço", ""),
    ("みゃ", "mya", "mja", "mja", ""),
    ("みゅ", "myu", "mjɯ", "mjɯ", ""),
    ("みょ", "myo", "mjo", "mjo", ""),
    ("りゃ", "rya", "ɾja", "ɾja", ""),
    ("りゅ", "ryu", "ɾjɯ", "ɾjɯ", ""),
    ("りょ", "ryo", "ɾjo", "ɾjo", ""),
    ("ぎゃ", "gya", "gja", "gja", ""),
    ("ぎゅ", "gyu", "gjɯ", "gjɯ", ""),
    ("ぎょ", "gyo", "gjo", "gjo", ""),
    ("じゃ", "ja", "zja", "dʑa", ""),
    ("じゅ", "ju", "zjɯ", "dʑɯ", ""),
    ("じょ", "jo", "zjo", "dʑo", ""),
    ("ぢゃ", "ja", "zja", "dʑa",
     NOTE_YOTSUGANA.format("じゃ") + "tag JapaneseDya (Nihon-shiki) to avoid collision with じゃ",
     "JapaneseDya"),
    ("ぢゅ", "ju", "zjɯ", "dʑɯ",
     NOTE_YOTSUGANA.format("じゅ") + "tag JapaneseDyu (Nihon-shiki) to avoid collision with じゅ",
     "JapaneseDyu"),
    ("ぢょ", "jo", "zjo", "dʑo",
     NOTE_YOTSUGANA.format("じょ") + "tag JapaneseDyo (Nihon-shiki) to avoid collision with じょ",
     "JapaneseDyo"),
    ("びゃ", "bya", "bja", "bja", ""),
    ("びゅ", "byu", "bjɯ", "bjɯ", ""),
    ("びょ", "byo", "bjo", "bjo", ""),
    ("ぴゃ", "pya", "pja", "pja", ""),
    ("ぴゅ", "pyu", "pjɯ", "pjɯ", ""),
    ("ぴょ", "pyo", "pjo", "pjo", ""),
]

# 4. Special morae (3300000).
SPECIAL = [
    ("ん", "n", "N", "ɴ",
     "Moraic nasal; tag JapaneseN. Citation form [ɴ]; assimilates to a following "
     "consonant (m, n, ŋ). Hepburn writes n' before a vowel or y", "JapaneseN"),
    ("っ", "", "Q", "ʔ",
     "Sokuon; tag JapaneseSokuon. No standalone Hepburn form: written by doubling "
     "the next consonant (tch before ch). In words it lengthens the following consonant",
     "JapaneseSokuon"),
    ("ー", "", "R", "ː",
     "Chōonpu, katakana only; tag JapaneseChoon. No standalone Hepburn form: written "
     "as a macron on the preceding vowel", "JapaneseChoon"),
]

# 5. Extended katakana (3400000): 外来語の表記 (Cabinet notice, 1991),
# first list (第1表) and second list (第2表). ヴ itself is in the dakuten block.
# Order: by row of the base kana (ア, カ, サ, タ, ハ), then by vowel.
EXTENDED = [
    ("イェ", "ye", "je", "je", "外来語の表記 list 2"),
    ("ウィ", "wi", "wi", "wi", "外来語の表記 list 2"),
    ("ウェ", "we", "we", "we", "外来語の表記 list 2"),
    ("ウォ", "wo", "wo", "wo", "外来語の表記 list 2"),
    ("ヴァ", "va", "va", "ba", "外来語の表記 list 2. " + NOTE_V),
    ("ヴィ", "vi", "vi", "bi", "外来語の表記 list 2. " + NOTE_V),
    ("ヴェ", "ve", "ve", "be", "外来語の表記 list 2. " + NOTE_V),
    ("ヴォ", "vo", "vo", "bo", "外来語の表記 list 2. " + NOTE_V),
    ("ヴュ", "vyu", "vjɯ", "bjɯ", "外来語の表記 list 2. " + NOTE_V),
    ("クァ", "kwa", "kwa", "kwa", "外来語の表記 list 2"),
    ("クィ", "kwi", "kwi", "kwi", "外来語の表記 list 2"),
    ("クェ", "kwe", "kwe", "kwe", "外来語の表記 list 2"),
    ("クォ", "kwo", "kwo", "kwo", "外来語の表記 list 2"),
    ("グァ", "gwa", "gwa", "gwa", "外来語の表記 list 2"),
    ("シェ", "she", "sje", "ɕe", "外来語の表記 list 1"),
    ("ジェ", "je", "zje", "dʑe", "外来語の表記 list 1"),
    ("チェ", "che", "tje", "tɕe", "外来語の表記 list 1"),
    ("ツァ", "tsa", "tsa", "tsa", "外来語の表記 list 1. " + NOTE_LOAN),
    ("ツィ", "tsi", "tsi", "tsi", "外来語の表記 list 2. " + NOTE_LOAN),
    ("ツェ", "tse", "tse", "tse", "外来語の表記 list 1. " + NOTE_LOAN),
    ("ツォ", "tso", "tso", "tso", "外来語の表記 list 1. " + NOTE_LOAN),
    ("ティ", "ti", "ti", "ti", "外来語の表記 list 1. " + NOTE_LOAN),
    ("ディ", "di", "di", "di", "外来語の表記 list 1. " + NOTE_LOAN),
    ("テュ", "tyu", "tjɯ", "tjɯ", "外来語の表記 list 2. " + NOTE_LOAN),
    ("デュ", "dyu", "djɯ", "djɯ", "外来語の表記 list 1. " + NOTE_LOAN),
    ("トゥ", "tu", "tɯ", "tɯ", "外来語の表記 list 2. " + NOTE_LOAN),
    ("ドゥ", "du", "dɯ", "dɯ", "外来語の表記 list 2. " + NOTE_LOAN),
    ("ファ", "fa", "fa", "ɸa", "外来語の表記 list 1. Phonemic /f/ is a marginal loanword phoneme"),
    ("フィ", "fi", "fi", "ɸi", "外来語の表記 list 1. Phonemic /f/ is a marginal loanword phoneme"),
    ("フェ", "fe", "fe", "ɸe", "外来語の表記 list 1. Phonemic /f/ is a marginal loanword phoneme"),
    ("フォ", "fo", "fo", "ɸo", "外来語の表記 list 1. Phonemic /f/ is a marginal loanword phoneme"),
    ("フュ", "fyu", "fjɯ", "ɸjɯ", "外来語の表記 list 2. Phonemic /f/ is a marginal loanword phoneme"),
]

# 6. Obsolete kana (3500000).
OBSOLETE = [
    ("ゐ", "i", "i", "i",
     "Obsolete; historically /wi/, merged with い. Modified Hepburn i "
     "(traditional Hepburn wi); tag JapaneseWiOld", "JapaneseWiOld"),
    ("ゑ", "e", "e", "e",
     "Obsolete; historically /we/, merged with え. Modified Hepburn e "
     "(traditional Hepburn we); tag JapaneseWeOld", "JapaneseWeOld"),
]

BLOCKS = [
    (3000000, GOJUON, False),
    (3100000, DAKUTEN, False),
    (3200000, YOON, False),
    (3300000, SPECIAL, False),
    (3400000, EXTENDED, True),
    (3500000, OBSOLETE, False),
]


def to_katakana(s):
    out = []
    for ch in s:
        cp = ord(ch)
        if 0x3041 <= cp <= 0x3096:
            out.append(chr(cp + 0x60))
        else:
            out.append(ch)
    return "".join(out)


def is_hiragana(s):
    return all(0x3041 <= ord(ch) <= 0x309F for ch in s)


def pascal(romaji):
    return romaji[:1].upper() + romaji[1:]


def build_rows():
    rows = []
    tags = set()
    ext_collisions = []
    for base, table, is_extended in BLOCKS:
        for i, entry in enumerate(table):
            kana, romaji, phonemic, phonetic, notes = entry[:5]
            tag = entry[5] if len(entry) > 5 else "Japanese" + pascal(romaji)
            if is_extended and tag in tags:
                old = tag
                tag += "Ext"
                ext_collisions.append((kana, old, tag))
                notes = (notes + ". " if notes else "") + \
                    "Tag %s (collision with an earlier %s)" % (tag, old)
            assert tag not in tags, "duplicate tag: %s (%s)" % (tag, kana)
            tags.add(tag)
            if kana == "ー" or not is_hiragana(kana):
                text = kana
            else:
                text = kana + "/" + to_katakana(kana)
            assert len(table) * 10 < 100000, "sub-block overflow"
            row = [str(base + i * 10), tag, "Japanese", text, romaji, "",
                   phonemic, phonetic, notes]
            for field in row:
                assert "\t" not in field and "\n" not in field, row
                assert "ɡ" not in field, row  # ASCII g only
                assert "͡" not in field and "͜" not in field, row  # no tie bars
            rows.append([unicodedata.normalize("NFC", f) for f in row])
    ids = [r[0] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate id"
    return rows, ext_collisions


def main():
    rows, ext_collisions = build_rows()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(COLUMNS) + "\n")
        for row in rows:
            f.write("\t".join(row) + "\n")
    print("wrote %d rows to %s" % (len(rows), os.path.normpath(OUT)))
    for base, table, _ in BLOCKS:
        print("  %d: %d rows" % (base, len(table)))
    for kana, old, new in ext_collisions:
        print("  Ext collision: %s %s -> %s" % (kana, old, new))


if __name__ == "__main__":
    main()
