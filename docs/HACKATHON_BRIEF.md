# Ylookup x Encode AI Hackathon

> This is the original organiser event brief, kept for reference. For what this repo
> actually is and how to run it, see the [README](../README.md).

Rebuild private markets. 5-6 September 2026, Encode Hub, Shoreditch. Solo or teams of up to 4.

## The task

SpreadsheetBench: 400 real spreadsheet tasks from Excel forums. Given a workbook and an instruction, return the workbook with the answer filled in. Fine-tune a model, build a harness around one, or both. Ranked by the judges running your pipeline on tasks you have not seen. Everything you need is in [`research/`](research/).

## Timeline

| When | What |
|---|---|
| Sat 09:00 | Doors |
| Sat 10:00 | Intro, task brief, credits handed out |
| Sat 12:00 | Hacking starts |
| Sun 12:00 | Submissions close |
| Sun 12:00-16:00 | Judging, demos, results |

## How to submit

1. Put your code in a public GitHub repo. Code written before Sat 12:00 does not count.
2. Write one paragraph on your approach, 150 to 300 words: the problem you picked, what you built, what worked, what did not. It goes in your repo as `SUBMISSION.md`, from the template in [`research/SUBMISSION_TEMPLATE.md`](research/SUBMISSION_TEMPLATE.md).
3. Your repo must contain `predictions.jsonl`, `outputs/`, `traces/` and `run.log` of your run on the 400, and `results.json` from the shipped evaluator. Agents and anything that executes model-written code run inside a Docker sandbox you ship; judges grade the workbooks it writes. See [`research/SUBMISSION.md`](research/SUBMISSION.md).
4. Before Sun 12:00, send us your repo URL through the form we share on Sunday. One submission per team.

## Prizes

- $2,000 prize pool plus build credits for everyone.
- Winners pitch EQT Ventures.
