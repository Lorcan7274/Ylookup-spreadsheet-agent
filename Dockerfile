# SpreadsheetBench pipeline container.
#
#   docker build -t team .
#   docker run --rm -e TINKER_API_KEY=... -v <dataset dir>:/data:ro -v <empty dir>:/out team
#
# Reads /data (dataset.json, spreadsheet/<id>/*init*.xlsx, prompt.txt), writes
# predictions.jsonl, outputs/, traces/, run.log to /out. Model-written code executes
# only inside this container. LibreOffice is included so the pipeline can recalculate
# formulas exactly the way the evaluator does.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    LC_ALL=C.UTF-8 \
    UV_LINK_MODE=copy

# LibreOffice headless for formula recalculation (same engine the grader uses)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libreoffice-calc fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# dependencies first, for layer caching. The submission agent samples Qwen through Tinker.
COPY research/pyproject.toml research/uv.lock ./
RUN uv sync --frozen --no-dev --extra tinker

# code
COPY research/sb.py sb.py
COPY research/baseline/ baseline/
COPY research/config/qwen.yaml config/qwen.yaml
# agent_predict.py resolves its tool modules at /agent inside the image.
COPY agent/ /agent/
COPY docker_entrypoint.sh /app/docker_entrypoint.sh
RUN chmod +x /app/docker_entrypoint.sh

ENV PATH="/app/.venv/bin:$PATH"

# Run the base Qwen spreadsheet agent against the organiser's mounts. Extra flags
# can be appended, for example: docker run ... team --ids 13-1,51-12
ENTRYPOINT ["/app/docker_entrypoint.sh"]
