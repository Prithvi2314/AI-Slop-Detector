from transformers import pipeline , AutoTokenizer
from preprocessor import clean_text


MODEL_NAME = "frankhanhj/roberta-base-all-sources-ai-identifier"

detector = pipeline(
    "text-classification",
    model=MODEL_NAME
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def split_into_chunks(text , chunk_size = 450):

    tokens = tokenizer(
        text,
        add_special_tokens = False,
        verbose = False
    )["input_ids"]

    chunks =[]

    for i in range(0,len(tokens),chunk_size):

        chunk_tokens = tokens[i:i + chunk_size]

        chunk_text = tokenizer.decode(
            chunk_tokens,
            skip_special_tokens = True
        )

        chunks.append(chunk_text)


    return chunks


def detect_text(text):
    text = clean_text(text)

    if not text:
        raise ValueError("Please provide text to Analyze.")

    chunks = split_into_chunks(text)
    

    for index, chunk in enumerate(chunks,start=1):
        chunk_tokens = tokenizer(
            chunk,
            add_special_tokens =False
        )["input_ids"]

        print(f"chunk {index}: {len(chunk_tokens)} tokens")

    total_tokens = 0 
    total_ai_score = 0.0

    for chunk in chunks:

        chunk_tokens = tokenizer(
            chunk,
            add_special_tokens=False
        )["input_ids"]

        token_count = len(chunk_tokens)

        predictions = detector(chunk, top_k=None)
        # print("DEBUG PREDICTIONS:", predictions)
        

        ai_score = next(
            item["score"]
            for item in predictions
            if item["label"].lower() == "ai"
        )

        total_ai_score += ai_score * token_count
        total_tokens +=token_count

    final_ai_score = total_ai_score / total_tokens

    if final_ai_score >= 0.5:
        final_label = "ai"
        final_score = final_ai_score
    else:
        final_label = "human"
        final_score = 1 - final_ai_score

    return [{
        "label":final_label,
        "score":final_score
    }]





if __name__ == "__main__":

    sample_text = """
    i am prithvi , i had completed my studying but i still couldn't crack a interview , 
    so here  i am tryig to build the basic ai slop detector , but still coundn't do it bcz bcz there are so many loop hole i need to claer 
    and polish my code to make more accurate and reliable to use.
    """

    result = detect_text(sample_text)

    print("Final prediction:", result)

