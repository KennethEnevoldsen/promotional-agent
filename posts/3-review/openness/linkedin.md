Most embedding models on MTEB publish their weights. Far fewer publish what it took to
build them.

Of the 171 models with complete MTEB(Multilingual, v2) results:

• 153 are open-weight
• 10 are fully open — weights, training code and training data
• 8 are proprietary

Fully reproducible models are under 6% of the board. "Open" in common usage means the
middle tier, and the gap between publishing weights and publishing the recipe is where
almost the entire field sits.

The best model in each tier: microsoft/harrier-oss-v1-27b at 74.27 (open weights),
Bytedance/Seed1.6-embedding-1215 at 70.26 (proprietary), nvidia/llama-embed-nemotron-8b
at 69.46 (fully open).

Two things this does not show.

It is not evidence that open models beat proprietary ones. Only 8 proprietary models have
complete results here, out of 51 with any — the well-known API models are mostly
partially evaluated rather than absent. A lead over a thin, self-selected sample says
little about capability. What the data does support is the composition.

And 6% is not an accusation. Publishing training data is genuinely hard — licensing,
scale, competitive cost. The number is worth stating precisely because it is easy to
assume "open model" means reproducible, when it almost never does.

One note on method, since it changed the answer. This originally ran on MTEB(eng, v2),
picked for a mechanical reason that stopped being true. Redone on the multilingual set,
the picture shifted: on English the best proprietary and best open-weight models were
separated by 0.01 points; on multilingual the open-weight model leads by four. Same
question, different benchmark, different answer — which is why the multilingual set is
the default here.

Numbers recomputed from the results repository, not taken from model cards. The query
that produced them is in the repo alongside the post.
