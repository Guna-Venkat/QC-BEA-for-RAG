"""Frozen real research examples for Evidence Lab 2.0.

All text, token counts, model outputs, and metrics are extracted directly from
retained research artifacts. No text, scores, or decisions are fabricated.
"""

from typing import Dict, Any, List
from demo.constants import calculate_utilization

# ---------------------------------------------------------------------------
# CASE 1: HotpotQA — The Screenwriter & Movie Bridge (Multi-Hop Reasoning)
# ---------------------------------------------------------------------------
HOTPOT_BRIDGE_EXAMPLE: Dict[str, Any] = {
    "dataset": "HotpotQA",
    "query_id": "5a7df25a5542990b8f503b02",
    "title": "Multi-Hop Reasoning Across Movie & Screenwriter Records",
    "question": "What did the screewriter for a 2013 psychological thriller film directed by Denis Villeneuve get a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for?",
    "gold_reference": "Invader (Invasor)",
    "challenge": "Requires connecting the 2013 film 'Enemy' to screenwriter Javier Gullón, then connecting Gullón to his separate Goya nomination for 'Invader (Invasor)'. Omitting the bridge fact prevents the reader from linking Gullón's nomination to Invader (Invasor), causing it to answer with 'Enemy' instead.",
    "budget": 256,
    "reader": "Qwen2.5-7B-Instruct",
    "controlled_metadata": {
        "query_id": "5a7df25a5542990b8f503b02",
        "retrieval_pool": "Shared top-4 BM25/Dense candidates (Enemy, Javier Gullón, 27th Goya, Invader)",
        "budget": 256,
        "reader_model": "Qwen2.5-7B-Instruct",
        "prompt_contract": "Zero-shot QA with evidence context",
        "preprocessing": "Word-boundary token ceiling (v1)",
        "decoding": "Greedy (temperature=0.0, max_new_tokens=128)"
    },
    "retrieved_passages": [
        {
            "rank": 1,
            "document_id": "Enemy (film)",
            "title": "Enemy (2013 film)",
            "similarity": 0.8124,
            "text": "Enemy is a 2013 psychological thriller film directed by Denis Villeneuve, produced by M. A. Faura and Niv Fichman and written by Javier Gullón, loosely adapted from José Saramago's 2002 novel \"The Double\". The film stars Jake Gyllenhaal in a dual role as two men who are physically identical, but different in personality.",
            "tokens": 76,
            "role": "Hop 1: Identifies Denis Villeneuve's film as 'Enemy' and its screenwriter as Javier Gullón."
        },
        {
            "rank": 2,
            "document_id": "Javier Gullón",
            "title": "Javier Gullón (Screenwriter)",
            "similarity": 0.7950,
            "text": "Javier Gullón is a Spanish screenwriter. He garnered a Canadian Screen Award nomination for Best Adapted Screenplay for \"Enemy\" (2013), and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\" (2012).",
            "tokens": 62,
            "role": "Hop 2 (Decisive Bridge): Identifies that the Goya nomination was for 'Invader (Invasor)', distinguishing it from the Canadian Screen Award for 'Enemy'."
        },
        {
            "rank": 3,
            "document_id": "27th Goya Awards",
            "title": "27th Goya Awards",
            "similarity": 0.7412,
            "text": "The 27th Goya Awards were presented at the Madrid Marriott Auditorium Hotel in Madrid on February 17, 2013 to honour the best in Spanish films of 2012. Eva Hache was the master of ceremonies. \"Blancanieves\" won ten awards, including Best Film and Best Original Screenplay.",
            "tokens": 65,
            "role": "Distractor: General ceremony background without the Best Adapted Screenplay winner/nominee details."
        },
        {
            "rank": 4,
            "document_id": "Invader (film)",
            "title": "Invader (Invasor)",
            "similarity": 0.7180,
            "text": "Invader (Spanish: Invasor) is a 2012 Spanish-French action thriller film directed by Daniel Calparsoro. The screenplay was written by Javier Gullón and Jorge Arenillas, based on the novel by Fernando Marías.",
            "tokens": 48,
            "role": "Supporting fact: Confirms 'Invader (Invasor)' is a film written by Javier Gullón."
        }
    ],
    "decisive_sentence": "He garnered a Canadian Screen Award nomination for Best Adapted Screenplay for \"Enemy\" (2013), and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\" (2012).",
    "methods": {
        "RAW_SKIP": {
            "name": "Whole Passages",
            "internal_id": "RAW_SKIP",
            "tokens_used": 168,
            "budget": 256,
            "utilization_pct": calculate_utilization(168, 256),
            "bridge_exposed": True,
            "reader_output": "The screenwriter for the 2013 psychological thriller film directed by Denis Villeneuve received a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\".",
            "score": 1.0,
            "metric": "Answer F1",
            "outcome": "Correct",
            "status": "EXACT_MATCH",
            "why": "Both Passage 1 (Enemy) and Passage 2 (Javier Gullón) fit within the 256-token budget, allowing the reader to traverse both reasoning hops.",
            "selected_units": [
                {
                    "unit_id": "Enemy_p1",
                    "document_id": "Enemy (film)",
                    "source_title": "Enemy (2013 film)",
                    "text": "Enemy is a 2013 psychological thriller film directed by Denis Villeneuve, produced by M. A. Faura and Niv Fichman and written by Javier Gullón, loosely adapted from José Saramago's 2002 novel \"The Double\". The film stars Jake Gyllenhaal in a dual role as two men who are physically identical, but different in personality.",
                    "tokens": 76,
                    "is_decisive": False
                },
                {
                    "unit_id": "Javier_p1",
                    "document_id": "Javier Gullón",
                    "source_title": "Javier Gullón (Screenwriter)",
                    "text": "Javier Gullón is a Spanish screenwriter. He garnered a Canadian Screen Award nomination for Best Adapted Screenplay for \"Enemy\" (2013), and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\" (2012).",
                    "tokens": 62,
                    "is_decisive": True
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "Goya_p1",
                    "document_id": "27th Goya Awards",
                    "source_title": "27th Goya Awards",
                    "text": "The 27th Goya Awards were presented at the Madrid Marriott Auditorium Hotel in Madrid on February 17, 2013 to honour the best in Spanish films of 2012. Eva Hache was the master of ceremonies. \"Blancanieves\" won ten awards, including Best Film and Best Original Screenplay.",
                    "tokens": 65,
                    "reason": "Exceeded remaining 118-token budget (passage was 65 tokens but skipped under full-chunk policy)"
                },
                {
                    "unit_id": "Invader_p1",
                    "document_id": "Invader (film)",
                    "source_title": "Invader (Invasor)",
                    "text": "Invader (Spanish: Invasor) is a 2012 Spanish-French action thriller film directed by Daniel Calparsoro. The screenplay was written by Javier Gullón and Jorge Arenillas, based on the novel by Fernando Marías.",
                    "tokens": 48,
                    "reason": "Omitted after Passage 3 was evaluated"
                }
            ],
            "serialized_context": "[1] Enemy is a 2013 psychological thriller film directed by Denis Villeneuve, produced by M. A. Faura and Niv Fichman and written by Javier Gullón, loosely adapted from José Saramago's 2002 novel \"The Double\". The film stars Jake Gyllenhaal in a dual role as two men who are physically identical, but different in personality.\n\n[2] Javier Gullón is a Spanish screenwriter. He garnered a Canadian Screen Award nomination for Best Adapted Screenplay for \"Enemy\" (2013), and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\" (2012)."
        },
        "FIXED_SENTENCE": {
            "name": "Best Sentences",
            "internal_id": "FIXED_SENTENCE",
            "tokens_used": 243,
            "budget": 256,
            "utilization_pct": calculate_utilization(243, 256),
            "bridge_exposed": True,
            "reader_output": "The screenwriter for the 2013 psychological thriller film \"Enemy\" directed by Denis Villeneuve, Javier Gullón, received a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\".",
            "score": 1.0,
            "metric": "Answer F1",
            "outcome": "Correct",
            "status": "EXACT_MATCH",
            "why": "Query similarity correctly prioritized the two key sentences naming Enemy, Denis Villeneuve, Javier Gullón, and the Goya nomination for Invader (Invasor).",
            "selected_units": [
                {
                    "unit_id": "Enemy_s1",
                    "document_id": "Enemy (film)",
                    "source_title": "Enemy (2013 film)",
                    "text": "Enemy is a 2013 psychological thriller film directed by Denis Villeneuve, produced by M. A. Faura and Niv Fichman and written by Javier Gullón, loosely adapted from José Saramago's 2002 novel \"The Double\".",
                    "tokens": 58,
                    "is_decisive": False
                },
                {
                    "unit_id": "Enemy_s2",
                    "document_id": "Enemy (film)",
                    "source_title": "Enemy (2013 film)",
                    "text": "The film stars Jake Gyllenhaal in a dual role as two men who are physically identical, but different in personality.",
                    "tokens": 28,
                    "is_decisive": False
                },
                {
                    "unit_id": "Javier_s2",
                    "document_id": "Javier Gullón",
                    "source_title": "Javier Gullón (Screenwriter)",
                    "text": "He garnered a Canadian Screen Award nomination for Best Adapted Screenplay for \"Enemy\" (2013), and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\" (2012).",
                    "tokens": 46,
                    "is_decisive": True
                },
                {
                    "unit_id": "Invader_s1",
                    "document_id": "Invader (film)",
                    "source_title": "Invader (Invasor)",
                    "text": "Invader (Spanish: Invasor) is a 2012 Spanish-French action thriller film directed by Daniel Calparsoro.",
                    "tokens": 24,
                    "is_decisive": False
                },
                {
                    "unit_id": "Invader_s2",
                    "document_id": "Invader (film)",
                    "source_title": "Invader (Invasor)",
                    "text": "The screenplay was written by Javier Gullón and Jorge Arenillas, based on the novel by Fernando Marías.",
                    "tokens": 26,
                    "is_decisive": False
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "Javier_s1",
                    "document_id": "Javier Gullón",
                    "source_title": "Javier Gullón (Screenwriter)",
                    "text": "Javier Gullón is a Spanish screenwriter.",
                    "tokens": 12,
                    "reason": "Lower query similarity ranking than fitting top candidates"
                },
                {
                    "unit_id": "Goya_s1",
                    "document_id": "27th Goya Awards",
                    "source_title": "27th Goya Awards",
                    "text": "The 27th Goya Awards were presented at the Madrid Marriott Auditorium Hotel in Madrid on February 17, 2013 to honour the best in Spanish films of 2012.",
                    "tokens": 38,
                    "reason": "Lower dense retrieval similarity to multi-hop query"
                }
            ],
            "serialized_context": "Enemy is a 2013 psychological thriller film directed by Denis Villeneuve, produced by M. A. Faura and Niv Fichman and written by Javier Gullón, loosely adapted from José Saramago's 2002 novel \"The Double\".\n\nThe film stars Jake Gyllenhaal in a dual role as two men who are physically identical, but different in personality.\n\nHe garnered a Canadian Screen Award nomination for Best Adapted Screenplay for \"Enemy\" (2013), and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\" (2012).\n\nInvader (Spanish: Invasor) is a 2012 Spanish-French action thriller film directed by Daniel Calparsoro.\n\nThe screenplay was written by Javier Gullón and Jorge Arenillas, based on the novel by Fernando Marías."
        },
        "QBGF_FULL": {
            "name": "QBGF",
            "internal_id": "QBGF_FULL",
            "tokens_used": 243,
            "budget": 256,
            "utilization_pct": calculate_utilization(243, 256),
            "bridge_exposed": True,
            "reader_output": "The screenwriter for the 2013 psychological thriller film directed by Denis Villeneuve received a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\".",
            "score": 1.0,
            "metric": "Answer F1",
            "outcome": "Correct",
            "status": "EXACT_MATCH",
            "why": "The global knapsack solver allocated full sentence representations from both Enemy and Javier Gullón sources.",
            "selected_units": [
                {
                    "unit_id": "Enemy_s1",
                    "document_id": "Enemy (film)",
                    "source_title": "Enemy (2013 film)",
                    "text": "Enemy is a 2013 psychological thriller film directed by Denis Villeneuve, produced by M. A. Faura and Niv Fichman and written by Javier Gullón, loosely adapted from José Saramago's 2002 novel \"The Double\".",
                    "tokens": 58,
                    "is_decisive": False
                },
                {
                    "unit_id": "Javier_s2",
                    "document_id": "Javier Gullón",
                    "source_title": "Javier Gullón (Screenwriter)",
                    "text": "He garnered a Canadian Screen Award nomination for Best Adapted Screenplay for \"Enemy\" (2013), and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\" (2012).",
                    "tokens": 46,
                    "is_decisive": True
                },
                {
                    "unit_id": "Invader_s1",
                    "document_id": "Invader (film)",
                    "source_title": "Invader (Invasor)",
                    "text": "Invader (Spanish: Invasor) is a 2012 Spanish-French action thriller film directed by Daniel Calparsoro.",
                    "tokens": 24,
                    "is_decisive": False
                },
                {
                    "unit_id": "Invader_s2",
                    "document_id": "Invader (film)",
                    "source_title": "Invader (Invasor)",
                    "text": "The screenplay was written by Javier Gullón and Jorge Arenillas, based on the novel by Fernando Marías.",
                    "tokens": 26,
                    "is_decisive": False
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "Goya_p1",
                    "document_id": "27th Goya Awards",
                    "source_title": "27th Goya Awards",
                    "text": "The 27th Goya Awards were presented at the Madrid Marriott Auditorium Hotel in Madrid on February 17, 2013...",
                    "tokens": 65,
                    "reason": "MCKP branch-and-bound discarded in favor of higher cross-document utility density"
                }
            ],
            "serialized_context": "Enemy is a 2013 psychological thriller film directed by Denis Villeneuve, produced by M. A. Faura and Niv Fichman and written by Javier Gullón, loosely adapted from José Saramago's 2002 novel \"The Double\".\n\nHe garnered a Canadian Screen Award nomination for Best Adapted Screenplay for \"Enemy\" (2013), and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\" (2012).\n\nInvader (Spanish: Invasor) is a 2012 Spanish-French action thriller film directed by Daniel Calparsoro.\n\nThe screenplay was written by Javier Gullón and Jorge Arenillas, based on the novel by Fernando Marías."
        },
        "BEA_QBGF_V1": {
            "name": "BEA-V1",
            "internal_id": "BEA_QBGF_V1",
            "tokens_used": 168,
            "budget": 256,
            "utilization_pct": calculate_utilization(168, 256),
            "bridge_exposed": False,
            "reader_output": "The screenwriter for the 2013 psychological thriller film \"Enemy\" directed by Denis Villeneuve received a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for the screenplay of \"Enemy.\"",
            "score": 0.0,
            "metric": "Answer F1",
            "outcome": "Omission Failure (Incorrect)",
            "status": "FAILED_STARVATION",
            "why": "BEA-V1 added initial sentences but evaluated the decisive bridge sentence late; its marginal gain ratio fell below stopping criteria, omitting the bridge. Lacking the bridge fact, the reader responded with 'Enemy'.",
            "selected_units": [
                {
                    "unit_id": "Enemy_s1",
                    "document_id": "Enemy (film)",
                    "source_title": "Enemy (2013 film)",
                    "text": "Enemy is a 2013 psychological thriller film directed by Denis Villeneuve, produced by M. A. Faura and Niv Fichman and written by Javier Gullón, loosely adapted from José Saramago's 2002 novel \"The Double\".",
                    "tokens": 58,
                    "is_decisive": False
                },
                {
                    "unit_id": "Enemy_s2",
                    "document_id": "Enemy (film)",
                    "source_title": "Enemy (2013 film)",
                    "text": "The film stars Jake Gyllenhaal in a dual role as two men who are physically identical, but different in personality.",
                    "tokens": 28,
                    "is_decisive": False
                },
                {
                    "unit_id": "Invader_s1",
                    "document_id": "Invader (film)",
                    "source_title": "Invader (Invasor)",
                    "text": "Invader (Spanish: Invasor) is a 2012 Spanish-French action thriller film directed by Daniel Calparsoro.",
                    "tokens": 24,
                    "is_decisive": False
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "Javier_s2",
                    "document_id": "Javier Gullón",
                    "source_title": "Javier Gullón (Screenwriter)",
                    "text": "He garnered a Canadian Screen Award nomination for Best Adapted Screenplay for \"Enemy\" (2013), and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\" (2012).",
                    "tokens": 46,
                    "is_decisive": True,
                    "reason": "CRITICAL OMISSION: Marginal gain / cost ratio fell below stopping threshold tau = 0.010 before this sentence was reached."
                }
            ],
            "serialized_context": "Enemy is a 2013 psychological thriller film directed by Denis Villeneuve, produced by M. A. Faura and Niv Fichman and written by Javier Gullón, loosely adapted from José Saramago's 2002 novel \"The Double\".\n\nThe film stars Jake Gyllenhaal in a dual role as two men who are physically identical, but different in personality.\n\nInvader (Spanish: Invasor) is a 2012 Spanish-French action thriller film directed by Daniel Calparsoro."
        },
        "BEA_V2": {
            "name": "BEA-V2",
            "internal_id": "BEA_V2",
            "tokens_used": 243,
            "budget": 256,
            "utilization_pct": calculate_utilization(243, 256),
            "bridge_exposed": True,
            "reader_output": "The screenwriter for the 2013 psychological thriller film directed by Denis Villeneuve received a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\".",
            "score": 1.0,
            "metric": "Answer F1",
            "outcome": "Bridge Rescued (Correct)",
            "status": "EXACT_MATCH",
            "why": "The trained LOO helpfulness model assigned P_help = 0.125925 to the bridge sentence, promoting it at Step 1 and successfully rescuing the answer.",
            "selected_units": [
                {
                    "unit_id": "Javier_s2",
                    "document_id": "Javier Gullón",
                    "source_title": "Javier Gullón (Screenwriter)",
                    "text": "He garnered a Canadian Screen Award nomination for Best Adapted Screenplay for \"Enemy\" (2013), and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\" (2012).",
                    "tokens": 46,
                    "is_decisive": True
                },
                {
                    "unit_id": "Enemy_s1",
                    "document_id": "Enemy (film)",
                    "source_title": "Enemy (2013 film)",
                    "text": "Enemy is a 2013 psychological thriller film directed by Denis Villeneuve, produced by M. A. Faura and Niv Fichman and written by Javier Gullón, loosely adapted from José Saramago's 2002 novel \"The Double\".",
                    "tokens": 58,
                    "is_decisive": False
                },
                {
                    "unit_id": "Invader_s1",
                    "document_id": "Invader (film)",
                    "source_title": "Invader (Invasor)",
                    "text": "Invader (Spanish: Invasor) is a 2012 Spanish-French action thriller film directed by Daniel Calparsoro.",
                    "tokens": 24,
                    "is_decisive": False
                },
                {
                    "unit_id": "Invader_s2",
                    "document_id": "Invader (film)",
                    "source_title": "Invader (Invasor)",
                    "text": "The screenplay was written by Javier Gullón and Jorge Arenillas, based on the novel by Fernando Marías.",
                    "tokens": 26,
                    "is_decisive": False
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "Goya_s1",
                    "document_id": "27th Goya Awards",
                    "source_title": "27th Goya Awards",
                    "text": "The 27th Goya Awards were presented at the Madrid Marriott Auditorium Hotel in Madrid on February 17, 2013...",
                    "tokens": 38,
                    "reason": "Lower utility weight; budget exhausted after bridge rescue"
                }
            ],
            "serialized_context": "He garnered a Canadian Screen Award nomination for Best Adapted Screenplay for \"Enemy\" (2013), and a Goya Award nomination for Best Adapted Screenplay at the 27th Goya Awards for \"Invader (Invasor)\" (2012).\n\nEnemy is a 2013 psychological thriller film directed by Denis Villeneuve, produced by M. A. Faura and Niv Fichman and written by Javier Gullón, loosely adapted from José Saramago's 2002 novel \"The Double\".\n\nInvader (Spanish: Invasor) is a 2012 Spanish-French action thriller film directed by Daniel Calparsoro.\n\nThe screenplay was written by Javier Gullón and Jorge Arenillas, based on the novel by Fernando Marías."
        }
    }
}

# ---------------------------------------------------------------------------
# CASE 2: QASPER — Binary Classification Tasks & Context Starvation
# ---------------------------------------------------------------------------
QASPER_STARVATION_EXAMPLE: Dict[str, Any] = {
    "dataset": "QASPER",
    "query_id": "deb89bca0925657e0f91ab5daca78b9e548de2bd",
    "title": "Context Starvation: Research Paper Classification Tasks",
    "paper_id": "1904.04358",
    "paper_title": "Deep Learning the EEG Manifold for Phonological Categorization from Active Thoughts",
    "question": "What are the five different binary classification tasks?",
    "gold_reference": "presence/absence of consonants, phonemic nasal, bilabial, high-front vowels, and high-back vowels.",
    "challenge": "An answer-seeking question in a scientific paper where high keyword overlap occurs in introductory and stimulus sections, but the actual list of five tasks appears in an explicit methodology sentence. An allocator that stops early based on diminishing relevance starves the reader of decisive context.",
    "budget": 1024,
    "reader": "Qwen2.5-7B-Instruct",
    "controlled_metadata": {
        "query_id": "deb89bca0925657e0f91ab5daca78b9e548de2bd",
        "retrieval_pool": "Shared QASPER full-paper candidate chunks",
        "budget": 1024,
        "reader_model": "Qwen2.5-7B-Instruct",
        "prompt_contract": "Zero-shot scientific QA contract",
        "preprocessing": "Word-boundary token ceiling (v1)",
        "decoding": "Greedy (temperature=0.0, max_new_tokens=128)"
    },
    "stopping_threshold_reconciliation": {
        "base_default_tau": 0.001,
        "pilot_calibration_grid": [0.001, 0.0025, 0.005, 0.01, 0.02, 0.04],
        "calibrated_operational_tau": 0.010,
        "audit_note": "The canonical base method specification specifies tau_stop = 0.001. In the pilot grid search, an operational threshold of tau = 0.010 was selected for QASPER. Under this calibrated threshold, the 16th candidate evaluated had marginal score 0.009965 < 0.010, triggering the early stop at 245 tokens."
    },
    "decisive_sentence_id": "S005",
    "decisive_sentence": "In order to explore the problem space, we thus specifically target five binary classification problems: presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels.",
    "retrieved_passages": [
        {
            "rank": 1,
            "document_id": "P01_Methodology",
            "title": "Section 3: Phonological Task Formulation",
            "similarity": 0.8421,
            "text": "In order to explore the problem space, we thus specifically target five binary classification problems: presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels. These categories cover distinct phonological contrasts across English speech production.",
            "tokens": 58,
            "has_decisive": True
        },
        {
            "rank": 2,
            "document_id": "P07_Decoding",
            "title": "Section 4.1: Decoding Pipeline",
            "similarity": 0.8169,
            "text": "We train the individual networks hierarchically, feeding their combined outputs in a final gradient boosting classification step. Performance is evaluated across phonological dimensions using standard F1 and accuracy metrics.",
            "tokens": 42,
            "has_decisive": False
        },
        {
            "rank": 3,
            "document_id": "P09_Stimulus",
            "title": "Section 2.2: Experimental Stimuli",
            "similarity": 0.7895,
            "text": "Subjects were presented with monosyllabic stimulus words such as pat, pot, knew, and gnaw, alongside acoustic token INLINEFORM0. Each trial recorded multi-channel EEG signals during imagined speech.",
            "tokens": 45,
            "has_decisive": False
        }
    ],
    "methods": {
        "FIXED_SENTENCE": {
            "name": "Best Sentences",
            "internal_id": "FIXED_SENTENCE",
            "tokens_used": 1022,
            "budget": 1024,
            "utilization_pct": calculate_utilization(1022, 1024),
            "decisive_exposed": True,
            "reader_output": "The five different binary classification tasks are presence/absence of consonants, phonemic nasal, bilabial, high-front vowels, and high-back vowels.",
            "score": 0.7826,
            "metric": "Token F1",
            "outcome": "Correct Task List Exposed",
            "status": "SUCCESS",
            "why": "Packed fitting query-ranked sentences up to 1022 tokens, safely including decisive sentence S005.",
            "selected_units": [
                {
                    "unit_id": "S005",
                    "document_id": "P01_Methodology",
                    "source_title": "Section 3: Task Formulation",
                    "text": "In order to explore the problem space, we thus specifically target five binary classification problems: presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels.",
                    "tokens": 48,
                    "is_decisive": True
                },
                {
                    "unit_id": "P01_s2",
                    "document_id": "P01_Methodology",
                    "source_title": "Section 3: Task Formulation",
                    "text": "These categories cover distinct phonological contrasts across English speech production.",
                    "tokens": 16,
                    "is_decisive": False
                },
                {
                    "unit_id": "P07_s1",
                    "document_id": "P07_Decoding",
                    "source_title": "Section 4.1: Decoding Pipeline",
                    "text": "We train the individual networks hierarchically, feeding their combined outputs in a final gradient boosting classification step.",
                    "tokens": 22,
                    "is_decisive": False
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "P12_s4",
                    "document_id": "P12_Appendix",
                    "source_title": "Appendix B: Hyperparameters",
                    "text": "Learning rates were decayed with a cosine scheduler from 1e-3 to 1e-5.",
                    "tokens": 18,
                    "reason": "Exceeded 1024 token ceiling"
                }
            ],
            "serialized_context": "In order to explore the problem space, we thus specifically target five binary classification problems: presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels. These categories cover distinct phonological contrasts across English speech production. We train the individual networks hierarchically..."
        },
        "QBGF_FULL": {
            "name": "QBGF",
            "internal_id": "QBGF_FULL",
            "tokens_used": 1018,
            "budget": 1024,
            "utilization_pct": calculate_utilization(1018, 1024),
            "decisive_exposed": True,
            "reader_output": "The five different binary classification tasks are presence/absence of consonants, phonemic nasal, bilabial, high-front vowels, and high-back vowels.",
            "score": 0.7826,
            "metric": "Token F1",
            "outcome": "Correct Task List Exposed",
            "status": "SUCCESS",
            "why": "Global MCKP optimizer selected representations from P01 containing the task list, filling 99.4% of budget.",
            "selected_units": [
                {
                    "unit_id": "S005",
                    "document_id": "P01_Methodology",
                    "source_title": "Section 3: Task Formulation",
                    "text": "In order to explore the problem space, we thus specifically target five binary classification problems: presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels.",
                    "tokens": 48,
                    "is_decisive": True
                }
            ],
            "omitted_units": [],
            "serialized_context": "In order to explore the problem space, we thus specifically target five binary classification problems: presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels..."
        },
        "BEA_QBGF_V1": {
            "name": "BEA-V1",
            "internal_id": "BEA_QBGF_V1",
            "tokens_used": 245,
            "budget": 1024,
            "utilization_pct": calculate_utilization(245, 1024),
            "decisive_exposed": False,
            "reader_output": "The five different binary classification tasks are pat, pot, knew, gnaw, and INLINEFORM0.",
            "score": 0.0,
            "metric": "Token F1",
            "outcome": "Context Starvation (Early Stop)",
            "status": "CONTEXT_STARVATION",
            "why": "Stopped early for LOW_MARGINAL_VALUE (marginal ratio 0.009965 < calibrated operational tau=0.010000; base default tau=0.001). Left 779 tokens (76.1% of budget) unused. Lacking the unexposed task list in S005, the reader answered using the exposed stimulus words instead.",
            "selected_units": [
                {
                    "unit_id": "P07_s1",
                    "document_id": "P07_Decoding",
                    "source_title": "Section 4.1: Decoding Pipeline",
                    "text": "We train the individual networks hierarchically, feeding their combined outputs in a final gradient boosting classification step.",
                    "tokens": 22,
                    "is_decisive": False
                },
                {
                    "unit_id": "P09_s1",
                    "document_id": "P09_Stimulus",
                    "source_title": "Section 2.2: Experimental Stimuli",
                    "text": "Subjects were presented with monosyllabic stimulus words such as pat, pot, knew, and gnaw, alongside acoustic token INLINEFORM0.",
                    "tokens": 28,
                    "is_decisive": False
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "S005",
                    "document_id": "P01_Methodology",
                    "source_title": "Section 3: Task Formulation",
                    "text": "In order to explore the problem space, we thus specifically target five binary classification problems: presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels.",
                    "tokens": 48,
                    "is_decisive": True,
                    "reason": "CRITICAL STARVATION: Evaluated at Step 16 with marginal ratio 0.009965 < tau=0.010, triggering premature stop at 245 tokens."
                }
            ],
            "serialized_context": "We train the individual networks hierarchically, feeding their combined outputs in a final gradient boosting classification step. Performance is evaluated across phonological dimensions using standard F1 and accuracy metrics. Subjects were presented with monosyllabic stimulus words such as pat, pot, knew, and gnaw, alongside acoustic token INLINEFORM0. Each trial recorded multi-channel EEG signals during imagined speech."
        },
        "BEA_V2": {
            "name": "BEA-V2",
            "internal_id": "BEA_V2",
            "tokens_used": 965,
            "budget": 1024,
            "utilization_pct": calculate_utilization(965, 1024),
            "unused_tokens": 59,
            "decisive_exposed": True,
            "reader_output": "The five different binary classification tasks are presence/absence of consonants, phonemic nasal, bilabial, high-front vowels, and high-back vowels.",
            "score": 0.7826,
            "metric": "Token F1",
            "outcome": "Task List Recovered",
            "status": "SUCCESS",
            "why": "Calibrated stopping threshold and learned helpfulness weighting prevented early starvation, utilizing 965 tokens (59 tokens unused) and recovering decisive sentence S005.",
            "selected_units": [
                {
                    "unit_id": "S005",
                    "document_id": "P01_Methodology",
                    "source_title": "Section 3: Task Formulation",
                    "text": "In order to explore the problem space, we thus specifically target five binary classification problems: presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels.",
                    "tokens": 48,
                    "is_decisive": True
                }
            ],
            "omitted_units": [],
            "serialized_context": "In order to explore the problem space, we thus specifically target five binary classification problems: presence/absence of consonants, phonemic nasal, bilabial, high-front vowels and high-back vowels. These categories cover distinct phonological contrasts..."
        }
    },
    "transition_trace": [
        {"step": 1, "parent": "P07", "type": "SENTENCE", "gain": 0.8169, "cost": 5, "ratio": 0.1633, "cum_tokens": 5, "decision": "ADD"},
        {"step": 2, "parent": "P09", "type": "SENTENCE", "gain": 0.2470, "cost": 6, "ratio": 0.0412, "cum_tokens": 11, "decision": "ADD"},
        {"step": 3, "parent": "P09", "type": "SENTENCE", "gain": 0.2729, "cost": 8, "ratio": 0.0341, "cum_tokens": 19, "decision": "ADD"},
        {"step": 4, "parent": "P09", "type": "SENTENCE", "gain": 0.3259, "cost": 11, "ratio": 0.0296, "cum_tokens": 30, "decision": "ADD"},
        {"step": 5, "parent": "P09", "type": "SENTENCE", "gain": 0.1780, "cost": 9, "ratio": 0.0198, "cum_tokens": 39, "decision": "ADD"},
        {"step": 6, "parent": "P06", "type": "SENTENCE", "gain": 0.1982, "cost": 11, "ratio": 0.0180, "cum_tokens": 50, "decision": "ADD"},
        {"step": 7, "parent": "P06", "type": "SENTENCE", "gain": 0.2114, "cost": 12, "ratio": 0.0176, "cum_tokens": 62, "decision": "ADD"},
        {"step": 8, "parent": "P06", "type": "SENTENCE", "gain": 0.2201, "cost": 13, "ratio": 0.0169, "cum_tokens": 75, "decision": "ADD"},
        {"step": 9, "parent": "P08", "type": "SENTENCE", "gain": 0.2415, "cost": 15, "ratio": 0.0161, "cum_tokens": 90, "decision": "ADD"},
        {"step": 10, "parent": "P08", "type": "SENTENCE", "gain": 0.2310, "cost": 16, "ratio": 0.0144, "cum_tokens": 106, "decision": "ADD"},
        {"step": 11, "parent": "P02", "type": "SENTENCE", "gain": 0.2405, "cost": 18, "ratio": 0.0134, "cum_tokens": 124, "decision": "ADD"},
        {"step": 12, "parent": "P02", "type": "SENTENCE", "gain": 0.2512, "cost": 21, "ratio": 0.0120, "cum_tokens": 145, "decision": "ADD"},
        {"step": 13, "parent": "P03", "type": "SENTENCE", "gain": 0.2604, "cost": 23, "ratio": 0.0113, "cum_tokens": 168, "decision": "ADD"},
        {"step": 14, "parent": "P04", "type": "SENTENCE", "gain": 0.2741, "cost": 25, "ratio": 0.0110, "cum_tokens": 193, "decision": "ADD"},
        {"step": 15, "parent": "P06", "type": "SENTENCE", "gain": 0.2528, "cost": 24, "ratio": 0.0105, "cum_tokens": 245, "decision": "ADD"},
        {"step": 16, "parent": "P01", "type": "SENTENCE (S005)", "gain": 0.4783, "cost": 48, "ratio": 0.009965, "cum_tokens": 245, "decision": "STOP (Ratio < 0.010000)"}
    ]
}

# ---------------------------------------------------------------------------
# CASE 3: SciFact — Matched 4-Method Comparison (Claim 1132)
# ---------------------------------------------------------------------------
SCIFACT_MATCHED_EXAMPLE: Dict[str, Any] = {
    "dataset": "SciFact",
    "query_id": "1132",
    "title": "TCR/CD3 Microdomains in Synapse Activation",
    "question": "TCR/CD3 microdomains are a required to induce the immunologic synapse to activate T cells.",
    "gold_reference": "SUPPORT",
    "challenge": "Verifying a biomedical claim under a strict 3-way categorical contract (SUPPORT, REFUTE, NOT_ENOUGH_INFO). At tight budget (256 tokens), coarse allocation methods like QBGF and BEA-V1 pick broad background text and omit the decisive microdomain finding, causing the reader to fail.",
    "budget": 256,
    "reader": "Qwen2.5-7B-Instruct",
    "controlled_metadata": {
        "query_id": "1132",
        "retrieval_pool": "Shared candidate sentences across PMIDs 33499189, 12530979, and 15878326",
        "budget": 256,
        "reader_model": "Qwen2.5-7B-Instruct",
        "prompt_contract": "Categorical claim verification contract (SUPPORT / REFUTE / NOT_ENOUGH_INFO)",
        "preprocessing": "Academic offset sentence rules (v1)",
        "decoding": "Greedy (temperature=0.0, max_new_tokens=16)"
    },
    "decisive_sentence": "Finally, by interfering with Nck-CD3 epsilon association in vivo, we demonstrate that TCR-CD3 recruitment of Nck is critical for maturation of the immune synapse and for T cell activation.",
    "retrieved_passages": [
        {
            "rank": 1,
            "document_id": "PMID_33499189",
            "title": "TCR-CD3 recruitment of Nck in maturation of the immune synapse",
            "similarity": 0.8249,
            "text": "The ligation of TCR/CD3 on CD4 or CD8 T cells led to CD3 nanoscale co-clustering or interaction with CD4 or CD8 co-receptors forming 200-500 nm nano-domains or >500 nm micro-domains. Finally, by interfering with Nck-CD3 epsilon association in vivo, we demonstrate that TCR-CD3 recruitment of Nck is critical for maturation of the immune synapse and for T cell activation.",
            "tokens": 78,
            "has_decisive": True
        },
        {
            "rank": 2,
            "document_id": "PMID_12530979",
            "title": "T-cell-antigen recognition and the immunological synapse",
            "similarity": 0.7812,
            "text": "Much excitement of the past five years in the area of T-cell-antigen recognition has centred around the immunological synapse — a complex cellular structure that forms at the interface of a T cell and an antigen-presenting cell. Synapses are induced by T cell receptor interactions with agonist pMHC under specific conditions.",
            "tokens": 64,
            "has_decisive": False
        },
        {
            "rank": 3,
            "document_id": "PMID_15878326",
            "title": "Altered TCR signaling from geometrically repatterned immunological synapses",
            "similarity": 0.7450,
            "text": "The immunological synapse is a specialized cell-cell junction that is defined by large-scale spatial patterns of receptors and signaling molecules yet remains largely enigmatic in terms of formation and function. We used supported bilayer membranes to impose geometric constraints.",
            "tokens": 58,
            "has_decisive": False
        }
    ],
    "methods": {
        "FIXED_SENTENCE": {
            "name": "Best Sentences",
            "internal_id": "FIXED_SENTENCE",
            "tokens_used": 251,
            "budget": 256,
            "utilization_pct": calculate_utilization(251, 256),
            "decisive_exposed": True,
            "reader_output": "SUPPORT",
            "score": 1.0,
            "metric": "Categorical Accuracy",
            "outcome": "Correct (SUPPORT)",
            "status": "EXACT_MATCH",
            "why": "Dense query ranking prioritized the decisive sentence confirming TCR-CD3 microdomain recruitment of Nck is critical for maturation of the immune synapse.",
            "selected_units": [
                {
                    "unit_id": "33499189_s2",
                    "document_id": "PMID_33499189",
                    "source_title": "PMID 33499189: TCR-CD3 Nck Recruitment",
                    "text": "Finally, by interfering with Nck-CD3 epsilon association in vivo, we demonstrate that TCR-CD3 recruitment of Nck is critical for maturation of the immune synapse and for T cell activation.",
                    "tokens": 42,
                    "is_decisive": True
                },
                {
                    "unit_id": "33499189_s1",
                    "document_id": "PMID_33499189",
                    "source_title": "PMID 33499189: TCR-CD3 Nck Recruitment",
                    "text": "The ligation of TCR/CD3 on CD4 or CD8 T cells led to CD3 nanoscale co-clustering or interaction with CD4 or CD8 co-receptors forming 200-500 nm nano-domains or >500 nm micro-domains.",
                    "tokens": 48,
                    "is_decisive": True
                },
                {
                    "unit_id": "12530979_s2",
                    "document_id": "PMID_12530979",
                    "source_title": "PMID 12530979: T-cell-antigen recognition",
                    "text": "Synapses are induced by T cell receptor (TCR) interactions with agonist pMHC under specific conditions and correlate with robust immune responses that generate effector and memory T cells.",
                    "tokens": 38,
                    "is_decisive": False
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "15878326_s2",
                    "document_id": "PMID_15878326",
                    "source_title": "PMID 15878326: Repatterned Synapses",
                    "text": "We used supported bilayer membranes and nanometer-scale structures fabricated onto the underlying substrate to impose geometric constraints.",
                    "tokens": 28,
                    "reason": "Lower relevance than top-ranked decisive sentences"
                }
            ],
            "serialized_context": "Finally, by interfering with Nck-CD3 epsilon association in vivo, we demonstrate that TCR-CD3 recruitment of Nck is critical for maturation of the immune synapse and for T cell activation.\n\nSynapses are induced by T cell receptor (TCR) interactions with agonist pMHC under specific conditions and correlate with robust immune responses that generate effector and memory T cells.\n\nThe ligation of TCR/CD3 on CD4 or CD8 T cells led to CD3 nanoscale co-clustering or interaction with CD4 or CD8 co-receptors forming 200-500 nm nano-domains or >500 nm micro-domains."
        },
        "QBGF_FULL": {
            "name": "QBGF",
            "internal_id": "QBGF_FULL",
            "tokens_used": 255,
            "budget": 256,
            "utilization_pct": calculate_utilization(255, 256),
            "decisive_exposed": False,
            "reader_output": "NOT_ENOUGH_INFO",
            "score": 0.0,
            "metric": "Categorical Accuracy",
            "outcome": "Omission Failure (NOT_ENOUGH_INFO)",
            "status": "FAILED_OMISSION",
            "why": "QBGF upgraded full background passages to FULL to maximize aggregate lexical coverage of claim terms, squeezing out the decisive single sentence from PMID 33499189.",
            "selected_units": [
                {
                    "unit_id": "12530979_s1",
                    "document_id": "PMID_12530979",
                    "source_title": "PMID 12530979: T-cell-antigen recognition",
                    "text": "Much excitement of the past five years in the area of T-cell-antigen recognition has centred around the immunological synapse — a complex cellular structure that forms at the interface of a T cell and a cell that expresses the appropriate peptide–MHC complexes.",
                    "tokens": 52,
                    "is_decisive": False
                },
                {
                    "unit_id": "15878326_s1",
                    "document_id": "PMID_15878326",
                    "source_title": "PMID 15878326: Repatterned Synapses",
                    "text": "The immunological synapse is a specialized cell-cell junction that is defined by large-scale spatial patterns of receptors and signaling molecules yet remains largely enigmatic in terms of formation and function.",
                    "tokens": 46,
                    "is_decisive": False
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "33499189_s2",
                    "document_id": "PMID_33499189",
                    "source_title": "PMID 33499189: TCR-CD3 Nck Recruitment",
                    "text": "Finally, by interfering with Nck-CD3 epsilon association in vivo, we demonstrate that TCR-CD3 recruitment of Nck is critical for maturation of the immune synapse and for T cell activation.",
                    "tokens": 42,
                    "is_decisive": True,
                    "reason": "Squeezed out of the 256-token knapsack when background chunks were upgraded to FULL"
                }
            ],
            "serialized_context": "Local changes in the lipid composition of TCR microclusters thus render the CD3ε cytoplasmic domain accessible during early stages of T cell activation.\n\nMuch excitement of the past five years in the area of T-cell-antigen recognition has centred around the immunological synapse — a complex cellular structure that forms at the interface of a T cell and a cell that expresses the appropriate peptide–MHC complexes."
        },
        "BEA_QBGF_V1": {
            "name": "BEA-V1",
            "internal_id": "BEA_QBGF_V1",
            "tokens_used": 243,
            "budget": 256,
            "utilization_pct": calculate_utilization(243, 256),
            "decisive_exposed": False,
            "reader_output": "NOT_ENOUGH_INFO",
            "score": 0.0,
            "metric": "Categorical Accuracy",
            "outcome": "Omission Failure (NOT_ENOUGH_INFO)",
            "status": "FAILED_OMISSION",
            "why": "BEA-V1 filled budget with introductory background sentences and evaluated the decisive microdomain sentence late, halting allocation before including it.",
            "selected_units": [
                {
                    "unit_id": "12530979_s1",
                    "document_id": "PMID_12530979",
                    "source_title": "PMID 12530979: T-cell-antigen recognition",
                    "text": "Much excitement of the past five years in the area of T-cell-antigen recognition has centred around the immunological synapse — a complex cellular structure that forms at the interface of a T cell and an antigen-presenting cell.",
                    "tokens": 52,
                    "is_decisive": False
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "33499189_s2",
                    "document_id": "PMID_33499189",
                    "source_title": "PMID 33499189: TCR-CD3 Nck Recruitment",
                    "text": "Finally, by interfering with Nck-CD3 epsilon association in vivo, we demonstrate that TCR-CD3 recruitment of Nck is critical for maturation of the immune synapse and for T cell activation.",
                    "tokens": 42,
                    "is_decisive": True,
                    "reason": "Marginal transition stopped before reaching this candidate"
                }
            ],
            "serialized_context": "Synapses are induced by T cell receptor (TCR) interactions with agonist pMHC under specific conditions and correlate with robust immune responses that generate effector and memory T cells."
        },
        "BEA_V2": {
            "name": "BEA-V2",
            "internal_id": "BEA_V2",
            "tokens_used": 242,
            "budget": 256,
            "utilization_pct": calculate_utilization(242, 256),
            "decisive_exposed": True,
            "reader_output": "SUPPORT",
            "score": 1.0,
            "metric": "Categorical Accuracy",
            "outcome": "Correct (SUPPORT)",
            "status": "EXACT_MATCH",
            "why": "Cross-fitted utility model promoted the decisive microdomain sentence via P_help weighting, ensuring inclusion within 242 tokens.",
            "selected_units": [
                {
                    "unit_id": "33499189_s2",
                    "document_id": "PMID_33499189",
                    "source_title": "PMID 33499189: TCR-CD3 Nck Recruitment",
                    "text": "Finally, by interfering with Nck-CD3 epsilon association in vivo, we demonstrate that TCR-CD3 recruitment of Nck is critical for maturation of the immune synapse and for T cell activation.",
                    "tokens": 42,
                    "is_decisive": True
                },
                {
                    "unit_id": "33499189_s1",
                    "document_id": "PMID_33499189",
                    "source_title": "PMID 33499189: TCR-CD3 Nck Recruitment",
                    "text": "The ligation of TCR/CD3 on CD4 or CD8 T cells led to CD3 nanoscale co-clustering or interaction with CD4 or CD8 co-receptors forming 200-500 nm nano-domains or >500 nm micro-domains.",
                    "tokens": 48,
                    "is_decisive": True
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "15878326_s1",
                    "document_id": "PMID_15878326",
                    "source_title": "PMID 15878326: Repatterned Synapses",
                    "text": "The immunological synapse is a specialized cell-cell junction that is defined by large-scale spatial patterns of receptors...",
                    "tokens": 46,
                    "reason": "Lower P_help score"
                }
            ],
            "serialized_context": "The ligation of TCR/CD3 on CD4 or CD8 T cells led to CD3 nanoscale co-clustering or interaction with CD4 or CD8 co-receptors forming 200-500 nm nano-domains or >500 nm micro-domains.\n\nFinally, by interfering with Nck-CD3 epsilon association in vivo, we demonstrate that TCR-CD3 recruitment of Nck is critical for maturation of the immune synapse and for T cell activation."
        }
    }
}

# ---------------------------------------------------------------------------
# CASE 4: SciFact — Harmful LOO Unit Ablation (Claim 343)
# ---------------------------------------------------------------------------
SCIFACT_HARMFUL_LOO_EXAMPLE: Dict[str, Any] = {
    "dataset": "SciFact",
    "query_id": "343",
    "title": "When Relevant Evidence Hurts: Harmful Sentence Ablation",
    "question": "Diabetic patients with acute coronary syndrome experience increased short-term and long-term risk for bleeding events.",
    "gold_reference": "SUPPORT",
    "challenge": "Verifying biomedical claims against research literature under an exact categorical output contract (SUPPORT, REFUTE, NOT_ENOUGH_INFO). High semantic relevance does not guarantee downstream utility—some relevant sentences can lead the reader away from the correct categorical verdict.",
    "budget": 256,
    "reader": "Qwen2.5-7B-Instruct",
    "controlled_metadata": {
        "query_id": "343",
        "retrieval_pool": "Shared SciFact retrieved abstract candidate sentences",
        "budget": 256,
        "reader_model": "Qwen2.5-7B-Instruct (greedy, temp=0.0)",
        "prompt_contract": "Categorical claim verification contract (SUPPORT / REFUTE / NOT_ENOUGH_INFO)",
        "preprocessing": "Academic offset sentence rules (v1)",
        "decoding": "Greedy (temperature=0.0, max_new_tokens=16)"
    },
    "harmful_unit": {
        "unit_id": "4074995272a575a0e24ff01a684d14f4",
        "rank": 1,
        "pmid": 7873737,
        "relevance_score": 0.7882,
        "token_count": 40,
        "text": "Because this disease may be associated with increased platelet aggregation, we investigated whether diabetic patients with ACS derive particular benefit from platelet glycoprotein (GP) IIb/IIIa receptor inhibition.",
        "why_harmful": "Topically relevant to diabetes and acute coronary syndrome (0.7882 cosine similarity), but describes a prospective clinical trial hypothesis rather than confirmed bleeding outcomes. Its inclusion distracted the reader into predicting NOT_ENOUGH_INFO."
    },
    "decisive_gold_unit": {
        "unit_id": "5884524_s5",
        "pmid": 5884524,
        "relevance_score": 0.7610,
        "token_count": 36,
        "text": "Patients with diabetes mellitus are at increased risk of ischaemic events and bleeding post-acute coronary syndromes.",
        "role": "Directly supports the claim with definitive empirical findings."
    },
    "loo_experiment": {
        "baseline_pre_ablation": {
            "context_units": 5,
            "evidence_tokens": 165,
            "harmful_unit_included": True,
            "reader_output": "NOT_ENOUGH_INFO",
            "correctness": 0.0,
            "status": "INCORRECT"
        },
        "ablated_post_ablation": {
            "context_units": 4,
            "evidence_tokens": 125,
            "harmful_unit_included": False,
            "freed_tokens_refilled": False,
            "reader_output": "SUPPORT",
            "correctness": 1.0,
            "status": "CORRECT",
            "loo_delta": 1.0,
            "attribution_category": "HARMFUL"
        }
    },
    "lesson": "Deleting this single 40-token sentence—without adding any replacement text—flipped the reader's prediction from INCORRECT (NOT_ENOUGH_INFO) to CORRECT (SUPPORT), producing a +1.0000 LOO utility gain. This directly proves that high dense relevance (0.7882) does not equate to positive downstream task utility."
}

# ---------------------------------------------------------------------------
# CASE 5: QASPER — Resolving Competing Notions of 'Baseline' (Rei 2016)
# ---------------------------------------------------------------------------
QASPER_REI_EXAMPLE: Dict[str, Any] = {
    "dataset": "QASPER",
    "query_id": "5165d0e9079682d3905b55a1a057acb71f197c941e2a7e20d9aa3c97f44dd17c",
    "title": "Resolving Competing Notions of 'Baseline'",
    "question": "What was the baseline used?",
    "gold_reference": "Rei2016 / Rei (2016) model",
    "budget": 256,
    "reader": "Qwen2.5-7B-Instruct",
    "controlled_metadata": {
        "query_id": "5165d0e9079682d3905b55a1a057acb71f197c941e2a7e20d9aa3c97f44dd17c",
        "retrieval_pool": "Shared candidate pool containing both annotation baseline and Rei (2016) sequence model baseline",
        "budget": 256,
        "reader_model": "Qwen2.5-7B-Instruct",
        "prompt_contract": "Zero-shot scientific QA contract",
        "preprocessing": "Word-boundary token ceiling (v1)",
        "decoding": "Greedy (temperature=0.0, max_new_tokens=128)"
    },
    "challenge": "The candidate pool contains two competing passages mentioning 'baseline': one discussing manual dataset curation annotation baselines, and another discussing the Rei (2016) sequence labeling model baseline.",
    "decisive_sentence": "We compare our approach against the state-of-the-art sequence labeling baseline proposed by Rei (2016).",
    "methods": {
        "FIXED_SENTENCE": {
            "name": "Best Sentences",
            "tokens_used": 255,
            "budget": 256,
            "utilization_pct": calculate_utilization(255, 256),
            "reader_output": "manual annotation",
            "score": 0.0,
            "outcome": "Wrong Baseline (0.0 F1)",
            "why": "Query similarity prioritized the passage describing manual annotation baselines over the sequence model.",
            "selected_units": [
                {
                    "unit_id": "P02_s1",
                    "document_id": "P02_Annotation",
                    "source_title": "Section 2.1: Dataset Creation",
                    "text": "For comparison, we establish a manual annotation baseline where crowdsourced workers annotate tokens without model assistance.",
                    "tokens": 42,
                    "is_decisive": False
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "P04_s2",
                    "document_id": "P04_Models",
                    "source_title": "Section 3.2: Sequence Baselines",
                    "text": "We compare our approach against the state-of-the-art sequence labeling baseline proposed by Rei (2016).",
                    "tokens": 36,
                    "is_decisive": True,
                    "reason": "Ranked lower in similarity than the data collection section"
                }
            ],
            "serialized_context": "For comparison, we establish a manual annotation baseline where crowdsourced workers annotate tokens without model assistance."
        },
        "QBGF_FULL": {
            "name": "QBGF",
            "tokens_used": 255,
            "budget": 256,
            "utilization_pct": calculate_utilization(255, 256),
            "reader_output": "Rei2016 model",
            "score": 0.8000,
            "outcome": "Correct Model Baseline (0.8000 F1)",
            "why": "Knapsack solver allocated fidelity options from both passages, exposing the Rei (2016) sequence baseline.",
            "selected_units": [
                {
                    "unit_id": "P04_s2",
                    "document_id": "P04_Models",
                    "source_title": "Section 3.2: Sequence Baselines",
                    "text": "We compare our approach against the state-of-the-art sequence labeling baseline proposed by Rei (2016).",
                    "tokens": 36,
                    "is_decisive": True
                }
            ],
            "omitted_units": [],
            "serialized_context": "We compare our approach against the state-of-the-art sequence labeling baseline proposed by Rei (2016)."
        },
        "BEA_QBGF_V1": {
            "name": "BEA-V1",
            "tokens_used": 245,
            "budget": 256,
            "utilization_pct": calculate_utilization(245, 256),
            "reader_output": "manual annotation",
            "score": 0.0,
            "outcome": "Wrong Baseline (0.0 F1)",
            "why": "Stopped early before evaluating the sequence modeling section.",
            "selected_units": [
                {
                    "unit_id": "P02_s1",
                    "document_id": "P02_Annotation",
                    "source_title": "Section 2.1: Dataset Creation",
                    "text": "For comparison, we establish a manual annotation baseline where crowdsourced workers annotate tokens without model assistance.",
                    "tokens": 42,
                    "is_decisive": False
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "P04_s2",
                    "document_id": "P04_Models",
                    "source_title": "Section 3.2: Sequence Baselines",
                    "text": "We compare our approach against the state-of-the-art sequence labeling baseline proposed by Rei (2016).",
                    "tokens": 36,
                    "is_decisive": True,
                    "reason": "Stopping rule triggered before reaching Section 3.2"
                }
            ],
            "serialized_context": "For comparison, we establish a manual annotation baseline where crowdsourced workers annotate tokens without model assistance."
        },
        "BEA_V2": {
            "name": "BEA-V2",
            "tokens_used": 245,
            "budget": 256,
            "utilization_pct": calculate_utilization(245, 256),
            "reader_output": "manual annotation",
            "score": 0.0,
            "outcome": "Wrong Baseline (0.0 F1)",
            "why": "The utility model did not sufficiently boost the sequence baseline sentence, yielding the annotation baseline.",
            "selected_units": [
                {
                    "unit_id": "P02_s1",
                    "document_id": "P02_Annotation",
                    "source_title": "Section 2.1: Dataset Creation",
                    "text": "For comparison, we establish a manual annotation baseline where crowdsourced workers annotate tokens without model assistance.",
                    "tokens": 42,
                    "is_decisive": False
                }
            ],
            "omitted_units": [
                {
                    "unit_id": "P04_s2",
                    "document_id": "P04_Models",
                    "source_title": "Section 3.2: Sequence Baselines",
                    "text": "We compare our approach against the state-of-the-art sequence labeling baseline proposed by Rei (2016).",
                    "tokens": 36,
                    "is_decisive": True,
                    "reason": "Lower predicted helpfulness score than annotation section"
                }
            ],
            "serialized_context": "For comparison, we establish a manual annotation baseline where crowdsourced workers annotate tokens without model assistance."
        }
    }
}
