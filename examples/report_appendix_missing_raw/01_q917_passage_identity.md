# Case 1 — QASPER Question 917 / Paper 266: Passage Identity Under Fixed Context Budget

## Executive Summary & Scientific Significance
This case study demonstrates the **Passage Identity Principle**: under an identical context budget ($k=4$ chunks, $\sim 820\text{--}990$ tokens), the **specific choice of which passages enter the context** completely dictates downstream reader success. Pure lexical retrieval rank (BM25) and dense query-passage semantic similarity both failed to surface the single decisive passage at Rank 8, leading to partial answers or hallucinations. Only the learned passage router (R2) promoted Rank 8 into the budget, enabling exact downstream task success.

---

## Benchmark & Query Metadata

- **Dataset:** QASPER
- **Paper ID:** `266`
- **Question ID:** `917`
- **Question (verbatim):** `What languages are seen in the news and TED datasets?`
- **Gold Answer (verbatim):** `English, German`
- **Question Type:** `free_form`
- **Frozen Reader:** Mistral-7B-Instruct-v0.2 (SARA projection, temperature=0, seed=42)
- **Evaluated Budget:** Fixed $k=4$ passages

---

## Routing Comparison at Fixed Budget $k=4$

| Route | Selection Policy | Selected Chunks (Ranks) | Context Tokens | Raw Reader Output | Token F1 | Exact Match | Decisive Passage (Rank 8) Included? |
|:---|:---|:---:|:---:|:---|:---:|:---:|:---:|
| **R0: BM25 Prefix** | Top-4 BM25 retrieved order | `[1, 2, 3, 4]` | 826 | `English` | 0.6667 | 0.0 | ❌ No |
| **R1: Semantic Top-k** | Dense SFR-Mistral cosine top-4 | `[2, 3, 4, 5]` | 991 | `English, Spanish` | 0.5000 | 0.0 | ❌ No (Hallucinated Spanish) |
| **R2: Learned Router** | Trained passage utility selector | `[1, 2, 6, 8]` | 945 | `English, German` | **1.0000** | **1.0** | **✅ Yes (Decisive)** |

---

## The Decisive Passage: Rank 8

Lexical search assigned this passage **Rank 8 (BM25 score: 1.2291)**, putting it well outside the standard prefix budget of $k=4$.

- **Full Chunk ID:** `266_chunk_f28e546d-3f89-4dfc-b0f7-83ddc4553ee1`
- **Retrieved Rank:** 8
- **BM25 Retrieval Score:** 1.229125
- **Selected by:** R2 (Learned Router) ONLY. Omitted by R0 and R1.
- **Verbatim Text:**

> Systems, Methods and Resources ::: Test data under analysis	As one of our aims is to compare coreference chain properties in automatic translation with those of the source texts and human reference, **we derive data from ParCorFull, an English-German corpus annotated with full coreference chains .** The corpus contains ca. 160.7 thousand tokens manually annotated with about 14.9 thousand mentions and 4.7 thousand coreference chains. **For our analysis, we select a portion of English news texts and TED talks from ParCorFull and translate them with the three NMT systems described in SECREF4 above.** As texts considerably differ in their length, we select 17 news texts (494 sentences) and four TED talks (518 sentences). The size (in tokens) of the total data set under analysis – source (src) and human translations (ref) from ParCorFull and the automatic translations produced within this study (S1, S2 and S3) are presented in Table TABREF20. Notably, automatic translations of TED talks contain more words than the corresponding reference translation, which means that machine-translated texts of this type have also more potential tokens to enter in a coreference relation, and potentially indicating a shining through effect.

### Why Rank 8 is Decisive
Rank 8 is the **only chunk in the entire candidate pool** that explicitly connects the dataset name (*ParCorFull*), the language pair (*English-German*), and the evaluated genres (*English news texts and TED talks*). Without Rank 8, the reader lacks evidence that the translation direction is English-German.

---

## Verbatim Evidence Pool (Ranks 1–10)

### Rank 1
- **Chunk ID:** `266_chunk_2226fcac-fda6-4577-bf16-2c3e2aabcba6`
- **BM25 Score:** 2.455052
- **Selected by:** R0, R2
- **Verbatim Text:**
> There is also a variation in terms of chain number between translations of TED talks and news. While automatic translations of news texts contain more chains than the corresponding human annotated sources and references, machine-translated TED talks contain less chains than the sources and human translations. However, there is not much variation between the chain features of the three MT outputs. The chains are also longer in machine-translated output than in reference translations as can be seen by the number of mentions per chain and the length of the longest chain.
- *Analysis:* Discusses variations in coreference chains between news and TED talks. Mentions translation, but never specifies the languages.

### Rank 2
- **Chunk ID:** `266_chunk_256a5dde-179e-4b64-a3ba-a857902cd389`
- **BM25 Score:** 2.350529
- **Selected by:** R0, R1, R2
- **Verbatim Text:**
> Results and Analyses ::: MT quality at system level	We evaluate the quality of the three transformer engines with two automatic metrics, BLEU  and METEOR . Table TABREF25 shows the scores in two cases: all, when the complete texts are evaluated and coref, when only the subset of sentences that have been augmented in S3 are considered – 265 out of 494 for news and 239 out of 518 for TED. For news, the best system is that trained on more data, S2; but for TED talks S3 with less data has the best performance. The difference between the behaviour of the systems can be related to the different genres. We have seen that news are dominated by nominal mentions while TED is dominated by pronominal ones. Pronouns mostly need coreference information to be properly translated, while noun phrases can be improved simply because more instances of the nouns appear in the training data. With this, S3 improves the baseline S1 in +1.1 BLEU points for TED$_{coref}$ but -0.2 BLEU points for news$_{coref}$.
- *Analysis:* Discusses MT quality (BLEU, METEOR) across news and TED genres, but mentions zero language names.

### Rank 3
- **Chunk ID:** `266_chunk_5066b412-c14d-4b8a-9234-32782ce96199`
- **BM25 Score:** 2.329555
- **Selected by:** R0, R1
- **Verbatim Text:**
> Results and Analyses ::: Error analysis	The total distribution for the 10 categories of errors defined in Section SECREF23 can be seen in Figure FIGREF29. Globally, the proportion of errors due to our closed categories (gender, number, case and ambiguous) is larger for TED talks than for news (see analysis in Section SECREF28). Gender is an issue with all systems and genres which does not get solved by the addition of more data. Additionally, news struggle with wrong words and named entities; for this genre the additional error types (see analysis in Section SECREF30) represent around 60% of the errors of S1/S3 to be compared to the 40% of TED talks.
- *Analysis:* Error distribution analysis (gender, number, case) across TED and news genres. Zero language names specified.

### Rank 4
- **Chunk ID:** `266_chunk_82bed694-d901-4c2c-80c4-eaf707f9392b`
- **BM25 Score:** 1.824116
- **Selected by:** R0, R1
- **Verbatim Text:**
> Results and Analyses ::: Error analysis ::: Types of erroneous mentions	Finally, we also analyse the types of the mentions marked as errors. They include either nominal phrases or pronouns. Table TABREF32 shows that there is a variation between the news texts and TED talks in terms of these features. News contain more erroneous nominal phrases, whereas TED talks contain more pronoun-related errors. Whereas both the news and the TED talks have more errors in translating anaphors, there is a higher proportion of erroneous antecedents in the news than in the TED talks. It is also interesting to see that S3 reduces the percentage of errors in anaphors for TED, but has a similar performance to S2 on news.
- *Analysis:* Mentions erroneous nominal phrases vs pronouns in news vs TED. Zero language names specified.

### Rank 5
- **Chunk ID:** `266_chunk_05e76fe2-f372-4850-ac63-f727c75f2256`
- **BM25 Score:** 1.402521
- **Selected by:** R1
- **Verbatim Text:**
> Results and Analyses ::: Chain features	First, we compare the distribution of several chain features in the three MT outputs, their source texts and the corresponding human translations. Table TABREF20 shows that, overall, all machine translations contain a greater number of annotated mentions in both news texts and TED talks than in the annotated source (src and src$_{\rm CoreNLP}$) and reference (ref) texts. Notice that src$_{\rm CoreNLP}$ —where coreferences are not manually but automatically annotated with CoreNLP— counts also the tokens that the mentions add to the sentences, but not the tags. The larger number of mentions may indicate a strong explicitation effect observed in machine-translated texts. Interestingly, CoreNLP detects a similar number of mentions in both genres, while human annotators clearly marked more chains for TED than for news. Both genres are in fact quite different in nature; whereas only $37\%$ of the mentions are pronominal in news texts (343 out of 915), the number grows to $58\%$ for TED (577 out of 989), and this could be an indicator of the difficulty of the genres for NMT systems.
- *Analysis:* Compares coreference chain distributions and mentions CoreNLP. Zero language names specified. Selected by R1 due to high dense query alignment.

### Rank 6
- **Chunk ID:** `266_chunk_5651734c-24ee-4373-8869-af17f3e4733b`
- **BM25 Score:** 1.351321
- **Selected by:** R2
- **Verbatim Text:**
> Systems, Methods and Resources ::: State-of-the-art NMT	Our NMT systems are based on a transformer architecture  as implemented in the Marian toolkit  using the transformer big configuration. We train three systems (S1, S2 and S3) with the corpora summarised in Table TABREF5. The first two systems are transformer models trained on different amounts of data (6M vs. 18M parallel sentences as seen in the Table). The third system includes a modification to consider the information of full coreference chains throughout a document augmenting the sentence to be translated with this information and it is trained with the same amount of sentence pairs as S1. A variant of the S3 system participated in the news machine translation of the shared task held at WMT 2019 .
- *Analysis:* Provides architectural context (Marian toolkit, transformer big, WMT 2019 shared task). Promoted by R2 alongside Rank 8.

### Rank 7
- **Chunk ID:** `266_chunk_1caf17c1-8f8b-4497-a883-c095c7fd7ac9`
- **BM25 Score:** 1.278204
- **Selected by:** None at $k=4$
- **Verbatim Text:**
> However, even if the systems differ in the overall performance, the change is not related to the number of errors in coreference chains. Table TABREF25 also reports the number of mistakes in the translation of coreferent mentions. Whereas the number of errors correlates with translation quality (as measured by BLEU) for news$_{coref}$ this is not the case of TED$_{coref}$.

### Rank 8
- *(See "The Decisive Passage: Rank 8" above)*

### Rank 9
- **Chunk ID:** `266_chunk_ee20e5ec-d8d8-4529-94e8-4039ce751445`
- **BM25 Score:** 1.197171
- **Selected by:** None at $k=4$
- **Verbatim Text:**
> S2: Lassen sie uns... einen kurzen Blick auf die Geschichte [des Stasi] werfen denn es wirklich wichtig, [seine] Selbstauffassung zu verstehen. The gender-related errors are common to all the automatic translations. Interestingly, systems S1 and S3 have more problems with gender in translations of TED talks, whereas they do better in translating news, which leads us to assume that this is a data-dependent issue: while the antecedent for news is in the same sentence it is not for TED talks. A closer look at the texts with a high number of gender problems confirms this assumption —they contain references to females who were translated with male forms of nouns and pronouns (e.g. Mannschaftskapitän instead of Mannschaftskapitänin). We also observe errors related to gender for the cases of explicitation in translation. Some impersonal English constructions not having direct equivalents in German are translated with personal constructions, which requires an addition of a pronoun. Such cases of explicitation were automatically detected in parallel data in , . They belong to the category of obligatory explicitation, i.e.
- *Analysis:* Contains German example sentences and German words ("Mannschaftskapitän", "Mannschaftskapitänin"), but discusses gender-related errors rather than defining the primary dataset languages.

### Rank 10
- **Chunk ID:** `266_chunk_cd890417-c352-488c-9060-712c89b6ef00`
- **BM25 Score:** 1.074654
- **Selected by:** None at $k=4$
- **Verbatim Text:**
> Summary and Conclusions	We analysed coreferences in the translation outputs of three transformer systems that differ in the training data and in whether they have access to explicit intra- and cross-sentential anaphoric information (S3) or not (S1, S2). We see that the translation errors are more dependent on the genre than on the nature of the specific NMT system: whereas news (with mainly NP mentions) contain a majority of errors related to wrong word selection, TED talks (with mainly pronominal mentions) are prone to accumulate errors on gender and number. System S3 was specifically designed to solve this issue, but we cannot trace the improvement from S1 to S3 by just counting the errors and error types, as some errors disappear and others emerge: coreference quality and automatic translation quality do not correlate in our analysis on TED talks. As a further improvement to address the issue, we could add more parallel data to our training corpus with a higher density of coreference chains such as movie subtitles or parallel TED talks. We also characterised the originals and translations according to coreference features such as total number of chains and mentions, average chain length and size of the longest chain.

---

## Mechanistic Takeaway for RAG System Design

1. **High lexical relevance $\neq$ answer sufficiency:** Chunks 1 to 5 repeated the keywords "news", "TED talks", "translation", and "genres" dozens of times, scoring high BM25 values ($1.40\text{--}2.45$). Yet none of them answered the question.
2. **Dense retrieval vulnerability to generic topical matches:** R1 selected `[2, 3, 4, 5]` because those passages had high semantic alignment to the concept of news and TED machine translation. However, lacking the specific factual token "German", the reader hallucinated "Spanish".
3. **Passage Identity supersedes budget size:** Changing $k$ from 4 to 8 in a fixed prefix strategy would eventually reach Rank 8, but costs double the compute and context window. R2 solved the problem at $k=4$ by skipping non-informative top ranks `[3, 4, 5]` and pulling Rank 8 directly into the prompt.

---

## Verifiable Source Artifacts
- Candidate pool and BM25 scores: `results/week2/raw/dev_retrieval.jsonl` (line with `"question_id": "917"`)
- R0 generation record: `results/week2/raw/dev_fixed_k_matrix.jsonl` (`question_id: 917`, `k: 4`)
- R0, R1, R2 routing assignments: `results/week6/passage_routing/routing_predictions/dev_routing_assignments.csv` (`question_id: 917`)
- R1 generation cache: `results/week6/passage_routing/sara_generations/cache_R1_semantic_topk_k4.jsonl` (`question_id: 917`)
- R2 generation cache: `results/week6/passage_routing/sara_generations/cache_R2_learned_router_k4.jsonl` (`question_id: 917`)
- Complete machine-readable bundle: [01_q917_candidate_pool.json](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/01_q917_candidate_pool.json)

