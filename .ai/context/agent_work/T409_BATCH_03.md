---
object_type: agent_work_observation_checkpoint
trust_zone: learning-sidecar
lifecycle_status: active
provenance_note: "T409 read-only USFM observation checkpoint from eng-web_usfm.zip."
reason_for_inclusion: "Per-batch in-situ marker inventory for Codex/human triage."
---

# T409 Batch 03 — USFM Observation Checkpoint

**Books:** Ezra, Neh, Esth, Job, Ps, Prov, Eccl, Song
**Files read:** 8/8

**Non-authorizing:** risk labels are agent triage from observed markers only.

### Ezra (`16-EZReng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | 15 |
| bytes_read | 168452 |
| char_count | 168209 |
| line_count | 411 |
| sha256_short | `4b370951577f8d2b` |
| verse_count | 280 |
| chapter_count | 10 |
| strong_H | 5957 |
| strong_G | 0 |
| files_read | True |
| risk_class | `medium_risk` |
| risk_label_scope | `book_level` |

**Risk why:** List markers (ili/li1=32)

**Notable markers:** \f=24, \b=10, \li1=32

<details><summary>line-leading markers</summary>

```json
{
  "b": 10,
  "c": 10,
  "h": 1,
  "id": 1,
  "ide": 1,
  "li1": 32,
  "mi": 6,
  "mt1": 1,
  "mt2": 1,
  "p": 55,
  "pi1": 10,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 280
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "b": 10,
  "c": 10,
  "f": 24,
  "fr": 12,
  "ft": 12,
  "h": 1,
  "id": 1,
  "ide": 1,
  "li1": 32,
  "mi": 6,
  "mt1": 1,
  "mt2": 1,
  "p": 55,
  "pi1": 10,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 280,
  "w": 11914,
  "wh": 4
}
```

</details>

### Neh (`17-NEHeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | 16 |
| bytes_read | 235701 |
| char_count | 235232 |
| line_count | 576 |
| sha256_short | `ff83a1784ec29862` |
| verse_count | 406 |
| chapter_count | 13 |
| strong_H | 8337 |
| strong_G | 0 |
| files_read | True |
| risk_class | `medium_risk` |
| risk_label_scope | `book_level` |

**Risk why:** List markers (ili/li1=40)

**Notable markers:** \f=26, \b=2, \li1=40

<details><summary>line-leading markers</summary>

```json
{
  "b": 2,
  "c": 13,
  "h": 1,
  "id": 1,
  "ide": 1,
  "li1": 40,
  "mt1": 1,
  "mt2": 1,
  "p": 107,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 406
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "b": 2,
  "c": 13,
  "f": 26,
  "fr": 13,
  "ft": 13,
  "h": 1,
  "id": 1,
  "ide": 1,
  "li1": 40,
  "mt1": 1,
  "mt2": 1,
  "p": 107,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 406,
  "w": 16674,
  "wh": 4
}
```

</details>

### Esth (`18-ESTeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | 17 |
| bytes_read | 138410 |
| char_count | 137992 |
| line_count | 251 |
| sha256_short | `4cf6bbd3e566f96d` |
| verse_count | 167 |
| chapter_count | 10 |
| strong_H | 5075 |
| strong_G | 0 |
| files_read | True |
| risk_class | `low_risk` |
| risk_label_scope | `book_level` |

**Risk why:** Prose narrative/epistle; no exceptional marker pressure

**Notable markers:** \f=12

<details><summary>line-leading markers</summary>

```json
{
  "c": 10,
  "h": 1,
  "id": 1,
  "ide": 1,
  "mt1": 1,
  "mt2": 1,
  "p": 66,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 167
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "c": 10,
  "f": 12,
  "fr": 6,
  "ft": 6,
  "h": 1,
  "id": 1,
  "ide": 1,
  "mt1": 1,
  "mt2": 1,
  "p": 66,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 167,
  "w": 10150,
  "wh": 2
}
```

</details>

### Job (`19-JOBeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | 18 |
| bytes_read | 434576 |
| char_count | 433527 |
| line_count | 3406 |
| sha256_short | `0a26a0f438b5a1e4` |
| verse_count | 1070 |
| chapter_count | 42 |
| strong_H | 15249 |
| strong_G | 0 |
| files_read | True |
| risk_class | `high_risk` |
| risk_label_scope | `book_level` |

**Risk why:** \sp speaker labels; dialogue structure

**Notable markers:** \f=36, \q1=992, \q2=1099, \b=142

<details><summary>line-leading markers</summary>

```json
{
  "b": 142,
  "c": 42,
  "h": 1,
  "id": 1,
  "ide": 1,
  "mt1": 1,
  "mt2": 1,
  "p": 53,
  "q1": 992,
  "q2": 1099,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 1070
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "b": 142,
  "c": 42,
  "f": 36,
  "fr": 18,
  "ft": 18,
  "h": 1,
  "id": 1,
  "ide": 1,
  "mt1": 1,
  "mt2": 1,
  "p": 53,
  "q1": 992,
  "q2": 1099,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 1070,
  "w": 30498,
  "wh": 4
}
```

</details>

### Ps (`20-PSAeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | 19 |
| bytes_read | 927751 |
| char_count | 926074 |
| line_count | 8334 |
| sha256_short | `396a93dd10087234` |
| verse_count | 2461 |
| chapter_count | 150 |
| strong_H | 30954 |
| strong_G | 0 |
| files_read | True |
| risk_class | `medium_risk` |
| risk_label_scope | `book_level` |

**Risk why:** \d superscriptions; poetry q1/q2/b density

**Notable markers:** \fqa=1, \f=96, \d=276, \qs=142, \q1=2504, \q2=2970, \b=97, \ms1=5

<details><summary>line-leading markers</summary>

```json
{
  "b": 97,
  "c": 150,
  "cl": 1,
  "d": 138,
  "h": 1,
  "id": 1,
  "ide": 1,
  "ms1": 5,
  "mt1": 1,
  "p": 1,
  "q1": 2504,
  "q2": 2970,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 2461
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "b": 97,
  "c": 150,
  "cl": 1,
  "d": 138,
  "f": 96,
  "fqa": 1,
  "fr": 48,
  "ft": 48,
  "h": 1,
  "id": 1,
  "ide": 1,
  "ms1": 5,
  "mt1": 1,
  "p": 1,
  "q1": 2504,
  "q2": 2970,
  "qs": 142,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 2461,
  "w": 61908,
  "wh": 12
}
```

</details>

### Prov (`21-PROeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | 20 |
| bytes_read | 359962 |
| char_count | 359297 |
| line_count | 2906 |
| sha256_short | `d8af12f9422a6b68` |
| verse_count | 915 |
| chapter_count | 31 |
| strong_H | 12546 |
| strong_G | 0 |
| files_read | True |
| risk_class | `medium_risk` |
| risk_label_scope | `book_level` |

**Risk why:** Poetry line density (q=1893)

**Notable markers:** \f=28, \q1=901, \q2=992, \b=54

<details><summary>line-leading markers</summary>

```json
{
  "b": 54,
  "c": 31,
  "h": 1,
  "id": 1,
  "ide": 1,
  "mt1": 1,
  "p": 6,
  "q1": 901,
  "q2": 992,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 915
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "b": 54,
  "c": 31,
  "f": 28,
  "fr": 14,
  "ft": 14,
  "h": 1,
  "id": 1,
  "ide": 1,
  "mt1": 1,
  "p": 6,
  "q1": 901,
  "q2": 992,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 915,
  "w": 25092,
  "wh": 4
}
```

</details>

### Eccl (`22-ECCeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | 21 |
| bytes_read | 135740 |
| char_count | 135493 |
| line_count | 391 |
| sha256_short | `9a72fa832bcc6665` |
| verse_count | 222 |
| chapter_count | 12 |
| strong_H | 4994 |
| strong_G | 0 |
| files_read | True |
| risk_class | `low_risk` |
| risk_label_scope | `book_level` |

**Risk why:** Prose narrative/epistle; no exceptional marker pressure

**Notable markers:** \f=6, \q1=36, \q2=65

<details><summary>line-leading markers</summary>

```json
{
  "c": 12,
  "h": 1,
  "id": 1,
  "ide": 1,
  "mt1": 1,
  "mt2": 1,
  "p": 48,
  "q1": 36,
  "q2": 65,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 222
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "c": 12,
  "f": 6,
  "fr": 3,
  "ft": 3,
  "h": 1,
  "id": 1,
  "ide": 1,
  "mt1": 1,
  "mt2": 1,
  "p": 48,
  "q1": 36,
  "q2": 65,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 222,
  "w": 9988,
  "wh": 4
}
```

</details>

### Song (`23-SNGeng-web.usfm`)

| Field | Value |
|-------|-------|
| canonical_order | 22 |
| bytes_read | 62002 |
| char_count | 61902 |
| line_count | 549 |
| sha256_short | `3fb80c8e6b5bff0b` |
| verse_count | 117 |
| chapter_count | 8 |
| strong_H | 2118 |
| strong_G | 0 |
| files_read | True |
| risk_class | `high_risk` |
| risk_label_scope | `book_level` |

**Risk why:** \sp speaker labels; poetry

**Notable markers:** \f=8, \sp=66, \q1=135, \q2=226, \b=18

<details><summary>line-leading markers</summary>

```json
{
  "b": 18,
  "c": 8,
  "h": 1,
  "id": 1,
  "ide": 1,
  "mt1": 1,
  "p": 5,
  "q1": 135,
  "q2": 226,
  "sp": 33,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 117
}
```

</details>

<details><summary>inline markers</summary>

```json
{
  "b": 18,
  "c": 8,
  "f": 8,
  "fr": 4,
  "ft": 4,
  "h": 1,
  "id": 1,
  "ide": 1,
  "mt1": 1,
  "p": 5,
  "q1": 135,
  "q2": 226,
  "sp": 33,
  "toc1": 1,
  "toc2": 1,
  "toc3": 1,
  "v": 117,
  "w": 4236,
  "wh": 2
}
```

</details>
