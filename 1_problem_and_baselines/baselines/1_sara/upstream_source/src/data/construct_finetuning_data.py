import traceback

## prepare data
import datasets
import json
import os
import re
import random
import string
import numpy as np
from openai import AzureOpenAI
from tqdm import tqdm
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Document

from datasets import load_dataset

from src.prompts import prompt_reformat_data, prompt_reformat_data_no_context
from src.utils import data_utils, get_full_text_qasper
from src.model.retriever import getBM25Retriever

from src.arguments import parse_args
from src.utils.data_utils import rank_documents, read_jsonl
import logging
from typing import Union, List


logging.getLogger("bm25s").setLevel(logging.WARNING)
logging.getLogger("llama_index").setLevel(logging.WARNING)
logging.getLogger("bm25s").disabled = True


templates_for_qa = [
    "Question: {question}?\nAnswer:",
    "{question}?",
    "Answer the following question:\n\n{question}",
    "Answer this question:\n\n{question}?",
    "Please answer this question: {question}",
    "Answer the question...{question}?",
    "What is the answer to this question? {question}\n\n",
    "Can you tell me the answer to {question}?",
    "Next question: {question}\n\n",
    "Q: {question}",
    "{question}\nWhat is the answer?",
    "Write the answer to this query: {question}",
    "{question}???",
]

templates_for_sum = [
    "Write a short summary for the text\n\nSummary:",
    "Briefly summarize this article:\nSummary:", 
    "What is a shorter version of this:\n\nSummary:",
    "Write a brief summary in a sentence or less.", 
    "What is a very short summary of the above text?",
    "Summarize the aforementioned text in a single phrase.",
    "Can you generate a short summary of the above paragraph?",
    "Summarize the above articles\n\ntl;dr:",
]
template_for_fact_checking = [
    "Verify the following claims with \"True\" or \"False\":\n{question}",
]


def process_ms_marco(split: str = "train", chunk_size: int = 256):
    """
    The MS MARCO v2.1 dataset provides ground-truth selected context. 
    """
    
    rows = []
    SPLIT = "train"
    print("Processing MS MARCO v2.1 ...")
    data = datasets.load_dataset('ms_marco',"v2.1", split=SPLIT)
    for index, sample in enumerate(tqdm(data, desc=args.dataset_name)):
        
        question = sample['query'].lstrip(string.punctuation)
        # question = random.choice(templates_for_qa).format_map(dict(question=question))
        answer = sample["answers"][0]

        mask = np.array(sample['passages']['is_selected']).astype(bool)
        context = np.array(sample['passages']['passage_text'])
        
        selected_context = context[mask].tolist()
        unselected_context = context[~mask].tolist()
        if selected_context != []:
            selected_context = rank_documents(documents=selected_context, question=question, chunk_size=chunk_size)
        
        if unselected_context != []:
            unselected_context = rank_documents(documents=unselected_context, question=question, chunk_size=chunk_size)

        rows.append({
            "id": index,
            "example_id": index,
            "question": question,
            "answer": answer,
            "context": selected_context + unselected_context,
            "task_type":"open_qa",
        })
        
    data_utils.write_jsonl(rows, os.path.join(args.output_dir, "..", "data", f"ms_marco_v2.1_{SPLIT}.jsonl"))

def process_webqa():
    """
    [Web Questions Dataset](https://huggingface.co/datasets/Stanford/web_questions) by Stanford
    Skip for now since the dataset does not offer evidence in text format
    """
    
    rows = []
    data = datasets.load_dataset('web_questions')
    print(len(data['train']))
    for idx, sample in enumerate(data['train']):
        question = sample['question']+'\n'
        question = random.choice(templates_for_qa).format_map(dict(question=question))
        answer = sample['answers'][0]

        messages = [
            {"role":"user","content":question},
            {"role":"assistant","content":answer},
        ]

        rows.append(
            {
                "id":f"web_questions_{idx}",
                "messages":messages,
                "task_type":"open_qa",
            }
        )
    print(rows[-1])

def process_qasper(split: str = "train", chunk_size: int = 256):
    rows = []
    path = os.path.join(args.output_dir, "..", "data", f"QASPER_{split}.jsonl")

    if os.path.exists(path):
        rows = read_jsonl(path)

    data = datasets.load_dataset('allenai/qasper', split=split)
    for index_row, row in enumerate(tqdm(data, desc=args.dataset_name)):
        full_text = get_full_text_qasper(row)
        for index_question, question in enumerate(row['qas']["question"]):
            answer, question_type, answerable = data_utils.extract_answer_and_question_type_qasper(row['qas']['answers'][
                                                                                            index_question]['answer'][
                                                                                            0])
            context = " ".join(row['qas']['answers'][index_question]['answer'][0]['evidence'])
            prompt = prompt_reformat_data.format(question=question, context=context, answer=answer)

            messages = [{"role": "user", "content": prompt}]

            try:

                response = client.chat.completions.create(
                    model="gpt-4o-mini", messages=messages,
                )

                reformatted_answer = response.choices[0].message.content

            except:
                traceback.print_exc()
                reformatted_answer = answer

            context = rank_documents(documents=full_text, question=question, chunk_size=chunk_size) # Note that we increase the top_k here

            # suffix = reformat_prompt_qasper(question_type)
            
            if answerable:

                rows.append({
                    "id": f"{len(rows)}",
                    "example_id": f"{index_row}",
                    "question": question, # + suffix,
                    "context": context,
                    # "additional_context": additional_context,
                    "answer": answer,
                    "answer_reformatted": reformatted_answer,
                    "choices": None,
                    "question_type": question_type,
                })
                if len(rows) % 10 == 0:
                    data_utils.write_jsonl(rows, path)


    data_utils.write_jsonl(rows, path)
    
    
    
    

def process_quality(split: str = "train", chunk_size: int = 256, mode: str = "multiple-choice"):
    data = datasets.load_dataset('emozilla/quality', split=split)
    rows = []

    path = os.path.join(args.output_dir, "..", "data", f"QuALITY_{split}.jsonl")


    if os.path.exists(path):
        rows = read_jsonl(path)



    for index_row, row in enumerate(tqdm(data, desc=args.dataset_name)):
        id = f"{len(rows)}"
        assert row['answer'] in range(4)
        question = row['question']
        
        
        context = rank_documents(documents=row['article'], question=question, chunk_size=chunk_size)
        
        question = row['question']
        answer = row['options'][row['answer']]
        
        assert len(row['options']) == 4
        correct_choice = "ABCD"[row['answer']]
        if mode == "multiple-choice":
            reformatted_answer = answer = correct_choice
            
        elif mode == "open_qa":
            prompt = prompt_reformat_data_no_context.format(question=question, answer=answer)
            if "answer_reformatted" in row:
                reformatted_answer = row['answer_reformatted']
                
                
                
            else:
                
                messages = [{"role": "user", "content": prompt}]  

                try:

                    response = client.chat.completions.create(
                        model="gpt-4o-mini", messages=messages,
                    )

                    reformatted_answer = response.choices[0].message.content

                except:
                    traceback.print_exc()
                    reformatted_answer = answer


        rows.append({
            "id": str(index_row),
            "example_id": str(index_row),
            "question": question,
            "context": context,
            "choices": row['options'],
            "correct_choice": correct_choice,
            "answer": answer,
            "answer_reformatted": reformatted_answer,
        })

        if len(rows) % 10 == 0:
            data_utils.write_jsonl(rows, path)
        
    data_utils.write_jsonl(rows, path)
    
    
def process_squad_v2(split: str = "train"):
    rows = []
    answerable = []
    data = datasets.load_dataset("rajpurkar/squad_v2", split=split)

    path = os.path.join(args.output_dir, "..", "data", f"SQuADv2_{split}.jsonl")

    if os.path.exists(path):
        rows = read_jsonl(path)

    rows.sort(key=lambda x: int(x['id']))

    new_rows = []
    existing_results = set()
    for row in rows: 
        if int(row['id']) not in existing_results:
            new_rows.append(row)
            existing_results.add(int(row['id']))
            
    del rows
    rows = new_rows

    for index, row in enumerate(tqdm(data, desc="SQuADv2")):
        question = row['question']
        context = row['context']

        if index in existing_results:
            continue


        if not row['answers']['text']:
            answer = ""
            continue

        else:
            if isinstance(row['answers']['text'], list):
                answer = row['answers']['text'][0]
            else:
                answer = row['answers']['text']



        prompt = prompt_reformat_data.format(question=question, context=context, answer=answer)

        messages = [{"role": "user", "content": prompt}]

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages,
            )

            reformatted_answer = response.choices[0].message.content

        except:
            traceback.print_exc()
            reformatted_answer = answer

        rows.append({
            "id": str(index),
            "example_id": str(index),
            "question": question,
            "context": [context],
            "answer": answer,
            "answer_reformatted": reformatted_answer,
            "question_type": "close_qa",
        })

        if len(rows) % 10 == 0:
            data_utils.write_jsonl(rows, path)



    data_utils.write_jsonl(rows, path)
    # with open("data/SQuAD_train.json", "w") as f:
    #     json.dump(training_examples, f)
        
        
def process_hotpotqa(split: str = "train"):
    rows = []
    data = datasets.load_dataset('hotpotqa/hotpot_qa', 'fullwiki', split='train')

    path = os.path.join(args.output_dir, "..", "data", "reformatted", f"HotpotQA_{split}.jsonl")

    if os.path.exists(path):
        rows = read_jsonl(path)

    new_rows = []
    existing_results = set()
    for row in rows:
        if int(row['id']) not in existing_results:
            new_rows.append(row)
            existing_results.add(int(row['id']))
    rows = new_rows


    for index, row in enumerate(tqdm(data, desc="HotpotQA")):
        if index in existing_results:
            continue
        question = row['question']
        answer = row['answer']
        context = row['context']
        assert isinstance(context['sentences'], list) and isinstance(context['sentences'][0], list) and isinstance(context['sentences'][0][0], str)

        prompt = prompt_reformat_data_no_context.format(question=question, answer=answer)

        messages = [{"role": "user", "content": prompt}]

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages,
            )

            reformatted_answer = response.choices[0].message.content

        except:
            traceback.print_exc()
            reformatted_answer = answer

        context = [re.sub(r"\s+", " ", " ".join(sents)) for sents in context['sentences']]
        rows.append({
            "id": str(index),
            "example_id": str(index),
            "question": question,
            "context": context,
            "answer": answer,
            "answer_reformatted": reformatted_answer,
            "question_type": "open_qa",
            "answerable": True
        })

        if len(rows) % 10 == 0:
            data_utils.write_jsonl(rows, path)


    data_utils.write_jsonl(rows, path)

def process_narrativeqa(split: str = "train", chunk_size: int = 256):
    data = load_dataset("narrativeqa", split=split)
    rows = []
    
    path = os.path.join(args.output_dir, "..", "data", "reformatted", f"NarrativeQA_{split}.jsonl")
    
    if os.path.exists(path):
        rows = read_jsonl(path)
        
    rows.sort(key=lambda x: int(x['id']))

    new_rows = []
    existing_results = set()
    for row in rows: 
        if int(row['id']) not in existing_results:
            new_rows.append(row)
            existing_results.add(int(row['id']))
    del rows
    rows = new_rows
    
    for index, row in enumerate(tqdm(data, desc="NarrativeQA")):
    
        question = row['question']['text']
        answer = row["answers"][0]['text']
        
        parser = SentenceSplitter(separator="\n", chunk_size=chunk_size, chunk_overlap=0)
        nodes = parser.get_nodes_from_documents([Document(text=row['document']['text'])])
        
        documents = [Document(doc_id=str(doc_id), text=node.get_content()) for doc_id, node in enumerate(nodes)]
        
        # Retrieve the top k nodes
        sparse_retriever, prepare_time = getBM25Retriever(documents, similarity_top_k=len(documents))
        ranked_nodes = sparse_retriever.retrieve(question)
        selected_nodes = ranked_nodes
        
        
        context = [node.get_content() for node in selected_nodes]
        # context = "\n".join(context)
        # additional_context = [doc.text for doc_id, doc in enumerate(documents) if str(doc_id) not in selected_node_ids]

        prompt = prompt_reformat_data_no_context.format(question=question, answer=answer)
        messages = [{"role": "user", "content": prompt}]
        
        try:

            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages,
            )

            reformatted_answer = response.choices[0].message.content

        except:
            traceback.print_exc()
            reformatted_answer = answer
        
        rows.append({
            "id": f"{index}",
            "example_id": f"{index}",
            "question": question,
            "answer": answer,
            "answer_reformatted": reformatted_answer,
            "context": context,
            "task_type": "close_qa",
        })
        if len(rows) % 100 == 0:
            data_utils.write_jsonl(rows, path)
        
    
    data_utils.write_jsonl(rows, path)
        
    
    
    



def process_triviaqa(split: str = "train"):
    TRIVIAQA = os.path.abspath(os.path.join(os.environ.get("SARA_DATA_DIR", "data"), "RAG", "TriviaQA"))
    
    path_verified_web_dev = os.path.join(TRIVIAQA, "qa", "verified-web-dev.json")
    dataset = json.load(open(path_verified_web_dev, 'r'))
    rows = []

    path = os.path.join(args.output_dir, "..", "data", "reformatted", f"TriviaQA_{split}.jsonl")

    if os.path.exists(path):
        rows = read_jsonl(path)
        new_rows = []
        existing_results = set()
        for row in rows:
            if int(row['id']) not in existing_results:
                new_rows.append(row)
                existing_results.add(int(row['id']))
        del rows
        rows = new_rows


    for i, entry in enumerate(dataset['Data']):

        context = []
        for search_result in entry['SearchResults']:
            with open(os.path.join(TRIVIAQA, "evidence", "web", search_result['Filename'])) as f:
                evidence = f.read()

            context.append(evidence)
            reformatted_answers = []
            
            for answer in entry["Answer"]["Aliases"]:
                prompt = prompt_reformat_data_no_context.format(question=entry["Question"], answer=answer)
                messages = [{"role": "user", "content": prompt}]
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini", messages=messages,
                    )

                    reformatted_answer = response.choices[0].message.content

                except:
                    traceback.print_exc()
                    reformatted_answer = answer
                
                reformatted_answers.append(reformatted_answer)
                

        datum = {
            "id": str(i),
            "example_id": entry["QuestionId"],
            "question": entry["Question"],
            "context": context,
            "answer": entry["Answer"]["Aliases"], # This is a list
            "answer_reformatted": reformatted_answers,
            "question_type": "free_form",
            "answerable": True
        }

        rows.append(datum)
        if len(rows) % 100 == 0:
            data_utils.write_jsonl(rows, path)

        
    data_utils.write_jsonl(rows, path)
    
    
def process_longbench(subset_name: str, split: str, chunk_size: int = 256):
    
    dataset = load_dataset("THUDM/LongBench", subset_name, split=split)
    
    # if subset_name in ["qmsum", "multi_news"]:
    #     task_name = "summarization"
    
    rows = []
    
    for index, row in enumerate(tqdm(dataset, desc=f"LongBench-{subset_name}")):
        if subset_name in ["qmsum", "multi_news"]:
            question = "Summarize the above passage."
            answer = row["answers"]
        
        else:
            raise NotImplementedError("OpenQA not implemented yet")
        
        parser = SentenceSplitter(separator="\n", chunk_size=chunk_size, chunk_overlap=0)
        context = re.sub("NEWLINE_CHAR", "", row['context'])
        context = re.sub(r"\s+", " ", re.sub("\n+", "\n", context)).strip()
        nodes = parser.get_nodes_from_documents([Document(text=context)])
        
        
        documents = [Document(doc_id=str(doc_id), text=node.get_content()) for doc_id, node in enumerate(nodes)]
        
        # Retrieve the top k nodes
        sparse_retriever, prepare_time = getBM25Retriever(documents, similarity_top_k=len(documents))
        selected_nodes = sparse_retriever.retrieve(question)
        
        
        
        context = [node.get_content() for node in selected_nodes]
        # context = "\n".join(context)
        # additional_context = [doc.text for doc_id, doc in enumerate(documents) if str(doc_id) not in selected_node_ids]

        
        
        datum = {
            "id": str(index),
            "example_id": str(index),
            "question": question,
            "context": context,
            "answer": answer, # This is a list
            "answer_reformatted": answer,
            "question_type": "summarization",
            "answerable": True
        }

        rows.append(datum)
        
    data_utils.write_jsonl(rows, os.path.join(args.output_dir, "..", "data", f"LongBench-{subset_name}_{split}.jsonl"))

        
        
        
        
        
    
    
    
    
if __name__ == "__main__":
    args = parse_args('data')

    client = AzureOpenAI(api_key=os.environ["AZURE_OPENAI_API_KEY"])
    
    

    # for split in ["train", "validation"]:
    # for split in ["validation"]:

    #     process_hotpotqa(split)
    #     process_quality(split, mode="multiple-choice")
    #     process_squad_v2(split)
    #     process_narrativeqa(split)
        
    for split in ['test']:
        # process_longbench("multi_news", split)
        process_longbench("qmsum", split)
    
    # process_ms_marco()
    # process_webqa() # Skip for now
    
    # for split in ["train", "test"]:
    #     process_qasper(split)
    
    # for split in ["validation"]:
    
    #     
        
        
    # process_triviaqa(split="train")
    
    

