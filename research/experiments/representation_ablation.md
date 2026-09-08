> Copied from the team's working repo (branch `e1-representation-study` of ElieBen-Shlomo/encode-hackathon), where the runner,
> attribution and paired-bootstrap scripts it cites live (`research/experiments/`, `research/eval/`). The submitted pipeline
> adopted this study's sampling findings (thinking level, completion cap, step-down on truncation); see SUBMISSION.md.

# Representation study (E1): how Qwen3.8-27B should read the spreadsheet

**Question.** The judged model is fixed (Qwen3.8-27B via Tinker, temperature 0). The two things the harness
controls are how the workbook is turned into prompt text (the *view*) and how much the model thinks (the
*renderer*). Which combination, under which solver, passes the most SpreadsheetBench tasks?

**Setup.** dev-100: a fixed stratified sample of the Verified 400 (69 cell-level, 31 sheet-level; ids in
`research/eval/splits/dev100.txt`). Every run is the same 100 tasks, scored by the shipped `evaluate.py`
after LibreOffice recalculation. One run per configuration (temperature 0 still varies by a task or two
between runs). Comparisons are paired bootstraps over task ids (`experiments/compare.py`, 10k resamples);
with n=100 an unpaired gap under about 8 points is noise. Run on a GCP VM (LibreOffice 7.4), 5 Sept 2026,
13:30 to 22:00 UTC, 26 configurations. Raw rows: `experiments/scoreboard.md`; probes: `experiments/probes.md`.

Two solvers:
- **values**: the shipped baseline strategy, one call, the model types JSON cell values, written by the baseline writer.
- **agent**: the model writes a Python script that edits the workbook; run in a sandbox; up to two traceback
  repairs. (This is the single-shot code loop on this branch. `main` has since gained a multi-turn
  verification-first agent, which should be re-measured with the views below.)

## 1. Thinking level (values solver, baseline `tsv` view)

| Renderer | Pass | Cell-level | Sheet-level | Median latency | s/task (conc. 6) | Failures: infra / format / coverage / reasoning |
|---|---|---|---|---|---|---|
| off (`qwen3_8_disable_thinking`) | 43% | 48% | 32% | 6 s | 19 | 8 / 7 / 4 / 35 |
| **low** | **65%** | 77% | 39% | 26 s | 52 | 5 / 8 / 7 / 12 |
| medium | 64% | 77% | 35% | 28 s | 57 | 7 / 10 / 4 / 12 |
| adaptive (low ≤20 cells, else medium) | 64% | 77% | 35% | 25 s | 54 | 8 / 8 / 5 / 13 |
| xhigh, 8192-token cap (the shipped default) | 52% | 67% | 19% | 70 s | 69 | 41 / 5 / 0 / 1 |
| xhigh, 16k cap | 64% | 77% | 35% | 100 s | 134 | 22 / 7 / 0 / 5 |

- off → low: **+22 points, CI [13, 31], P(low > off) = 1.000**. Reasoning failures fall from 35 to 12.
- low, medium and adaptive are indistinguishable (within 1 point).
- xhigh is dominated: at the shipped 8192 cap every one of its 41 extra failures is a reply cut off while
  still thinking (the renderer prefills the think tag, so the parser receives reasoning text or a JSON cut
  mid-way); at 16k it merely reaches medium's accuracy at 2.5× the latency, still losing 22 tasks to truncation.
  When xhigh does finish it is the most accurate variant (5 reasoning failures), which is why the
  truncation-with-step-down logic in `tinker_predict.py` matters.

**Decision: low.** Medium is equivalent and is the safe yaml default; xhigh should not be used at inference.

## 2. Solver × view (low thinking)

| View | values | agent | Probe accuracy | Prompt tokens p50 / p90 (agent) |
|---|---|---|---|---|
| windowed (Lorcan's digest, the current default) | 60% | 75% | 69% | 1043 / 2818 |
| tsv (shipped baseline, values only, 120×30) | 65% | 78% | 77% | 1113 / 3163 |
| markdown (grid content, markdown table) | 64% | 84% | 87% | 1577 / 4810 |
| schema (column table + sample rows) | – | 86% | 80% | 1474 / 4461 |
| **grid** (formulas → values, typed headers, names, ROI window) | 63% | **88%** | 86% | 1280 / 4218 |
| compact (SheetCompressor-style collapsed rows) | 54% | **89%** | 87% | 1554 / 4895 |
| html | 67% | – | 87% | – |
| json | 65% | – | 90% | – |
| addressed (`B2=1250.5`) | 67% | – | 91% | – |

Paired results (dev-100):

| Comparison | Δ points | 95% CI | P(B > A) |
|---|---|---|---|
| agent-windowed → agent-grid | +13 | [5, 22] | 0.998 |
| agent-windowed → agent-compact | +14 | [6, 22] | 1.000 |
| agent-tsv → agent-grid | +10 | [2, 19] | 0.988 |
| agent-grid → agent-compact | +1 | [−5, 7] | 0.56 |
| agent-grid → agent-schema | −2 | [−8, 4] | 0.21 |
| agent-grid → agent-markdown | −4 | [−11, 3] | 0.09 |
| agent-grid low → medium | −1 | [−6, 4] | 0.29 |
| values-tsv → agent-tsv (same view, solver only) | +13 | [1, 25] | 0.978 |
| values-tsv → values-grid | −2 | [−8, 4] | 0.21 |
| values-tsv → values-compact | −11 | [−18, −4] | 0.000 |
| values-tsv → values-addressed | +2 | [−6, 10] | 0.65 |

Reading:
- **The solver dominates the view.** Writing code beats typing values by 13 points on the same view, and by
  20–30 points once the view shows formulas and types. Sheet-level tasks are where it happens: values 39% →
  agent 90% (grid). Code removes the *format* bucket entirely (8 → 0: no dates-as-text, no numbers-as-text)
  and most of the *coverage* bucket (7 → 3: large ranges the values solver cannot type out).
- **For the code solver the view matters, and richness wins.** Formulas-plus-types views (grid, compact) are
  10–14 points above the windowed/tsv views, with CIs excluding zero. Schema (no data rows to speak of) is
  close behind, so the code solver needs the *layout*, not the data; markdown is a few points worse than the
  same content as a tab grid (not significant).
- **For the values solver the view barely matters**, except that collapsing rows (compact) *hurts* by 11
  points: a solver that must type every value needs to see every value. Layout variants (markdown/html/json/
  addressed) are all within noise of tsv.
- **Reading probes track the code solver's pass rate** (windowed 69→75, tsv 77→78, schema 80→86, grid 86→88,
  compact 87→89; markdown is the exception at 87→84). Views without formulas answer "what is the formula in
  E2?" 1–3% of the time; grid/compact/markdown/json 68–78%. Cell-address questions are answered best by the
  `addressed` layout (100%) and worst by `windowed` (82%).

## 3. Token budget (grid view, low)

| Budget | values | agent |
|---|---|---|
| unbudgeted (≈10k default) | 63% | 88% |
| 16k | 62% | – |
| 4k | 63% | 85% (−3, CI [−8, 2]) |
| 2k | 64% | – |

No measurable effect for values; a 4k cap costs the code solver about 3 points (not significant). The default
region-of-interest window already keeps prompts at ~1.3k tokens median, ~4.2k p90.

## 4. Decision

| | Recommendation | Why |
|---|---|---|
| Solver | code-writing agent | +13 points over values on the same view, +23 with the right view; kills the format and most coverage failures; sheet-level 39% → 90% |
| View | **grid** (compact is equivalent; schema is the fallback for very large sheets) | grid ≈ compact within 1 point; grid is ~20% cheaper in tokens and shows real rows, which the multi-turn agent's tools also rely on |
| Thinking | **low** (medium acceptable) | equal accuracy to medium, faster; xhigh dominated by truncation at any practical cap |
| Budget | none needed | ROI window keeps prompts small; a 4k cap only loses |
| For the values path, if kept | tsv or addressed, low | views within noise; never compact |

Expected effect versus the pipeline as it stood this morning (windowed digest, xhigh renderer, values-style
prompting through the shipped baseline): 52% → 88% on dev-100, from three changes that stack:
thinking off the truncation cliff (+12), typing → code (+13), values-only digest → formulas and types (+10).

## 5. Caveats and what to run next

- One run per configuration; temperature 0 is not deterministic on Tinker (the same prompt flipped a task
  between two runs). Differences under ~8 points unpaired, or with a CI containing zero above, are not decisions.
- dev-100 was used for all choices. The plan's check-50 (`research/eval/splits/check50.txt`, never touched)
  should confirm `agent-grid-low` against `agent-windowed-low` once before anything ships.
- The agent measured here is the single-shot code loop on this branch. `main` now has a multi-turn
  verification-first agent with the same `--digest` hook; the view result should transfer (it is a prompt
  change), but `agent-grid-low` vs `agent-windowed-low` should be re-run on it.
- Failure buckets for the best cell (agent-grid-low, 12 failures): 6 reasoning, 3 coverage, 1 infra,
  1 truncation, 1 error value. The remaining headroom is model reasoning, not representation.
- VM LibreOffice is 7.4 (Mac 26.8); scores are relative comparisons on one machine.
- xhigh with a 32k cap (values/tsv), finished after this was written: 65%, equal to low and medium; the cap,
  not the thinking level, was what broke xhigh.
