import openai
import transformers
from transformers import GPT2Tokenizer

# OpenAI GPT-2 tokenizer is the same as GPT-3 tokenizer
# we use it to count the number of tokens in the text
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

with open("data/geometry_slovenian.tex", "r") as f:
    text = f.read()


chunks = text.split('\n\n')
ntokens = []
for chunk in chunks:
    ntokens.append(len(tokenizer.encode(chunk)))
max(ntokens)


def group_chunks(chunks, ntokens, max_len=1000):
    """
    Group very short chunks, to form approximately a page long chunks.
    """
    batches = []
    cur_batch = ""
    cur_tokens = 0

    # iterate over chunks, and group the short ones together
    for chunk, ntoken in zip(chunks, ntokens):
        cur_tokens += ntoken + 2  # +2 for the newlines between chunks

        # if adding this chunk would exceed the max length, finalize the current batch and start a new one
        if ntoken + cur_tokens > max_len:
            batches.append(cur_batch)
            cur_batch = chunk
        else:
            cur_batch += "\n\n" + chunk
    batches.append(cur_batch)
    return batches

chunks = group_chunks(chunks, ntokens)
len(chunks)