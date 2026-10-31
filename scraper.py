import requests
from bs4 import BeautifulSoup
from preprocessor import clean_text

def scrape_text(url):
    try:


            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            response.raise_for_status()


            soup = BeautifulSoup(response.text, "html.parser")


            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()


            text = soup.get_text(separator=" " , strip= True)
            cleaned_text = clean_text(text)

            if not cleaned_text.strip():
                raise ValueError("No readable text found on this webpage.")

            return cleaned_text

    except requests.exceptions.Timeout:
        raise ValueError("The webpage took too Long to respond. Please try again.")
    
    except requests.exceptions.HTTPError as e:
        raise ValueError(f"Website returned an HTTP error: {e.response.status_code}. Please check the URL and try again.")

    except requests.exceptions.ConnectionError:
        raise ValueError("Could not connect to the website. Check the URL or your internet connection")

    except requests.exceptions.RequestException:
         raise ValueError("Could not fetch the webpage . Please check the URL and try again")




    
if __name__ == "__main__":

    url = "https://example.com"

    text = scrape_text(url)

    print(text)