"""Multi-turn local Python/Bash tool agent backed by a Tinker Qwen model.

    uv run baseline/agent_predict.py --out-dir submissions/qwen-agent --ids 13-1,51-12

Model and sampling defaults live in config/qwen.yaml. This runner executes model-written
commands on the local host and writes the standard predictions, outputs, traces, and run log.
"""

import argparse
import asyncio
import shutil
import sys
from pathlib import Path

import tinker
from common import append_jsonl, load_env, log, parse_ids, prepare_out_dir, selected_tasks
from tinker import types
from tinker_cookbook import renderers
from tinker_cookbook.model_info import get_recommended_renderer_name
from tinker_cookbook.tokenizer_utils import get_tokenizer
from tinker_predict import load_config

from sb import DEFAULT_DATASET

AGENT_DIR = Path(__file__).resolve().parents[2] / "agent"
sys.path.insert(0, str(AGENT_DIR))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", required=True)
    p.add_argument("--dataset-dir", default=str(DEFAULT_DATASET))
    p.add_argument("--ids", help="comma-separated task ids (default: all)")
    p.add_argument("--config", default="config/qwen.yaml", help="YAML inference settings file")
    p.add_argument("--base-model", help="e.g. Qwen/Qwen3.8-27B")
    p.add_argument(
        "--model-path",
        help="tinker://... sampler checkpoint. Overrides model_path in the YAML; omit both to sample the base model.",
    )
    p.add_argument("--project-id", help="Tinker project ID for the sampling session")
    p.add_argument("--concurrency", type=int, help="parallel tasks")
    p.add_argument("--max-tokens", type=int, help="maximum output tokens for each model turn")
    p.add_argument("--temperature", type=float, help="sampling temperature")
    p.add_argument("--max-turns", type=int, help="maximum Qwen turns per task")
    p.add_argument("--tool-timeout", type=int, help="seconds allowed for each Python or Bash tool call")
    p.add_argument("--review-after-edit", action=argparse.BooleanOptionalAction, default=None)
    p.add_argument("--auto-recalculate-formulas", action=argparse.BooleanOptionalAction, default=None)
    p.add_argument("--verify-changes", action=argparse.BooleanOptionalAction, default=None)
    p.add_argument("--critic-enabled", action=argparse.BooleanOptionalAction, default=None)
    p.add_argument("--max-critic-rounds", type=int)
    p.add_argument("--strict-critic-json", action=argparse.BooleanOptionalAction, default=None)
    p.add_argument("--critic-max-tokens", type=int)
    return p.parse_args()


async def main() -> None:
    load_env()
    args = parse_args()
    config = load_config(Path(args.config))
    base_model = args.base_model or config.get("base_model")
    if not base_model:
        raise ValueError("base_model must be set in the YAML config or passed as --base-model")
    # A command-line checkpoint is an explicit one-run override. Otherwise the
    # config can select a LoRA sampler checkpoint for reproducible Docker runs.
    model_path = args.model_path or config.get("model_path")
    project_id = args.project_id or config.get("project_id")
    concurrency = args.concurrency if args.concurrency is not None else config.get("concurrency", 4)
    max_tokens = args.max_tokens if args.max_tokens is not None else config.get("max_tokens", 8192)
    temperature = args.temperature if args.temperature is not None else config.get("temperature", 0)
    max_turns = args.max_turns if args.max_turns is not None else config.get("max_turns", 20)
    tool_timeout = args.tool_timeout if args.tool_timeout is not None else config.get("tool_timeout", 120)
    review_after_edit = args.review_after_edit if args.review_after_edit is not None else config.get("review_after_edit", True)
    auto_recalculate = args.auto_recalculate_formulas if args.auto_recalculate_formulas is not None else config.get("auto_recalculate_formulas", True)
    verify_changes = args.verify_changes if args.verify_changes is not None else config.get("verify_changes", True)
    critic_enabled = args.critic_enabled if args.critic_enabled is not None else config.get("critic_enabled", False)
    max_critic_rounds = args.max_critic_rounds if args.max_critic_rounds is not None else config.get("max_critic_rounds", 2)
    strict_critic_json = args.strict_critic_json if args.strict_critic_json is not None else config.get("strict_critic_json", True)
    critic_max_tokens = args.critic_max_tokens if args.critic_max_tokens is not None else config.get("critic_max_tokens", 8192)
    renderer_name = config.get("renderer") or get_recommended_renderer_name(base_model)

    print(f"Tinker project ID: {project_id or '<default project>'}", flush=True)
    sampler = tinker.ServiceClient(project_id=project_id).create_sampling_client(
        base_model=base_model, model_path=model_path
    )
    renderer = renderers.get_renderer(renderer_name, get_tokenizer(base_model))
    params = types.SamplingParams(max_tokens=max_tokens, temperature=temperature, stop=renderer.get_stop_sequences())

    from harness import solve_task
    from models import TinkerModel

    tasks = selected_tasks(Path(args.dataset_dir), parse_ids(args.ids))
    out_dir = Path(args.out_dir)
    prepare_out_dir(out_dir)
    log(out_dir, f"mode agent  model {model_path or base_model}  tasks {len(tasks)}  max_turns {max_turns} "
                 f"review {review_after_edit} recalc {auto_recalculate} verify {verify_changes} critic {critic_enabled}")
    model = TinkerModel(sampler, renderer, params, model_path or base_model)
    critic = None
    if critic_enabled:
        critic_params = types.SamplingParams(max_tokens=critic_max_tokens, temperature=temperature,
                                             stop=renderer.get_stop_sequences())
        critic = TinkerModel(sampler, renderer, critic_params, f"{model_path or base_model}:critic")
    semaphore = asyncio.Semaphore(concurrency)

    async def run_one(task: dict) -> None:
        async with semaphore:
            try:
                status = await solve_task(
                    model, task, out_dir, max_turns=max_turns, tool_timeout=tool_timeout,
                    review_after_edit=review_after_edit, auto_recalculate_formulas=auto_recalculate,
                    verify_changes=verify_changes, critic=critic, max_critic_rounds=max_critic_rounds,
                    strict_critic_json=strict_critic_json,
                )
            except Exception as exc:
                shutil.copy(task["init_xlsx"], out_dir / "outputs" / f"{task['id']}.xlsx")
                append_jsonl(out_dir / "predictions.jsonl", {
                    "id": task["id"], "output": f"outputs/{task['id']}.xlsx",
                    "status": f"error: harness crash: {exc}"[:200],
                })
                status = f"error: harness crash: {exc}"[:80]
        log(out_dir, f"{task['id']:<8} {status}")

    await asyncio.gather(*(run_one(task) for task in tasks))


if __name__ == "__main__":
    asyncio.run(main())
