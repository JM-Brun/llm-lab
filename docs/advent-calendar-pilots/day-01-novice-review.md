# Day 01 — novice-reader review protocol

**Purpose:** determine whether the Zipf story is independently understandable, scientifically careful and useful to a reader who has not studied the topic. This is a pedagogical acceptance test, not a proofreading exercise.

**Target reader:** someone comfortable reading a short popular-science article but not already familiar with Zipf's law, rank-frequency plots or language-model training. Do not choose a specialist in statistical linguistics or NLP as the only test reader.

**Time budget:** about 15–20 minutes including the short post-reading questions. The article itself claims approximately 10 minutes; measure the actual reading time rather than assuming the estimate is correct.

## 1. Set up the test

- Ask the reader to open either the French or English page, whichever they naturally prefer.
- Do not explain Zipf's law, the graph, the formula, or the LLM connection beforehand.
- Ask them to read the story once, without coaching. They may use the page normally, including opening the solution disclosure.
- Record the language, start/end time, whether they opened the solution, and any points where they paused, reread, or expressed uncertainty.
- Do not correct misunderstandings during the read.

Use a simple observation log:

| Field | Observation |
|---|---|
| Reader profile (non-identifying) | |
| Language | |
| Start / end time | |
| Time spent reading | |
| Opened worked solution? | |
| Pauses or rereads | |
| Unfamiliar terms | |
| Confusing passages | |

## 2. Ask these questions after reading

Ask openly first. Do not show the expected answer until the reader has responded.

1. **Main idea:** In your own words, what does the story say about how often words occur?
2. **Building the ranking:** In the small count table in the story, why is “de” / “the” at rank 1, and what would make its rank change?
3. **Graph:** What do the horizontal and vertical axes represent? What does a roughly straight line on log-log axes suggest, and what does it not prove?
4. **Transfer calculation:** With \(C=12,000\) and \(\alpha=1\), what frequency does the model predict at rank 6? Can you explain the calculation? This rank is deliberately different from the article's challenge so the question still tests transfer if the reader opened the solution.
5. **Limits:** Name one reason not to treat the formula as an exact law for every word or every corpus.
6. **LLM connection:** What is one cautious implication of unequal lexical frequencies for language-model training data? What cannot be concluded from the Zipf curve alone?
7. **Terminology:** In this story, what does *token* mean? How is that different from a tokenizer token in an LLM?

## 3. Score comprehension

Score each item from 0 to 2. Record the reader's own words and do not infer understanding from a yes/no response.

| Dimension | 0 — not understood | 1 — partial | 2 — clear |
|---|---|---|---|
| Main idea | Cannot describe the imbalance | Recognizes frequent vs rare words, but not the rank-frequency idea | Explains the unequal distribution and rank-frequency relation |
| Formula | Cannot interpret (r), (C), or (f(r)) | Understands some symbols but cannot use the relation | Correctly explains and applies the toy formula |
| Log-log plot | Misreads axes or treats the line as proof | Understands one axis or the approximate trend | Explains axes and the limits of a straight-line interpretation |
| Empirical limits | Treats Zipf as exact/universal | Mentions variation without a reason | Gives a relevant limitation or estimation caveat |
| LLM implication | Makes an unsupported performance claim | Recognizes rare forms are less represented | Gives a cautious training-data implication and states a limit |
| Lexical/model token distinction | Conflates the two | Understands they differ but cannot explain how | Distinguishes lexical occurrence from tokenizer unit |

Maximum: 12 points. Treat this as diagnostic evidence, not a statistically meaningful score. With one reader, do not generalize to the whole audience.

## 4. Acceptance criteria

The story can be accepted after revision when:

- The reader can state the central idea without repeating the title or a sentence verbatim.
- The reader can interpret rank and frequency and solve a transfer calculation at a new rank, with at most a small clarification.
- The reader understands that a log-log straight line is evidence for an approximate relation over a range, not proof of a universal exact law.
- The reader can state one qualified implication for training data without claiming that lexical frequency alone determines model performance.
- The distinction between lexical occurrence and tokenizer token is not a source of persistent confusion.
- The observed reading time is reasonably close to the advertised duration, or the duration estimate is corrected.
- No critical ambiguity, mathematical error, inaccessible interaction or broken navigation remains.

A low score is not a reason to coach the reader until they pass. It is evidence to revise the explanation, figure, example or vocabulary and then test again.

## 5. Turn feedback into changes

For every issue, record:

| Observation (quote or behavior) | Likely cause | Proposed change | Location | Re-test needed? |
|---|---|---|---|---|
| | | | | |

Prioritize in this order:

1. Misunderstandings of the central concept or formula.
2. Incorrect interpretation of the figure or empirical caveats.
3. Unsupported inference about LLM training.
4. Terminology and sentence-level clarity.
5. Cosmetic preferences that do not affect comprehension.

After changing article content, rerun the FR/EN Quarto preview, link checks and relevant browser/accessibility checks. Keep the pages planned and outside the public render list until acceptance.

## 6. Decision record

Complete after the test:

- **Date:**
- **Language tested:**
- **Observed reading time:**
- **Comprehension summary:**
- **Critical misunderstandings:**
- **Changes required:**
- **Re-test result:**
- **Decision:** accepted / revise and retest
- **Approval:**

**Do not draft Day 02 until Day 01 has an explicit acceptance decision.**
