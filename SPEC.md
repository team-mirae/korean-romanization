# KRAMS Specification (draft)

## 1. Reading rule

KRAMS spellings are read with the values of American English as defined in the [README](README.md), except where this specification lists an exception.

## 2. Exceptions borrowed from Japanese romaji

Some letters keep the values they have in Japanese romaji (Hepburn) instead of their American English values. Romaji is widely read around the world, and over time its pronunciation has become unambiguous, so these values are reliable even for readers who know no Japanese.

### 2.1 Consonants

| Spelling | Reads as | Korean | Note |
|---|---|---|---|
| `ts` | つ (`tsu`) | ㅈ / ㅊ / ㅉ | Marks the affricate family. Which spelling goes with which of the three members is not decided yet. |

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

| Spelling | Korean | Sound | Note |
|---|---|---|---|
| `e-` | ㅐ | [e] | Same sound as ㅔ in the broadcast standard. The hyphen is the long-sound mark, which here keeps ㅐ distinct from ㅔ (`e`). |
| `uh` | ㅓ | [ʌ] | The American "uh", as in *cut* and *sun*. |
| `ae` | ㅐ | [e] | Alternative spelling of `e-`, with exactly the same meaning. Meant for romaji-style IMEs, where typing a hyphen in the middle of a word is awkward. Examples: 새 → `sae` = `se-`, ㅒ → `yae` = `ye-`. |
| `xu` | ㅡ | [ɯ] | Based on the romaji `u` in す/つ. The `x` marks that the vowel is not ㅜ. |
| `xui` | ㅢ | [ɰi] | ㅡ + ㅣ. |

Example words: 개 → `ge-`, 내가 → `ne-ga`, 어머니 → `uhmuhni`, 거기 → `guhgi`, 한글 → `hangxul`, 으로 → `xuro`, 의사 → `xuisa`.

**The letter `x`** is reserved for the ㅡ marker. It is never pronounced, has no consonant value, and must not be read with its pinyin value (*sh*).

## 4. Separators

- **Hyphen (`-`):** reserved for the long-sound mark (§3). It is never used to separate syllables.
- **Apostrophe (`'`):** separates syllables where the boundary would otherwise be ambiguous.
- **`a` followed by `e`:** `ae` always reads as ㅐ. When ㅏ is followed by a syllable starting with ㅔ, such as the particle 에, an apostrophe goes between them: 바다에 → `bada'e` (`badae` would read as 바대).
- **`h` between vowels:** a vowel followed by `h` and another vowel splits as vowel + `h` | vowel. For example, `suhul` is 서울 (`suh` + `ul`). The other split, with `h` starting the next syllable, takes an apostrophe: 수헐 → `su'hul`.
