#!/usr/bin/env python3
"""Generate data/parts/english.tsv: the English letter and letter-group entries
of the KRAMS master table.

Spec: data/CONVENTIONS.md. Standard library only; all data is written out below.

The table records how a reader of American English (General American, San
Francisco Millennial speech: cot-caught merger, ɹ, flap ɾ, aspirated pʰ tʰ kʰ
in a stressed onset) interprets Latin letters. Each sound value of a letter or
letter group is one entry. Values are listed from most to least common; the
position in the list is n in the ID formula.

Each value is (example, phonemic, phonetic, notes).
- example: one lowercase example word.
- phonemic / phonetic: the value of the letter or group inside the example
  word, not the whole word. Both are empty for a silent value.

Groups that occur in no English word (KRAMS spellings such as wue, xu) are
given the reader's cold reading, with a KRAMS example word or the bare
spelling as the example, and a note saying so.
"""

import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "parts", "english.tsv")

COLUMNS = ["Id", "Tag", "Language", "Text", "Romanization", "Example",
           "Phonemic", "Phonetic", "Notes"]

LETTER_BASE = 2000000
LETTER_STRIDE = 10000
GROUP_BASE = 2500000
# CONVENTIONS.md: groupIndex x 10000. This fits only 50 groups (index 0-49)
# below the Japanese block at 3000000; groups past that are skipped with a
# warning. Lowering the stride (e.g. 5000) emits all of them, but needs a
# matching change to CONVENTIONS.md first.
GROUP_STRIDE = 5000
VALUE_STRIDE = 100
BLOCK_END = 3000000

COLD = "reader's cold reading of a non-English spelling"
COLD_KRAMS = "reader's cold reading of a KRAMS spelling; no English word has it"

# ---------------------------------------------------------------------------
# Single letters, A-Z. letterIndex = position in the alphabet (A = 0).
# ---------------------------------------------------------------------------
LETTERS = {
    "a": [
        ("apple", "æ", "æ", "short a, closed syllable"),
        ("cake", "eɪ", "eɪ", "long a, magic e"),
        ("about", "ə", "ə", "unstressed, reduced"),
        ("father", "ɑ", "ɑ", "also ball, water (cot-caught merger)"),
        ("any", "ɛ", "ɛ", "also many; before r as in care"),
        ("was", "ʌ", "ʌ", "after w, also what"),
        ("village", "ɪ", "ɪ", "unstressed -age"),
    ],
    "b": [
        ("bed", "b", "b", ""),
        ("lamb", "", "", "silent after m, also comb, debt"),
    ],
    "c": [
        ("cat", "k", "kʰ", "hard c before a, o, u; aspirated in a stressed onset"),
        ("city", "s", "s", "soft c before e, i, y"),
        ("scan", "k", "k", "unaspirated after s"),
        ("ocean", "ʃ", "ʃ", "c before ea, ia, ie"),
        ("cello", "tʃ", "tʃ", "Italian loan"),
        ("muscle", "", "", "silent in sc"),
    ],
    "d": [
        ("dog", "d", "d", ""),
        ("body", "d", "ɾ", "flapped between vowels"),
        ("jumped", "t", "t", "past tense -ed after a voiceless consonant"),
        ("soldier", "dʒ", "dʒ", "d before i + vowel"),
        ("wednesday", "", "", "silent"),
    ],
    "e": [
        ("bed", "ɛ", "ɛ", "short e, closed syllable"),
        ("me", "i", "i", "long e, open syllable"),
        ("cake", "", "", "word-final silent e"),
        ("taken", "ə", "ə", "unstressed, reduced"),
        ("pretty", "ɪ", "ɪ", "also England"),
        ("cafe", "eɪ", "eɪ", "French loan, written café"),
    ],
    "f": [
        ("fish", "f", "f", ""),
        ("of", "v", "v", "only in of"),
    ],
    "g": [
        ("go", "g", "g", "hard g"),
        ("gem", "dʒ", "dʒ", "soft g before e, i, y"),
        ("sign", "", "", "silent in gn"),
        ("beige", "ʒ", "ʒ", "French loan, also garage"),
    ],
    "h": [
        ("hat", "h", "h", ""),
        ("hour", "", "", "silent, also honest, vehicle"),
    ],
    "i": [
        ("sit", "ɪ", "ɪ", "short i, closed syllable"),
        ("bite", "aɪ", "aɪ", "long i, magic e"),
        ("machine", "i", "i", "loan value, also pizza"),
        ("animal", "ə", "ə", "unstressed, reduced"),
        ("onion", "j", "j", "glide before a vowel"),
        ("business", "", "", "silent"),
    ],
    "j": [
        ("jam", "dʒ", "dʒ", ""),
        ("jalapeno", "h", "h", "Spanish loan, written jalapeño"),
        ("hallelujah", "j", "j", "Hebrew/German value"),
    ],
    "k": [
        ("kite", "k", "kʰ", "aspirated in a stressed onset"),
        ("skin", "k", "k", "unaspirated after s"),
        ("knee", "", "", "silent in initial kn"),
    ],
    "l": [
        ("leg", "l", "l", "clear l in the onset"),
        ("ball", "l", "ɫ", "dark l in the coda"),
        ("walk", "", "", "silent, also talk, half, calm"),
    ],
    "m": [
        ("man", "m", "m", ""),
        ("mnemonic", "", "", "silent in initial mn"),
    ],
    "n": [
        ("no", "n", "n", ""),
        ("think", "ŋ", "ŋ", "before k or g"),
        ("autumn", "", "", "silent in final mn"),
    ],
    "o": [
        ("hot", "ɑ", "ɑ", "short o; also dog (cot-caught merger)"),
        ("go", "oʊ", "oʊ", "long o"),
        ("son", "ʌ", "ʌ", "also love, come"),
        ("do", "u", "u", "also to, who"),
        ("lemon", "ə", "ə", "unstressed, reduced"),
        ("wolf", "ʊ", "ʊ", "also woman"),
        ("one", "wʌ", "wʌ", "only in one, once"),
        ("women", "ɪ", "ɪ", "only in women"),
    ],
    "p": [
        ("pen", "p", "pʰ", "aspirated in a stressed onset"),
        ("spin", "p", "p", "unaspirated after s"),
        ("psychology", "", "", "silent in initial ps, pn"),
    ],
    "q": [
        ("queen", "k", "kʰ", "always followed by u; aspirated in a stressed onset"),
        ("mosquito", "k", "k", "unaspirated after s"),
    ],
    "r": [
        ("red", "ɹ", "ɹ", "rhotic; see the r groups for r-colored vowels"),
    ],
    "s": [
        ("sun", "s", "s", ""),
        ("is", "z", "z", "between vowels and in endings"),
        ("sugar", "ʃ", "ʃ", "also sure"),
        ("measure", "ʒ", "ʒ", "s before ure, ion"),
        ("island", "", "", "silent"),
    ],
    "t": [
        ("top", "t", "tʰ", "aspirated in a stressed onset"),
        ("water", "t", "ɾ", "flapped between vowels"),
        ("stop", "t", "t", "unaspirated after s"),
        ("mountain", "t", "ʔ", "glottal stop before syllabic n"),
        ("nation", "ʃ", "ʃ", "in -tion"),
        ("nature", "tʃ", "tʃ", "in -ture"),
        ("listen", "", "", "silent, also castle, often"),
    ],
    "u": [
        ("cup", "ʌ", "ʌ", "short u, closed syllable"),
        ("rule", "u", "u", "long u after r, l, j"),
        ("cute", "ju", "ju", "long u, magic e"),
        ("put", "ʊ", "ʊ", "also full, push"),
        ("focus", "ə", "ə", "unstressed, reduced"),
        ("language", "w", "w", "glide after g, q, s"),
        ("guess", "", "", "silent after g"),
        ("busy", "ɪ", "ɪ", "only in busy, business"),
    ],
    "v": [
        ("van", "v", "v", ""),
    ],
    "w": [
        ("we", "w", "w", ""),
        ("write", "", "", "silent in initial wr, also two, sword"),
    ],
    "x": [
        ("box", "ks", "ks", ""),
        ("exam", "gz", "gz", "ex before a stressed vowel"),
        ("xylophone", "z", "z", "word-initial"),
        ("anxious", "kʃ", "kʃ", "also luxury"),
        ("xi", "ʃ", "ʃ", "pinyin value, known to some readers from names"),
    ],
    "y": [
        ("yes", "j", "j", "consonant y"),
        ("my", "aɪ", "aɪ", "stressed final y"),
        ("happy", "i", "i", "unstressed final y"),
        ("gym", "ɪ", "ɪ", "Greek loans"),
    ],
    "z": [
        ("zoo", "z", "z", ""),
        ("azure", "ʒ", "ʒ", "also seizure"),
        ("nazi", "ts", "ts", "German loans"),
    ],
}

# ---------------------------------------------------------------------------
# Letter groups. groupIndex = position in this list. The order puts the groups
# KRAMS uses ahead of the less common English vowel groups, so that they stay
# inside the 50 group slots that CONVENTIONS.md allows.
# ---------------------------------------------------------------------------
GROUPS = [
    # Consonant groups.
    ("ch", [
        ("chair", "tʃ", "tʃ", ""),
        ("character", "k", "kʰ", "Greek loans; aspirated in a stressed onset"),
        ("chef", "ʃ", "ʃ", "French loans"),
    ]),
    ("sh", [
        ("ship", "ʃ", "ʃ", ""),
    ]),
    ("th", [
        ("think", "θ", "θ", "voiceless th"),
        ("this", "ð", "ð", "voiced th, function words"),
        ("thomas", "t", "tʰ", "names, also thyme"),
    ]),
    ("ph", [
        ("phone", "f", "f", ""),
    ]),
    ("gh", [
        ("ghost", "g", "g", "word-initial"),
        ("laugh", "f", "f", "word-final, also tough"),
        ("daughter", "", "", "silent, also in igh, eigh, ough"),
    ]),
    ("ng", [
        ("sing", "ŋ", "ŋ", ""),
        ("finger", "ŋg", "ŋg", "inside a root"),
        ("danger", "ndʒ", "ndʒ", "before e, i"),
    ]),
    ("ck", [
        ("ticket", "k", "k", ""),
    ]),
    ("wh", [
        ("what", "w", "w", "wine-whine merger"),
        ("who", "h", "h", "before o"),
    ]),
    ("qu", [
        ("queen", "kw", "kʰw", "aspirated in a stressed onset"),
        ("unique", "k", "k", "French loans, final -que"),
    ]),
    ("ts", [
        ("cats", "ts", "ts", "word-final, plural or third person"),
        ("tsunami", "s", "s", "word-initial; most readers drop the t, careful readers say ts"),
        ("tsar", "z", "z", "word-initial in Russian loans"),
    ]),
    ("dg", [
        ("edge", "dʒ", "dʒ", ""),
    ]),
    ("tch", [
        ("watch", "tʃ", "tʃ", ""),
    ]),
    # Groups that KRAMS uses or might use (SPEC.md section 3), as an
    # American reader reads them cold.
    ("ae", [
        ("gaelic", "eɪ", "eɪ", "usual cold reading of KRAMS ae (gae, sae), as in Mae, Rae, reggae"),
        ("aesthetic", "ɛ", "ɛ", "Greek/Latin loans"),
        ("algae", "i", "i", "Latin plurals, also Caesar"),
        ("maestro", "aɪ", "aɪ", "Italian/Spanish loans"),
        ("michael", "ə", "ə", "a reduced, e silent"),
    ]),
    ("eo", [
        ("video", "ioʊ", "ioʊ", "two syllables; the usual cold reading of eo, as in rodeo"),
        ("neon", "iɑ", "iɑ", "two syllables, also geography"),
        ("people", "i", "i", "only in people"),
        ("leopard", "ɛ", "ɛ", "also jeopardy"),
        ("pigeon", "ə", "ə", "unstressed, also surgeon"),
        ("seoul", "oʊ", "oʊ", "the name Seoul only"),
    ]),
    ("eu", [
        ("feud", "ju", "ju", ""),
        ("neutral", "u", "u", "after n, l, r (yod-dropping)"),
        ("europe", "jʊ", "jʊ", "before r"),
        ("museum", "iə", "iə", "two syllables"),
        ("freud", "ɔɪ", "ɔɪ", "German names"),
    ]),
    ("uh", [
        ("huh", "ʌ", "ʌ", "also uh, duh; the respelling vowel of cut; KRAMS uhmuhni reads the same"),
    ]),
    ("ah", [
        ("blah", "ɑ", "ɑ", "word-final ah, also the respelling vowel of father"),
        ("sarah", "ə", "ə", "unstressed final ah, h silent"),
        ("ahead", "əh", "əh", "split across the syllable boundary"),
    ]),
    ("oh", [
        ("oh", "oʊ", "oʊ", "also the respelling vowel of go"),
        ("john", "ɑ", "ɑ", "h silent"),
        ("ohio", "oʊh", "oʊh", "split across the syllable boundary"),
    ]),
    ("eh", [
        ("meh", "ɛ", "ɛ", "also the respelling vowel of bed"),
        ("eh", "eɪ", "eɪ", "the interjection"),
        ("behind", "ɪh", "ɪh", "split across the syllable boundary"),
    ]),
    ("ih", [
        ("ih", "ɪ", "ɪ", "pronunciation-respelling token (as in KIH-tee); no common English word"),
        ("shih", "i", "i", "as in shih tzu, h silent"),
        ("nihilism", "aɪ", "aɪ", "h silent"),
    ]),
    ("wo", [
        ("wonder", "wʌ", "wʌ", "also won, worry"),
        ("wok", "wɑ", "wɑ", "also wobble, wombat"),
        ("woke", "woʊ", "woʊ", "long o"),
        ("woman", "wʊ", "wʊ", "also wolf, wood"),
        ("women", "wɪ", "wɪ", "only in women"),
        ("two", "u", "u", "w silent, also sword"),
    ]),
    ("woe", [
        ("woe", "woʊ", "woʊ", "read as the English word woe; KRAMS woeguk reads the same"),
    ]),
    ("wue", [
        ("wueituh", "wu", "wu", COLD_KRAMS + "; ue read as in blue, true; readers who know Spanish (huevos) may give wɛ or weɪ"),
    ]),
    ("yu", [
        ("yule", "ju", "ju", "also yukon"),
        ("yummy", "jʌ", "jʌ", "short u"),
    ]),
    ("yuh", [
        ("yuh", "jʌ", "jʌ", "informal spelling of yeah, you; KRAMS yuhgi reads the same"),
    ]),
    ("ya", [
        ("yacht", "jɑ", "jɑ", "also yard, yawn"),
        ("yak", "jæ", "jæ", "short a, also yam"),
        ("ya", "jə", "jə", "informal you, as in see ya"),
    ]),
    ("ye", [
        ("yes", "jɛ", "jɛ", "short e"),
        ("bye", "aɪ", "aɪ", "word-final after a consonant, also rye"),
        ("ye", "ji", "ji", "the archaic word; the usual cold reading of a bare ye"),
    ]),
    ("yo", [
        ("yo", "joʊ", "joʊ", "also yoga, yogurt"),
        ("yonder", "jɑ", "jɑ", "short o"),
    ]),
    ("wa", [
        ("water", "wɑ", "wɑ", "a after w, also wash, wallet"),
        ("wax", "wæ", "wæ", "before k, g, x, ng"),
        ("was", "wʌ", "wʌ", "also what"),
        ("warm", "wɔ", "wɔ", "before r"),
        ("wage", "weɪ", "weɪ", "long a, magic e"),
    ]),
    ("wi", [
        ("win", "wɪ", "wɪ", "short i"),
        ("wide", "waɪ", "waɪ", "long i, magic e"),
        ("kiwi", "wi", "wi", "loans, also KRAMS wi"),
    ]),
    ("xu", [
        ("xuro", "zu", "zu", COLD_KRAMS + "; word-initial x read as z, as in xylophone"),
        ("xu", "ʃu", "ʃu", "the Chinese surname, read with the pinyin value by readers who know it"),
        ("sexual", "kʃu", "kʃu", "inside English words, also luxury"),
    ]),
    # r-colored groups.
    ("ar", [
        ("car", "ɑɹ", "ɑɹ", "stressed"),
        ("dollar", "ɚ", "ɚ", "unstressed"),
        ("war", "ɔɹ", "ɔɹ", "after w"),
        ("carry", "ɛɹ", "ɛɹ", "before a vowel (Mary-marry-merry merger)"),
    ]),
    ("er", [
        ("her", "ɝ", "ɝ", "stressed"),
        ("butter", "ɚ", "ɚ", "unstressed"),
        ("very", "ɛɹ", "ɛɹ", "before a vowel"),
        ("hero", "ɪɹ", "ɪɹ", "before a vowel, also zero"),
    ]),
    ("ir", [
        ("bird", "ɝ", "ɝ", "stressed"),
        ("mirror", "ɪɹ", "ɪɹ", "before a vowel"),
        ("virus", "aɪɹ", "aɪɹ", "long i before a vowel"),
    ]),
    ("or", [
        ("for", "ɔɹ", "ɔɹ", "stressed"),
        ("doctor", "ɚ", "ɚ", "unstressed"),
        ("word", "ɝ", "ɝ", "after w, also work, world"),
    ]),
    ("ur", [
        ("turn", "ɝ", "ɝ", "stressed"),
        ("saturday", "ɚ", "ɚ", "unstressed"),
        ("rural", "ʊɹ", "ʊɹ", "before a vowel, also tourist"),
        ("bury", "ɛɹ", "ɛɹ", "only in bury"),
    ]),
    # Vowel groups, most common first.
    ("ee", [
        ("see", "i", "i", ""),
        ("been", "ɪ", "ɪ", "only in been"),
        ("matinee", "eɪ", "eɪ", "French loans, also entree"),
    ]),
    ("ea", [
        ("eat", "i", "i", ""),
        ("bread", "ɛ", "ɛ", "also head, dead"),
        ("great", "eɪ", "eɪ", "also break, steak"),
        ("heart", "ɑ", "ɑ", "before r, also hearth"),
        ("idea", "iə", "iə", "two syllables, also area"),
    ]),
    ("oo", [
        ("food", "u", "u", ""),
        ("book", "ʊ", "ʊ", "before k, also good, foot"),
        ("blood", "ʌ", "ʌ", "also flood"),
        ("door", "ɔ", "ɔ", "before r, also floor"),
    ]),
    ("ou", [
        ("out", "aʊ", "aʊ", ""),
        ("soup", "u", "u", "French loans, also you, group"),
        ("touch", "ʌ", "ʌ", "also young, country"),
        ("four", "ɔ", "ɔ", "before r, also your, course"),
        ("could", "ʊ", "ʊ", "also would, should"),
        ("soul", "oʊ", "oʊ", "also shoulder"),
        ("famous", "ə", "ə", "unstressed -ous"),
    ]),
    ("ow", [
        ("cow", "aʊ", "aʊ", ""),
        ("snow", "oʊ", "oʊ", "also know, show"),
    ]),
    ("ai", [
        ("rain", "eɪ", "eɪ", ""),
        ("said", "ɛ", "ɛ", "also again"),
        ("captain", "ə", "ə", "unstressed"),
        ("aisle", "aɪ", "aɪ", "also loans such as Thai, bonsai"),
    ]),
    ("ay", [
        ("day", "eɪ", "eɪ", ""),
        ("says", "ɛ", "ɛ", "only in says"),
        ("kayak", "aɪ", "aɪ", "loans, also bayou"),
    ]),
    ("oa", [
        ("boat", "oʊ", "oʊ", ""),
        ("broad", "ɑ", "ɑ", "also abroad (cot-caught merger)"),
        ("boa", "oʊə", "oʊə", "two syllables, also koala"),
    ]),
    ("eigh", [
        ("eight", "eɪ", "eɪ", "also weigh, neighbor"),
        ("height", "aɪ", "aɪ", "also sleight"),
    ]),
    ("igh", [
        ("night", "aɪ", "aɪ", ""),
    ]),
    ("ew", [
        ("new", "u", "u", "yod-dropping after n, d, t"),
        ("few", "ju", "ju", "after f, m, v, p"),
        ("sew", "oʊ", "oʊ", "only in sew, shew"),
    ]),
    ("ue", [
        ("blue", "u", "u", ""),
        ("value", "ju", "ju", "after f, v, m, c"),
        ("tongue", "", "", "silent after g, also league"),
    ]),
    ("oi", [
        ("oil", "ɔɪ", "ɔɪ", ""),
        ("choir", "waɪ", "waɪ", "only in choir"),
        ("reservoir", "wɑ", "wɑ", "French loans, also memoir"),
    ]),
    ("oy", [
        ("boy", "ɔɪ", "ɔɪ", ""),
        ("coyote", "aɪ", "aɪ", "Spanish loan"),
    ]),
    ("au", [
        ("haul", "ɑ", "ɑ", "also caught (cot-caught merger)"),
        ("laugh", "æ", "æ", "also aunt"),
        ("chauffeur", "oʊ", "oʊ", "French loans"),
        ("kraut", "aʊ", "aʊ", "German loans"),
    ]),
    ("aw", [
        ("saw", "ɑ", "ɑ", "cot-caught merger"),
    ]),
    ("ie", [
        ("pie", "aɪ", "aɪ", "word-final"),
        ("field", "i", "i", "also believe"),
        ("friend", "ɛ", "ɛ", "only in friend"),
        ("quiet", "aɪə", "aɪə", "two syllables, also science"),
    ]),
    ("ei", [
        ("receive", "i", "i", "after c, also seize"),
        ("vein", "eɪ", "eɪ", "also rein, beige"),
        ("seismic", "aɪ", "aɪ", "Greek and German loans"),
        ("their", "ɛ", "ɛ", "before r"),
    ]),
    ("ey", [
        ("money", "i", "i", "unstressed final, also key"),
        ("they", "eɪ", "eɪ", "also obey, grey"),
        ("geyser", "aɪ", "aɪ", "also eye"),
    ]),
    ("ui", [
        ("fruit", "u", "u", "also juice"),
        ("build", "ɪ", "ɪ", "also guilt"),
        ("guide", "aɪ", "aɪ", "u silent after g"),
        ("suite", "wi", "wi", "French loans"),
        ("ruin", "uɪ", "uɪ", "two syllables"),
    ]),
    ("oe", [
        ("toe", "oʊ", "oʊ", "also hoe, Joe"),
        ("shoe", "u", "u", "also canoe"),
        ("does", "ʌ", "ʌ", "only in does"),
        ("poem", "oʊə", "oʊə", "two syllables"),
        ("phoenix", "i", "i", "Greek/Latin loans"),
        ("chloe", "oʊi", "oʊi", "two syllables in names, also Zoe"),
    ]),
    # More KRAMS spellings (SPEC.md section 3) and other English groups.
    ("xui", [
        ("xuisa", "zwi", "zwi", COLD_KRAMS + "; x read as z, ui as in suite; some readers give zui in two syllables"),
    ]),
    ("yae", [
        ("yae", "jeɪ", "jeɪ", COLD_KRAMS + "; ae read as in Mae, Rae"),
    ]),
    ("woae", [
        ("woae", "woʊeɪ", "woʊeɪ", COLD_KRAMS + "; read as wo + ae in two syllables"),
    ]),
    ("wuh", [
        ("wuh", "wʌ", "wʌ", COLD + "; KRAMS writes w-uh"),
    ]),
    ("ough", [
        ("though", "oʊ", "oʊ", ""),
        ("through", "u", "u", ""),
        ("tough", "ʌf", "ʌf", "also rough, enough"),
        ("cough", "ɑf", "ɑf", "also trough"),
        ("bought", "ɑ", "ɑ", "before t (cot-caught merger)"),
        ("bough", "aʊ", "aʊ", "also plough, drought"),
    ]),
    ("zz", [
        ("buzz", "z", "z", ""),
        ("pizza", "ts", "ts", "Italian loans"),
    ]),
    ("tz", [
        ("waltz", "ts", "ts", "German loans, also blitz"),
    ]),
]


def pascal(s):
    """PascalCase of a lowercase letter string: 'eigh' -> 'Eigh'."""
    return s[:1].upper() + s[1:]


def check_ipa(tag, ipa):
    for bad, why in [("ɡ", "use ASCII g"), ("͡", "no tie bars"), ("͜", "no tie bars"),
                     ("ˈ", "no stress marks"), ("ˌ", "no stress marks"), (".", "no syllable dots"),
                     ("\t", "no tabs")]:
        assert bad not in ipa, f"{tag}: {why}: {ipa!r}"


def make_rows():
    rows = []
    skipped = []

    def add(id_, text, values_index, values):
        example, phonemic, phonetic, notes = values
        tag = "English" + pascal(text) + "_" + pascal(example)
        assert text == text.lower() and example == example.lower(), tag
        assert example.isalpha() and text.isalpha(), tag
        assert bool(phonemic) == bool(phonetic), f"{tag}: silent must be silent in both"
        check_ipa(tag, phonemic)
        check_ipa(tag, phonetic)
        assert "\t" not in notes and "\n" not in notes, tag
        rows.append([str(id_), tag, "English", text, text, example,
                     phonemic, phonetic, notes])

    letters = sorted(LETTERS)
    assert letters == [chr(c) for c in range(ord("a"), ord("z") + 1)]
    for li, letter in enumerate(letters):
        values = LETTERS[letter]
        assert len(values) * VALUE_STRIDE <= LETTER_STRIDE
        for n, v in enumerate(values):
            add(LETTER_BASE + li * LETTER_STRIDE + n * VALUE_STRIDE, letter, n, v)

    seen_groups = set()
    for gi, (group, values) in enumerate(GROUPS):
        assert group not in seen_groups, group
        seen_groups.add(group)
        assert len(group) >= 2
        assert len(values) * VALUE_STRIDE <= GROUP_STRIDE
        if GROUP_BASE + gi * GROUP_STRIDE + (len(values) - 1) * VALUE_STRIDE >= BLOCK_END:
            skipped.append(group)
            continue
        for n, v in enumerate(values):
            add(GROUP_BASE + gi * GROUP_STRIDE + n * VALUE_STRIDE, group, n, v)

    # Each value of a letter or group must be distinct.
    by_text = {}
    for r in rows:
        by_text.setdefault(r[3], []).append(r[7] or "(silent)")
    for text, vals in by_text.items():
        assert len(vals) == len(set(vals)), f"repeated value in {text}: {vals}"

    tags = [r[1] for r in rows]
    assert len(tags) == len(set(tags)), "duplicate tags"
    ids = [int(r[0]) for r in rows]
    assert len(ids) == len(set(ids)), "duplicate ids"
    assert all(2000000 <= i < BLOCK_END for i in ids)
    return rows, skipped


def main():
    rows, skipped = make_rows()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write("\t".join(COLUMNS) + "\n")
        for r in rows:
            f.write("\t".join(unicodedata.normalize("NFC", c) for c in r) + "\n")
    print(f"wrote {len(rows)} rows to {os.path.normpath(OUT)}")
    if skipped:
        print(f"warning: {len(skipped)} groups do not fit the ID block with "
              f"GROUP_STRIDE={GROUP_STRIDE} and were skipped: {' '.join(skipped)}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
