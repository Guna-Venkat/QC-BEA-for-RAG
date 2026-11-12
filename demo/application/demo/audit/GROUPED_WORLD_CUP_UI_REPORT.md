# Grouped World Cup preset and Live Lab presentation patch

**Subsequent user-requested reversal:** The default example has been restored to the original 15 passages. Grouped-preset measurements below describe the earlier, now inactive version. The simplified BEA-V2 labels and wrapped answer cards remain.

## Outcome

The main Live Lab now uses five longer passages, labels the method **BEA-V2**, and displays removal answers as compact, wrapped HTML cards. This patch is confined to `demo/`. No algorithm, threshold, learned predictor, benchmark result, split, reference answer, or reader setting was changed.

## Preset design

Five substantial sources make passage-level versus sentence-level selection easier to inspect than fifteen short sources. This is a presentation hypothesis, not an assertion that any method answers better. No method was tuned to win. The query remains the original multi-aspect expansion/workload/collusion question; it was not expanded to ask about hosting.

### Grouped World Cup preset and compact reader answers

The default **Budget-sensitive multi-aspect question** now loads **World Cup — Grouped Passage Demo**: five longer, titled passage cards. Expand a card to read/edit its full text. Counts use the pinned Qwen tokenizer. Click the preset button to replace a previously loaded 15-passage session with the grouped version; doing so clears stale comparison/impact outputs. Custom edits remain supported.

| Passage | Topic | Qwen source tokens |
|---|---|---:|
| P1 | Tournament Expansion and Group Structure | 286 |
| P2 | Tournament Workload | 294 |
| P3 | Three-Team Format and Collusion | 297 |
| P4 | Host Countries and Venues | 281 |
| P5 | Additional Tournament Information | 291 |

These are exact source excerpts regrouped into five demonstration documents, joined by blank lines. Their order and boundaries are demo-specific, not original article paragraph boundaries. The original question and Preset Reference Answer are unchanged. Original text, exact retained spans, offsets, and omissions are documented in `assets/presets/world_cup_grouped_v2.json`; the original 15-passage preset remains intact in `assets/presets/world_cup.json` and is accessible through `load_preset('original')`. Neither version is benchmark gold or a new research cohort.

The main method title is simply **BEA-V2**. Its runtime threshold, predictor identity and calibration notes are available in the collapsed **Advanced details · BEA-V2 execution** panel. The actual threshold and saved predictor execution have not changed.

**Reader Answers** shows original and removal answers in two wrapped HTML cards, each with its score. Narrow screens stack the cards. Long text has optional internal vertical scrolling; there is no code-block horizontal scrolling. Scores, LOO subtraction, prompts and generations are unchanged.

## Source preservation

| Grouped passage | Original source regions |
|---|---|
| P1 | P5 expansion background; P6 final format; final sentence of P1 |
| P2 | P7 workload changes; P12 hydration breaks |
| P3 | P8 original three-team proposal; P9 collusion risks |
| P4 | Hosting excerpt from P1; opening-match/host excerpt from P13; venue excerpt from P14; P15 regions |
| P5 | P2 hosting history; P10 rules introduction; substitutions/restarts excerpt from P11 |

No factual sentences were paraphrased, duplicated to pad length, or invented. Source-span receipts include old/new character offsets and exact substrings. Omitted non-whitespace regions have separate exact omission receipts; retained and omitted receipts cover the entire original. Titles are presentation labels, not additions to reader evidence. Grouped sections are not represented as one uninterrupted original quotation. `build_grouped_preset.py` reproduces the grouping and receipts without embedding or generation.

## Validation

- **190 tests passed** across `demo/tests`.
- Actual Streamlit browser check: five titled source cards, no visible verbose BEA-v2 line, no application exception.
- HTML browser check: the user's supplied answer pair wraps at desktop and mobile widths; no horizontal answer overflow; HTML is escaped. The displayed 0.441/0.478 examples are supplied layout fixtures, not new generations.
- Both budgets and all four canonical selectors completed mechanical qualification using the actual pinned Qwen tokenizer and saved BEA-V2 predictors. **Encoder and reader were synthetic test fixtures**. The following numbers test packing only; they are not SFR inference or quality results.

| Budget | Method | Evidence tokens | Selected units | Stop reason |
|---:|---|---:|---:|---|
| 256 | FIXED_SENTENCE | 254 | 6 | BUDGET_PACKING |
| 256 | QBGF | 251 | 9 | BUDGET_PACKING |
| 256 | BEA_V1 | 253 | 13 | BUDGET_EXHAUSTED |
| 256 | BEA_V2 | 255 | 9 | BUDGET_EXHAUSTED |
| 1024 | FIXED_SENTENCE | 1024 | 27 | BUDGET_PACKING |
| 1024 | QBGF | 1021 | 30 | BUDGET_PACKING |
| 1024 | BEA_V1 | 931 | 23 | LOW_MARGINAL_VALUE |
| 1024 | BEA_V2 | 999 | 5 | BUDGET_EXHAUSTED |

A new real SFR/Qwen run was not launched: another app's loaded models left approximately 6.4 GiB GPU memory free. Existing processes were left running. No new F1/EM or winner claim is made for this grouped preset. Actual live answers must be obtained through the app when resources permit.

**481 protected non-demo research files** match the pre-existing audit checksum inventory. The original preset also matches its recorded SHA256. No Git staging, commit, push, cache deletion or full research run occurred.

## Files

- `assets/presets/world_cup_grouped_v2.json`: new grouped preset and exhaustive source receipts.
- `build_grouped_preset.py`: deterministic regrouping recipe.
- `live/preset.py`: versioned loading, exact preset recognition, titles and diagnostic topic mapping.
- `live/ui.py`: compact passage cards, plain BEA-V2 heading, advanced runtime expander, wrapped answer cards.
- `live/presentation.py`: escaped responsive answer pair.
- `tests/test_grouped_preset.py`: preservation/count/receipt/layout regressions.
- Existing historical preset tests now explicitly load the original version; their expected historical sentence counts are preserved.
- `APPLICATION_GUIDE.md`: current usage and provenance notes.

## Screenshots

![Five passage Live Lab](../artifacts/grouped_preset/five_passage_live_lab.png)

![Compact reader answers — supplied layout fixture](../artifacts/grouped_preset/reader_answers_compact.png)

![Mobile reader cards](../artifacts/grouped_preset/reader_answers_mobile.png)

## Use

Refresh Live Lab, then click **Budget-sensitive multi-aspect question** to load the five-passage version and clear old outputs. Choose 256 or 1024, enable the live models, and run **Compare Four Methods**. All four methods use the same five provided source documents and frozen execution logic. Existing model-loading and reader-unavailable safeguards remain active.
