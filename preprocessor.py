import re 

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with a single space
    text = text.strip()

    return text


if __name__ == "__main__":

    sample_text = """
    This    is      some
    messy text.

    It has     extra spaces.
    """

    cleaned = clean_text(sample_text)

    print(cleaned)