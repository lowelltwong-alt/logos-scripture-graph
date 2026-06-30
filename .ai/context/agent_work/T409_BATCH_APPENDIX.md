---
object_type: agent_work_observation_checkpoint
trust_zone: learning-sidecar
lifecycle_status: active
provenance_note: "T409 read-only USFM observation checkpoint from eng-web_usfm.zip."
reason_for_inclusion: "Per-batch in-situ marker inventory for Codex/human triage."
---

# T409 Batch APPENDIX — USFM Observation Checkpoint

**Books:** FRT, GLO, Tob, Jdt, AddEsth, Wis, Sir, Bar, 1Macc, 2Macc, 1Esd, PrMan, Ps151, 3Macc, 2Esd, 4Macc, AddDan
**Files read:** 17/17

**Non-authorizing:** risk labels are agent triage from observed markers only.

### FRT (`00-FRTeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 9522 |
| char_count | 9460 |
| line_count | 37 |
| sha256_short | `09ecf533d97af7e0` |
| verse_count | 0 |
| chapter_count | 0 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `complex` |
| risk_label_scope | `raw_marker_only` |

**Risk why:** Excluded/deuterocanonical/front matter; non-66 scope

**Notable markers:** \f=2, \ili=4

<details><summary>line-leading markers</summary>

```json
{
  "h": 1,
  "id": 1,
  "ili": 4,
  "ip": 20,
  "is1": 7,
  "mt1": 1,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "bk": 36,
  "f": 2,
  "fr": 1,
  "ft": 1,
  "h": 1,
  "id": 1,
  "ili": 4,
  "ip": 20,
  "is1": 7,
  "mt1": 1,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1
}
```

</details>

### GLO (`106-GLOeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 18991 |
| char_count | 18621 |
| line_count | 101 |
| sha256_short | `82933d659dc27b4a` |
| verse_count | 0 |
| chapter_count | 0 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `medium_risk` |
| risk_label_scope | `book_level` |

**Risk why:** List markers (ili/li1=94)

**Notable markers:** \ili=94

<details><summary>line-leading markers</summary>

```json
{
  "h": 1,
  "id": 1,
  "ili": 94,
  "ip": 1,
  "mt1": 1,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "h": 1,
  "id": 1,
  "ili": 94,
  "ip": 1,
  "k": 188,
  "mt1": 1,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1
}
```

</details>

### Tob (`41-TOBeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 39030 |
| char_count | 38550 |
| line_count | 406 |
| sha256_short | `683f9eaebd16cfa1` |
| verse_count | 244 |
| chapter_count | 14 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `complex` |
| risk_label_scope | `raw_marker_only` |

**Risk why:** Excluded/deuterocanonical/front matter; non-66 scope

**Notable markers:** \fqa=16, \f=32, \x=2, \q1=27, \q2=32

<details><summary>line-leading markers</summary>

```json
{
  "c": 14,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 82,
  "q1": 27,
  "q2": 32,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 244
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "bk": 2,
  "c": 14,
  "f": 32,
  "fqa": 16,
  "fr": 16,
  "ft": 18,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 82,
  "q1": 27,
  "q2": 32,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 244,
  "x": 2,
  "xo": 1,
  "xt": 1
}
```

</details>

### Jdt (`42-JDTeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 62461 |
| char_count | 62143 |
| line_count | 505 |
| sha256_short | `d8d450dec5bd9cce` |
| verse_count | 339 |
| chapter_count | 16 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `complex` |
| risk_label_scope | `raw_marker_only` |

**Risk why:** Excluded/deuterocanonical/front matter; non-66 scope

**Notable markers:** \fqa=8, \f=18, \q1=20, \q2=34, \b=5

<details><summary>line-leading markers</summary>

```json
{
  "b": 5,
  "c": 16,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 84,
  "q1": 20,
  "q2": 34,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 339
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "b": 5,
  "bk": 2,
  "c": 16,
  "f": 18,
  "fqa": 8,
  "fr": 9,
  "ft": 11,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 84,
  "q1": 20,
  "q2": 34,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 339
}
```

</details>

### AddEsth (`43-ESGeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 44033 |
| char_count | 43699 |
| line_count | 287 |
| sha256_short | `872957c59c2bee8b` |
| verse_count | 205 |
| chapter_count | 10 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `complex` |
| risk_label_scope | `raw_marker_only` |

**Risk why:** Excluded/deuterocanonical/front matter; non-66 scope

**Notable markers:** \fqa=1, \f=62

<details><summary>line-leading markers</summary>

```json
{
  "c": 10,
  "h": 1,
  "id": 1,
  "ip": 2,
  "is1": 1,
  "mt1": 1,
  "mt2": 1,
  "p": 62,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 205
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "c": 10,
  "f": 62,
  "fl": 33,
  "fqa": 1,
  "fr": 31,
  "ft": 33,
  "h": 1,
  "id": 1,
  "ip": 2,
  "is1": 1,
  "mt1": 1,
  "mt2": 1,
  "p": 62,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 205
}
```

</details>

### Wis (`45-WISeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 69658 |
| char_count | 69446 |
| line_count | 1617 |
| sha256_short | `d06898f80170f21a` |
| verse_count | 436 |
| chapter_count | 19 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `medium_risk` |
| risk_label_scope | `book_level` |

**Risk why:** Footnote/variant density (f=86, fqa=42)

**Notable markers:** \fqa=42, \f=86, \x=2, \q1=424, \q2=681, \b=50

<details><summary>line-leading markers</summary>

```json
{
  "b": 50,
  "c": 19,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "q1": 424,
  "q2": 681,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 436
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "b": 50,
  "bk": 2,
  "c": 19,
  "f": 86,
  "fqa": 42,
  "fr": 43,
  "ft": 47,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "q1": 424,
  "q2": 681,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 436,
  "x": 2,
  "xo": 1,
  "xt": 1
}
```

</details>

### Sir (`46-SIReng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 178459 |
| char_count | 177451 |
| line_count | 4898 |
| sha256_short | `102424b55c3e48a2` |
| verse_count | 1383 |
| chapter_count | 51 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `medium_risk` |
| risk_label_scope | `book_level` |

**Risk why:** Footnote/variant density (f=170, fqa=28)

**Notable markers:** \fqa=28, \f=170, \x=2, \q1=1425, \q2=1781, \b=245

<details><summary>line-leading markers</summary>

```json
{
  "b": 245,
  "c": 51,
  "h": 1,
  "id": 1,
  "ip": 2,
  "is1": 1,
  "mt1": 2,
  "mt2": 1,
  "p": 1,
  "q1": 1425,
  "q2": 1781,
  "q3": 1,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 1383
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "b": 245,
  "bk": 4,
  "c": 51,
  "f": 170,
  "fqa": 28,
  "fr": 85,
  "ft": 87,
  "h": 1,
  "id": 1,
  "ip": 2,
  "is1": 1,
  "mt1": 2,
  "mt2": 1,
  "p": 1,
  "q1": 1425,
  "q2": 1781,
  "q3": 1,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 1383,
  "x": 2,
  "xo": 1,
  "xt": 1
}
```

</details>

### Bar (`47-BAReng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 28698 |
| char_count | 28554 |
| line_count | 251 |
| sha256_short | `ec251954c01deff8` |
| verse_count | 213 |
| chapter_count | 6 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `complex` |
| risk_label_scope | `raw_marker_only` |

**Risk why:** Excluded/deuterocanonical/front matter; non-66 scope

**Notable markers:** \fqa=2, \f=8, \s1=1

<details><summary>line-leading markers</summary>

```json
{
  "c": 6,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 24,
  "s1": 1,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 213
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "bk": 4,
  "c": 6,
  "f": 8,
  "fqa": 2,
  "fr": 4,
  "ft": 4,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 24,
  "s1": 1,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 213
}
```

</details>

### 1Macc (`52-1MAeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 135279 |
| char_count | 134607 |
| line_count | 1135 |
| sha256_short | `44cfd0193d3d760a` |
| verse_count | 924 |
| chapter_count | 16 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `medium_risk` |
| risk_label_scope | `book_level` |

**Risk why:** Footnote/variant density (f=214, fqa=48)

**Notable markers:** \fqa=48, \f=214, \q1=1, \q2=2

<details><summary>line-leading markers</summary>

```json
{
  "c": 16,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 185,
  "q1": 1,
  "q2": 2,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 924
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "bk": 2,
  "c": 16,
  "f": 214,
  "fqa": 48,
  "fr": 107,
  "ft": 119,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 185,
  "q1": 1,
  "q2": 2,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 924
}
```

</details>

### 2Macc (`53-2MAeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 107855 |
| char_count | 107461 |
| line_count | 707 |
| sha256_short | `cb76a13985932620` |
| verse_count | 555 |
| chapter_count | 15 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `medium_risk` |
| risk_label_scope | `book_level` |

**Risk why:** Footnote/variant density (f=306, fqa=130)

**Notable markers:** \fqa=130, \f=306, \b=5

<details><summary>line-leading markers</summary>

```json
{
  "b": 5,
  "c": 15,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 124,
  "pc": 1,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 555
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "b": 5,
  "bk": 2,
  "c": 15,
  "f": 306,
  "fqa": 130,
  "fr": 153,
  "ft": 174,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 124,
  "pc": 1,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 555
}
```

</details>

### 1Esd (`54-1ESeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 72995 |
| char_count | 72673 |
| line_count | 542 |
| sha256_short | `7d05bfcd8356d134` |
| verse_count | 448 |
| chapter_count | 9 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `medium_risk` |
| risk_label_scope | `book_level` |

**Risk why:** Footnote/variant density (f=328, fqa=166)

**Notable markers:** \fqa=166, \f=328, \x=38

<details><summary>line-leading markers</summary>

```json
{
  "c": 9,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 78,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 448
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "bk": 2,
  "c": 9,
  "f": 328,
  "fq": 4,
  "fqa": 166,
  "fr": 164,
  "ft": 37,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 78,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 448,
  "x": 38,
  "xo": 19,
  "xt": 19
}
```

</details>

### PrMan (`55-MANeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 3119 |
| char_count | 3107 |
| line_count | 27 |
| sha256_short | `018518186f0722c3` |
| verse_count | 15 |
| chapter_count | 1 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `complex` |
| risk_label_scope | `raw_marker_only` |

**Risk why:** Excluded/deuterocanonical/front matter; non-66 scope

**Notable markers:** \fqa=4, \f=8

<details><summary>line-leading markers</summary>

```json
{
  "c": 1,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "mt2": 1,
  "mt3": 2,
  "p": 1,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 15
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "bk": 2,
  "c": 1,
  "f": 8,
  "fqa": 4,
  "fr": 4,
  "ft": 4,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "mt2": 1,
  "mt3": 2,
  "p": 1,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 15
}
```

</details>

### Ps151 (`56-PS2eng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 1072 |
| char_count | 1064 |
| line_count | 32 |
| sha256_short | `1fb30c4c048b6fec` |
| verse_count | 7 |
| chapter_count | 1 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `complex` |
| risk_label_scope | `raw_marker_only` |

**Risk why:** Excluded/deuterocanonical/front matter; non-66 scope

**Notable markers:** \f=2, \d=2, \q1=7, \q2=8

<details><summary>line-leading markers</summary>

```json
{
  "c": 1,
  "cp": 1,
  "d": 1,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "q1": 7,
  "q2": 8,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 7
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "bk": 2,
  "c": 1,
  "cp": 1,
  "d": 1,
  "f": 2,
  "fr": 1,
  "ft": 1,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "q1": 7,
  "q2": 8,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 7
}
```

</details>

### 3Macc (`57-3MAeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 40582 |
| char_count | 40460 |
| line_count | 261 |
| sha256_short | `02e9245f072fda29` |
| verse_count | 228 |
| chapter_count | 7 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `complex` |
| risk_label_scope | `raw_marker_only` |

**Risk why:** Excluded/deuterocanonical/front matter; non-66 scope

**Notable markers:** \f=4

<details><summary>line-leading markers</summary>

```json
{
  "c": 7,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 19,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 228
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "bk": 2,
  "c": 7,
  "f": 4,
  "fr": 2,
  "ft": 2,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 19,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 228
}
```

</details>

### 2Esd (`58-2ESeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 130988 |
| char_count | 129842 |
| line_count | 1155 |
| sha256_short | `96cfee2e746cb0c8` |
| verse_count | 944 |
| chapter_count | 16 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `medium_risk` |
| risk_label_scope | `book_level` |

**Risk why:** Footnote/variant density (f=180, fqa=54)

**Notable markers:** \fqa=54, \f=180, \x=2

<details><summary>line-leading markers</summary>

```json
{
  "c": 16,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 188,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 944
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "bk": 6,
  "c": 16,
  "f": 180,
  "fqa": 54,
  "fr": 90,
  "ft": 93,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "p": 188,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 944,
  "x": 2,
  "xo": 1,
  "xt": 1
}
```

</details>

### 4Macc (`59-4MAeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 62521 |
| char_count | 62155 |
| line_count | 564 |
| sha256_short | `5a55fef9593503a0` |
| verse_count | 484 |
| chapter_count | 18 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `complex` |
| risk_label_scope | `raw_marker_only` |

**Risk why:** Excluded/deuterocanonical/front matter; non-66 scope

**Notable markers:** none

<details><summary>line-leading markers</summary>

```json
{
  "c": 18,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "nb": 2,
  "p": 53,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 484
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "bk": 2,
  "c": 18,
  "h": 1,
  "id": 1,
  "ip": 1,
  "mt1": 1,
  "nb": 2,
  "p": 53,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 484
}
```

</details>

### AddDan (`66-DAGeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | excluded |
| bytes_read | 88642 |
| char_count | 87751 |
| line_count | 812 |
| sha256_short | `01ce54762a8be2ca` |
| verse_count | 530 |
| chapter_count | 14 |
| strong_H | 0 |
| strong_G | 0 |
| files_read | True |
| risk_class | `complex` |
| risk_label_scope | `raw_marker_only` |

**Risk why:** Excluded/deuterocanonical/front matter; non-66 scope

**Notable markers:** \fqa=1, \f=30, \q1=14, \q2=23, \b=1, \s1=4

<details><summary>line-leading markers</summary>

```json
{
  "b": 1,
  "c": 14,
  "h": 1,
  "id": 1,
  "ide": 1,
  "m": 3,
  "mt1": 1,
  "mt2": 2,
  "p": 183,
  "pi1": 25,
  "q1": 14,
  "q2": 23,
  "q3": 6,
  "s1": 4,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 530
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "b": 1,
  "bk": 22,
  "c": 14,
  "f": 30,
  "fqa": 1,
  "fr": 15,
  "ft": 15,
  "h": 1,
  "id": 1,
  "ide": 1,
  "m": 3,
  "mt1": 1,
  "mt2": 2,
  "p": 183,
  "pi1": 25,
  "q1": 14,
  "q2": 23,
  "q3": 6,
  "s1": 4,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 530,
  "wh": 4
}
```

</details>
