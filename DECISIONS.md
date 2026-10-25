# Decision log

Your methods section, in your own words.
About one to two pages in total.

Answer these as you go, not the night before it is due.
Each answer is easier to write while the decision is still fresh, and prompt 1 only works if you write it before you see your own-corpus numbers.
Specifics beat polish: a short, honest answer with a number in it is worth more than a long vague one.

Each prompt ends with a marker line.
Replace that line with your answer.
`uv run p2 check` reports a marker as unfinished work, and `uv run p2 check --final` fails while any marker is left, so a finished log is part of being done.

Please do not let the agent write these for you.
These answers are about what you chose and what you knew, and the agent cannot know that.
Prompt 3 in particular only works in your own words.

---

## 1. Why this corpus, and what you expected

Why did you pick the corpus you used in stage 2, and why does it belong to a field or a question you care about?
Then say what you expected before you measured anything: which of `bm25`, `dense`, `hybrid` and `rerank` do you think will win on it, and which will do worst, and why?

Commit this answer before your first `uv run p2 score` on the own corpus.
Git history then shows that the expectation came first, which is what lets it be wrong in a way that teaches you something.
If you were surprised later, say so in prompt 4 or in EVAL.md; do not come back and rewrite this one.

I originally started with the USGS corpus, but I wanted to work with something I actually had experience with rather than just using one of the fallback options. During my time at NCAR, I worked quite a bit with drought indices like PDSI, SPI, and SPEI, including reimplementing PDSI's water balance calculations and working with climate model data from CESM. One thing I found interesting throughout that work was how different drought indices could give different results even when looking at the same conditions, which made me curious about how well a retrieval system could distinguish between papers discussing similar methods. So I ended up choosing a corpus of 345 research abstracts about drought and climate science. I think this also creates an interesting challenge because many of these papers share the same terminology, but that doesn't necessarily mean they answer the same question.

As for the retrieval systems, I expect rerank to perform the best overall, although I am not entirely sure how much better it will be. From Stage 1, BM25 seemed to do well when the query contained specific terminology, while dense retrieval was better at understanding questions that described a concept without necessarily naming it. I would normally think hybrid should benefit from combining both approaches, but that wasn't really what happened in Stage 1. Because of that, I actually expect hybrid to perform the worst overall, especially if a relevant paper ranks highly in only one of the two systems and gets pushed down during fusion. Rerank should have an advantage because it can examine whether an abstract actually addresses the question rather than relying entirely on keyword matches or embedding similarity. However, it still depends on what hybrid retrieves in the first place. If a relevant paper never reaches its candidate pool, then even a better understanding of the question won't help it recover that paper.

---

## 2. A fork in the road

Name one real design choice where you could have gone two ways: the chunk size, the embedding model, how the two systems are fused, how many documents the reranker sees, a sentence in `prompts/answer.txt`, how you cleaned the corpus.

Say which you picked, what the alternative was, and what you gave up by not taking it.
If you measured both, give both numbers.
If you rejected the alternative without measuring it, say why that was a fair call, and what it cost you in time, tokens or complexity.

"There was no alternative" is not an answer.
Find the fork.

One decision I had to make was whether to remove the citation headers from the reranker's passages or simply increase the 600-character limit. I chose to remove the citation headers rather than increase the character limit because I wanted to test whether giving Claude more abstract content within the same 600-character budget would help. The alternative was to raise the character limit, which might have exposed more relevant information but would also increase the number of tokens being processed. We didn't test that alternative, although looking back, it might have been worth considering since some of the relevant sentences were still outside the 600 characters even after removing the headers. The ablation itself took 30 Claude calls, and the results were actually slightly worse, with nDCG@10 decreasing from 0.687 to 0.673. The difference was only −0.014, with a confidence interval of [−0.047, +0.014]. Since the interval included zero, I couldn't distinguish the performance of the two versions. I still think it was a reasonable way to isolate one change, but the results showed a problem with my assumption. Removing the header didn't guarantee that Claude would actually see the evidence needed to make a relevance judgment.

---

## 3. Where you overruled the agent

One time Claude suggested, wrote or claimed something and you did not take it.
It might be a relevance judgment you disagreed with, a retriever it called finished when a run file showed otherwise, a number it summarized wrongly, or a license it said was fine.

What did it do?
How did you notice?
What did you do instead?

If it genuinely never happened, say so plainly, and then say what you would have had to check in order to notice.
Being honest here costs you far less than a story you cannot defend when you record your video.

For c06, Claude's initial summary of the Uzbekistan paper left out the evidence I needed to determine whether the study actually used SPEI. Since the query specifically required CMIP6 projections using SPEI, I didn't want to exclude the paper simply because the extracted sentences didn't mention it. I asked Claude to pull the full abstracts for papers 5 (10-3390-atmos15070866), the Uzbekistan drought-projection study, and 7 (10-3390-forecast2020004), the India forecasting study, so I could check them more closely. It turned out that paper 5 did explicitly calculate SPEI using projected temperature and precipitation, including results under CMIP6 scenarios. Because of this, I decided to include it in the relevant set, even though it wasn't part of my original selection. Paper 7, on the other hand, used scPDSI rather than SPEI, so I kept that one excluded. That was exactly the kind of situation where I didn't want to rely on Claude's initial summary alone. The extracted sentences weren't necessarily incorrect. They just left out enough information that I could have ruled out a relevant paper without realizing it. For c06, checking the full abstract was what changed my judgment. I added paper 5 only after confirming that it actually used SPEI under CMIP6 projections.

---

## 4. A number you do not trust

Pick one number in `EVAL.md` that you do not fully trust, and say why.
It could be a mean over a small query class, a difference whose interval includes zero, a verified share of 100%, a score on a gold set you wrote yourself, or a result you got only once.

What would have to be true for you to trust it?
Did you do anything to test it, and what did that show?

One number I'm still somewhat skeptical about is the 8 out of 8 verified answers from the cited-answer evaluation. At first, that sounds like a perfect result, but there were only eight answerable questions, and the 95% confidence interval was still [0.676, 1.000]. Finding a quotation inside a cited chunk is one thing. Checking whether that quotation actually supports the associated claim is another. To investigate this, I manually reviewed three answers, a01, a02, and a07, and checked all six of their claims against the cited passages. All six claims held up during my audit, which gave me more confidence in those answers. Still, that isn't enough evidence to generalize the verification rate to a much larger set of questions. I would want to test more questions and manually examine more claims before trusting the verified rate as representative of the system's actual reliability.

---

## 5. What is still wrong

One thing in your system, your corpus or your gold set that is not right, not finished, or that you do not fully understand.

What would you do next, and how would you find out whether it matters?
Name the file, the query or the document where someone could look.

I think the biggest remaining problem with my system is candidate generation. Even though rerank performed the best overall, 63 of the 155 relevant query-document pairs never reached Claude's top-20 candidate pool. This means that no matter how well Claude understands a question, it cannot rank a relevant paper that it was never given. The problem was especially noticeable for c08, where only 1 of 10 relevant papers reached rerank, and c19, where only 2 of 12 did. The candidate-coverage results can be reproduced using scripts/candidate_recall.py, and the specific failures for queries like c08 and c19 are documented in the Section 6 table in EVAL.md.

If I were to continue improving the system, I would start by testing different ways of selecting the candidate documents before reranking. We already measured an interleaved BM25 and dense candidate pool, which increased coverage for c06 from 4 of 9 to 8 of 9 relevant papers. The interleaved candidate pool only increased overall coverage from 92 to 93 of the 155 relevant query-document pairs. We also never ran Claude on that variant, so its actual effect on final rankings remains unknown. I would want to compare the final rankings, possibly try a larger candidate pool, and see whether the additional relevant documents translate into better retrieval performance. At this point, I see candidate generation as the bigger limitation compared with making small improvements to how Claude ranks papers it already receives.
