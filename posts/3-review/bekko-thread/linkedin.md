A new embedding model on MTEB is worth a look for how it is built, not just where it
lands.

hotchpotch/bekko-embedding-v1-a8m holds 106M parameters, but only 7.7M of them are
active — the rest sit in a shared multilingual embedding table that is looked up rather
than computed. On MTEB(Multilingual, v2) it scores 56.73 across 131 tasks.

For comparison, a static embedding model of near-identical total size — 108M parameters,
computing nothing per token at all — scores 47.21. So roughly nine points is what that
small amount of per-token compute buys, at the same memory footprint. That is the whole
design argument for this family, and it is visible directly on the leaderboard.

The larger sibling makes a sharper point. bekko-embedding-v1-a25m scores 58.36. Jina's
jina-embeddings-v3 scores 58.37 — a hundredth of a point apart — while computing 12.7
times more per token.

Task by task the two profiles nearly overlap, which is the part a single average hides.
Bekko is ahead on bitext mining and pair classification; jina-v3 is ahead on clustering
and semantic textual similarity. Matching on the mean while differing in shape would be a
different and less interesting result; matching in both is what makes the comparison
worth showing.

Two caveats worth stating.

Active parameters and total parameters are different numbers here, and the difference is
the entire story — calling this "a 7.7M model" would misrepresent its memory, and calling
it "a 106M model" would misrepresent its compute.

And the Pareto framing is scoped: it holds among multilingual models at or below 60M
active parameters with complete results on the benchmark. A model outside that cohort
could change the picture.

Numbers recomputed from the MTEB results repository rather than taken from the model
card, and they match what the contributor reported. The queries are in the repo next to
the post.

Model and results contributed by hotchpotch.
