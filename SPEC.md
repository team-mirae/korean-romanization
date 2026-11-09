# KRAMS Specification (draft)

## 1. Reading rule

KRAMS spellings are read with the values of American English as defined in the [README](README.md), except where this specification lists an exception.

## 2. Exceptions borrowed from Japanese romaji

Some letters keep the values they have in Japanese romaji (Hepburn) instead of their American English values. Romaji is widely read around the world, and over time its pronunciation has become unambiguous, so these values are reliable even for readers who know no Japanese.

### 2.1 Consonants

| Spelling | Reads as | Korean | Note |
|---|---|---|---|
| `ts` | つ (`tsu`) | ㅊ | The start of *tsunami* said with the *t*, or the end of *cats*. |
| `z` | ざ行 (s + ゛) | ㅈ | The *z* of ざ ず ぜ ぞ (`za zu ze zo`), never the buzzing English *z* of *zoo* or *zip*. At the start of a word it is a soft "dz", as in *zen* (ぜん), *zabuton* (ざぶとん) and *Zojirushi* (ぞうじるし). Between vowels it is lighter, as in *Suzuki* (すずき), *azuki* (あずき) and *kamikaze* (かみかぜ). |

`zz` (ㅉ) is the tense form of `z`, following §5.

### 2.2 Vowels

Each of these vowel letters has exactly one value. The American English readings listed here never apply.

| Spelling | Always reads | Korean | Never reads |
|---|---|---|---|
| `u` | う | ㅜ | ゆ / ㅠ (as in *cute*, *use*) |
| `a` | あ | ㅏ | エイ / ㅔㅣ (as in *cake*, *late*) |
| `i` | い | ㅣ | アイ / ㅏㅣ (as in *bite*, *time*) |
| `e` | え | ㅔ | イー / ㅣ (as in *be*, *me*) |
| `o` | お | ㅗ | ア / ㅏ (as in *hot*, *stop*) |

## 3. Other vowels

### 3.1 Simple vowels

| Spelling | Alternative | Korean | Sound | Note |
|---|---|---|---|---|
| `ae` | `e-` | ㅐ | [e] | Same sound as ㅔ in the broadcast standard. `ae` is the default. `e-` uses the hyphen long-sound mark and means exactly the same thing. |
| `uh` | | ㅓ | [ʌ] | The American "uh", as in *cut* and *sun*. |
| `xu` | | ㅡ | [ɯ] | Based on the romaji `u` in す/つ. The `x` marks that the vowel is not ㅜ. |
| `xui` | | ㅢ | [ɰi] | ㅡ + ㅣ. |

### 3.2 Glide vowels

\* = identical to romaji.

| Spelling | Alternative | Korean | Sound | Note |
|---|---|---|---|---|
| `ya`\* | | ㅑ | [ja] | |
| `yuh` | | ㅕ | [jʌ] | |
| `yo`\* | | ㅛ | [jo] | |
| `yu`\* | | ㅠ | [ju] | |
| `yae` | `ye-` | ㅒ | [je] | |
| `ye` | | ㅖ | [je] | |
| `wa`\* | | ㅘ | [wa] | |
| `w-uh` | | ㅝ | [wʌ] | The hyphen after `w` marks ㅝ as distinct from ㅓ. This is the only place a hyphen follows `w`. |
| `wi` | | ㅟ | [wi] | |
| `woe` | | ㅚ | [we] | Spelled to show ㅗ. |
| `woae` | `woe-` | ㅙ | [we] | ㅗ + ㅐ. |
| `wue` | | ㅞ | [we] | ㅜ + ㅔ. |

ㅚ, ㅙ and ㅞ have the same sound. They are told apart by spelling: `wo-` for the ㅗ-based vowels and `wu-` for the ㅜ-based one.

**`we` is not a valid KRAMS spelling**, because it would be ambiguous among the three. An input method (IME) that receives `we` should suggest all three candidates: ㅚ, ㅙ and ㅞ.

### 3.3 Conversion and examples

Converters that produce KRAMS output the default spellings. Readers and converters must accept both spellings as input.

Example words: 개 → `gae`, 내가 → `naega`, 새 → `sae`, 어머니 → `uhmuhni`, 거기 → `guhgi`, 한글 → `hangxul`, 으로 → `xuro`, 의사 → `xuisa`, 여기 → `yuhgi`, 예 → `ye`, 왜 → `woae`, 외국 → `woeguk`, 웨이터 → `wueituh`, 뭐 → `mw-uh`.

**The letter `x`** is reserved for the ㅡ marker. It is never pronounced, has no consonant value, and must not be read with its pinyin value (*sh*).

## 4. Separators

- **Hyphen (`-`):** used in exactly two places: after a vowel as the long-sound mark in the alternative spellings (§3), and after `w` in `w-uh` (ㅝ). It is never used to separate syllables.
- **Apostrophe (`'`):** separates syllables where the boundary would otherwise be ambiguous.
- **`a` followed by `e`:** `ae` always reads as ㅐ. When ㅏ is followed by a syllable starting with ㅔ, such as the particle 에, an apostrophe goes between them: 바다에 → `bada'e` (`badae` would read as 바대).
- **`h` between vowels:** a vowel followed by `h` and another vowel splits as vowel + `h` | vowel. For example, `suhul` is 서울 (`suh` + `ul`). The other split, with `h` starting the next syllable, takes an apostrophe: 수헐 → `su'hul`.

## 5. Initial consonants

| Family | Lax | Aspirated | Tense |
|---|---|---|---|
| Velar | ㄱ `g` | ㅋ `k` | ㄲ `gg` / `kk` |
| Alveolar | ㄷ `d` | ㅌ `t` | ㄸ `dd` / `tt` |
| Bilabial | ㅂ `b` | ㅍ `p` | ㅃ `bb` / `pp` |
| Palatal | ㅈ `z` (§2.1) | ㅊ `ts` (§2.1) | ㅉ `zz` |
| Sibilant | ㅅ `s` | — | ㅆ `ss` |

| Consonant | Spelling |
|---|---|
| ㄴ | `n` |
| ㅁ | `m` |
| ㄹ | `r` |
| ㅇ | not written |
| ㅎ | `h` |

- **Tense consonants** are written as a doubled letter, like romaji gemination (っか → `kka`). For the velar, alveolar and bilabial families, both spellings are accepted. Which one is the default has not been decided yet.
- **Silent ㅇ** is not written. A syllable that starts with ㅇ is written as its vowel alone.
- **Final consonants** are not defined yet.

Examples: 가 `ga`, 카 `ka`, 까 `gga`/`kka`, 다 `da`, 타 `ta`, 따 `dda`/`tta`, 바 `ba`, 파 `pa`, 빠 `bba`/`ppa`, 자 `za`, 차 `tsa`, 짜 `zza`, 사 `sa`, 싸 `ssa`, 나 `na`, 마 `ma`, 라 `ra`, 아 `a`, 하 `ha`.

## 6. Input method (IME) guidelines

This section is a guideline for developers of IMEs that accept KRAMS input. It does not change how KRAMS is written.

### 6.1 Keys

| Key | Action |
|---|---|
| `Space` | Syllable separator. Ends the current syllable and keeps composing, without inserting a space. |
| `Shift` + `Space` | Commits the composition, then inserts a space. |
| `Shift` + `Enter` | Commits the composition and inserts nothing else. |

Example: typing `sa rang` shows the composition 사랑, with no space. Pressing `Shift` + `Space` then commits 사랑 followed by a space.

### 6.2 Syllable boundaries

- **`Space` marks syllable boundaries during input,** so the user does not need to type the apostrophe from §4. For example, `ga e` composes 가에 and `gae` composes 개.
- **Text typed without a space is split using the default rules in §4.**
- **The IME also suggests candidates where §3.2 asks for it.** For example, `we` offers ㅚ, ㅙ and ㅞ.
