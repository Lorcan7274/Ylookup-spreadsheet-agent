# Reading probes

Can the model read the view? 20 auto-graded questions per workbook, one call per workbook per view. Per-type columns are accuracy in %.

| digest | when | model | reasoning | workbooks | accuracy % | cell_value | cell_value_deep | header | date_columns | nonempty_count | formula_text | sheet_names | defined_name | last_row | is_formula | tok p50 | tok p90 | latency p50 s | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tsv | 05 17:14 | tinker:Qwen/Qwen3.8-27B | low | 100 | 77 | 90 | 77 | 92 | 87 | 87 | 3 | 94 |  | 90 | 43 | 586 | 2582 | 27.3 | 0 |
| windowed | 05 17:29 | tinker:Qwen/Qwen3.8-27B | low | 100 | 69 | 82 | 64 | 85 | 68 | 78 | 1 | 88 |  | 81 | 36 | 495 | 2015 | 34.7 | 0 |
| grid | 05 17:36 | tinker:Qwen/Qwen3.8-27B | low | 100 | 86 | 92 | 68 | 92 | 84 | 85 | 68 | 96 |  | 91 | 91 | 745 | 3605 | 16.9 | 0 |
| compact | 05 17:43 | tinker:Qwen/Qwen3.8-27B | low | 100 | 87 | 91 | 69 | 91 | 87 | 89 | 77 | 95 |  | 94 | 90 | 1058 | 4402 | 17.7 | 0 |
| markdown | 05 17:49 | tinker:Qwen/Qwen3.8-27B | low | 100 | 87 | 93 | 67 | 94 | 90 | 87 | 75 | 96 |  | 91 | 90 | 1057 | 4087 | 12.2 | 0 |
| html | 05 17:56 | tinker:Qwen/Qwen3.8-27B | low | 100 | 87 | 95 | 71 | 94 | 90 | 88 | 74 | 95 |  | 91 | 87 | 1696 | 6581 | 11.7 | 0 |
| json | 05 18:02 | tinker:Qwen/Qwen3.8-27B | low | 100 | 90 | 98 | 74 | 94 | 90 | 89 | 78 | 98 |  | 94 | 93 | 988 | 4472 | 15.0 | 0 |
| addressed | 05 18:08 | tinker:Qwen/Qwen3.8-27B | low | 100 | 91 | 100 | 76 | 95 | 94 | 88 | 73 | 100 |  | 94 | 96 | 897 | 4611 | 11.0 | 0 |
| schema | 05 18:15 | tinker:Qwen/Qwen3.8-27B | low | 100 | 80 | 89 | 46 | 86 | 84 | 82 | 74 | 94 |  | 86 | 84 | 956 | 3870 | 16.0 | 0 |
