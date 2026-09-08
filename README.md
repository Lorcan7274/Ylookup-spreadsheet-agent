# Ylookup — a verification-first spreadsheet agent

A multi-turn LLM agent that edits real Excel workbooks to follow natural-language
instructions, and **checks its own work before it finishes**. On the 400-task
[SpreadsheetBench](https://github.com/RUCKBReasoning/SpreadsheetBench) benchmark it
reaches an **88.25% pass rate** (82.31% cell accuracy), graded by the shipped
evaluator. Built at the Ylookup × Encode AI Hackathon, where it took **1st place in
the research track**.

## Why verification-first

SpreadsheetBench grades the exact cell values a workbook holds *after* LibreOffice
recalculates its formulas. In practice the model rarely fails because it can't do the
task — it fails on the margins: an off-by-one boundary, a number written as text, a
stale formula cache, a sort that also disturbed an unrelated column. A single-shot
"return every answer value as JSON" approach both runs out of tokens on large sheets
and has no way to catch those mistakes.

So the agent is built around a hard rule: **every edit is followed by a mandatory,
evidence-backed review turn, and the model may not finish while a review or repair is
outstanding.** Instead of emitting final values, the model writes a spreadsheet
*operation* (Python/`openpyxl` or Bash); the harness then recalculates, diffs, and
snapshots the result and hands that evidence back for the model to check against the
instruction. Getting the answer once is optional; convincing the harness it's correct
is not.

## How it works

For each task the model gets the instruction, an answer-aware
[workbook digest](agent/digest.py), the graded answer range, and — when the
instruction matches — a short task-specific [playbook](agent/skills.py) (filtering,
sorting, aggregation, deletion, conditional edits). It then runs a loop of up to 20
turns, emitting exactly one JSON action per turn
([`agent/harness.py`](agent/harness.py)):

| Action | Purpose |
|---|---|
| `inspect_workbook`, `inspect_range` | read structure, values, formulas, styles |
| `assert_sorted`, `assert_blank` | cheap deterministic checks |
| `run_python` / `run_bash` (`inspect` or `edit`) | execute model-written code in a sandbox |
| `recalculate_workbook` | refresh formula results via LibreOffice |
| `finish` | accept the output workbook |

Code runs in a per-task sandbox ([`agent/sandbox.py`](agent/sandbox.py)) with
`IN_XLSX`/`OUT_XLSX` env vars; `OUT_XLSX` starts as a copy of the input and is the only
file the model edits. Edit actions must declare the ranges they intend to change.

After **every successful edit**, the harness ([`agent/verify.py`](agent/verify.py)):

1. **Recalculates** the formula cells in the graded range with headless LibreOffice —
   the same engine the grader uses — so cached formula values can't drift.
2. **Diffs** the workbook before vs. after, type-aware (so `1` ≠ `"1"`), and flags any
   changed cell that falls **outside** the ranges the model declared — catching
   collateral damage.
3. **Snapshots** the current answer cells in a grading-focused view.
4. **Forces an independent review turn**: the model re-reads the instruction against
   that evidence and must issue a repair edit if anything is wrong. `finish` is blocked
   until the review passes.

Two safety nets close it out: the output must load as a valid workbook before `finish`
is accepted, and a last-ditch fallback copies the untouched input workbook so a crash
never loses a task. An optional independent critic model can add further repair rounds
(disabled for the submitted run).

## The model

`Qwen/Qwen3.8-27B`, sampled through [Tinker](https://tinker.thinkingmachines.ai/) —
renderer `qwen3_8_medium_reasoning`, temperature 0, 32,768 max tokens per turn, with a
truncation ladder (`fallback_renderers: auto`) that re-samples one thinking level lower
when a reply is cut off mid-thought instead of feeding the parser partial reasoning.
Those settings come from a representation study on a stratified dev split
([`research/experiments/representation_ablation.md`](research/experiments/representation_ablation.md)),
not guesswork. Everything is in [`research/config/qwen.yaml`](research/config/qwen.yaml).

We also fine-tuned a LoRA on evaluated-correct agent traces
([`research/training/`](research/training)); it didn't beat the base-model agent on
measured accuracy, so the submission ships the base model. Its training log is
[`lora.log`](lora.log).

## Running it

The submission is the Docker image. It reads the judge-mounted dataset from `/data`
(read-only) and writes `predictions.jsonl`, `outputs/`, `traces/`, and `run.log` to
`/out`. All model-written code executes only inside the container, which bundles
LibreOffice for recalculation.

```sh
docker build -t ssagent .
docker run --rm -e TINKER_API_KEY=... \
  -v /path/to/dataset:/data:ro \
  -v /path/to/out:/out \
  ssagent
```

The Tinker project id is pinned in `research/config/qwen.yaml`; only `TINKER_API_KEY`
is read from the environment. Extra flags pass straight through, e.g.
`docker run ... ssagent --ids 13-1,51-12`.

Grade a run with the shipped evaluator:

```sh
cd research
uv sync --extra tinker
uv run evaluate.py --predictions ../predictions.jsonl --all --out ../results.json
```

For local development without Tinker, [`agent/run.py`](agent/run.py) runs the same
harness against a `mock` or OpenRouter model, plus a `null` mode that copies the input
workbook through to smoke-test the mounts and `/out` layout end to end.

## Repo layout

```
agent/                 the verification-first tool agent
  harness.py           multi-turn loop, review gate, critic
  verify.py            type-aware diff + formula detection
  digest.py            answer-aware workbook summary + verification snapshot
  workbook_tools.py    inspect_range / assert_sorted / assert_blank
  sandbox.py           sandboxed Python/Bash execution
  skills.py            task-specific playbooks
  models.py            mock / OpenRouter / Tinker model adapters
  run.py               local dev entrypoint (mock/OpenRouter, null mode)
research/
  baseline/            inference runners — agent_predict.py is the Docker submission
  config/              qwen.yaml (agent sampling), qwen_lora.yaml (LoRA experiment)
  training/            LoRA fine-tuning + SFT data construction
  teacher/             teacher / SFT data-generation scripts
  experiments/         the representation study and scoreboards
  tests/               pytest suite (run in CI)
  sb.py                dataset loading, LibreOffice recalculation, grading helpers
  evaluate.py          the shipped SpreadsheetBench evaluator
datasets/              data plan + train/test split definitions (dataset fetched at runtime)
Dockerfile             submission container (Qwen via Tinker + LibreOffice)
docker_entrypoint.sh   container entrypoint; owns run.log via tee
predictions.jsonl      the 400-task run: one prediction record per task
outputs/               400 completed .xlsx workbooks
traces/                400 per-task agent traces (model calls + tool activity)
run.log                unedited log from the 400-task run
results.json           grade from the shipped evaluator (88.25% pass rate)
SUBMISSION.md          the hackathon approach writeup
docs/HACKATHON_BRIEF.md the original organiser event brief
```

## Results

From the shipped evaluator over all 400 tasks:

```json
{
  "items": 400,
  "graded": 400,
  "missing": 0,
  "errors": 0,
  "pass_rate": 0.8825,
  "cell_accuracy": 0.8231,
  "pass_rate_cell_level": 0.88,
  "pass_rate_sheet_level": 0.888
}
```

## Credits

Built by a four-person team at the **Ylookup × Encode AI Hackathon**, London,
5–6 September 2026 — **1st place, research track**.

- Maanav Chittireddy ([@saimaanav](https://github.com/saimaanav))
- Veejay Roy ([@vjroy](https://github.com/vjroy))
- Lorcan Purcell ([@Lorcan7274](https://github.com/Lorcan7274))
- Elie Ben-Shlomo ([@ElieBen-Shlomo](https://github.com/ElieBen-Shlomo))

Original hackathon repo:
[ElieBen-Shlomo/encode-hackathon-condensed](https://github.com/ElieBen-Shlomo/encode-hackathon-condensed).
