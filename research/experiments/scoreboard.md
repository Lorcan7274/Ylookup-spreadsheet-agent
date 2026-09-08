# Representation study scoreboard

One row per run. Buckets are failure attribution (see experiments/attribute.py). Runs live in research/private/runs/.

| run | when | n | pass % | cell acc % | cell-lvl % | sheet-lvl % | in tok p50/p90 | out tok mean | latency p50 s | s/task | calls/task | length hits | statuses | pass | infra | truncation | format | coverage | error_value | reasoning |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| values-tsv-xhigh-m8192 | 05 14:17 | 100 | 52.0 | 49.2 | 66.7 | 19.4 | 891/2941 | 4930.0 | 70.0 | 69.1 | 1 | 41 | no JSON object in reply:41 ok:59 | 52 | 41 | 1 | 5 | 0 | 0 | 1 |
| values-tsv-off | 05 14:26 | 100 | 43.0 | 49.4 | 47.8 | 32.3 | 855/2905 | 1243.0 | 5.7 | 18.9 | 1 | 8 | Extra data:1 no JSON object in reply:8 ok:91 | 43 | 8 | 3 | 7 | 4 | 0 | 35 |
| values-tsv-medium | 05 14:36 | 100 | 64.0 | 49.7 | 76.8 | 35.5 | 853/2903 | 4005.0 | 28.0 | 56.9 | 1 | 7 | no JSON object in reply:9 ok:91 | 64 | 7 | 3 | 10 | 4 | 0 | 12 |
| values-tsv-low | 05 14:44 | 100 | 65.0 | 49.7 | 76.8 | 38.7 | 879/2929 | 3462.0 | 25.7 | 52.2 | 1 | 5 | no JSON object in reply:9 ok:91 | 65 | 5 | 3 | 8 | 7 | 0 | 12 |
| values-tsv-adaptive | 05 14:55 | 100 | 64.0 | 49.7 | 76.8 | 35.5 | 853/2929 | 3774.0 | 25.0 | 54.0 | 1 | 8 | no JSON object in reply:10 ok:90 | 64 | 8 | 2 | 8 | 5 | 0 | 13 |
| values-tsv-xhigh | 05 17:04 | 100 | 64.0 | 49.5 | 76.8 | 35.5 | 891/2941 | 7448.0 | 99.5 | 134.0 | 1 | 22 | no JSON object in reply:22 ok:78 | 64 | 22 | 2 | 7 | 0 | 0 | 5 |
| agent-tsv-low | 05 18:29 | 100 | 78.0 | 99.0 | 75.4 | 83.9 | 1113/3163 | 2268.0 | 23.7 | 37.1 | 1.09 | 2 | exec failed after retrie:1 ok:99 | 78 | 0 | 1 | 0 | 6 | 3 | 12 |
| values-grid-low | 05 18:38 | 100 | 63.0 | 49.8 | 76.8 | 32.3 | 1046/3984 | 3530.0 | 28.6 | 61.9 | 1 | 2 | no JSON object in reply:5 ok:95 | 63 | 2 | 3 | 9 | 11 | 0 | 12 |
| agent-tsv-medium | 05 18:46 | 100 | 81.0 | 54.4 | 81.2 | 80.7 | 1087/3137 | 2033.0 | 31.1 | 45.6 | 1.08 | 0 | ok:100 | 81 | 0 | 3 | 0 | 4 | 2 | 10 |
| values-grid-medium | 05 19:04 | 100 | 61.0 | 49.6 | 73.9 | 32.3 | 1020/3958 | 4038.0 | 43.7 | 80.6 | 1 | 7 | Expecting ',' delimiter:1 no JSON object in reply:7 ok:92 | 61 | 7 | 1 | 8 | 8 | 1 | 14 |
| values-windowed-low | 05 19:24 | 100 | 60.0 | 49.9 | 75.4 | 25.8 | 809/2584 | 3147.0 | 29.5 | 59.5 | 1 | 2 | no JSON object in reply:5 ok:95 | 60 | 2 | 7 | 11 | 8 | 0 | 12 |
| agent-grid-low | 05 19:30 | 100 | 88.0 | 56.8 | 87.0 | 90.3 | 1280/4218 | 2192.0 | 25.5 | 44.0 | 1.04 | 3 | no code block:1 ok:99 | 88 | 1 | 1 | 0 | 3 | 1 | 6 |
| agent-windowed-low | 05 19:41 | 100 | 75.0 | 56.6 | 75.4 | 74.2 | 1043/2818 | 2081.0 | 29.8 | 45.8 | 1.13 | 0 | ok:100 | 75 | 0 | 2 | 0 | 7 | 4 | 12 |
| agent-grid-medium | 05 19:50 | 100 | 87.0 | 56.7 | 87.0 | 87.1 | 1254/4192 | 2330.0 | 30.6 | 49.5 | 1.05 | 1 | ok:100 | 87 | 0 | 1 | 0 | 5 | 1 | 6 |
| values-html-low | 05 20:14 | 100 | 67.0 | 49.8 | 81.2 | 35.5 | 1969/7023 | 3436.0 | 31.0 | 64.6 | 1 | 6 | no JSON object in reply:6 ok:94 | 67 | 6 | 4 | 11 | 4 | 0 | 8 |
| values-compact-low | 05 20:16 | 100 | 54.0 | 49.8 | 65.2 | 29.0 | 1320/4661 | 4208.0 | 36.1 | 72.9 | 1 | 7 | no JSON object in reply:10 ok:90 | 54 | 7 | 2 | 9 | 8 | 0 | 20 |
| values-json-low | 05 20:37 | 100 | 65.0 | 49.8 | 79.7 | 32.3 | 1307/5086 | 3331.0 | 31.3 | 65.9 | 1 | 4 | no JSON object in reply:5 ok:95 | 65 | 4 | 3 | 11 | 7 | 0 | 10 |
| values-markdown-low | 05 20:39 | 100 | 64.0 | 49.9 | 76.8 | 35.5 | 1343/4576 | 3684.0 | 27.5 | 68.1 | 1 | 4 | no JSON object in reply:4 ok:96 | 64 | 4 | 1 | 10 | 8 | 1 | 12 |
| agent-compact-low | 05 20:55 | 100 | 89.0 | 54.2 | 92.8 | 80.7 | 1554/4895 | 2071.0 | 26.6 | 41.3 | 1.04 | 0 | ok:100 | 89 | 0 | 1 | 0 | 3 | 2 | 5 |
| values-addressed-low | 05 21:03 | 100 | 67.0 | 49.9 | 81.2 | 35.5 | 1254/5113 | 3399.0 | 30.0 | 64.8 | 1 | 3 | no JSON object in reply:5 ok:95 | 67 | 3 | 2 | 10 | 8 | 0 | 10 |
| agent-markdown-low | 05 21:07 | 100 | 84.0 | 56.7 | 84.1 | 83.9 | 1577/4810 | 1796.0 | 26.1 | 35.4 | 1.05 | 0 | ok:100 | 84 | 0 | 1 | 1 | 5 | 2 | 7 |
| agent-schema-low | 05 21:16 | 100 | 86.0 | 56.7 | 85.5 | 87.1 | 1474/4461 | 1995.0 | 24.7 | 36.2 | 1.04 | 0 | ok:100 | 86 | 0 | 2 | 0 | 4 | 0 | 8 |
| values-grid-low-b2000 | 05 21:37 | 100 | 64.0 | 49.8 | 78.3 | 32.3 | 1046/3515 | 3613.0 | 30.3 | 64.0 | 1 | 5 | no JSON object in reply:6 ok:94 | 64 | 5 | 2 | 9 | 10 | 0 | 10 |
| values-grid-low-b16000 | 05 21:38 | 100 | 62.0 | 49.8 | 75.4 | 32.3 | 1046/3984 | 3713.0 | 30.1 | 66.0 | 1 | 5 | no JSON object in reply:6 ok:94 | 62 | 5 | 2 | 10 | 11 | 0 | 10 |
| agent-grid-low-b4000 | 05 21:53 | 100 | 85.0 | 99.2 | 81.2 | 93.5 | 1280/4218 | 2014.0 | 23.2 | 34.6 | 1.07 | 1 | ok:100 | 85 | 0 | 1 | 1 | 2 | 4 | 7 |
| values-grid-low-b4000 | 05 21:59 | 100 | 63.0 | 49.8 | 76.8 | 32.3 | 1046/3984 | 3715.0 | 28.3 | 67.0 | 1 | 5 | Expecting property name :1 no JSON object in reply:6 ok:93 | 63 | 5 | 2 | 9 | 10 | 0 | 11 |
