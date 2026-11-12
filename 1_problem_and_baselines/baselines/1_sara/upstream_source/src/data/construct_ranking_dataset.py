from datasets import load_dataset
from rank_bm25 import BM25Okapi
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
import json
import os

# Load the dataset
data = load_dataset("rajpurkar/squad_v2")

# Tokenize the contexts for BM25
all_contexts = [example['context'] for example in data['train']]
tokenized_contexts = [context.split() for context in all_contexts]

# Initialize BM25
bm25 = BM25Okapi(tokenized_contexts)

# Function to sample negative contexts
def sample_negative_contexts(example, all_contexts, bm25, num_negatives=4):
    positive_context = example['context']
    query = positive_context.split()

    # Get BM25 scores for all contexts
    scores = bm25.get_scores(query)

    # Rank contexts by BM25 score, excluding the positive context
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    negative_contexts = set()

    for idx in ranked_indices:
        if all_contexts[idx] != positive_context:  # Exclude positive context
            negative_contexts.add(all_contexts[idx])
        if len(negative_contexts) == num_negatives:
            break

    return {
        'id': example['id'],
        'title': example['title'],
        'context': example['context'],
        'question': example['question'],
        'answer': example['answers']['text'],
        'negative_context': list(negative_contexts)
    }

# Parallel processing
def process_data(example):
    return sample_negative_contexts(example, all_contexts, bm25)

if __name__ == "__main__":
    path = os.path.join(os.environ.get("SARA_DATA_DIR", "data"), "train_SQuAD-v2.json")
    
    # with ProcessPoolExecutor(max_workers=40) as executor:
    #     new_data = list(tqdm(executor.map(process_data, data['train'], ), total=len(data['train']), desc="Processing dataset"))

    # # Save the new dataset
    # with open(path, 'w') as f:
    #     json.dump(new_data, f)

    with open(path, 'r') as f:
        data = json.load(f)

    new_data = []
    for example in tqdm(data):
        new_data.append({
            'id': example['id'],
            'title': example['title'],
            'context': example['context'],
            'question': example['question'],
            'answer': example['answers']['text'],
            'negative_context': example['negative_context']
        })

    with open(path, 'w') as f:
        json.dump(new_data, f)

