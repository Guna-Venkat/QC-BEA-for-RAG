# Project RAG and simple granularity controls

These are project protocol controls, not claimed imports of a single new baseline paper. SFR is the pinned [Salesforce embedding model](https://huggingface.co/Salesforce/SFR-Embedding-Mistral); BM25 is the lexical retrieval control.

- code/1_retrieval_and_scoring.py: Lab.prepare ranks the passage pool and scores source units.
- code/2_raw_skip_sentence_and_h3_allocator.py: choose/serialize implement NONE, RAW_SKIP, FIXED_SENTENCE, C2 and H3; QBGF is separately explained in5_qbgf.
- code/3_bm25_retriever.py: actual lexical scoring utility.
- configs/: exact shared reader/retrieval protocol.
- project_results/: recorded merged validation and paired extension tables, not recomputed here.

BM25_PLAIN_RAG and SFR_PLAIN_RAG mean budget-matched RAW_SKIP whole-passage RAG at256/1024, not unrestricted full-context RAG. FIXED_SENTENCE has no top8 cap; C2 is the separate top8 control. H3 is the prevalidated hierarchical control. Reader/prompt/parser/budget identities remain frozen.

These controls are distinct from adapted-Mistral SARA specialist references and external paper-only RECOMP scores.
