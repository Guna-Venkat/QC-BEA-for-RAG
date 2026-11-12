#!/usr/bin/env python
# coding: utf-8



    
    















rows = []
## wikiqa
data = datasets.load_dataset('wiki_qa')
print(len(data['train']))
for idx,sample in enumerate(data['train']):
    if sample['label'] == 0: continue
    question = sample['question'] + '\n'
    question = random.choice(templates_for_qa).format_map(dict(question=question))
    answer = sample['answer']

    messages = [
        {"role":"user","content":question},
        {"role":"assistant","content":answer},
    ]

    rows.append(
        {
            "id":f"wiki_qa_{idx}",
            "messages":messages,
            "task_type":"open_qa",
        }
    )
print(rows[-1])





## yahoo_qa
data = datasets.load_dataset('yahoo_answers_qa')
print(len(data['train']))
print(data['train'][0])
for idx,sample in enumerate(data['train']):
    question = sample['question'] + '\n'
    question = random.choice(templates_for_qa).format_map(dict(question=question))
    answer = sample['answer']

    messages = [
        {"role":"user","content":question},
        {"role":"assistant","content":answer},
    ]

    rows.append(
        {
            "id":f"yahoo_answers_qa_{idx}",
            "messages":messages,
            "task_type":"open_qa",
        }
    )
print(rows[-1])





## freebase_qa
data = datasets.load_dataset('freebase_qa')
print(len(data['train']))
print(data['train'][0])
for idx,sample in enumerate(data['train']):
    question = sample['RawQuestion'] + '\n'
    question = random.choice(templates_for_qa).format_map(dict(question=question))
    answer = sample["Parses"]['Answers'][0]['AnswersName'][0][0]

    messages = [
        {"role":"user","content":question},
        {"role":"assistant","content":answer},
    ]

    rows.append(
        {
            "id":f"freebase_qa_{idx}",
            "messages":messages,
            "task_type":"open_qa",
        }
    )
print(rows[-1])









## coqa
data = datasets.load_dataset("coqa")
print(len(data['train']))
print(data['train'][0])
for idx,sample in enumerate(data['train']):
    messages = []
    assert len(sample['answers']['input_text']) == len(sample['questions'])
    for idx,(q,a) in enumerate(zip(sample['questions'],sample['answers']['input_text'])):

        question = q + '\n'
        if idx == 0:
            question = random.choice(templates_for_qa).format_map(dict(question=question))
        answer = a

        messages.append({"role":"user","content":question})
        messages.append({"role":"assistant","content":answer})

    rows.append(
        {
            "id":f"coqa_{idx}",
            "messages":messages,
            "task_type":"close_qa",
            "background":sample['story'],
        }
    )
print(rows[-1])





## drop
data = datasets.load_dataset("drop")
print(len(data['train']))
print(data['train'][0])
for idx,sample in enumerate(data['train']):
    messages = []
    question = sample['question'] + '\n'
    question = random.choice(templates_for_qa).format_map(dict(question=question))
    answer = sample["answers_spans"]['spans'][0]

    messages.append({"role":"user","content":question})
    messages.append({"role":"assistant","content":answer})

    rows.append(
        {
            "id":f"drop_{idx}",
            "messages":messages,
            "task_type":"close_qa",
            "background":sample['passage'],
        }
    )
print(rows[-1])











## pubmed_qa
data = datasets.load_dataset("pubmed_qa","pqa_labeled")
print(len(data['train']))
print(data['train'][0])
for idx,sample in enumerate(data['train']):
    messages = []
    question = sample['question']
    answer = sample['long_answer'] + "So the final answer is: " + sample["final_decision"]
    question = random.choice(templates_for_qa).format_map(dict(question=question))

    messages.append({"role":"user","content":question})
    messages.append({"role":"assistant","content":answer})

    rows.append(
        {
            "id":f"pubmed_qa_{idx}",
            "messages":messages,
            "task_type":"close_qa",
            "background":"\n".join(sample['context']['contexts']),
        }
    )
print(rows[-1])





## quail
data = datasets.load_dataset("quail")
print(len(data['train']))
print(data['train'][0])
for idx,sample in enumerate(data['train']):
    messages = []
    question = sample['question'] + '\n'
    for answer_id,answer in enumerate(sample['answers']):
        question += ["A. ","B. ","C. ","D. "][answer_id]+answer+'\n'
    answer = ["A","B","C","D"][sample["correct_answer_id"]]
    question = random.choice(templates_for_qa).format_map(dict(question=question))

    messages.append({"role":"user","content":question})
    messages.append({"role":"assistant","content":answer})

    rows.append(
        {
            "id":f"quail_{idx}",
            "messages":messages,
            "task_type":"close_qa",
            "background":sample['context'],
        }
    )
rows[-1]





## squad_v2
data = datasets.load_dataset("squad_v2")
print(len(data['train']))
print(data['train'][0])
for idx,sample in enumerate(data['train']):
    messages = []
    question = sample['question']
    answer = sample['answers']['text'][0] if len(sample['answers']['text'])>0 else "I don't know." 
    question = random.choice(templates_for_qa).format_map(dict(question=question))

    messages.append({"role":"user","content":question})
    messages.append({"role":"assistant","content":answer})

    rows.append(
        {
            "id":f"squad_v2_{idx}",
            "messages":messages,
            "task_type":"close_qa",
            "background":sample['context'],
        }
    )
rows[-1]





## cnn_dm
data = datasets.load_dataset("cnn_dailymail",'3.0.0')
data = list(data['train'])
for idx,sample in enumerate(data[:10_0000]):
    messages = []
    answer = sample['highlights']
    question = random.choice(templates_for_sum)

    messages.append({"role":"user","content":question})
    messages.append({"role":"assistant","content":answer})

    rows.append(
        {
            "id":f"cnn_dailymail_{idx}",
            "messages":messages,
            "task_type":"summarization",
            "background":sample['article'],
        }
    )
rows[-1]





## samsum
dataset = datasets.load_dataset("samsum")
print(len(dataset['train']))
print(dataset['train'][0])
# "samsum_6054" empty background
for idx,sample in enumerate(dataset['train']):
    messages = []
    answer = sample['summary']
    question = random.choice(templates_for_sum)

    messages.append({"role":"user","content":question})
    messages.append({"role":"assistant","content":answer})

    rows.append(
        {
            "id":f"samsum_{idx}",
            "messages":messages,
            "task_type":"summarization",
            "background":sample['dialogue'].replace("\r\n",'\n'),
        }
    )
rows[-1]





## dialogsum
dataset = datasets.load_dataset("knkarthick/dialogsum")
print(len(dataset['train']))
print(dataset['train'][0])
for idx,sample in enumerate(dataset['train']):
    messages = []
    answer = sample['summary']
    question = random.choice(templates_for_sum)

    messages.append({"role":"user","content":question})
    messages.append({"role":"assistant","content":answer})

    rows.append(
        {
            "id":f"dialogsum_{idx}",
            "messages":messages,
            "task_type":"summarization",
            "background":sample['dialogue'],
        }
    )
rows[-1]





len(rows)





## pwc
# https://huggingface.co/datasets/sggetao/PwC/tree/main



import json
import os
dataset = [json.loads(x) for x in open(os.path.join(os.environ.get("SARA_DATA_DIR", "data"), "NLP", "pwc", "PwC_train.jsonl")).readlines()]
print(len(dataset))
for idx,sample in enumerate(dataset):
    messages = []
    answer = sample['answer']
    question = sample['prompt']

    messages.append({"role":"user","content":question})
    messages.append({"role":"assistant","content":answer})

    rows.append(
        {
            "id":f"pwc_{idx}",
            "messages":messages,
            "task_type":"close_qa",
            "background":sample['input'],
        }
    )
rows[-1]





## nq_open
dataset = datasets.load_dataset("nq_open")
print(len(dataset['train']))
print(dataset['train'][0])
for idx,sample in enumerate(dataset['train']):
    messages = []
    answer = sample['answer'][0]
    question = sample['question']
    question = random.choice(templates_for_qa).format_map(dict(question=question))
    

    messages.append({"role":"user","content":question})
    messages.append({"role":"assistant","content":answer})

    rows.append(
        {
            "id":f"nq_{idx}",
            "messages":messages,
            "task_type":"open_qa",
        }
    )
rows[-1]





def write_to_jsonl(data, filename):
    """
    Writes a list of dictionaries to a JSON Lines (jsonl) file.

    Args:
        data (list): List of dictionaries to write to the file.
        filename (str): Path to the output jsonl file.
    """
    with open(filename, 'w') as file:
        for item in data:
            file.write(json.dumps(item) + '\n')





write_to_jsonl(rows, "data/instruction_tuning_data.jsonl")





## fm2
fm2 = [json.loads(x) for x in open("data/eval/fm2/fm2-train.jsonl").readlines()]
print(len(fm2))
for idx,sample in enumerate(fm2):
    question = sample['question']
    messages = [
        {"role":"user","content":template_for_fact_checking[0].format_map(dict(question=question))},
        {"role":"assistant","content":"True" if 'supports' in sample['answer'] else "False"},
    ]
    rows.append(
        {
            "id":f"fm2_{idx}",
            "task_type":"fact_checking",
            "messages":messages,
        }
    )    





## triviaqa
tqa = [json.loads(x) for x in open("data/eval/triviaqa/tqa-train.jsonl").readlines()]
print(len(tqa))
for idx,sample in enumerate(tqa):
    messages = []
    answer = sample['answer'][0]
    question = sample['question']
    question = random.choice(templates_for_qa).format_map(dict(question=question))
    
    messages.append({"role":"user","content":question})
    messages.append({"role":"assistant","content":answer})

    rows.append(
        {
            "id":f"triviaqa_{idx}",
            "messages":messages,
            "task_type":"open_qa",
        }
    )















