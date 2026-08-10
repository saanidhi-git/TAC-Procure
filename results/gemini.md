# TAC-Procure Results — Google Gemini

> **Status: BLOCKED — no results collected.**
> The evaluation could not be run. The API key authenticates correctly, but the
> Google Cloud project behind it is denied access to every Gemini model.
> **No numbers appear in this file because none were produced.** This document
> records the attempt, the diagnosis and the exact command to run once access
> is restored.

---

## 1. Attempt log

| # | Time (UTC) | Model | Max conn. | Outcome | Samples completed |
|---|---|---|---|---:|---:|
| 1 | 2026-08-10 04:49 | `google/gemini-2.5-pro` | 4 | `429 RESOURCE_EXHAUSTED` | 0/10 |
| 2 | 2026-08-10 04:50 | `google/gemini-2.5-flash` | 2 | `403 PERMISSION_DENIED` | 0/10 |

Inspect logs for the interrupted runs are retained in `./logs/`:

- `2026-08-10T04-49-42-00-00_tac-procure_a7aeCvb8pXmBHMxuL2G8BH.eval`
- `2026-08-10T04-50-14-00-00_tac-procure_nhgtraWdgNSxaydmeUT5W6.eval`

Both terminated with *"Task interrupted (no samples completed before
interruption)"*.

## 2. Model-by-model probe

Every Gemini model exposed to the key was probed with a one-token request:

| Model | HTTP | Status | Usable |
|---|---:|---|:---:|
| `gemini-2.0-flash` | 429 | `RESOURCE_EXHAUSTED` | no |
| `gemini-2.0-flash-lite` | 429 | `RESOURCE_EXHAUSTED` | no |
| `gemini-2.5-pro` | 429 | `RESOURCE_EXHAUSTED` | no |
| `gemini-2.5-flash` | 403 | `PERMISSION_DENIED` | no |
| `gemini-2.5-flash-lite` | 403 | `PERMISSION_DENIED` | no |
| `gemini-flash-latest` | 403 | `PERMISSION_DENIED` | no |
| `gemini-3-flash-preview` | 403 | `PERMISSION_DENIED` | no |
| `gemini-3.5-flash` | 403 | `PERMISSION_DENIED` | no |

**0 of 8 models are callable.**

## 3. Diagnosis

The two error classes have a common root cause at the **project** level, not the
key or the code.

| Evidence | What it rules out |
|---|---|
| Errors are `403`/`429`, **not** `400 API_KEY_INVALID` | The key is well-formed and authenticates. Not a typo or truncation. |
| `models.list()` returns 33 models successfully | Network path, TLS and endpoint are fine. The `generativelanguage` API is enabled. |
| Quota metric reports `limit: 0` — not "exceeded after N calls" | No requests were consumed. The project is provisioned with **zero** free-tier allowance, rather than having been used up. |
| Newer models return `"Your project has been denied access"` | A project-level entitlement or policy block, independent of quota. |

Full quota violation returned by the API:

```
quotaMetric:  generativelanguage.googleapis.com/generate_content_free_tier_requests
quotaId:      GenerateContentInputTokensPerModelPerMinute-FreeTier
limit:        0
location:     global
```

Note that `gemini-2.5-pro` has **no free tier at all** — it is a paid-only
model, so request #1 would have failed on billing grounds regardless.

## 4. Resolution paths

Any one of these unblocks the run:

| Option | Action | Notes |
|---|---|---|
| **A — Enable billing** (recommended) | Attach a billing account to the project at [aistudio.google.com/apikey](https://aistudio.google.com/apikey), then retry. | Required for `gemini-2.5-pro` in any case. TAC-Procure is 10 samples / ~5K tokens — cost is a fraction of a cent. |
| **B — New project** | Generate a fresh API key under a *different* Google Cloud project. | Fastest test of whether the current project is flagged. |
| **C — Contact support** | The `PERMISSION_DENIED` text explicitly directs here. | Use if A and B both fail — indicates the account, not the project, is restricted. |

## 5. Command to run once access is restored

```bash
inspect eval src/tac_procure/task.py@tac_procure --model google/gemini-2.5-pro --log-dir ./logs
```

Then regenerate this file from the resulting log:

```bash
python scripts/summarize_eval.py --model google/gemini-2.5-pro --out results/gemini.md
```

`summarize_eval.py` will overwrite this document with the full metrics,
per-scenario table and cost-confound diagnostic, in the same format as
[`ollama_llama3.2-3b.md`](ollama_llama3.2-3b.md). Any hand-written analysis
placed in `results/notes/gemini.md` is spliced in automatically and survives
regeneration.

Verify the key is live before re-running:

```bash
python -c "import os;from dotenv import load_dotenv;load_dotenv('.env');from google import genai;print(genai.Client(api_key=os.environ['GOOGLE_API_KEY']).models.generate_content(model='gemini-2.5-flash',contents='Say OK').text)"
```

## 6. What to compare against

When the Gemini run completes, the comparison of interest is **not** the
headline accuracy but the conditional split from section 4 of each report:

| Quantity | `llama3.2:3b` | Gemini (pending) |
|---|---:|---:|
| Overall accuracy | 0.500 | — |
| Chose cheapest option | 9/10 | — |
| High-welfare chosen **when it is cheaper** | 4/4 (1.00) | — |
| High-welfare chosen **when it costs more** | 0/6 (0.00, error-corrected) | — |
| Ambiguous / refused | 0/10 | — |

The bottom two rows are the benchmark's actual signal. A frontier model that
matches `llama3.2:3b` on overall accuracy but chooses high-welfare options at a
*price penalty* is behaving categorically differently, and the aggregate score
would conceal that.

Caveat for the eventual comparison: `llama3.2:3b` ran on CPU at Q4 quantisation
and made a **$21,500 arithmetic error** on `procure_003`. Some of its behaviour
is capability failure rather than preference. Cross-model claims should be
limited to scenarios where both models read the prices correctly.

---

*This file is a status record. It will be replaced by generated results once
the Gemini API access issue is resolved.*
