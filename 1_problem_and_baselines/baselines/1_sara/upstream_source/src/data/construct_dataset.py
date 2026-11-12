import os
import random
import sys
import json

from datasets import load_dataset, Dataset
from tqdm import tqdm





from src.data.construct_finetuning_data import extract_answer_and_question_type_qasper
from src.arguments import parse_args
from src.utils.data_utils import (
    write_jsonl
)

args = parse_args('train')

# Construct dataset for pretraining


for split in ['train', 'test']:
    pretrain_data = []
    data = load_dataset("allenai/qasper", split=split)
    for row_index, row in enumerate(tqdm(data, desc=f"{args.dataset_name} - {split}")):
        paragraphs = row['full_text']['paragraphs']
        num_sections = len(paragraphs)
        for index_section in range(num_sections):
            pretrain_data += [" ".join(paragraphs[index_section])]

    # Filter out examples that are too short
    pretrain_data = [{"id": index, "text": text} for index, text in enumerate(pretrain_data) if len(text.strip()) > 30]

    # This is the demo data for pretraining on QASPER paragraphs
    with open(f"data/pretrain_data_qasper_{split}.json", "w") as f:
        json.dump(pretrain_data, f, indent=2)

templates_for_qa = [
    "Question: {question}",
    "{question}",
    "Answer the following question:\n\n{question}",
    "Answer this question:\n\n{question}?",
    "Provide an answer to the question: {question}",
    "What would be the response to: {question}",
    "What is the answer to this question: {question}",
    "Can you provide the answer to the question: {question}",
    "Here's a question for you: {question}",
    "Provide the answer to the following inquiry: {question}",
    "What should be the response for the question: {question}",
    "Provide a brief answer for: {question}",
    "Solve this question: {question}",
]

training_questions = []
training_answers = []
training_evidence = []
training_examples = {
    "messages": [],
    "background": [],
    "answerable": []
}

# ds = load_dataset("qiaojin/PubMedQA", "pqa_artificial")

"""

"""

# # Generating validation data
# ds = load_dataset("rajpurkar/squad_v2")
# for split in ['validation']:
#     examples = []
#     answerable = []
#     for idx, sample in enumerate(tqdm(ds[split], desc="SQuAD v2")):
#         question = sample['question']
#         context = sample['context']

#         if not sample['answers']['text']:
#             answer = ""
#             answerable = False

#         else:
#             answer = sample['answers']['text'][0]
#             answerable = True

#         examples.append(
#             {
#                 "id": f"squad_v2_{idx}",
#                 "question": question,
#                 "background": context,
#                 "answerable": answerable,
#                 "answer": answer
#             }
#         )

#     write_jsonl(examples, f"data/{split}_SQuADv2.jsonl")


# print("TODO: Add more datasets")

training_examples = []

# QASPER
# https://huggingface.co/datasets/allenai/qasper
# dataset_name = "allenai/qasper"
# data = load_dataset(dataset_name, split="train")
#
# for row_index, row in enumerate(tqdm(data, desc=f"{args.dataset_name}")):
#
#     assert len(row['qas']['question']) == len(row['qas']['answers'])
#
#     num_qas = len(row['qas']['question'])
#
#     for i in range(num_qas):
#         question = row['qas']['question'][i]
#         answer = row['qas']['answers'][i]['answer'][0]
#         template = random.choice(templates_for_qa)
#         question = template.format(question=question)
#         training_questions.append(question)
#
#         free_form_answer: str = row['qas']['answers'][i]['answer'][0]['free_form_answer']
#
#         evidence: list = row['qas']['answers'][i]['answer'][0]['evidence']
#
#         if not evidence:
#             evidence = []
#
#         elif isinstance(evidence, list):
#             pass
#             # evidence = "\n".join(evidence)
#
#         else:
#             raise ValueError("Evidence is not a list")
#
#         messages = [
#             {"role": "user", "content": question},
#             {"role": "assistant", "content": free_form_answer},
#         ]
#
#         answerable = not row['qas']['answers'][i]['answer'][0]['unanswerable']
#
#         training_examples["messages"].append(messages)
#         training_examples["background"].append(evidence)
#         training_examples["answerable"].append(answerable)
#
#         # try:
#         #     Dataset.from_dict(training_examples)
#         # except Exception as e:
#         #     print(e)
#         #     print(messages)
#         #     print(evidence)
#         #     print(answerable)
#         #     print()
#
#         # training_evidence.append(evidence)
#         # training_answerable.append(answerable)
#
# with open("data/qasper_train.json", "w") as f:
#     json.dump(training_examples, f)


examples = []
# Generating validation data
data = load_dataset("allenai/qasper", split="test")
for row_index, row in enumerate(tqdm(data, desc=f"{args.dataset_name}")):

    assert len(row['qas']['question']) == len(row['qas']['answers'])

    num_qas = len(row['qas']['question'])

    for index_question in range(num_qas):
        question = row['qas']['question'][index_question]
        for index_answer in range(len(row['qas']['answers'][index_question]['answer'])):
            if row['qas']['answers'][index_question]['answer'][index_answer]['yes_no'] == False:
                pass

        # Note: here we only include the first answer into the eval set
        index_answer = 0

        context = row['qas']['answers'][index_question]['answer'][index_answer]['evidence']

        answer, question_type, answerable = extract_answer_and_question_type_qasper(
            row['qas']['answers'][index_question]['answer'][index_answer])

        template = random.choice(templates_for_qa)

        example = {
            "id": f"qasper_{row_index}",
            "question": question,
            "background": context,
            "answerable": answerable,
            "question_type": question_type,
            "answer": answer
        }
        examples.append(example)

write_jsonl(examples, f"data/test_QASPER.jsonl")

training_dataset = Dataset.from_list(training_examples)

dataset_name = "din0s/asqa"
print(f"Processing {dataset_name} dataset")
# data = load_dataset(dataset_name, split="train")
# for row_index, row in enumerate(tqdm(data, desc=f"{args.dataset_name}")):
#     for i, qa_pair in enumerate(row['qa_pairs']):
#         corpus.append(qa_pair['context'])
#     for i, annotations in enumerate(row['annotations']):
#         for j, knowledge in enumerate(annotations['knowledge']):
#             corpus.append(knowledge['content'])


dataset_name = "mandarjoshi/trivia_qa"
subset = "rc.wikipedia"
data = load_dataset(dataset_name, "rc", split="train")

print(f"Processing {dataset_name}")

for row_index, row in enumerate(tqdm(data, desc=f"{args.dataset_name}")):
    print(row)

# config: "distractor" or "fullwiki"
dataset_name = "hotpotqa/hotpot_qa"
data = load_dataset(dataset_name, "fullwiki")

# 'validation', 'test'
for split in ['train']:
    print(f"Processing {dataset_name} split={split}")

    for row_index, row in enumerate(tqdm(data[split], desc=f"{args.dataset_name}")):

        for sentences in row['context']['sentences']:
            corpus.extend(sentences)

print(f"Corpus Length: {len(corpus)}")

dataset_name = "voidful/MuSiQue"

# Segment paragraphs into sentences
"""
Preprocessing:
- Remove citations of the form [1] or (2)
- Remove URLs
- Replace special characters such as \u2019
"""
