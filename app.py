from flask import Flask, request,render_template 
from detector import detect_text
from scraper import scrape_text

app = Flask(__name__)

@app.route('/')
def home():
    return render_template(
    "index.html",
    text="",
    url="",
    text_result=None,
    text_score=None,
    url_result=None,
    url_score=None
)

@app.route("/analyze", methods=["POST"])
def analyze():

    text= request.form.get("text","")

    text_result = None
    text_score = None
    text_explanation = None

    if not text.strip():
        text_result = "Please enter some text to analyze."

       
    else:
        prediction = detect_text(text)

        label = prediction[0]['label']  # Assuming the prediction is a list of dictionaries with a 'label' key.
        text_score = prediction[0]['score']

        if label == "ai":
            text_result = "Likely AI-generated"
        else:
            text_result = "Likely Human-generated"

    return render_template(
         "index.html",
            text=text,
            url="",
            text_result=text_result,
            text_score=text_score,
            url_result=None,
            url_score=None
)


@app.route("/analyze-url", methods= ["POST"])
def analyze_url():

    url = request.form.get("url", "").strip()

    if not url:
        url_result = "Please enter a webpage URL."
        url_score = None

    elif not url.startswith(("http://", "https://")):
        url_result = "Please enter a URL starting with http:// or https://."
        url_score = None

    else:
        try:
            text = scrape_text(url) 

            if not text.strip():
                url_result = "No readable text was found on tha webpage."
                url_score = None

            else:
                prediction = detect_text(text)

                label = prediction[0]["label"]
                url_score = prediction[0]["score"]

                if label =="ai":
                    url_result = "Likely AI-generated"
                else:
                    url_result = "Likely Human-generated"

        except ValueError as e:
            url_result = str(e)
            url_score = None

        except Exception as e:
            url_result =(
                 "We couldn't analyze that webpage. "
                 "Please try another URL."
            )
            url_score = None
            print("URL analysis error:", e)

    return render_template(
        "index.html",
        text="",
        url=url,
        text_result=None,
        text_score=None,
        url_result=url_result,
        url_score=url_score
    )


if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)