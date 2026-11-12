# RECOMP published-paper results — literature only

Source: [ICLR2024 paper](paper/recomp_iclr_2024.pdf), physical page7, Table2. [Official paper](https://proceedings.iclr.cc/paper_files/paper/2024/file/bda88ed2892f5e61c9a9bf215c566913-Paper-Conference.pdf). The reader is Flan-UL2(20B); these are paper-reported HotpotQA results, not project runs.

| Paper setting | Evidence tokens | EM | F1 |
| --- | ---: | ---: | ---: |
| Top5documents, no compression |684|32.80|43.90|
| Learned extractive compressor |75|30.40|40.14|
| Learned abstractive compressor |64|28.20|37.91|

This illustrates the paper’s quality/context trade-off under its own setup. It does not supply a missing matched RECOMP score for our project.
