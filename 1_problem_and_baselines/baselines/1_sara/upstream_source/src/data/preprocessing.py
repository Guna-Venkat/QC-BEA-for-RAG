import random
import traceback
import os
import sys

import torch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from collections import Counter

import signal
from functools import wraps
from functools import partial



from src.const import COMPRESS
from src.utils.lm_utils import ParaphraseInstructions, ParagraphRecoveryInstructions, find_matched_index

from src.prompts import PROMPT_MISTRAL, PROMPT_LLAMA3, PROMPT_QUESTION_ONLY, PROMPT_LLAMA3_QUESTION_ONLY, PROMPT_LLAMA3_QUESTION_AND_GOLDEN_CONTEXT, PROMPT_ONE_CONTEXT, PROMPT_QUESTION_AND_GOLDEN_CONTEXT, ANSWER_INSTRUCTION, ANSWER_INSTRUCTION_MULTI_CHOICE

from nltk.tokenize import sent_tokenize




class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Function call timed out")

def timeout(seconds=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Set the signal handler and alarm
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)  # Disable the alarm
            return result
        return wrapper
    return decorator



def split_background(background, tokenizer, total_max_len, single_max_len, single_min_len=20):
    """
    split a long document into multiple smaller chunks between single_max_len and single_mini_len

    Args:
        background: string

    Return:
        background: a list of string
    """
    ids = tokenizer(background, add_special_tokens=False, max_length=total_max_len, truncation=True).input_ids
    background = [ids[idx:idx + single_max_len] for idx in range(0, len(ids), single_max_len)]
    assert len(background) >= 1, background
    if len(background[-1]) <= single_min_len and len(background) > 1:
        background = background[:-1]
    background = [tokenizer.decode(x) for x in background]
    return background


def _concat_messages_mixtral(messages, tokenizer):
    ## Mixtral Chat Format
    return _concat_messages_mistral(messages, tokenizer)


def _concat_messages_mistral(messages, tokenizer):
    ## Mistral Chat Format
    message_text = ""
    for message in messages:
        if message["role"] == "user":
            message_text += "[INST] " + message["content"].strip() + " [/INST]"
        elif message["role"] == "assistant":
            message_text += message["content"].strip() + tokenizer.eos_token
        else:
            raise ValueError("Invalid role: {}".format(message["role"]))
    return message_text


def _concat_messages_llama(messages, tokenizer):
    ## Llama Chat Format
    # For prompt formats, see [Model Card](https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_1/)
    # if messages[0]['role'] != "system":
    #     messages.insert(0, {'role': 'system', 'content': 'You are a helpful assistant.'})
    input_ids = tokenizer.apply_chat_template(messages)
    # `skip_special_tokens`: Whether to keep tokens like <|begin_of_text|>
    message_text = tokenizer.decode(input_ids, skip_special_tokens=False)
    return message_text

def _encode(instruction, document, tokenizer,
        max_seq_length, 
        model_name_or_path: str = None,
        do_train=True):
    
    assert "gemma" in model_name_or_path.lower(), f"Model not supported: {model_name_or_path}"
    
    
    
    if do_train:
        # encoded = tokenizer.batch_encode_plus(text, return_tensors="pt", padding=True, max_length=max_seq_length, truncation=True)
        input = tokenizer(f"{instruction.strip()} {document}", return_tensors="pt", max_length=max_seq_length, padding='max_length', truncation=True)
        input_masked = tokenizer(instruction, truncation=True, return_tensors="pt")# , padding=True, max_length=max_seq_length, truncation=True)
        input_ids = input['input_ids'][0]
        
        assert len(input_ids) <= max_seq_length
        
        input_ids_masked = input_masked['input_ids'][0]
        
        num_head_tokens = sum(input_ids[:len(input_ids_masked)] == input_ids_masked)
        
        labels = input_ids.clone()
        labels[:num_head_tokens] = -100
        labels[input_ids == tokenizer.pad_token_type_id] = -100
        attention_mask = torch.zeros_like(input_ids)
        attention_mask[input_ids != tokenizer.pad_token_type_id] = 1
        
    else:
        tokenized_example = tokenizer(f"{instruction.strip()} {document}", return_tensors='pt') # , max_length=max_seq_length, truncation=True)
        input_ids = tokenized_example.input_ids.flatten()
        
        labels = torch.ones_like(input_ids) * -100
        attention_mask = torch.ones_like(input_ids)
        
    return {
        "input_ids": input_ids,
        "labels": labels,
        "attention_mask": attention_mask,
    }
    


def _encode_chat_format(
        messages,
        tokenizer,
        max_seq_length,
        chat_format='mistral', 
        model_name_or_path: str = None,
        do_train=True
):
    """
    encode messages to input_ids and make non-assistant part

    Args:
        messages (list): list of dict with 'role' and 'content' field
        tokenizer: llm tokenizer
        max_seq_lengh: maximun context length  

    Return:
        input_ids and labels
    """
    if "llama" in model_name_or_path.lower():
        _concat_messages = _concat_messages_llama
        
    elif "mistral" in model_name_or_path.lower():
        _concat_messages = _concat_messages_mistral

    elif "mixtral" in model_name_or_path.lower():
        _concat_messages = _concat_messages_mixtral
        
    if "mistral" in model_name_or_path.lower() or "mixtral" in model_name_or_path.lower():
        assert messages[0]['role'] == 'user'
        input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors='pt', max_length=max_seq_length, tokenize=True, padding='max_length')[0]
        input_no_pad = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors='pt', max_length=max_seq_length, tokenize=True)[0]
        
        input_masked = tokenizer.apply_chat_template([messages[0]], add_generation_prompt=True, return_tensors='pt', tokenize=True)[0]
        input_masked = tokenizer.apply_chat_template([messages[0]], add_generation_prompt=True, return_tensors='pt', tokenize=True)[0]
        
        assert (input_ids[-len(input_no_pad):(len(input_masked)-len(input_no_pad))] == input_masked).all()
        labels = torch.ones_like(input_ids) * -100
        labels[-len(input_no_pad)+len(input_masked):] = input_ids[-len(input_no_pad)+len(input_masked):]
        
        attention_mask = torch.zeros_like(input_ids)
        attention_mask[input_ids != tokenizer.pad_token_id] = 1
        
        
        """
        example_text = _concat_messages(messages, tokenizer).strip()
        tokenized_example = tokenizer(example_text, return_tensors='pt', max_length=max_seq_length, truncation=True)
        input_ids = tokenized_example.input_ids
        # tokenizer.convert_ids_to_tokens(input_ids[0])
        labels = input_ids.clone()

        # mask the non-assistant part for avoiding loss
        for message_idx, message in enumerate(messages):
            if message["role"] != "assistant":
                if message_idx == 0:
                    message_start_idx = 0
                else:
                    message_start_idx = tokenizer(
                        _concat_messages(messages[:message_idx], tokenizer), return_tensors='pt', max_length=max_seq_length,
                        truncation=True
                    ).input_ids.shape[1]

                if chat_format in ['mistral', 'mixtral', 'llama']:
                    messages_so_far = _concat_messages(messages[:message_idx + 1], tokenizer)

                message_end_idx = tokenizer(
                    messages_so_far,
                    return_tensors='pt',
                    max_length=max_seq_length,
                    truncation=True
                ).input_ids.shape[1]
                labels[:, message_start_idx:message_end_idx] = -100

                if message_end_idx >= max_seq_length:
                    break
        """
        
    elif "llama" in model_name_or_path.lower():
        assert messages[0]['role'] == 'user'
        assert messages[1]['role'] == 'assistant'
        
        if do_train:
        
            # example_text = _concat_messages(messages, tokenizer).strip()
            
            input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors='pt', max_length=max_seq_length, tokenize=True, padding='max_length')[0]
            input_masked = tokenizer.apply_chat_template([messages[0]], add_generation_prompt=True, return_tensors='pt', tokenize=True)[0]
        
            assert (input_ids[:len(input_masked)] == input_masked).all()
            labels = input_ids.clone()
        
            
            labels[:len(input_masked)] = -100
            labels[input_ids == tokenizer.pad_token_id] = -100
            attention_mask = torch.zeros_like(input_ids)
            attention_mask[input_ids != tokenizer.pad_token_id] = 1
            
            """
        
            tokenized_example = tokenizer(example_text, return_tensors='pt', max_length=max_seq_length, truncation=True)
            
            # tokenizer.convert_ids_to_tokens(input_ids[0])
            labels = input_ids.clone()
            # assert tokenizer.eos_token_id in input_ids, (tokenizer("this is good."+tokenizer.eos_token +'\n').input_ids,input_ids)
            
            
            decoded = tokenizer.decode(input_ids[0])
            assistant_text = "<|start_header_id|>assistant<|end_header_id|>"
            assert assistant_text in decoded, decoded
            i = 0
            indices = torch.where(labels[0] == 128006)[0]  # Get all indices where tensor == value
            i = indices[-1].item() if len(indices) > 0 else -1  # Get the last index or -1 if not found

            # This stands for the header "<|start_header_id|>assistant<|end_header_id|>\n\n"
            assert input_ids[0][i] == 128006 and input_ids[0][i+1] == 78191 and input_ids[0][i+2] == 128007 and input_ids[0][i+3] == 271
            i = i + 4
            labels[:, :i] = -100
            """
            
            
            
        else:
            messages = [messages[0]]
            example_text = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
            tokenized_example = tokenizer(example_text, return_tensors='pt', max_length=max_seq_length, truncation=True)
            input_ids = tokenized_example.input_ids.flatten()
            
            labels = torch.ones_like(input_ids) * -100
            attention_mask = torch.ones_like(input_ids)
            
        # assistant_start_idx = decoded.find(assistant_text)
        # assert [128006, 78191, 128007, 271]  # <|start_header_id|>assistant<|end_header_id|>\n\n
    

        
    else:
        raise ValueError(f"Model not supported: {model_name_or_path}")

    # assert tokenizer.eos_token_id in input_ids, input_ids
    return {
        "input_ids": input_ids,
        "labels": labels,
        "attention_mask": attention_mask,
    }


def encode_with_chat_format_pretrain(
        example,
        tokenizer,
        max_seq_length,
        retrieval_embed_length,
        chat_format='mistral',
        do_train=True,
        model_name_or_path: str = None
):
    """
    encode messages into input_ids and labels for paraphrase pretrain

    Args:
        example: data sample with 'text' filed
        tokenizer: llm_tokenizer
        max_seq_length: maximun context length
        retrieval_embed_length: number of tokens for retrieval (typically 1 for dense retrieval model)

    Return:
        input_ids,labels and retriever_input_text
    """
    try:
        document = example['text'].strip()
        compress_token = " ".join([COMPRESS] * retrieval_embed_length)
        instruction = random.choice(ParaphraseInstructions).format_map(dict(compress_token=compress_token))
        
        
        if "gemma" in model_name_or_path.lower():
            # Not encoding into chat format
            encoded = _encode(instruction=instruction, 
                              document=document if do_train else " ", 
                              tokenizer=tokenizer, 
                              max_seq_length=max_seq_length, 
                              model_name_or_path=model_name_or_path, 
                              do_train=do_train)

        else:
        # For testing, we only need the instruction
            messages = [
                {"role": "user", "content": instruction},
                {"role": "assistant", "content": document if do_train else " "},
            ]

            encoded = _encode_chat_format(messages, tokenizer, max_seq_length, chat_format, model_name_or_path=model_name_or_path, do_train=do_train)

        return {
            "input_ids": encoded['input_ids'],
            "attention_mask": encoded['attention_mask'],
            "labels": encoded['labels'],
            "retriever_input_text": [document],
        }
    except:
        traceback.print_exc()
        raise Exception
    
    
def encode_with_chat_format_pretrain_instruction(
        example,
        tokenizer,
        max_seq_length,
        retrieval_embed_length,
        chat_format='mistral',
        do_train=True,
        model_name_or_path: str = None
):
    """
    encode messages into input_ids and labels for paraphrase pretrain

    Args:
        example: data sample with 'text' filed
        tokenizer: llm_tokenizer
        max_seq_length: maximun context length
        retrieval_embed_length: number of tokens for retrieval (typically 1 for dense retrieval model)

    Return:
        input_ids,labels and retriever_input_text
    """
    try:
        
        
        
        document = example['text'].strip()
        compress_tokens = " ".join([COMPRESS] * retrieval_embed_length)
        instruction = random.choice(ParaphraseInstructions).format_map(dict(compress_token=compress_tokens))
        
        # Manually control the length of the instruction
        document = " ".join(document.split(" ")[:100])
        
        prompt = tokenizer.encode(tokenizer.bos_token + instruction, add_special_tokens=False)
        summary = tokenizer.encode(document + tokenizer.eos_token, add_special_tokens=False)
        
        input_ids = prompt + summary
        labels = len(prompt) * [-100] + summary
        compress_token_id = tokenizer.convert_tokens_to_ids(COMPRESS)
        num_compress_tokens = Counter(input_ids)[compress_token_id]
        assert num_compress_tokens == 1, f"Must contain 1 COMPRESS token, but got {num_compress_tokens}"
        assert len(input_ids) == len(labels), (len(input_ids), len(labels))

        return {
            "input_ids": input_ids,
            "labels": labels,
            "attention_mask": [1] * len(input_ids),
            "retriever_input_text": [document],
        }
    except:
        traceback.print_exc()
        raise Exception





def encode_with_chat_format_paragraph(
        example,
        tokenizer,
        max_seq_length,
        retrieval_embed_length,
        chat_format='mistral',
        do_train=True,
        model_name_or_path: str = None
):
    """
    encode messages into input_ids and labels for paraphrase pretrain

    Args:
        example: data sample with 'text' filed
        tokenizer: llm_tokenizer
        max_seq_length: maximun context length
        retrieval_embed_length: number of tokens for retrieval (typically 1 for dense retrieval model)
        split_sentences: whether to split the document into sentences so that each compress token encodes one sentence.

    Return:
        input_ids,labels and retriever_input_text
    """

    try:

        if isinstance(example['text'], list):
            assert isinstance(example['text'][0], str), f"Example must be a str or a list of str, but got {example['text']}"
            retrieval_embed_length = len(example['text'])
        
            document = " ".join(example['text'])
            
        else:
            assert isinstance(example['text'], str)
            sentences = [s.strip() for s in sent_tokenize(example['text'])]
            
            retrieval_embed_length = len(sentences)
            document = " ".join(sentences)
            
            
        

        compress_tokens = "".join([COMPRESS] * retrieval_embed_length)
        instruction = random.choice(ParagraphRecoveryInstructions).format_map(dict(compress_tokens=compress_tokens))

        # For testing, we only need the instruction
        messages = [
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": document if do_train else " "},
        ]

        encoded = _encode_chat_format(messages, tokenizer, max_seq_length=max_seq_length, chat_format=chat_format, model_name_or_path=model_name_or_path, do_train=do_train)
        # Not sure if this is necessary:
        
        """
        if not do_train:
            encoded["input_ids"] = encoded["input_ids"][encoded["input_ids"] != tokenizer.eos_token_id]
            encoded["labels"] = encoded["labels"][encoded["labels"] != tokenizer.eos_token_id]

            assert len(encoded["input_ids"]) == len(encoded["labels"]), (
                len(encoded["input_ids"]), len(encoded["labels"]))
        """
        
        return {
            "input_ids": encoded['input_ids'],
            "attention_mask": encoded['attention_mask'],
            "labels": encoded['labels'],
            "retriever_input_text": sentences,
        }
        

    except Exception as e:
        traceback.print_exc()
        print(e)


def encode_with_chat_format_finetune_stage1(
        example,
        tokenizer,
        max_seq_length,
        retrieval_embed_length,
        use_rag_tuning=True,
        retriever_tokenizer=None,
        chat_format='mistral',
        model_name_or_path: str = None,
        num_evidence: int = None,
        num_additional_evidence: int = None,
        compressor_encode_method: str = "paragraph"
):
    
    """
    compressor_encode_method: Whether encoding the evidence as a `paragraph` or a `sentence`

    """
    
    assert "question" in example, "Question must be provided in the example."
    
    if use_rag_tuning:
        if isinstance(example['context'], list):
            context = "\n".join(example['context'][:num_evidence])

        elif isinstance(example['context'], str):
            context = example['context']

        else:
            raise ValueError("Context must be provided in the example.")
        
        if context == "":
            print("Empty context")
            template = PROMPT_QUESTION_ONLY
            
        else:

            if num_additional_evidence >= 1:
                
                if compressor_encode_method == "sentence":
                    raise NotImplementedError("Sentence-based compression is not supported for this method.")
                   
                    
                elif compressor_encode_method == "paragraph":
                    # Put COMPRESS tokens in-context
                    model_input_compress_token = PROMPT_ONE_CONTEXT.format(question=example['question'], context=COMPRESS, answer_instruction=ANSWER_INSTRUCTION)
                    
                
            else:
                model_input_compress_token = PROMPT_QUESTION_AND_GOLDEN_CONTEXT.format(question=example['question'], context=context, answer_instruction=ANSWER_INSTRUCTION)
            
            model_input_nl = PROMPT_ONE_CONTEXT.format(question=example['question'], context=context, answer_instruction=ANSWER_INSTRUCTION)
            
            # Generation based on golden context
            
            
    else:

        template = PROMPT_QUESTION_ONLY
        
        
    if isinstance(example['answer'], list):
        answer = example['answer'][0].strip()
        
    elif isinstance(example['answer'], str):
        answer = example['answer'].strip()
        
    else:
        raise ValueError("Answer must be provided in the example.")
        

    

    messages_compress_token = [{'role': 'user', 'content': model_input_compress_token}, {'role': 'assistant', 'content': answer}]
    messages_nl = [{'role': 'user', 'content': model_input_nl}, {'role': 'assistant', 'content': answer}]

    ret = {}

    if use_rag_tuning:
        assert messages_compress_token[0]['role'] == messages_nl[0]['role'] == 'user'
            
        ret['retriever_input_text'] = context
            
    encoded_compress_token = _encode_chat_format(model_name_or_path=model_name_or_path,
                                    messages=messages_compress_token, 
                                    tokenizer=tokenizer, 
                                    max_seq_length=max_seq_length, 
                                    chat_format=chat_format)
    
    encoded_nl = _encode_chat_format(model_name_or_path=model_name_or_path,
                                    messages=messages_nl, 
                                    tokenizer=tokenizer, 
                                    max_seq_length=max_seq_length, 
                                    chat_format=chat_format)
    
    
    
    ret['input_ids'] = encoded_compress_token['input_ids']
    ret['labels'] = encoded_compress_token['labels']
    ret['attention_mask'] = encoded_compress_token['attention_mask']
    ret['input_ids_nl'] = encoded_nl['input_ids']
    ret['labels_nl'] = encoded_nl['labels']
    ret['attention_mask_nl'] = encoded_nl['attention_mask']
        

    return ret
    
    

# @timeout(seconds=10) 
def encode_with_chat_format_finetune(
        example,
        tokenizer,
        max_seq_length,
        retrieval_embed_length,
        use_rag_tuning=True,
        use_retriever_embed=False,
        retriever_tokenizer=None,
        chat_format='mistral',
        model_name_or_path: str = None,
        num_evidence: int = None,
        num_additional_evidence: int = None,
        compressor_encode_method: str = "paragraph"
):
    '''
    Here we assume each example has three fields:
        1) messages
        2) context
        3) additional_context (or "negative_context")
        4) task_type  
    '''
    # messages = example['messages']
    
    assert "question" in example, "Question must be provided in the example."
    additional_context = []
    
    if use_rag_tuning:
        if isinstance(example['context'], list):
            context = ""
            for i in range(num_evidence):
                context += f"Document {i + 1}. {example['context'][i]}\n"
            

        elif isinstance(example['context'], str):
            context = example['context']

        else:
            raise ValueError("Context must be provided in the example.")
        
        if context == "":
            print("Empty context")
            template = PROMPT_QUESTION_ONLY
            
        else:

            # Put COMPRESS tokens in-context
            if use_retriever_embed:
                
                assert isinstance(example['context'], list)
                
                if len(example["context"]) <= num_evidence:
                    additional_context_placeholder = ""
                    
                else:
                    assert min(num_additional_evidence, len(example["context"]) - num_evidence) > 0
                    additional_context_placeholder = ""
                    
                    if compressor_encode_method == "sentence":
                    
                        for i in range(0, min(num_additional_evidence, len(example["context"]) - num_evidence)):
                            
                            # additional_context_placeholder += f"{i + 1}. {COMPRESS}\n"
                            sentences = sent_tokenize(example["context"][i])
                            additional_context_placeholder += f"Document {i + 1}. {COMPRESS * len(sentences)}\n"
                            
                            additional_context.extend(sentences)
                            
                    elif compressor_encode_method == "paragraph":
                        for i in range(0, min(num_additional_evidence, len(example["context"]) - num_evidence)):
                            additional_context_placeholder += f"{i + 1}. {COMPRESS}\n"
                            additional_context.append(example["context"][i])
                            
                    additional_context_placeholder += "\n"
                # Maybe the mistral template will suffice
                # if "mistral" in model_name_or_path.lower():
                template = PROMPT_MISTRAL
                    
                # elif "llama" in model_name_or_path.lower():
                #     template = PROMPT_LLAMA3
                    
                # else:
                #     raise ValueError("Model not supported")
            
            # Generation based on golden context
            else:
                template = PROMPT_QUESTION_AND_GOLDEN_CONTEXT
            
    else:

        template = PROMPT_QUESTION_ONLY
        
        
    if isinstance(example['answer'], list):
        answer = example['answer'][0]
        
    elif isinstance(example['answer'], str):
        answer = example['answer']
    else:
        answer = None
        

    messages = [{'role': 'user', 'content': None}, {'role': 'assistant', 'content': answer}]

    ret = {}
    
    # Initialize RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,  # Approximate target chunk size in words
        chunk_overlap=0,  # No overlap
        separators=["\n", ". ", "! ", "? "]  # Natural sentence boundaries
    )

    # Split the text
    # sharded_background = text_splitter.split_text(background)
    # sharded_background = [chunk.strip(string.punctuation) for chunk in sharded_background]

    # if use_rag_tuning and use_retriever_embed:
    # Split the background into multiple sentences
    # sharded_background = sent_tokenize(background)
    
    if example['question_type'] == "multi-choice":
        question = f"{example['question']}\n"
        for i, choice in enumerate(example['choices']):
            question += f"{'ABCD'[i]}. {choice}\n"
    
    else:
        question = example['question']

    if use_rag_tuning:
        assert messages[0]['role'] == 'user'
        
        if use_retriever_embed:
            
            messages[0]['content'] = template.format(question=question, context=context,
                                                    additional_context=additional_context_placeholder, answer_instruction=ANSWER_INSTRUCTION if example['question_type'] == "open_qa" else ANSWER_INSTRUCTION_MULTI_CHOICE)
            
            ret['retriever_input_text'] = additional_context

        else:
            
            messages[0]['content'] = template.format(question=question, context=context, answer_instruction=ANSWER_INSTRUCTION if example['question_type'] == "open_qa" else ANSWER_INSTRUCTION_MULTI_CHOICE)
                
    else:
        if context:
            messages[0]['content'] = template.format(question=question, answer_instruction=ANSWER_INSTRUCTION if example['question_type'] == "open_qa" else ANSWER_INSTRUCTION_MULTI_CHOICE, context=context)
        else:
            messages[0]['content'] = template.format(question=question, answer_instruction=ANSWER_INSTRUCTION if example['question_type'] == "open_qa" else ANSWER_INSTRUCTION_MULTI_CHOICE)
            
    encoded = _encode_chat_format(model_name_or_path=model_name_or_path,
                                    messages=messages, 
                                    tokenizer=tokenizer, 
                                    max_seq_length=max_seq_length, 
                                    chat_format=chat_format)
    
    ret['input_ids'] = encoded['input_ids']
    ret['labels'] = encoded['labels']
    ret['attention_mask'] = encoded['attention_mask']
        

    return ret


def encode_with_qa_format(
        example,
        tokenizer,
        max_seq_length,
        retrieval_embed_length,
        use_rag_tuning=True,
        use_retriever_embed=False,
        use_paraphrase_finetune=False,
        background_dropout_rate=0.0, ):
    '''
    Here we assume each example has three fields:
        1) question
        2) answer
        3) background  
    '''

    def get_input_and_labels(prompt, label, background=None):
        input_ids = tokenizer(prompt, max_length=max_seq_length, truncation=True).input_ids
        labels = [-100] * len(input_ids)

        ## match backgrounds
        if background is not None:
            background_ids = tokenizer(background, add_special_tokens=False).input_ids
            background_start_idx = find_matched_index(input_ids, background_ids)
            if background_start_idx != -1:
                labels[background_start_idx:background_start_idx + len(background_ids)] = input_ids[
                                                                                          background_start_idx:background_start_idx + len(
                                                                                              background_ids)]

        ## match labels
        label_ids = tokenizer(label, add_special_tokens=False).input_ids
        label_start_idx = find_matched_index(input_ids, label_ids)
        if label_start_idx != -1:  ## extreme long propmt
            labels[label_start_idx:label_start_idx + len(label_ids)] = input_ids[
                                                                       label_start_idx:label_start_idx + len(label_ids)]
            labels[-1] = input_ids[-1]  ## eos

        return torch.tensor(input_ids), torch.tensor(labels)

    question, answer, task_type = example['question'].strip(), example['answer'].strip(), example['task_type'].strip()
    start_prompt = get_start_prompt(task_type, include_retrieval=use_rag_tuning)
    ret = {}

    if use_rag_tuning and use_retriever_embed:
        background = example['background'].strip()
        ret['retriever_input_text'] = [background]

    if use_rag_tuning:

        prompt_background = " ".join([COMPRESS] * retrieval_embed_length)

        if use_paraphrase_finetune:
            template = PROMPT_TEMPLATES[task_type][True][True]
            prompt = start_prompt + "\n\n" + template.format_map(
                dict(question=question, answer=answer, background=prompt_background, real_background=background))
            input_ids, labels = get_input_and_labels(prompt, answer, background)
        else:
            template = PROMPT_TEMPLATES[task_type][True][False]
            prompt = start_prompt + "\n\n" + template.format_map(
                dict(question=question, answer=answer, background=prompt_background))
            input_ids, labels = get_input_and_labels(prompt, answer)
        ret["input_ids"] = input_ids.flatten()
        ret['labels'] = labels.flatten()

        ## for traditional-RAG, used as teacher model input
        prompt_background = background
        template = PROMPT_TEMPLATES[task_type][True][False]
        prompt = start_prompt + "\n\n" + template.format_map(
            dict(question=question, answer=answer, background=prompt_background))
        input_ids, labels = get_input_and_labels(prompt, answer)
        ret["input_ids"] = input_ids.flatten()
        ret['labels'] = labels.flatten()

    else:
        template = PROMPT_TEMPLATES[task_type][False]
        prompt = start_prompt + template.format_map(dict(question=question, answer=answer))
        input_ids, labels = get_input_and_labels(prompt, answer)
        ret["input_ids"] = input_ids.flatten()
        ret['labels'] = labels.flatten()

    return ret


def encode_with_completion_format_pretrain(example, tokenizer, max_seq_length, retrieval_embed_length, compress_token_id):
    document = example['text'].strip()

    ## trick for only calculating loss on the document
    _document = tokenizer.eos_token + document
    compress_token = " ".join([COMPRESS] * retrieval_embed_length)

    prompt = random.choice(ParaphraseInstructions).strip()
    prompt = prompt.format_map(dict(compress_token=compress_token, document=_document))

    # prompt = prompt + " " + tokenizer.eos_token

    tokenized_prompt = tokenizer(prompt, max_length=max_seq_length, truncation=True)
    input_ids = tokenized_prompt.input_ids
    # assert len([x for x in input_ids if x==tokenizer.eos_token_id])==2,input_ids
    first_eos_index = input_ids.index(tokenizer.eos_token_id)
    input_ids = input_ids[:first_eos_index] + input_ids[first_eos_index + 1:]  ## strip the additional eos
    input_ids = torch.tensor(input_ids)

    labels = input_ids.clone()
    labels[labels == compress_token_id] = -100
    labels[:first_eos_index] = -100

    ## maybe we should add some attentino mask in the background part to make it hard for LLM to paraphrase
    return {
        "input_ids": input_ids.flatten(),
        "labels": labels.flatten(),
        "retriever_input_text": [document],
    }


def encode_with_completion_format_finetune(
        example,
        tokenizer,
        max_seq_length,
        retrieval_embed_length,
        use_rag_tuning=True,
        use_retriever_embed=False,
        retriever_tokenizer=None,
        background_dropout_rate=0.0,
):
    '''
    Here we assume each example has three fields:
        1) prompt
        2) completion
        3) background  
    '''

    def get_input_and_labels(prompt, completion):
        example_text = prompt + " " + completion  # + " " + tokenizer.eos_token
        tokenized_example = tokenizer(example_text, max_length=max_seq_length, truncation=True, return_tensors='pt')
        input_ids = tokenized_example.input_ids
        labels = input_ids.clone()
        tokenized_prompt_length = \
            tokenizer(prompt, max_length=max_seq_length, truncation=True, return_length=True).length[0]
        labels[:, :tokenized_prompt_length] = -100
        return input_ids, labels

    # dataset = "_".join(example['id'].split("_")[:-1])
    # if dataset not in ["triviaqa","hotpotqa","nq"]:
    ####### FineTune #######
    original_prompt, completion = example['prompt'].strip(), example['completion'].strip()
    ret = {}

    num_split = 1
    if use_rag_tuning and use_retriever_embed:
        background = example['background'].strip()
        sharded_background = split_background(background, retriever_tokenizer, total_max_len=max_seq_length,
                                              single_max_len=180)
        num_split = len(sharded_background)
        ret['retriever_input_text'] = sharded_background

    if use_rag_tuning:

        for idx, prompt_background in enumerate([
            " ".join([COMPRESS] * retrieval_embed_length * num_split),
            background,
        ]):
            prompt = original_prompt
            rag_instruction = random.choice(RAGInstructions).format_map({"background": prompt_background})
            prompt = rag_instruction + prompt
            input_ids, labels = get_input_and_labels(prompt, completion)
            prefix = ""
            if idx == 0: prefix = "compress_"
            ret[prefix + "input_ids"] = input_ids.flatten()
            ret[prefix + 'labels'] = labels.flatten()
    else:
        input_ids, labels = get_input_and_labels(original_prompt, completion)
        ret["input_ids"] = input_ids.flatten()
        ret['labels'] = labels.flatten()

    return ret

    # else:
    #     ####### Validation #######
    #     question,answer,background = example['prompt'],example['completion'],example['background']
    #     prompt_background = " ".join([COMPRESS]*retrieval_embed_length)
    #     prompt_dict = {
    #         "background":prompt_background,
    #         "question":question,
    #         "answer":"",
    #     }
    #     prompt = RAG_QA_PROMPT.format_map(prompt_dict).strip()
    #     tokenized_prompt = tokenizer(prompt,max_length=max_seq_length,truncation=True,return_tensors='pt')

    #     return {
    #         "input_ids":tokenized_prompt.input_ids.flatten(),
    #         "retriever_input_text":background,
    #         "answer":answer,
    #     }


QA_PROMPT = "Q: {question}?\nA: {answer}"
RAG_QA_PROMPT = "Background: {background}\n\n" + QA_PROMPT
PARAPHRASE_RAG_QA_PROMPT = "Background: {background}\nThe above background document is just a paraphrase of the following: {real_background}\n\n" + QA_PROMPT

FECT_CHECKING_PROPMT = "Claim: {question}\nAnswer: {answer}"
RAG_FECT_CHECKING_PROPMT = "Background: {background}\n\n" + FECT_CHECKING_PROPMT
PARAPHRASE_RAG_FECT_CHECKING_PROPMT = "Background: {background}\nThe above background document is just a paraphrase of the following: {real_background}\n\n" + FECT_CHECKING_PROPMT

MULTIPLE_CHOICE_PROMPT = "Question: {question}\nAnswer: {answer}"
RAG_MULTIPLE_CHOICE_PROMPT = "Background: {background}\n\n" + MULTIPLE_CHOICE_PROMPT
PARAPHRASE_RAG_MULTIPLE_CHOICE_PROMPT = "Background: {background}\nThe above background document is just a paraphrase of the following: {real_background}\n\n" + MULTIPLE_CHOICE_PROMPT

PROMPT_TEMPLATES = {
    "open_qa": {True: {True: PARAPHRASE_RAG_QA_PROMPT, False: RAG_QA_PROMPT}, False: QA_PROMPT},
    'fact_checking': {True: {True: PARAPHRASE_RAG_FECT_CHECKING_PROPMT, False: RAG_FECT_CHECKING_PROPMT},
                      False: FECT_CHECKING_PROPMT},
    'multiple_choice': {True: {True: PARAPHRASE_RAG_MULTIPLE_CHOICE_PROMPT, False: RAG_MULTIPLE_CHOICE_PROMPT},
                        False: MULTIPLE_CHOICE_PROMPT},
}


def get_start_prompt(task_type, include_retrieval):
    if task_type == 'open_qa':
        return {
            True: "Refer to the background document and answer the questions:",
            False: "Answer the questions:"
        }[include_retrieval]
    elif task_type == 'fact_checking':
        return {
            True: "Refer to the background document and verify the following claims with \"True\" or \"False\":",
            False: "Verify the following claims with \"True\" or \"False\":"
        }[include_retrieval]
    elif task_type == 'multiple_choice':
        return {
            True: f"The following are multiple choice questions (with answers).\nPlease refer to the background document and answer the questions:",
            False: f"The following are multiple choice questions (with answers)."
        }[include_retrieval]
