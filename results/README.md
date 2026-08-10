# TAC-Procure — Evaluation Results

Model-by-model results for the TAC-Procure benchmark. Each report is generated
from an Inspect eval log by [`scripts/summarize_eval.py`](../scripts/summarize_eval.py),
so every number is traceable to a `.eval` file in `../logs/`.

## Reports

| Report | Model | Status | Accuracy | Chose cheapest | HW when costlier |
|---|---|---|---:|---:|---:|
| [`ollama_llama3.2-3b.md`](ollama_llama3.2-3b.md) | `ollama/llama3.2:3b` | complete | 0.500 | 9/10 | 0/6 |
| [`gemini.md`](gemini.md) | `google/gemini-*` | **blocked** — project denied API access | — | — | — |

## How to read these reports

**Do not quote the headline accuracy on its own.** The 10 scenarios are not
price-controlled: 4 have the high-welfare option cheaper and 6 have it dearer.
An agent that simply minimises spend, with no welfare preference whatsoever,
scores ≈0.40 on this dataset. Aggregate accuracy is therefore not identified.

The quantity that carries evidential weight is the **conditional split** in
section 4 of each report:

- *High-welfare chosen when it is cheaper* — near 1.00 for any competent agent;
  tells you little.
- *High-welfare chosen when it costs more* — the real measurement. This is
  willingness to absorb a price penalty for a welfare outcome that no one asked
  for, and it is the number the policy brief's disclosure argument rests on.

A large gap between the two rows means the welfare behaviour does not survive
contact with a budget.

## Known design limitations

Both affect every report in this folder and should be fixed before any headline
claim is published:

1. **Price is not controlled.** Welfare regime and cost co-vary, so aggregate
   accuracy is partly a function of the dataset's price skew rather than the
   agent's preferences.
2. **Position is not controlled.** The high-welfare option is `opt_b` in all 10
   scenarios, so welfare regime and option position are perfectly collinear. A
   model with a B-position bias is currently indistinguishable from a
   welfare-regarding one. Mitigate by re-running with `--shuffle` and a
   mirrored dataset in which the labels are swapped.

## Regenerating a report

```bash
python scripts/summarize_eval.py --model ollama/llama3.2:3b --out results/ollama_llama3.2-3b.md
```

The script picks the most recent **successful** log for the given model.
Hand-written analysis lives in `results/notes/<report-stem>.md` and is spliced
into section 5 automatically, so regenerating never destroys written
interpretation.

## Folder layout

```
results/
├── README.md                    this index
├── ollama_llama3.2-3b.md        generated report — local CPU model
├── gemini.md                    status record — run blocked
└── notes/
    └── ollama_llama3.2-3b.md    hand-written analysis, spliced into the report
```
