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

TODO: your answer to prompt 2.

---

## 3. Where you overruled the agent

One time Claude suggested, wrote or claimed something and you did not take it.
It might be a relevance judgment you disagreed with, a retriever it called finished when a run file showed otherwise, a number it summarized wrongly, or a license it said was fine.

What did it do?
How did you notice?
What did you do instead?

If it genuinely never happened, say so plainly, and then say what you would have had to check in order to notice.
Being honest here costs you far less than a story you cannot defend when you record your video.

TODO: your answer to prompt 3.

---

## 4. A number you do not trust

Pick one number in `EVAL.md` that you do not fully trust, and say why.
It could be a mean over a small query class, a difference whose interval includes zero, a verified share of 100%, a score on a gold set you wrote yourself, or a result you got only once.

What would have to be true for you to trust it?
Did you do anything to test it, and what did that show?

TODO: your answer to prompt 4.

---

## 5. What is still wrong

One thing in your system, your corpus or your gold set that is not right, not finished, or that you do not fully understand.

What would you do next, and how would you find out whether it matters?
Name the file, the query or the document where someone could look.

TODO: your answer to prompt 5.
