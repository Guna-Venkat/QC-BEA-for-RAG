# Case 4 — SARA Question 1001 / Paper 293: Decisive Rank-6 Evidence and Granular Budget Scaling

## Executive Summary & Scientific Significance
This case study provides empirical evidence for the **Granular Context Scaling Threshold** in Retrieval-Augmented Generation. 

For Question 1001 on Paper 293, lexical BM25 retrieval ranked introductory passages with high keyword frequency at Ranks 1 to 5. However, these top ranks only mentioned high-level terms (such as *"psycho-linguistic features"* or the shorthand *"NLP Features"*), leaving the reader unable to enumerate the actual feature set. Across fixed budgets $k=2$, $k=4$, and $k=5$, reader performance plateaued at **0.1429 F1**, stubbornly outputting the generic label `"NLP Features"`.

Only when the budget was expanded to **$k=6$** was the decisive methodology passage at **Rank 6** admitted into the context. Immediately, reader F1 surged from **0.1429 to 0.6000**, correctly listing `Emotion Sensor Feature`, `Empath`, `Parts-of-speech tags`, and `Punctuation features`.

---

## Benchmark & Query Metadata

- **Dataset:** QASPER
- **Paper ID:** `293`
- **Question ID:** `1001`
- **Question (verbatim):** `Which psycholinguistic and basic linguistic features are used?`
- **Gold Answer (verbatim):** `Emotion Sensor Feature, Part of Speech, Punctuation, Sentiment Analysis, Empath, TF-IDF Emoticon features`
- **Question Type:** `free_form`
- **Controlled Reader:** Mistral-7B-Instruct-v0.2 (SARA projection, temperature=0, seed=42)

---

## Generation Progression Across Fixed Budgets ($k = 0 \to 10$)

| Budget $k$ | Cumulative Context Tokens | Raw Reader Output | Token F1 | Rouge-L | Decisive Rank 6 Included? |
|:---:|:---:|:---|:---:|:---:|:---:|
| $k=0$ | 133 | `No linguistic features are used.` | 0.1333 | 0.1111 | ❌ No |
| $k=2$ | 448 | `NLP Features` | 0.1429 | 0.0000 | ❌ No |
| $k=4$ | 826 | `NLP Features` | 0.1429 | 0.0000 | ❌ No |
| $k=5$ | 1084 | `NLP Features` | 0.1429 | 0.0000 | ❌ No |
| **$k=6$** | **1326** | **`Emotion Sensor Feature, Empath, Parts-of-speech tags, Punctuation features`** | **0.6000** | **0.4762** | **✅ YES (Threshold crossed)** |
| $k=8$ | 1735 | `Emotion Sensor Dataset, Controlled Topical Signals from Empath, Emoticons, punctuation features, parts-of-speech tags` | 0.4167 | 0.2308 | ✅ Yes (Diluted with distractors) |
| $k=10$ | 2128 | `Emotion Sensor Feature, Controlled Topical Signals from Empath, Normalized frequency of POS tags` | 0.3478 | 0.3077 | ✅ Yes (Over-context degradation) |

---

## The Decisive Evidence: Rank 6

- **Chunk ID:** `293_chunk_11813f79-19af-44f4-9d2f-3ae82f54ba73`
- **Retrieved Rank:** 6
- **BM25 Retrieval Score:** 1.337668
- **Verbatim Passage Text:**

> Methodology ::: NLP Features	**We have identified a novel combination of features which are highly effective in aggression classification when applied in addition to the features obtained from the deep learning classifier at the classification layer. We have introduced two new features in addition to the previously available features. The first one is the Emotion Sensor Feature which use a statistical model to classify the words into 7 different classes based on the sentences obtained from twitter and blogs which contain total 1,185,540 words. The second one is the collection of selected topical signal from text collected using Empath (see Table 1.). Different from previous approaches,  where  have used Emotion features in the form of frequency while  have used emotion feature vector obtained from LIWC 2007. Unlike we have used only 6 topical signals from Emapth. We have borrowed the idea of using other features like punctuation features and parts-of-speech tags from . The Table 1. lists and describes features, tools used to obtain them and the number of features resulted from each type.**

---

## Verbatim Evidence Pool (Ranks 1–10)

### Rank 1
- **Chunk ID:** `293_chunk_c447ec3e-cdf7-4cb0-9131-2f242ec381fd`
- **BM25 Score:** 3.118557
- **Verbatim Text:**
> Some approaches like: has used emotions frequency as one of the features, while some others use sentiment emotion as feature. Also,,  have converted emoticons to their description.  have used TF-IDF of emoticons per-class as one of the features. Compared to all these approaches, we have concentrated to capture multiple linguistic/pattern based relations, key-terms and key-patters (with their association in text) through a combination of deep learning architectures with model averaging. We have also used NLP features as additional features with our deep learning architecture, obtained from psycho-linguistic and basic linguistic features.
- *Analysis:* High BM25 score due to matching "psycho-linguistic and basic linguistic features". However, it merely states that NLP features are "obtained from psycho-linguistic and basic linguistic features" without naming any specific feature types.

### Rank 2
- **Chunk ID:** `293_chunk_6097e73f-f027-4ea0-8e93-8f1691ced556`
- **BM25 Score:** 2.677598
- **Verbatim Text:**
> This may be due to the text style or level of complexities of both datasets. So, we concentrated to develop a robust system for English code-mixed texts, and uni-lingual texts, which can also handle different writing styles. Our approach is based on three main ideas: Deep-Text Learning. The goal is to learn long range associations, dependencies between regions of text, N-grams, key-patterns, topical information, and sequential dependencies. Exploiting psycho-linguistic features with basic linguistic features as meta-data. The main aim is to minimize the direct dependencies on in-depth grammatical structure of the language (i.e., to support code-mixed data). We have also included emoticons, and punctuation features with it. We use the term "NLP Features" to represent it in the entire paper. Dual embedding based on FastText and Glove. This dual embedding helps in high vocabulary coverage and to capture the rare and partially incorrect words in the text (specially by FastText ). Our "Deep-text architecture" uses model averaging strategy with three different deep learning architectures.
- *Analysis:* Crucial failure-inducing sentence: *"We use the term 'NLP Features' to represent it in the entire paper."* When the reader is given only Ranks 1 and 2 (or up to Rank 5), it latches onto this definition and answers `"NLP Features"`.

### Rank 3
- **Chunk ID:** `293_chunk_754090fb-31ff-4385-9948-c68c14a23a06`
- **BM25 Score:** 1.846498
- **Verbatim Text:**
> For example, "Dear India, stop playing with the emotions of your people for votes." Non-Aggressive(NAG) - Generally these type of text lack any kind of aggression it is basically used to state facts, wishing on occasions and polite and supportive. The additional discussion on aggressiveness task can be found in Kaggle task , which just divided the task into two classes - i.e., presence or absence of aggression in tweets. The informal setting/environment of social media often encourage multilingual speakers to switch back and forth between languages when speaking or writing. These all resulted in code-mixing and code-switching. Code-mixing refers to the use of linguistic units from different languages in a single utterance or sentence, whereas code-switching refers to the co-occurrence of speech extracts belonging to two different grammatical systems. This language interchange makes the grammar more complex and thus it becomes tough to handle it by traditional algorithms. Thus the presence of high percentage of code-mixed content in social media text has increased the complexity of the aggression detection task. For example, the dataset provided by the organizers of TRAC-2018 ,  is actually a code-mixed dataset.
- *Analysis:* Discusses aggression labels and code-mixing definitions. Contains zero feature names.

### Rank 4
- **Chunk ID:** `293_chunk_92b075a7-4be7-46b4-a3c4-56893abfb7e2`
- **BM25 Score:** 1.777101
- **Verbatim Text:**
> A Unified System for Aggression Identification in English Code-Mixed and Uni-Lingual Texts	Wide usage of social media platforms has increased the risk of aggression, which results in mental stress and affects the lives of people negatively like psychological agony, fighting behavior, and disrespect to others. Majority of such conversations contains code-mixed languages[28]. Additionally, the way used to express thought or communication style also changes from one social media plat-form to another platform (e.g., communication styles are different in twitter and Facebook). These all have increased the complexity of the problem. To solve these problems, we have introduced a unified and robust multi-modal deep learning architecture which works for English code-mixed dataset and uni-lingual English dataset both.The devised system, uses psycho-linguistic features and very ba-sic linguistic features. Our multi-modal deep learning architecture contains, Deep Pyramid CNN, Pooled BiLSTM, and Disconnected RNN(with Glove and FastText embedding, both). Finally, the system takes the decision based on model averaging. We evaluated our system on English Code-Mixed TRAC 2018 dataset and uni-lingual English dataset obtained from Kaggle.
- *Analysis:* Abstract/Introduction summarizing the system. Repeats the phrase *"uses psycho-linguistic features and very basic linguistic features"* but describes the deep learning models (DPCNN, BiLSTM, DRNN) rather than the linguistic features.

### Rank 5
- **Chunk ID:** `293_chunk_7192a83a-a6f6-4173-a99d-34c339d2b887`
- **BM25 Score:** 1.585685
- **Verbatim Text:**
> Methodology ::: Data Preprocessing	We consider the text to be well formatted before applying the text to the embedding layer. First, we detect non-English text(which are few) and translate all of them to English using Google Translate. Still, there is some code mixed words like "mc", "bc" and other English abbreviations and spelling errors like "nd" in place of "and", "u" in place of "you" causes deep learning model to confuse with sentences of the same meaning. We follow the strategy of preprocessor as in to normalize the abbreviations and remove spelling errors, URLs and punctuation marks, converting emojis to their description. https://spacy.io/usage/linguistic-features#pos-tagging
- *Analysis:* Preprocessing section describing abbreviation normalization and POS tagging URL. Does not detail the psycholinguistic feature set.

### Rank 6
- *(See "The Decisive Evidence: Rank 6" above)*

### Rank 7
- **Chunk ID:** `293_chunk_16888280-6d35-4370-8cec-4921dab36d38`
- **BM25 Score:** 0.954664
- **Verbatim Text:**
> Finally, Our Proposed Method, which represents the model averaging of three models with NLP features.

### Rank 8
- **Chunk ID:** `293_chunk_33e28109-92fe-4d0f-a2f5-91a4cd799f34`
- **BM25 Score:** 0.909179
- **Verbatim Text:**
> The intuition behind the NLP features are the following: Emotion Sensor Dataset We have introduced to use of emotion sensor features, as a meta-data information. We have obtained the word sensor dataset from Kaggle. In this dataset each word is statistically classified into 7 distinct classes (Disgust, Surprise, Neutral, Anger, Sad, Happy and Fear) using Naive Bayes, based on sentences collected from twitter and blogs. Controlled Topical Signals from Empath. Empath can analyse the text across 200 gold standard topics and emotions. Additionally, it uses neural embedding to draw connotation among words across more than 1.8 billion words. We have used only selected categories like violence, hate, anger, aggression, social media and dispute from 200 Empath categories useful for us unlike which takes 194 categories. Emoticons frequently used on social media indicates the sense of sentence, , . Normalized frequency of POS tags According to , , ,  POS Tags provide the degree of target aggressiveness.
- *Analysis:* Explains the intuition behind each feature. When added at $k=8$, it provides supplemental descriptions, but introduces verbosity that slightly degrades output conciseness ($F_1$ drops to 0.4167).

### Rank 9
- **Chunk ID:** `293_chunk_7785834a-114c-4570-a2c2-5761cb12e393`
- **BM25 Score:** 0.773143
- **Verbatim Text:**
> We have used only 20 NLP features (except TF-IDF Emoticon feature and Punctuation feature as given in Table TABREF25) for Kaggle dataset (as these are not present in the Kaggle dataset).

### Rank 10
- **Chunk ID:** `293_chunk_a09d114c-3126-438a-abc7-01af371bb87d`
- **BM25 Score:** 0.772530
- **Verbatim Text:**
> Experiment and Evaluation ::: Evaluation Strategy	To compare our experimental results we have used top-5 systems from the published results of TRAC-2018. To compare our results on Kaggle dataset, we have used the last & the best published result on Kaggle website as a baseline. We have conducted the separate experiments, to properly investigate the performance of (a) each of the classifiers (used in our model averaging based system), (b) impact of the NLP features on each of these classifiers and finally, (c) the performance of our proposed system. In Table TABREF57, TABREF57 and TABREF57, models, named as DPCNN(ref SECREF30), DRNN (ref SECREF34) and Pooled BiLSTM(ref SECREF45) are corresponding models without NLP features. Similarly, DPCNN+NLP Features, DRNN + NLP Features and Pooled BiLSTM + NLP Features are corresponding models with NLP features. The Model Averaging (A+B+C) is the ensemble of three models (i.e., model averaging of DPCNN, DRNN and Pooled BiLSTM) without NLP features.

---

## Mechanistic Insights for Context-Budget Allocation

1. **The Lexical Trap:** Passages that introduce or define a term often score highest in BM25 because they repeat the query keywords. However, they frequently defer technical definitions to later methodology sections.
2. **Sharp Nonlinear F1 Jump at Budget Boundaries:** The reader does not smoothly improve from $k=0$ to $k=6$. It is completely stuck at $F_1 = 0.1429$ across $k=2, 4, 5$, until the exact threshold ($k=6$) brings in Rank 6.
3. **Over-Context Saturation:** Performance does not monotonically increase past $k=6$. Adding Ranks 7, 8, 9, 10 adds distractors and verbose explanations that dilute reader attention, causing F1 to drop from **0.6000 at $k=6$** down to **0.3478 at $k=10$**.

---

## Verifiable Source Artifacts
- Master retrieval pool: `results/week2/raw/dev_retrieval.jsonl` (line with `"question_id": "1001"`)
- Multi-budget matrix generations: `results/week2/raw/dev_fixed_k_matrix.jsonl` (lines with `"question_id": "1001"`, $k \in \{0, 2, 4, 5, 6, 8, 10\}$)
- Machine-readable pool and evaluation records: [04_q1001_top10.json](file:///home/gunavenkat/Downloads/CS787-RAG-Project/FINAL_PROJECT_MAIN/examples/report_appendix_missing_raw/04_q1001_top10.json)

