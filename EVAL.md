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

All three systems used 300-word chunks with 50 words of overlap and scored documents using their highest-scoring chunk. I selected the approaches based on Labs 12 and 13, while Claude Code adapted and implemented them and the evaluation pipeline for P2.

For dense, I kept bge-small-en-v1.5 with normalized embeddings, cosine similarity, and no query prefix, scoring document chunks rather than whole articles as in Lab 12. My Lab 13 results also influenced this choice, since rrf_bge achieved an MRR of 0.83 compared with 0.76 for rrf_potion.

For hybrid, I used equal-weight reciprocal rank fusion of BM25 and dense, with k = 60 and each document receiving the sum of its 1 / (60 + rank) contributions. Like Lab 13, it combines the complete document rankings, but P2 also supports chunk-level fusion when retrieving passages for answers.

For rerank, Claude Sonnet reorders hybrid's top 20 candidates using passages limited to 600 characters, while everything below those candidates keeps its original hybrid ranking. Claude Code adapted the prompt from help-center content to a document collection, restricted the returned ranking positions to 1–20, supported chunk-based answering, and saved responses and traces through p2.claude.call.

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.592 | 0.471 | 0.443 |
| rerank | 0.758 | 0.800 | 0.761 |
| rerank10 | 0.592 | 0.688 | 0.598 |

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
| rerank10 | Recall@10 | 0.500 | 0.405 | 0.917 |
| rerank10 | MRR@10 | 0.536 | 0.571 | 1.000 |
| rerank10 | nDCG@10 | 0.466 | 0.440 | 0.936 |
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
| rerank10 minus bm25 | Recall@10 | -0.033 | [-0.250, +0.192] | 0.324 | not distinguishable |
| rerank10 minus bm25 | MRR@10 | +0.180 | [-0.083, +0.439] | 0.377 | not distinguishable |
| rerank10 minus bm25 | nDCG@10 | +0.080 | [-0.160, +0.314] | 0.344 | not distinguishable |
| rerank10 minus dense | Recall@10 | +0.033 | [-0.125, +0.192] | 0.231 | not distinguishable |
| rerank10 minus dense | MRR@10 | +0.125 | [-0.071, +0.321] | 0.284 | not distinguishable |
| rerank10 minus dense | nDCG@10 | +0.118 | [-0.056, +0.284] | 0.246 | not distinguishable |
| rerank10 minus hybrid | Recall@10 | +0.000 | [+0.000, +0.000] | - | identical on every query |
| rerank10 minus hybrid | MRR@10 | +0.217 | [+0.044, +0.399] | 0.259 | rerank10 higher |
| rerank10 minus hybrid | nDCG@10 | +0.155 | [+0.045, +0.272] | 0.164 | rerank10 higher |
| rerank10 minus rerank | Recall@10 | -0.167 | [-0.292, -0.058] | 0.166 | rerank higher |
| rerank10 minus rerank | MRR@10 | -0.113 | [-0.250, +0.000] | 0.179 | not distinguishable |
| rerank10 minus rerank | nDCG@10 | -0.163 | [-0.288, -0.058] | 0.169 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time. Two systems that score the same on every query have no interval to speak of, so their MDD is shown as -.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

On the 20 Stage 1 practice queries, rerank came out first with an MRR@10 of 0.800. Dense followed at 0.562, then BM25 at 0.507, with hybrid last at 0.471. What stood out to me was that rerank's improvement was not just a higher point estimate. Its differences against all three other systems had paired 95% confidence intervals that excluded zero, which gives us evidence that the improvement was distinguishable on this particular evaluation.

Specifically, rerank improved MRR@10 over hybrid by 0.329, with an interval of [+0.164, +0.504]. Its improvement over dense was 0.237 [+0.083, +0.408], while the difference against BM25 was 0.293 [+0.043, +0.533]. All three intervals remained positive. I couldn't draw the same conclusion about the differences between BM25, dense, and hybrid. Dense was ahead of BM25 by 0.055, with an interval of [−0.225, +0.343], while hybrid was below BM25 by 0.037 and below dense by 0.092. Both of those intervals also included zero, so there wasn't enough evidence to distinguish their performance from each other.

The number of queries ended up mattering quite a bit when I started interpreting these differences. The minimum detectable differences ranged from approximately 0.19 to 0.41 across the comparisons among the four main retrieval systems, which is quite large considering the MRR differences between BM25, dense, and hybrid. For example, dense's advantage of 0.055 over BM25 was much smaller than the MDD of 0.412 for that comparison. That doesn't mean BM25 and dense perform equally well. With only 20 queries, the evaluation wasn't sensitive enough to reliably detect a difference that small. It's easy to arrange the four systems by their scores and assume that each position tells us something meaningful. The confidence intervals made me a little more cautious about doing that.

The results were also quite different depending on the query class. BM25 performed the best on identifier queries, achieving an MRR@10 of 0.810, while dense only reached 0.333. For paraphrase queries, the situation was almost the opposite. BM25 didn't retrieve a relevant answer in the top ten for any of the seven queries, giving it an MRR@10 of 0.000, while dense and rerank both achieved 0.714. On mixed queries, hybrid performed the best among the three initial retrieval approaches at 0.792, while rerank achieved 1.000. What caught my attention was how differently the systems performed depending on how the question was worded, even though they were searching the same documents.

This lines up with Lecture 12's point that a retrieval approach can perform well for one type of query and struggle with another. BM25 benefited from exact terminology, whereas dense retrieval seemed better at handling questions that described a concept without using its technical name. I would still be cautious about generalizing the class-level results, considering there were only seven identifier queries, seven paraphrase queries, and six mixed queries. The pattern is there, but these sample sizes are too small for me to assume it would hold across a larger collection of questions.

Lecture 13 discussed how fusion can help when the retrieval systems find different useful documents, but it can also hurt when one system is already performing well. The other limitation was with reranking itself. If a relevant document never reaches the candidate pool, the reranker cannot recover it. My results supported the reranking part of that approach, since rerank was distinguishably better than each of the other three systems. The fusion results were less convincing, though. Hybrid had the lowest overall MRR@10, and its differences from BM25 and dense were not statistically distinguishable. The individual queries showed another problem. On ten of the twenty practice queries, hybrid placed the first relevant document below where the better of its two retrieval arms had ranked it. This was different from my own Lab 13 results, where rrf_bge achieved 0.83 compared with BM25's 0.78. That Lab 13 comparison was performed on the help-center corpus, rather than the 30 CFR practice collection used for this evaluation.

Combining two retrieval systems, then, isn't automatically an improvement. For example, on p03 and p06, BM25 had retrieved the relevant documents, but hybrid pushed them outside the top 20 candidates given to Claude. At that point, rerank couldn't recover them regardless of how well it understood the question. So while the results support the usefulness of reranking, they leave open whether the particular fusion method I used was actually the best way to construct its candidate pool. I carried that question into the evaluation of my own corpus.

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

I chose rerank for the cited-answer stage, even though it required 24 Claude calls instead of the 12 that hybrid would have needed, because rerank had performed the best on the 30 CFR practice queries. This also followed what I saw in Lab 13, where answering from rrf_bge verified 8 of 8 answers compared with 7 of 8 from BGE alone. I left prompts/answer.txt unchanged, so there wasn't a prompt modification to compare against. The results were still fairly good: all 8 answerable questions verified [0.676, 1.000], none were incorrectly declined, all 4 unanswerable questions were declined [0.510, 1.000], and all 13 quotations appeared in their cited chunks. Those results look strong at first, but we're still working with only eight answerable questions and four unanswerable ones. The confidence intervals reflect that uncertainty.

For the three-answer citation audit, I selected a01, a02, and a07 and checked whether the quoted evidence actually supported each claim. I reviewed the claims, their quoted evidence, and the full cited chunks.

For a01, both claims are supported. The cited §50.10 passage explicitly requires MSHA notification immediately and within 15 minutes once the operator knows or should know of a qualifying accident. Subsection (a) identifies a death at the mine as one of those accidents, so the quoted evidence supports both the deadline and the type of accident.

For a02, both claims are also supported. Section 75.403 requires at least 80% incombustible content where rock dust is required. When methane is present in a ventilating current, the minimum increases by 0.4 percentage points for every 0.1% methane. The answer correctly identifies the minimum for the no-methane situation.

For a07, both claims are supported. Sections 56.9300(b) and 57.9300(b) specify that berms or guardrails must be at least mid-axle height of the largest self-propelled mobile equipment that usually travels the roadway. The quotations support that requirement in both sections. The full chunks also contain conditions and exceptions concerning when berms are required, but those do not contradict the specific height claims.

All six claims I checked across the three audited answers were directly supported by their cited chunks.

The automated verifier confirmed that all 13 quotations existed in their cited chunks. My manual audit went further by checking whether the quoted passages actually supported the claims beside them. For these three answers, the support was direct, although the full regulatory context was still important for avoiding overly broad interpretations.

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

I originally started with the USGS corpus, but I wanted something that was more connected to the work I had done at NCAR. At NCAR, much of my work involved the Palmer Drought Severity Index (PDSI), Standardized Precipitation Index (SPI), and Standardized Precipitation Evapotranspiration Index (SPEI), so building a collection around those indices felt like a natural direction. They all measure drought, but not in quite the same way. SPI focuses on precipitation, SPEI standardizes the water balance between precipitation and potential evapotranspiration, while PDSI uses a modeled soil-water balance. The corpus ended up containing 345 scientific paper abstracts, collected through OpenAlex searches of titles and abstracts using scripts/fetch_drought_corpus.py. Altogether, the collection is approximately 0.9 MB, with 106,262 words and an estimated 148,766 tokens. Each document includes the paper's title, abstract, and a citation header with information such as the authors, journal, publication year, DOI, and license. The abstracts also lost some of their original formatting and section labels because they were reconstructed from OpenAlex's word index.

For licensing, I used the brief's allowed category of CC0, CC BY, and CC BY-SA text, including open-access articles published under those licenses. I wasn't comfortable relying only on OpenAlex's licensing information, though. In our initial sample, two of the eight papers had incorrect license labels. Instead, I required the license to be confirmed through the publisher-deposited Crossref metadata before including a paper. Of the final 345 documents, 299 were licensed under CC BY 4.0 and 46 under CC BY 3.0. I also ran p2 license --online, which successfully checked all 345 papers against Crossref with no flags or failures.

There were a few documents I wasn't entirely comfortable including. One was a Springer paper (10-1007-s11269-018-2090-6) whose Crossref record listed CC BY only in the context of text and data mining, while the publisher's page presented a bot check that prevented further confirmation. Claude removed the Springer paper during the licensing review, and I agreed with leaving it out rather than include something whose redistribution permissions we couldn't confidently verify. Three IEEE papers were also removed after p2 license flagged the "Published in IEEE ..." text that our fetch script had added to their citation headers. Their Crossref licenses were CC BY, so the warning came from the generated metadata rather than the license records themselves. I'd rather leave out a few potentially useful papers than publish a collection containing documents whose redistribution permissions we couldn't confidently verify.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

For my gold set, I used 30 queries, with 20 labeled claude (c01 through c20) and 10 labeled hand (h01 through h10). I divided them evenly into three classes: 10 identifier, 10 paraphrase, and 10 mixed queries. Keeping the three classes balanced meant that I could test different retrieval problems without having one query style dominate the evaluation. Identifier queries use specific terminology like SPEI, GRACE, or CMIP6 (Coupled Model Intercomparison Project Phase 6, a coordinated set of climate-model experiments used to study climate change), while paraphrase queries ask about similar concepts in more ordinary language. The mixed queries fall somewhere between the two. This also follows the same classification used in the shared corpus, making it easier to compare how the systems behave across different types of questions.

My general relevance rule was that a paper needed to provide substantive evidence addressing the actual information being requested, rather than simply mentioning the same terminology. When a query specified an index, method, location, or projection period, I generally required the abstract to support that requirement. For broader explanatory questions, a paper could still count if it meaningfully addressed part of what was being asked. I also counted negative findings when they directly addressed the query, and based the judgments on the information available in the indexed abstracts rather than outside knowledge.

To find candidates, I started by combining the top ten results from BM25, dense, and hybrid for each query. That original candidate pool had a weakness, though. A relevant paper could be missed entirely if none of the systems placed it near the top, which became especially noticeable with paraphrase queries. Starting with c08, Claude began running keyword searches alongside the pooled results from the three retrieval systems. We later found that c01 through c07 hadn't received that additional search, so Claude went back and checked those queries as well. I reviewed the new candidates and made the relevance judgments, with the audit adding six across c02, c04, c06, c08, and c12. In the final gold set, 64 of the 155 relevant query-document pairs, or approximately 41%, were outside the top ten of all three pooled systems: BM25, dense, and hybrid.

I used binary relevance judgments, with 1 indicating a relevant document, for a total of 155 positive query-document pairs. I didn't read all 345 documents in full or independently read every candidate's complete abstract. Instead, I reviewed the abstract excerpts relevant to each question, examined full abstracts when a decision needed more context, and revisited several judgments when the initial excerpts were incomplete or ambiguous. One limitation is that this doesn't guarantee every relevant paper in the corpus was found. There were also borderline cases, such as h05, where the selected paper provided meaningful evidence about compound heat and drought damage but didn't fully answer the comparison against either condition alone. I still labeled it relevant under my broader rule, although the binary labels don't capture that distinction. I think the resulting judgments are useful for comparing the systems, but I wouldn't consider the gold set completely exhaustive.

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

Rerank finished first on my drought corpus with an MRR@10 of 0.879. Hybrid was next at 0.777, followed by dense at 0.734 and BM25 at 0.675. This was somewhat consistent with what I originally expected in DECISIONS.md, since I predicted that rerank would perform the best. I had also predicted that hybrid would finish last. That part turned out to be wrong. In fact, hybrid finished second. Hybrid was actually the surprise here, especially since it had performed worse than both of its retrieval arms during Stage 1.

The paired confidence intervals gave me a somewhat different picture than simply comparing the scores. Rerank outperformed BM25 by 0.204 in MRR@10, with a 95% confidence interval of [+0.094, +0.329], and dense by 0.144, with an interval of [+0.021, +0.274]. Both intervals exclude zero, so there is evidence that rerank performed better than those two systems on this evaluation. Hybrid was also distinguishably better than BM25 in MRR@10, with a difference of +0.102 and a 95% confidence interval of [+0.024, +0.202]. Rerank was also ahead of hybrid by 0.102, but its confidence interval [−0.004, +0.211] included zero, so that advantage wasn't statistically distinguishable. So while rerank had the higher point estimate, I cannot confidently conclude that it was better than hybrid based on MRR@10 alone.

The remaining comparisons were also not distinguishable. Hybrid was ahead of dense by 0.043, while dense was ahead of BM25 by 0.059, but neither difference was large enough relative to the uncertainty in the estimates. The minimum detectable differences were approximately 0.157 for rerank versus hybrid, 0.145 for hybrid versus dense, and 0.192 for dense versus BM25. With only 30 queries, I don't think a higher MRR@10 by itself is enough to say that one system performs better. The differences may be real, but this evaluation doesn't provide enough evidence to separate those systems reliably.

The other evaluation metrics made the results a little less straightforward. Rerank improved nDCG@10 over hybrid by 0.087, with a confidence interval of [+0.025, +0.155], which excludes zero. Recall@10 told a different story, with an improvement of only 0.035 that wasn't statistically distinguishable. This suggests rerank was doing more to improve where relevant papers appeared in the ranking than to substantially increase how many reached the top ten.

I also compared the results between the hand and claude query groups. MRR@10 and nDCG@10 were lower for all four systems on the hand-origin queries, although none of those group differences were statistically distinguishable. Rerank was the one exception for Recall@10, where it actually performed slightly better on the hand-origin queries, at 0.678 compared with 0.655 for the Claude-origin queries. For rerank, MRR@10 decreased from 0.935 on the 20 Claude-origin queries to 0.767 on the 10 hand-origin queries. The hand queries also had less content-word overlap with their best relevant documents, averaging 0.50 compared with 0.72 for the Claude queries. The way the questions were written might have made them harder to retrieve, but these results alone aren't enough for me to say that was the cause.

Unlike the paired system comparisons, the hand and Claude groups contained different queries, so their confidence intervals were calculated by resampling each group rather than pairing the same questions. There were also only ten hand queries, making the estimates relatively uncertain. For the BM25-versus-dense comparison, the difference between the two query-origin groups was only +0.023 in MRR@10, calculated as Claude minus hand, with a confidence interval of [−0.227, +0.305]. Since this includes zero, there isn't enough evidence to conclude that the two retrieval approaches behaved differently depending on query origin.

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

During the investigation, Claude Code found that the citation headers were occupying most of the reranker's 600-character limit. This left very little room for the actual abstract, which was supposed to provide the evidence for determining relevance. The median header length was 427 characters, leaving only around 173 characters of the abstract for Claude to evaluate. There were even 10 papers where Claude never saw any of the abstract at all.

For the ablation, I changed how the candidate passages were constructed. Instead of including the citation header, each passage contained the paper's title once, followed by its abstract. Everything else was kept the same, including the hybrid top 20 candidates, their ordering, the Claude model, the prompt, and the 600-character limit. Before running the ablation, Claude Code checked all 30 queries and confirmed that both versions received the same 20 candidates in the same order. This meant the passage content was the only intended difference between them. With this change, the median amount of abstract text Claude could see increased from 173 to 495 characters, which I thought would be a fairly substantial improvement.

The results didn't really back up that prediction. The original reranker achieved an nDCG@10 of 0.687, while rerank_abstract achieved 0.673, a difference of −0.014 with a 95% confidence interval of [−0.047, +0.014]. MRR@10 also decreased by 0.019, with an interval of [−0.057, +0.009], and Recall@10 decreased by 0.021, with an interval of [−0.069, +0.021]. All three intervals include zero, meaning the differences were not statistically distinguishable under our evaluation. The minimum detectable difference for nDCG@10 was 0.044, which is also larger than the observed change. So while the point estimates were slightly worse, I don't think there is enough evidence to conclude that removing the header actually hurts performance.

The individual queries gave me a few clues about what might have happened. By nDCG@10, 16 of the 30 queries changed, with nine improving and seven getting worse. The generated table above measures reciprocal rank instead, which only changes when the position of the first relevant document changes. For h06, the relevant Cyprus paper dropped from rank 3 to outside the top 10, while a non-relevant paper about the São Francisco basin moved to rank 1. For c19, both relevant papers that reached Claude dropped in ranking, one from rank 2 to 8 and the other from rank 3 to outside the top 10. c14 was an exception, with a relevant Polish paper improving from rank 6 to rank 3.

What I hadn't accounted for was where the important evidence appeared in each document. In the header-free passages, the relevant Cyprus finding began at character 1,070, while the c19 findings appeared at characters 779 and 1,012. Even the Polish paper's deciding sentence began at character 615 in that version. All of these were still outside the 600-character limit, and the original passages placed them even farther back. Claude was technically receiving more of each abstract, but those extra characters still weren't reaching the information that mattered for the relevance judgments. The São Francisco paper also had its mention of reservoirs move inside the visible passage, which could explain why Claude ranked it higher, although I cannot confirm that from the results alone.

There is another limitation here, which is that both versions were only run once. Claude can also produce different rankings across runs, so I can't completely rule out normal run-to-run variation as another explanation. We did not repeat the experiment enough to separate those effects.

The ablation left me with a fairly simple conclusion: giving Claude more abstract text, by itself, didn't improve the rankings in this experiment. My hypothesis was not supported, but I wouldn't interpret that as proof that the original citation header was useful either. One possible explanation is that the relevant evidence was still being truncated, even after removing the header.

If I were to continue testing this, I would be interested in whether selecting more relevant passages from each abstract, rather than simply taking the first 600 characters, would make a larger difference. I would also want to repeat the runs to better understand how much variation comes from Claude itself.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

Most of the weaker rerank queries had already run into problems before Claude could evaluate the papers. The relevant documents simply weren't making it into the candidate pool. I went through ten of the weaker queries and compared what rerank returned against the papers I had judged relevant. There were a few different patterns, especially with plain-language questions, where the terminology in the query was quite different from what the papers actually used.

I chose these ten queries because they showed different problems with the retrieval system, whether that was relevant papers missing from the candidate pool or papers being ranked highly without actually answering the question.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|
| c08 | The relevant evaporative-demand formulation paper at rank 1. | Nine of ten relevant papers never reached the top 20, including several SPEI/PET comparison studies. | Vocabulary mismatch and candidate generation. The query described water being pulled from the land, while the relevant papers used terminology like PET and evapotranspiration. Potential evapotranspiration (PET) estimates how much water could leave the land through evaporation and plant transpiration when sufficient water is available. | Expand the query using related scientific terminology before retrieval, or combine the original query with a technical version. |
| c09 | A relevant paper covering future drought across Europe. | Four of five relevant papers were missing, including the Iberian studies. | Geographic terminology mismatch. The query used southern Europe, while relevant papers used names like the Iberian Peninsula, Douro, and Tagus. | Expand geographic terms to include relevant countries, regions, and river basins. |
| c14 | A perspective paper about hydrological drought definitions at rank 1, with the first relevant paper at rank 5. | Eight of ten relevant papers never reached Claude. | Vocabulary mismatch and topical similarity. The system found papers about hydrological drought generally, but not necessarily papers evaluating which index to use for streamflow shortages. | Expand terms such as river flow, streamflow, SRI, and SSI, while making index evaluation or comparison more explicit. |
| h10 | A relevant paper connecting drought indices with reported impacts. | Five of six relevant papers never reached the top 20, including studies using impact inventories and EM-DAT. | Vocabulary mismatch and limited candidate coverage. Relevant papers describe documented disasters and impact occurrences in several different ways. | Expand the query with drought-impact inventories, disaster records, EM-DAT, and documented impacts. |
| h05 | An Australian compound drought-heatwave study measuring event frequency and duration rather than damage. | The Portugal wildfire study, the only paper labeled relevant, never reached the top 20. | Vocabulary mismatch and partial corpus coverage. The query asks about damage, while the relevant study reports burned area. Also, no paper in the corpus fully answers the comparison against heat or drought individually. | Expand impact terminology to include burned area and other observed damages. For a broader corpus, I would also look for studies directly separating individual and compound effects. |
| c06 | A relevant CMIP6 drought-projection paper at rank 1. | Five of nine relevant papers were missing from the candidate pool. | Candidate coverage despite strong vocabulary overlap. The missed papers shared many query terms, so this doesn't appear to be a simple terminology problem. Similar studies may have been competing for the same ranking positions, although that hasn't been directly tested. | Test a larger or more diverse candidate pool, potentially using a union of BM25 and dense results instead of relying entirely on RRF's top 20. The interleaved BM25 and dense candidate pool increased c06's coverage from 4 of 9 to 8 of 9 relevant papers. That's a fairly substantial difference for one query, although we only measured which documents reached the candidate pool, not whether Claude would actually rank them better. |
| c11 | Relevant pine tree-ring studies appeared among the top results. | Six of sixteen relevant papers never reached the top 20. Five of the six relevant papers missed for c11 were about tree-growth responses to drought rather than directly reconstructing historical drought periods. All five came from the independent keyword search. These papers were included under my broader relevance rule because they help explain how tree rings record drought, but none reached the candidate pool. Another two relevant papers reached Claude's candidate pool but still ended up outside the final top ten, so this wasn't entirely a candidate-generation problem either. | Candidate coverage and variation in research terminology. Relevant studies use different tree-ring measurements, including ring width, density, and isotopes, to describe drought responses. I think the missed growth-response papers suggest the retrieval systems were better at finding direct drought reconstructions than studies explaining the underlying growth responses, although we haven't tested that explanation independently. c11 had both candidate-generation and ranking limitations, even though the top three results were relevant. | Expand the candidate search using tree-ring proxy terminology and evaluate whether a larger candidate pool improves coverage. |
| c19 | A paper about SPI/SPEI behavior at different timescales, but without evidence for choosing an optimal one. | Ten of twelve relevant papers never reached the top 20. The first relevant paper was at rank 2. | On-topic but not answering the question. Many abstracts mention multiple timescales without evaluating which one is most appropriate. | Give more emphasis to terms like optimal, recommended, correlation, and selection, rather than simply matching papers that use several timescales. |
| h06 | A Western Cape paper reporting low reservoir levels during drought, but not evaluating the relationship. | The relevant Cyprus paper was ranked third, while the Ceará paper never reached the top 20. | Topical similarity and missing evidence. The returned paper mentioned low reservoir storage, but this wasn't enough to answer how prolonged dryness affects reservoirs. The Cyprus paper's deciding sentence was also outside the visible 600 characters. | Retrieve passages containing the reservoir-storage relationship rather than only the beginning of each abstract, and improve the initial candidate coverage. |
| h09 | A warming-level drought-exposure paper that didn't explicitly establish SSP (Shared Socioeconomic Pathway, describing a possible future trajectory of population and socioeconomic development) scenarios. | Both relevant papers reached the top 20, but the first appeared at rank 3. | Ranking and constraint matching. Unlike the other cases, Claude had the relevant documents but placed papers without the required SSP evidence above them. | Make the reranker check explicitly whether the abstract establishes each required condition, especially the SSP component. |

I ended up grouping these failures into four main categories: vocabulary or geographic mismatches, problems with candidate generation, papers that were on the right topic but didn't actually answer the question, and ranking errors where the system failed to recognize specific requirements. Some of these problems overlap, but I think separating them helps explain where the retrieval pipeline was struggling.

I kept c11 in the analysis even though its first three results were relevant, because six of its sixteen relevant papers never reached the reranker. So the problem wasn't finding an initial relevant answer, but retrieving enough of the relevant literature.

I also went back to h05 because its top-ranked Australian paper could initially look relevant. It discusses compound heat and drought impacts, but the statement about greater damage is background information rather than something the study actually tests. Its reported findings concern the frequency and duration of compound events, not a comparison of their damage against heat or drought individually. Because of that, I kept the paper excluded under my original relevance rule. The Portugal wildfire paper remains a partial match, since it investigates damage associated with compound conditions without completely answering the comparison. I think this is more of a limitation of binary relevance labels than evidence that the Australian paper was incorrectly excluded.

I also revisited the compound drought-heatwave paper (10-1088-1748-9326-adad01) from h09, but kept it excluded because it measured severity-weighted population exposure rather than reporting how many people would be exposed specifically to severe drought. Although the topics are closely related, I don't think those two measurements answer the same question.

For nine of the ten weaker queries I examined, at least one relevant paper never made it into Claude's candidate pool. The plain-language questions seemed more affected by differences in terminology. c06 was an interesting exception, since its missed papers still shared most of the words used in the query. There was another issue with ranking itself. Claude sometimes placed a paper first because it was generally about the right subject, even when it didn't answer the specific question. Improving candidate coverage alone wouldn't fix that.

For the fixes involving candidate generation, I would first compare how many relevant papers actually reached hybrid's top 20 before and after the change. Across the entire evaluation, only 92 of 155 relevant query-document pairs reached that pool. However, I think the individual queries matter just as much. For example, c08 only had 1 of 10 relevant papers available, c14 had 2 of 10, and c06 had 4 of 9. I would want those numbers to increase without losing relevant documents on other queries. The interleaving experiment already showed why that matters, since it improved c06 from 4 of 9 to 8 of 9, but actually reduced c08 from 1 of 10 to zero. For problems involving ranking, such as c19, h06, and h09, I would compare the first relevant document's rank and nDCG@10 after making the changes. Ideally, I would also repeat the runs to see whether any improvement was consistent rather than just variation between Claude calls.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

Rerank remained the top system on both corpora, but hybrid behaved differently. It was last on 30 CFR and second on my drought corpus. All four systems achieved higher MRR@10 on my corpus, although the documents, queries, and relevance judgments were different, so I wouldn't interpret that as evidence that drought research was easier to search.

The MRR@10 values below are copied from the existing evaluation results.

| System | 30 CFR practice | Drought corpus |
|---|---:|---:|
| BM25 | 0.507 | 0.675 |
| Dense | 0.562 | 0.734 |
| Hybrid | 0.471 | 0.777 |
| Rerank | 0.800 | 0.879 |

Rerank's MRR@10 advantage over hybrid decreased from 0.329 [+0.164, +0.504] on 30 CFR to 0.102 [−0.004, +0.211] on my corpus. The first interval excluded zero, while the second included it, so the advantage was only statistically distinguishable on 30 CFR.

I think some of this difference could come from the collections themselves. The 30 CFR corpus had 2,484 relatively short legal sections, with a median length of 70 words, and many regulations repeated similar requirements across different types of mines. My corpus was smaller, with 345 scientific abstracts and a median length of 323 words. The drought papers also used quite a bit of specialized terminology. Of the 345 papers, 286 contained SPI, SPEI, or PDSI somewhere in their document text, including variants such as scPDSI and SPEI-3. The queries were also different in length. The 30 CFR practice queries had a median of 14.5 words, compared with 10.5 for the Claude-origin queries and 17.5 for the hand-origin ones. All of these differences could influence which documents the systems retrieve, although I did not isolate their individual effects.

To investigate the change in hybrid's performance, we measured how many documents BM25 and dense shared in their top ten results. On the 30 CFR practice queries, they shared an average of 2.30 documents, compared with 3.07 on my drought corpus. The 30 CFR test queries showed a similar result, with an average of 2.40 shared documents compared with 2.30 on the practice queries. The biggest difference was on paraphrase queries, where the average overlap increased from 0.00 to 2.60 documents. In that class, hybrid's average MRR@10 difference from the better retrieval arm on each query shifted from −0.563 on 30 CFR practice to +0.114 on my drought corpus. The better arm here is selected separately for each query using the relevance judgments, so it is an ideal reference rather than an actual retrieval system.

This seems consistent with the possibility that hybrid benefited when BM25 and dense agreed more often about which papers were relevant. I wouldn't treat the overlap measurements as a complete explanation for that change, though. For identifier queries, the average overlap was almost identical between the corpora, at 2.71 and 2.70 documents, yet hybrid's performance relative to the better arm still changed. So something else must also be influencing the results. Document length, query wording, repeated legal sections, and differences in how scientific terminology appears are all possible explanations, but I did not experimentally test each of them. A separate analysis from Stage 1 examined where the first relevant document appeared in each ranking. On ten of the twenty practice queries, hybrid pushed down papers that one of its retrieval arms had already found. That suggests a candidate-ranking problem, although it doesn't fully explain why hybrid performed differently across the two corpora.

There are also limitations to how much I can conclude from these results. The shared practice evaluation only had 20 queries, while my corpus had 30, and the minimum detectable differences for MRR@10 among the four main retrieval systems were roughly 0.19 to 0.41 and 0.13 to 0.19, respectively. This means smaller performance differences may not be distinguishable with these sample sizes. My relevance judgments may also be incomplete, since relevant papers could exist outside the candidate searches. Seven queries had only one relevant paper, meaning a single missed result could have a fairly large effect on their reciprocal-rank scores. Candidate coverage was another limitation, which I discussed in more detail in Section 6.

Reranking was useful on both collections. Fusion, though, behaved quite differently depending on which corpus the systems were searching. Hybrid was much more competitive on the drought papers, and the overlap measurements provide one possible reason for that. Two corpora and relatively small query sets aren't enough to identify exactly what caused those differences, much less predict whether rerank would win on other collections. What I can say is that the same retrieval architecture behaved quite differently depending on the documents and questions it was given, which was one of the more interesting findings of this project.

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
| traces/shared-practice-rerank10.jsonl | rerank10 | 20 | 20 | 2 | 124,213 | 1,637 | 64.2 | 6,211 | 82 | 3.2 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 40 | 371,296 | 4,458 | 133.1 | 9,282 | 111 | 3.3 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.293 | [-0.533, -0.043] | 7,740 | 3.0 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.237 | [-0.408, -0.083] | 7,740 | 3.0 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.329 | [-0.504, -0.164] | 7,740 | 3.0 | rerank higher |
| shared practice: bm25 minus rerank10 | 20 | -0.180 | [-0.439, +0.083] | 6,211 | 3.2 | not distinguishable |
| shared practice: dense minus rerank10 | 20 | -0.125 | [-0.321, +0.071] | 6,211 | 3.2 | not distinguishable |
| shared practice: hybrid minus rerank10 | 20 | -0.217 | [-0.399, -0.044] | 6,211 | 3.2 | rerank10 higher |
| shared practice: rerank10 minus rerank | 20 | -0.113 | [-0.250, +0.000] | 1,530 | -0.3 | not distinguishable |
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

I picked Stretch Option 3, Cost and Latency, because I wanted to understand what we could save by having Claude rerank ten papers instead of twenty, and how much retrieval quality we would give up in return. For this experiment, Claude implemented rerank10 in p2/retrievers/rerank10.py, which works the same way as the original reranker but only considers hybrid's top 10 candidates instead of the top 20. Everything else stayed the same, including the Claude model, prompt, and 600-character passage limit. I evaluated it on the 20 shared practice queries, with the results saved in runs/shared/rerank10.practice.trec and the call details recorded in traces/shared-practice-rerank10.jsonl.

The stretch-cost table showed a reduction in token usage, just not the 50% I might have expected from cutting the candidate count in half. The original reranker used an average of 7,740 input tokens per query, while rerank10 used 6,211, saving approximately 1,530 tokens or 20%. This makes sense considering that part of each prompt stays the same regardless of how many candidates are included. The smaller candidate list didn't actually improve latency. The original system averaged around 3.0 seconds per query, compared with 3.2 seconds for rerank10. I also wouldn't put too much weight on the difference between 3.0 and 3.2 seconds, since the original rerank timing came from an earlier run while rerank10 was measured using fresh calls. So the actual benefit was lower token usage, rather than faster responses.

The reduction in retrieval quality was more noticeable. MRR@10 decreased from 0.800 to 0.688, a difference of −0.113 with a 95% confidence interval of [−0.250, +0.000]. Since the interval includes zero at its upper endpoint, the difference wasn't statistically distinguishable, although it certainly doesn't provide evidence of an improvement. The quality loss was clearer in the other metrics. nDCG@10 fell from 0.761 to 0.598, a difference of −0.163 [−0.288, −0.058], while Recall@10 dropped from 0.758 to 0.592, a difference of −0.167 [−0.292, −0.058]. Both intervals exclude zero, meaning the original 20-candidate reranker performed distinguishably better on these two metrics. rerank10 still outperformed hybrid on MRR@10 by 0.217 [+0.044, +0.399], so the smaller reranker wasn't without value.

When I looked at the individual queries, three became worse and none improved. For p08, the first relevant document was originally at position 18 in hybrid's ranking, which meant rerank10 never even had the opportunity to consider it. This also helps explain why rerank10 had exactly the same Recall@10 as hybrid. Since it only rearranges the first ten candidates, it cannot introduce any additional relevant documents into those ten positions. For p01 and p05, however, the relevant documents were already within the first ten and still ended up being ranked lower. I'm not entirely sure whether that happened because Claude was given fewer documents for comparison or because of normal variation between runs, since each version was only evaluated once.

I wouldn't use rerank10 as the default for this project. Saving around 20% of the input tokens is useful, but here it came with distinguishably worse nDCG@10 and Recall@10 without any measured improvement in response time. I could see using rerank10 in an application where token cost is a bigger concern and finding one useful document matters more than retrieving several relevant ones. Even then, the MRR confidence interval is too wide to conclude that its top-result quality is effectively the same.

If I continued this experiment, I would try selecting ten candidates from a more diverse combination of BM25 and dense retrieval, rather than simply taking hybrid's first ten. The idea would be to preserve the lower token cost while making sure relevant documents that appear farther down one retrieval system's rankings still have a chance to reach Claude. I would compare the new variant against rerank10 using the same query set and token budget. If it substantially improved nDCG@10 and Recall@10 while keeping input tokens close to 6,211 per query, that would suggest candidate selection is a better place to optimize than simply reducing the number of documents.

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
