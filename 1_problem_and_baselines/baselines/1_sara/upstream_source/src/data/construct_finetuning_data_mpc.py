"""
Process the narrativeqa dataset for fine-tuning using multi-processing.

To run the code

python -m src.data.construct_finetuning_data_mpc --config config/language_modeling/eval.yaml --num_workers 1
--output_dir outputs
"""


import os
from multiprocessing import Pool, cpu_count, Manager
from tqdm import tqdm
import datasets
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Document
from datasets import load_dataset
import string
import numpy as np
from time import time
from openai import AzureOpenAI
import traceback
from src.prompts import prompt_reformat_data, prompt_reformat_data_no_context

from src.utils import data_utils
from src.arguments import parse_args
from src.model.retriever import getBM25Retriever


SPLIT = "train"
print("Processing NarrativeQA ...")
rows = []

client = AzureOpenAI(api_key=os.environ["AZURE_OPENAI_API_KEY"])


def process_one_sample_narrativeqa(args):
    """
    
    There are 3 splits in [NarrativeQA](https://huggingface.co/datasets/deepmind/narrativeqa): train (32747), validation (3461), test (10557)
    """
    chunk_size: int = 256
    index, sample = args
    if (index + 1) % 5000 == 0:
        print(f"Processed Index {index}")
    question = sample['question']['text']
    answer = sample["answers"][0]['text']
    
    parser = SentenceSplitter(separator="\n", chunk_size=chunk_size, chunk_overlap=0)
    nodes = parser.get_nodes_from_documents([Document(text=sample['document']['text'])])
    
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
    
    return {
        "id": f"{index}",
        "example_id": f"{index}",
        "question": question,
        "answer": answer,
        "answer_reformatted": reformatted_answer,
        "context": context,
        "task_type": "close_qa",
    }

def process_one_sample_ms_marco(args):
    """Processes a single MS MARCO sample."""
    index, sample, chunk_size = args
    
    question = sample['query'].lstrip(string.punctuation)
    answer = sample["answers"][0]

    mask = np.array(sample['passages']['is_selected']).astype(bool)
    context = np.array(sample['passages']['passage_text'])

    selected_context = context[mask].tolist()
    unselected_context = context[~mask].tolist()

    if selected_context:
        selected_context = data_utils.rank_documents(documents=selected_context, question=question, chunk_size=chunk_size)

    if unselected_context:
        unselected_context = data_utils.rank_documents(documents=unselected_context, question=question, chunk_size=chunk_size)

    return {
        "id": index,
        "example_id": index,
        "question": question,
        "answer": answer,
        "context": selected_context + unselected_context,
        "task_type": "open_qa",
    }



if __name__ == "__main__":
    SPLIT = "train"
    print("Processing NarrativeQA ...")
    
    args = parse_args('data')
    rows = []
    
    # TODO: For demo
    # data = datasets.Dataset.from_dict(data[:3])
    
    chunk_size = 256
    
    data = load_dataset("narrativeqa", split=SPLIT)
    print(len(data))
    with Pool(args.num_workers) as pool:
        results = list(pool.imap(process_one_sample_narrativeqa, enumerate(data)))
    
    
    path = os.path.abspath(os.path.join(args.output_dir, "..", "data", f"NarrativeQA_{SPLIT}.jsonl"))
    # t0 = time()
        
    # data = datasets.load_dataset('ms_marco',"v2.1", split=SPLIT) 
    # with Pool(args.num_workers) as pool: 
    #     results = list(tqdm(
    #         pool.imap_unordered(process_one_sample_ms_marco, [(i, sample, chunk_size) for i, sample in enumerate(data)]),
    #         total=len(data),
    #         desc="Processing MS MARCO"
    #     ))

    # print(f"Processing takes {time() - t0:.2f} seconds")

    rows.extend(results)
    rows.sort(key=lambda x: x["id"])
    # for i in range(len(rows)):
    #     rows[i]["id"] = str(i)
    #     rows[i]["example_id"] = str(i)
    # path = os.path.abspath(os.path.join(args.output_dir, "..", "data", f"MS_Marco_{SPLIT}.jsonl"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data_utils.write_jsonl(rows, path)
    print(f"Processing complete. Saved")