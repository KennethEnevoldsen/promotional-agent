---
id: lmeb
type: results_addition
trigger: results#670
trigger_date: 2026-08-10
expires: 2026-09-10
verified: true
subject: opensearch-project/opensearch-neural-sparse-encoding-doc-v2-mini
evidence: data.json
media: card-1-lmeb.png
sources:
  - https://github.com/embeddings-benchmark/results/pull/670
---

```
New on MTEB: opensearch-project/opensearch-neural-sparse-encoding-doc-v2-mini (11M active) sits on LMEB's Pareto frontier — nothing smaller scores higher, at any size up to 7.4B active. Sibling v2-distill (43M) is close behind at 56.53.

Part of a 12-model wave added to LMEB this week.
```

## The claim

`results#670` submits day-one-for-this-account LMEB results for 12 models: 4
`opensearch-project` neural-sparse encoders, `LiquidAI/LFM2.5-Embedding-350M`,
`perplexity-ai/pplx-embed-v1-0.6b`, and 6 `ibm-granite` variants. None of the 12 were
registered in this scan window — this is a `results_addition`, not a `model_addition`.
LMEB itself (`mteb#4614`) isn't new either: registered in May, and the board already
has 70 models with complete 22-task coverage before counting this batch.

So the post isn't "12 models landed" — a batch with no shared claim isn't one post
(CONTRIBUTING's "one post, one claim"). It's that
`opensearch-project/opensearch-neural-sparse-encoding-doc-v2-mini` — 11M active
parameters — is **non-dominated across the full 70-model board**: no model at or below
11M active scores higher, and nothing at any size up to
`tencent/KaLM-Embedding-Gemma3-12B-2511` (10.8B active) beats it either, since it beats
every model on the frontier below the very largest few. Confirmed independently by
`mtebpost.model_release.recommend_chart()`, not just eyeballed.

`opensearch-project/opensearch-neural-sparse-encoding-doc-v2-distill` (43M active,
56.53) is *also* on the frontier — the next step up — but isn't the card's subject: its
name is close enough in length and position to v2-mini's that both as labeled points
collide (tried it; even a forced label-side split ran the wider label off the canvas
edge). Named in the post text instead.

## LMEB, briefly

Long-horizon Memory Embedding Benchmark (`arXiv:2603.12572`) — 22 English retrieval
tasks across episodic, dialogue, semantic and procedural memory scenarios (`LoCoMo`,
`LongMemEval`, `ToolBench`, `MemBench`, etc.): can a model retrieve the right evidence
from a long-running interaction history, not just a single document. A capability
domain this account has not covered before — breadth, not just a new number.

## Where the rest of the 12-model batch lands

| model | rank of 70 | score |
|---|---:|---:|
| `perplexity-ai/pplx-embed-v1-0.6b` | 10 | 57.92 |
| `opensearch-project/opensearch-neural-sparse-encoding-doc-v3-gte` | 15 | 56.99 |
| `opensearch-project/opensearch-neural-sparse-encoding-doc-v2-distill` | 18 | 56.53 |
| `opensearch-project/opensearch-neural-sparse-encoding-doc-v3-distill` | 19 | 56.34 |
| `ibm-granite/granite-embedding-278m-multilingual` | 42 | 52.28 |
| `ibm-granite/granite-embedding-english-r2` | 46 | 52.03 |
| `LiquidAI/LFM2.5-Embedding-350M` | 48 | 51.05 |
| `ibm-granite/granite-embedding-107m-multilingual` | 51 | 50.76 |
| `ibm-granite/granite-embedding-small-english-r2` | 56 | 49.79 |
| `ibm-granite/granite-embedding-30m-english` | 58 | 48.85 |
| `ibm-granite/granite-embedding-125m-english` | 61 | 46.24 |

`perplexity-ai/pplx-embed-v1-0.6b` at 10th of 70 is itself notable — not spent here,
since the pareto claim is stronger and a post gets one claim — but worth remembering if
a future post needs an angle and this field has moved on.

## Notes

Credit: "Contributed by the OpenSearch project" rather than a personal GitHub handle —
`results#670`'s PR body has no named individual, and the four models are an
organizational submission (`opensearch-project` org account). No Bluesky handle in
`social-handles.yaml` either way.

`mteb/baseline-bm25s` and `hotchpotch/bekko-embedding-v1-a8m` also sit on the LMEB
frontier below v2-mini (see `data.json`) — left off the card and text since they aren't
this post's subject; the frontier line still shows their position.
