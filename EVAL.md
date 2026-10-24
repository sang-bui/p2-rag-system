# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.

TODO: describe your three systems.

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.592 | 0.471 | 0.443 |
| rerank | 0.758 | 0.800 | 0.761 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.595 | 0.917 |
| dense | MRR@10 | 0.333 | 0.714 | 0.653 |
| dense | nDCG@10 | 0.211 | 0.593 | 0.661 |
| hybrid | Recall@10 | 0.500 | 0.405 | 0.917 |
| hybrid | MRR@10 | 0.514 | 0.152 | 0.792 |
| hybrid | nDCG@10 | 0.397 | 0.202 | 0.779 |
| rerank | Recall@10 | 0.714 | 0.595 | 1.000 |
| rerank | MRR@10 | 0.714 | 0.714 | 1.000 |
| rerank | nDCG@10 | 0.690 | 0.626 | 1.000 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.067 | [-0.350, +0.225] | 0.415 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.055 | [-0.225, +0.343] | 0.412 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.039 | [-0.302, +0.231] | 0.385 | not distinguishable |
| hybrid minus bm25 | Recall@10 | -0.033 | [-0.250, +0.192] | 0.324 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.037 | [-0.178, +0.083] | 0.192 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.075 | [-0.238, +0.075] | 0.228 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.033 | [-0.125, +0.192] | 0.231 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.092 | [-0.306, +0.109] | 0.301 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.036 | [-0.200, +0.113] | 0.227 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.133 | [-0.100, +0.358] | 0.340 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.293 | [+0.043, +0.533] | 0.353 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.242 | [+0.012, +0.459] | 0.327 | rerank higher |
| rerank minus dense | Recall@10 | +0.200 | [+0.050, +0.367] | 0.224 | rerank higher |
| rerank minus dense | MRR@10 | +0.237 | [+0.083, +0.408] | 0.239 | rerank higher |
| rerank minus dense | nDCG@10 | +0.281 | [+0.142, +0.434] | 0.214 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | 0.166 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | 0.247 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.317 | [+0.193, +0.445] | 0.184 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

TODO: write what the practice-query intervals let you claim.

---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rerank | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 13 of 13 |
<!-- p2:end answers -->

Which system answered, and why that one?
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.

TODO: write your answer choices and your three-answer audit.

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

TODO: describe your corpus and its license basis.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

TODO: describe your gold set and your relevance rule.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.548 | 0.675 | 0.542 |
| dense | 0.542 | 0.734 | 0.542 |
| hybrid | 0.628 | 0.777 | 0.600 |
| rerank | 0.663 | 0.879 | 0.687 |
| ablation/rerank_abstract | 0.642 | 0.860 | 0.673 |

30 judged queries; nDCG uses binary labels; a random ranking of the 345 documents would get recall@10 near 0.029.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | identifier (n=10) | paraphrase (n=10) | mixed (n=10) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 0.713 | 0.307 | 0.624 |
| bm25 | MRR@10 | 0.800 | 0.525 | 0.700 |
| bm25 | nDCG@10 | 0.706 | 0.318 | 0.601 |
| dense | Recall@10 | 0.783 | 0.271 | 0.572 |
| dense | MRR@10 | 1.000 | 0.575 | 0.628 |
| dense | nDCG@10 | 0.789 | 0.316 | 0.519 |
| hybrid | Recall@10 | 0.869 | 0.396 | 0.619 |
| hybrid | MRR@10 | 0.867 | 0.739 | 0.725 |
| hybrid | nDCG@10 | 0.791 | 0.403 | 0.605 |
| rerank | Recall@10 | 0.847 | 0.417 | 0.725 |
| rerank | MRR@10 | 1.000 | 0.753 | 0.883 |
| rerank | nDCG@10 | 0.866 | 0.490 | 0.704 |
| ablation/rerank_abstract | Recall@10 | 0.844 | 0.377 | 0.704 |
| ablation/rerank_abstract | MRR@10 | 1.000 | 0.733 | 0.846 |
| ablation/rerank_abstract | nDCG@10 | 0.873 | 0.456 | 0.689 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=10) | claude (n=20) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 0.464 | 0.590 | -0.126 | [-0.434, +0.188] | not distinguishable |
| bm25 | MRR@10 | 0.550 | 0.738 | -0.188 | [-0.525, +0.150] | not distinguishable |
| bm25 | nDCG@10 | 0.444 | 0.591 | -0.147 | [-0.440, +0.155] | not distinguishable |
| dense | Recall@10 | 0.483 | 0.571 | -0.088 | [-0.355, +0.185] | not distinguishable |
| dense | MRR@10 | 0.625 | 0.789 | -0.164 | [-0.485, +0.151] | not distinguishable |
| dense | nDCG@10 | 0.454 | 0.585 | -0.132 | [-0.380, +0.126] | not distinguishable |
| hybrid | Recall@10 | 0.598 | 0.643 | -0.046 | [-0.327, +0.238] | not distinguishable |
| hybrid | MRR@10 | 0.598 | 0.867 | -0.269 | [-0.563, +0.017] | not distinguishable |
| hybrid | nDCG@10 | 0.526 | 0.636 | -0.111 | [-0.373, +0.154] | not distinguishable |
| rerank | Recall@10 | 0.678 | 0.655 | +0.023 | [-0.230, +0.268] | not distinguishable |
| rerank | MRR@10 | 0.767 | 0.935 | -0.168 | [-0.427, +0.063] | not distinguishable |
| rerank | nDCG@10 | 0.639 | 0.711 | -0.071 | [-0.303, +0.157] | not distinguishable |
| ablation/rerank_abstract | Recall@10 | 0.599 | 0.663 | -0.064 | [-0.350, +0.217] | not distinguishable |
| ablation/rerank_abstract | MRR@10 | 0.733 | 0.923 | -0.190 | [-0.490, +0.067] | not distinguishable |
| ablation/rerank_abstract | nDCG@10 | 0.592 | 0.713 | -0.120 | [-0.380, +0.135] | not distinguishable |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | +0.020 | -0.019 | +0.039 | [-0.227, +0.339] | not distinguishable |
| MRR@10 | -0.052 | -0.075 | +0.023 | [-0.227, +0.305] | not distinguishable |
| nDCG@10 | +0.005 | -0.010 | +0.015 | [-0.202, +0.254] | not distinguishable |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.50 (10 queries), claude 0.72 (20 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 10 hand and 20 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.007 | [-0.122, +0.121] | 0.180 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.059 | [-0.064, +0.201] | 0.192 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.0001 | [-0.102, +0.116] | 0.161 | not distinguishable |
| hybrid minus bm25 | Recall@10 | +0.080 | [-0.011, +0.192] | 0.149 | not distinguishable |
| hybrid minus bm25 | MRR@10 | +0.102 | [+0.024, +0.202] | 0.130 | hybrid higher |
| hybrid minus bm25 | nDCG@10 | +0.058 | [-0.002, +0.124] | 0.092 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.086 | [+0.015, +0.156] | 0.103 | hybrid higher |
| hybrid minus dense | MRR@10 | +0.043 | [-0.057, +0.139] | 0.145 | not distinguishable |
| hybrid minus dense | nDCG@10 | +0.058 | [-0.007, +0.119] | 0.092 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.114 | [+0.0003, +0.243] | 0.179 | rerank higher |
| rerank minus bm25 | MRR@10 | +0.204 | [+0.094, +0.329] | 0.173 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.145 | [+0.048, +0.256] | 0.153 | rerank higher |
| rerank minus dense | Recall@10 | +0.121 | [+0.066, +0.180] | 0.082 | rerank higher |
| rerank minus dense | MRR@10 | +0.144 | [+0.021, +0.274] | 0.187 | rerank higher |
| rerank minus dense | nDCG@10 | +0.145 | [+0.086, +0.203] | 0.085 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.035 | [-0.033, +0.119] | 0.112 | not distinguishable |
| rerank minus hybrid | MRR@10 | +0.102 | [-0.004, +0.211] | 0.157 | not distinguishable |
| rerank minus hybrid | nDCG@10 | +0.087 | [+0.025, +0.155] | 0.095 | rerank higher |
| ablation/rerank_abstract minus bm25 | Recall@10 | +0.094 | [-0.015, +0.221] | 0.175 | not distinguishable |
| ablation/rerank_abstract minus bm25 | MRR@10 | +0.185 | [+0.068, +0.314] | 0.182 | ablation/rerank_abstract higher |
| ablation/rerank_abstract minus bm25 | nDCG@10 | +0.131 | [+0.033, +0.244] | 0.155 | ablation/rerank_abstract higher |
| ablation/rerank_abstract minus dense | Recall@10 | +0.100 | [+0.047, +0.157] | 0.079 | ablation/rerank_abstract higher |
| ablation/rerank_abstract minus dense | MRR@10 | +0.125 | [+0.006, +0.255] | 0.183 | ablation/rerank_abstract higher |
| ablation/rerank_abstract minus dense | nDCG@10 | +0.131 | [+0.072, +0.191] | 0.086 | ablation/rerank_abstract higher |
| ablation/rerank_abstract minus hybrid | Recall@10 | +0.014 | [-0.065, +0.105] | 0.124 | not distinguishable |
| ablation/rerank_abstract minus hybrid | MRR@10 | +0.083 | [-0.021, +0.192] | 0.158 | not distinguishable |
| ablation/rerank_abstract minus hybrid | nDCG@10 | +0.073 | [+0.009, +0.144] | 0.100 | ablation/rerank_abstract higher |
| ablation/rerank_abstract minus rerank | Recall@10 | -0.021 | [-0.069, +0.021] | 0.064 | not distinguishable |
| ablation/rerank_abstract minus rerank | MRR@10 | -0.019 | [-0.057, +0.009] | 0.048 | not distinguishable |
| ablation/rerank_abstract minus rerank | nDCG@10 | -0.014 | [-0.047, +0.014] | 0.044 | not distinguishable |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

TODO: write what your own-corpus intervals let you claim.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

Hypothesis (written and committed before the ablation ran):

I expect rerank_abstract to improve nDCG@10 compared with the current rerank system because Claude is currently spending most of its 600-character limit reading citation information rather than the actual abstract. By removing the unnecessary header and giving it more of the abstract while keeping everything else the same, I think it should be better at distinguishing papers that actually answer the query from those that just share similar terminology.

<!-- p2:begin own-ablation -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| ablation/rerank_abstract minus bm25 | Recall@10 | +0.094 | [-0.015, +0.221] | 0.175 | not distinguishable |
| ablation/rerank_abstract minus bm25 | MRR@10 | +0.185 | [+0.068, +0.314] | 0.182 | ablation/rerank_abstract higher |
| ablation/rerank_abstract minus bm25 | nDCG@10 | +0.131 | [+0.033, +0.244] | 0.155 | ablation/rerank_abstract higher |
| ablation/rerank_abstract minus dense | Recall@10 | +0.100 | [+0.047, +0.157] | 0.079 | ablation/rerank_abstract higher |
| ablation/rerank_abstract minus dense | MRR@10 | +0.125 | [+0.006, +0.255] | 0.183 | ablation/rerank_abstract higher |
| ablation/rerank_abstract minus dense | nDCG@10 | +0.131 | [+0.072, +0.191] | 0.086 | ablation/rerank_abstract higher |
| ablation/rerank_abstract minus hybrid | Recall@10 | +0.014 | [-0.065, +0.105] | 0.124 | not distinguishable |
| ablation/rerank_abstract minus hybrid | MRR@10 | +0.083 | [-0.021, +0.192] | 0.158 | not distinguishable |
| ablation/rerank_abstract minus hybrid | nDCG@10 | +0.073 | [+0.009, +0.144] | 0.100 | ablation/rerank_abstract higher |
| ablation/rerank_abstract minus rerank | Recall@10 | -0.021 | [-0.069, +0.021] | 0.064 | not distinguishable |
| ablation/rerank_abstract minus rerank | MRR@10 | -0.019 | [-0.057, +0.009] | 0.048 | not distinguishable |
| ablation/rerank_abstract minus rerank | nDCG@10 | -0.014 | [-0.047, +0.014] | 0.044 | not distinguishable |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
ablation/rerank_abstract against rerank (BASE = "rerank" in p2/retrievers/rerank_abstract.py): it helped 1 queries, hurt 2 and left 27 unchanged.

| Query | Class | Origin | rerank RR | ablation/rerank_abstract RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| c14 | paraphrase | claude | 0.200 | 0.333 | +0.133 | helped |
| c19 | mixed | claude | 0.500 | 0.125 | -0.375 | hurt |
| h06 | paraphrase | hand | 0.333 | 0.000 | -0.333 | hurt |

RR is the reciprocal rank of the first relevant document in the top 10 (0 when none is there), the per-query value behind MRR@10; the queries at the top of each list are the ones to read.
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

Before running the ablation, I expected `rerank_abstract` to improve nDCG@10 compared with the original `rerank` system. Claude found that it was spending most of its 600-character limit reading citation information instead of the actual abstracts. The median header length was 427 characters, leaving only around 173 characters of the abstract for Claude to evaluate. There were even 10 papers where Claude never saw any of the abstract at all. My thinking was that removing this unnecessary information would give Claude more context to decide whether a paper actually answered the query, rather than relying mostly on the title or similar terminology.

For the ablation, I changed how the candidate passages were constructed. Instead of including the citation header, each passage contained the paper's title once, followed by its abstract. Everything else was kept the same, including the hybrid top 20 candidates, their ordering, the Claude model, the prompt, and the 600-character limit. Claude also verified that all 30 queries received the same candidates in the same order between the two versions. With this change, the median amount of abstract text Claude could see increased from 173 to 495 characters, which I thought would be a fairly substantial improvement.

However, the results did not support my original hypothesis. The original reranker achieved an nDCG@10 of 0.687, while `rerank_abstract` achieved 0.673, a difference of −0.014 with a 95% confidence interval of [−0.047, +0.014]. MRR@10 also decreased by 0.019, with an interval of [−0.057, +0.009], and Recall@10 decreased by 0.021, with an interval of [−0.069, +0.021]. All three intervals include zero, meaning the differences were not statistically distinguishable under our evaluation. The minimum detectable difference for nDCG@10 was 0.044, which is also larger than the observed change. So while the point estimates were slightly worse, I don't think there is enough evidence to conclude that removing the header actually hurts performance.

Looking at the individual queries was where things got more interesting. Out of the 30 queries, 16 had changes in nDCG@10, with nine improving and seven getting worse. For h06, the relevant Cyprus paper dropped from rank 3 to outside the top 10, while a non-relevant paper about the São Francisco basin moved to rank 1. For c19, both relevant papers that reached Claude dropped in ranking, one from rank 2 to 8 and the other from rank 3 to outside the top 10. On the other hand, c14 improved, with a relevant Polish paper moving from rank 6 to 3.

What I found particularly interesting was that the sentences which actually made these papers relevant were still outside the 600-character limit in both versions. For example, the important reservoir-storage finding in h06 was at character 1,070 (in the header-free version), while the relevant findings for c19 were at characters 779 and 1,012. Even the Polish paper in c14 had its deciding sentence at character 615 (in the header-free version), just outside what Claude could see. So although I gave Claude more of each abstract, I wasn't necessarily giving it the information it needed to make the correct relevance judgment. The São Francisco paper also had its mention of reservoirs move inside the visible passage, which could explain why Claude ranked it higher, although I cannot confirm that from the results alone.

There is another limitation here, which is that both versions were only run once. Since Claude's reranking is not necessarily deterministic, some changes in ranking could come from variation between runs rather than the passage formatting itself. We did not repeat the experiment enough to separate those effects.

Overall, I think this ablation showed that simply providing more information does not necessarily lead to better retrieval performance. My hypothesis was not supported, but I wouldn't interpret that as proof that the original citation header was useful either. One possible explanation is that the relevant evidence was still being truncated, even after removing the header. Additionally, for queries like c19 and c14, most of the relevant papers never reached the reranker in the first place. This means that improving how Claude reads a passage is only one part of the problem. The system also needs to retrieve the correct papers and expose the portions that actually answer the question.

If I were to continue testing this, I would be interested in whether selecting more relevant passages from each abstract, rather than simply taking the first 600 characters, would make a larger difference. I would also want to repeat the runs to better understand how much variation comes from Claude itself.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

Looking at the queries where rerank struggled, I noticed that most of the problems were not necessarily from Claude ranking the wrong papers, but from the relevant papers never making it into the candidate pool in the first place. I went through ten of the weaker queries and compared what rerank returned against the papers I had judged relevant. There were a few different patterns, especially with plain-language questions, where the terminology in the query was quite different from what the papers actually used.

| Query | What the best system returned | What was relevant | Cause | What I would try |
|---|---|---|---|---|
| c08 | The relevant evaporative-demand formulation paper at rank 1. | Nine of ten relevant papers never reached the top 20, including several SPEI/PET comparison studies. | Vocabulary mismatch and candidate generation. My question described water being pulled from the land, while the abstracts used terms like PET and evapotranspiration. | Expand the query using related scientific terminology before retrieval, or combine the original query with a technical version. |
| c09 | A relevant paper covering future drought across Europe. | Four of five relevant papers were missing, including the Iberian studies. | Geographic terminology mismatch. The query used southern Europe, while relevant papers used names like the Iberian Peninsula, Douro, and Tagus. | Expand geographic terms to include relevant countries, regions, and river basins. |
| c14 | A perspective paper about hydrological drought definitions at rank 1, with the first relevant paper at rank 5. | Eight of ten relevant papers never reached Claude. | Vocabulary mismatch and topical similarity. The system found papers about hydrological drought generally, but not necessarily papers evaluating which index to use for streamflow shortages. | Expand terms such as river flow, streamflow, SRI, and SSI, while making index evaluation or comparison more explicit. |
| c19 | A paper about SPI/SPEI behavior at different timescales, but without evidence for choosing an optimal one. | Ten of twelve relevant papers never reached the top 20. The first relevant paper was at rank 2. | On-topic but not answering the question. Many abstracts mention multiple timescales without evaluating which one is most appropriate. | Give more emphasis to terms like optimal, recommended, correlation, and selection, rather than simply matching papers that use several timescales. |
| c06 | A relevant CMIP6 drought-projection paper at rank 1. | Five of nine relevant papers were missing from the candidate pool. | Candidate coverage despite strong vocabulary overlap. The missed papers shared many query terms, so this doesn't appear to be a simple terminology problem. Similar studies may have been competing for the same ranking positions, although that hasn't been directly tested. | Test a larger or more diverse candidate pool, potentially using a union of BM25 and dense results instead of relying entirely on RRF's top 20. The interleaved BM25/dense top-20 candidate pool increased relevant-document coverage from 4/9 to 8/9. This is measured candidate coverage, not evidence that the final reranking performance would necessarily improve. |
| h10 | A relevant paper connecting drought indices with reported impacts. | Five of six relevant papers never reached the top 20, including studies using impact inventories and EM-DAT. | Vocabulary mismatch and limited candidate coverage. Relevant papers describe documented disasters and impact occurrences in several different ways. | Expand the query with drought-impact inventories, disaster records, EM-DAT, and documented impacts. |
| h06 | A Western Cape paper reporting low reservoir levels during drought, but not evaluating the relationship. | The relevant Cyprus paper was ranked third, while the Ceará paper never reached the top 20. | Topical similarity and missing evidence. The returned paper mentioned low reservoir storage, but this wasn't enough to answer how prolonged dryness affects reservoirs. The Cyprus paper's deciding sentence was also outside the visible 600 characters. | Retrieve passages containing the reservoir-storage relationship rather than only the beginning of each abstract, and improve the initial candidate coverage. |
| h05 | An Australian compound drought-heatwave study measuring event frequency and duration rather than damage. | The Portugal wildfire study, the only paper labeled relevant, never reached the top 20. | Vocabulary mismatch and partial corpus coverage. The query asks about damage, while the relevant study reports burned area. Also, no paper in the corpus fully answers the comparison against heat or drought individually. | Expand impact terminology to include burned area and other observed damages. For a broader corpus, I would also look for studies directly separating individual and compound effects. |
| h09 | A warming-level drought-exposure paper that didn't explicitly establish SSP scenarios. | Both relevant papers reached the top 20, but the first appeared at rank 3. | Ranking and constraint matching. Unlike the other cases, Claude had the relevant documents but placed papers without the required SSP evidence above them. | Make the reranker check explicitly whether the abstract establishes each required condition, especially the SSP component. |
| c11 | Relevant pine tree-ring studies appeared among the top results. | Six of sixteen relevant papers never reached the top 20. Five of the six missed relevant papers concerned tree-growth responses to drought, rather than primarily reconstructing historical drought periods. These papers were included under my broader relevance rule because they help explain how tree rings record drought, but none reached the candidate pool. Two of the ten relevant papers that did reach Claude still fell outside the final top 10. | Candidate coverage and variation in research terminology. Relevant studies use different tree-ring measurements, including ring width, density, and isotopes, to describe drought responses. I think the missed growth-response papers suggest the retrieval systems were better at finding direct drought reconstructions than studies explaining the underlying growth responses, although we haven't tested that explanation independently. c11 had both candidate-generation and ranking limitations, even though the top three results were relevant. | Expand the candidate search using tree-ring proxy terminology and evaluate whether a larger candidate pool improves coverage. |

Across these failures, the biggest pattern was candidate generation: on nine of the ten weak queries, at least one relevant paper never reached the reranker, and overall 63 of the 155 relevant query-document pairs were missing from its top-20 candidate pools. Vocabulary differences seemed particularly important for the plain-language queries, although c06 showed that relevant papers could still be missed even when they shared most of the query's terminology. I also noticed a separate ranking problem where Claude sometimes preferred papers that were generally about the same subject but didn't actually answer the specific question, which suggests that improving candidate coverage alone would not solve everything.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

Looking at the results between the shared 30 CFR corpus and my own drought corpus, the winner did not actually change. Rerank performed the best on both, achieving an MRR@10 of 0.800 on 30 CFR and 0.879 on my corpus. What I found more interesting, though, was how the other systems performed. Hybrid was actually the worst-performing system on 30 CFR, with an MRR@10 of 0.471, but moved to second place on my corpus with 0.777. All four systems had higher scores on my corpus, although I wouldn't necessarily say this means drought research is easier to search, since the queries, documents, and relevance judgments are different.

The MRR@10 values below are copied from the existing evaluation results.

| System | 30 CFR practice | Drought corpus |
|---|---:|---:|
| BM25 | 0.507 | 0.675 |
| Dense | 0.562 | 0.734 |
| Hybrid | 0.471 | 0.777 |
| Rerank | 0.800 | 0.879 |

Another difference was how much rerank improved over hybrid. On 30 CFR, the improvement was 0.329, with a 95% confidence interval of [+0.164, +0.504], which excluded zero. On my corpus, that difference decreased to 0.102, with an interval of [−0.004, +0.211]. So even though rerank still had the highest score, its advantage over hybrid was no longer statistically distinguishable. Hybrid also performed better than BM25 on my corpus, with a difference of 0.102 and an interval of [+0.024, +0.202]. This was quite different from what happened in Stage 1, especially considering how poorly the fusion approach performed there.

I think some of this difference could come from the collections themselves. The 30 CFR corpus had 2,484 relatively short legal sections, with a median length of 70 words, and many regulations repeated similar requirements across different types of mines. My corpus was smaller, with 345 scientific abstracts and a median length of 323 words. The drought papers also used quite a bit of specialized terminology, with 297 of the 345 papers containing index acronyms such as SPI, SPEI, or PDSI. The queries were different as well. The 30 CFR practice queries had a median length of 14.5 words, while the Claude-origin and hand-origin queries had medians of 10.5 and 17.5 words, respectively. All of these differences could influence which documents the systems retrieve, although I did not isolate their individual effects.

To investigate the change in hybrid's performance, we measured how many documents BM25 and dense shared in their top ten results. On the 30 CFR practice queries, they shared an average of 2.30 documents (2.40 on the 30 CFR test queries), compared with 3.07 on my drought corpus. The biggest difference was on paraphrase queries, where the average overlap increased from 0.00 to 2.60 documents. Interestingly, paraphrase queries were also where hybrid went from performing substantially below the better of its two retrieval arms, with a difference of −0.563, to slightly above it, with +0.114. The better arm here is selected separately for each query using the relevance judgments, so it is an ideal reference rather than an actual retrieval system.

This seems consistent with the possibility that hybrid benefited when BM25 and dense agreed more often about which papers were relevant. However, I don't think the overlap results prove that explanation. For identifier queries, the average overlap was almost identical between the corpora, at 2.71 and 2.70 documents, yet hybrid's performance relative to the better arm still changed. So something else must also be influencing the results. Document length, query wording, repeated legal sections, and differences in how scientific terminology appears are all possible explanations, but I did not experimentally test each of them. We did measure the overlap, and a separate Stage 1 analysis of the first relevant document's ranking showed that hybrid buried documents found by only one retrieval arm on ten of the twenty 30 CFR practice queries. That gives us evidence of a candidate-ranking problem, but not a complete explanation for the cross-corpus performance difference.

There are also limitations to how much I can conclude from these results. The shared practice evaluation only had 20 queries, while my corpus had 30, and the minimum detectable differences for MRR@10 were roughly 0.19 to 0.41 and 0.13 to 0.19, respectively. This means smaller performance differences may not be distinguishable with these sample sizes. My relevance judgments may also be incomplete, since relevant papers could exist outside the candidate searches. Seven of my queries had only one relevant paper, making their reciprocal-rank scores particularly sensitive to a single miss. Additionally, only 92 of the 155 relevant query-document pairs reached the reranker's candidate pool, meaning it could not recover the others regardless of how well it ranked the documents it received.

Overall, I think the comparison shows that reranking was consistently useful across both collections, but combining BM25 and dense retrieval did not behave the same way on each corpus. Hybrid was much more competitive on the drought papers, and the overlap measurements provide one possible reason for that. Still, with only two corpora and relatively small query sets, I wouldn't conclude that a particular corpus characteristic caused the improvement or that rerank would necessarily win on other collections. What I can say is that the same retrieval architecture behaved quite differently depending on the documents and questions it was given, which was one of the more interesting findings of this project.

---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-rerank.jsonl | rerank | 12 | 24 | 4 | 144,785 | 4,308 | 82.5 | 12,065 | 359 | 6.9 |
| traces/own-own-ablation-rerank_abstract.jsonl | rerank_abstract | 30 | 30 | 2 | 237,326 | 2,730 | 100.3 | 7,911 | 91 | 3.3 |
| traces/own-own-rerank.jsonl | rerank | 30 | 30 | 27 | 263,041 | 2,730 | 88.7 | 8,768 | 91 | 3.0 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 20 | 154,809 | 1,930 | 59.0 | 7,740 | 96 | 3.0 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 40 | 371,296 | 4,458 | 133.1 | 9,282 | 111 | 3.3 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.293 | [-0.533, -0.043] | 7,740 | 3.0 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.237 | [-0.408, -0.083] | 7,740 | 3.0 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.329 | [-0.504, -0.164] | 7,740 | 3.0 | rerank higher |
| own: bm25 minus rerank | 30 | -0.204 | [-0.329, -0.094] | 8,768 | 3.0 | rerank higher |
| own: dense minus rerank | 30 | -0.144 | [-0.274, -0.021] | 8,768 | 3.0 | rerank higher |
| own: hybrid minus rerank | 30 | -0.102 | [-0.211, +0.004] | 8,768 | 3.0 | not distinguishable |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 30 | 0.02 | 0.7 |
| traces/retrieval/own-own-dense.jsonl | dense | 30 | 0.36 | 11.9 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 30 | 0.22 | 7.4 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.03 | 1.5 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.51 | 25.7 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.63 | 31.7 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.07 | 1.7 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 1.02 | 25.4 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 1.24 | 31.1 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

Write the five things here.

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
_No repeated runs or answers files yet (598E: `p2 run ... --repeat 3` and `p2 answer ... --repeat 3`)._
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

598E: write the repeats result here.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

598E: write the claim and its outcome here.
