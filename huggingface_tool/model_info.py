import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


def get_huggingface_model_info(model_url) -> dict:
    """
    Retrieve model information from the Hugging Face model page.

    Args:
        model_url (str): The URL of the Hugging Face model page.
    """
    try:
        response = requests.get(model_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve page: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    repo_name = model_url.split("huggingface.co/")[1]

    description = None
    for tag in soup.find_all("p"):
        strong_tag = tag.find("strong")
        if strong_tag and "Model Summary" in strong_tag.get_text():
            description = tag.get_text(strip=True).replace("Model Summary:", "").strip()
            break

    release_date = None
    for tag in soup.find_all("li"):
        strong_tag = tag.find("strong")
        if strong_tag and "Release Date" in strong_tag.get_text():
            release_date = tag.get_text(strip=True).replace("Release Date:", "").strip()

            release_date = (
                release_date.replace("st", "")
                .replace("nd", "")
                .replace("rd", "")
                .replace("th", "")
            )

            # Parse the date string
            try:
                parsed_date = datetime.strptime(release_date, "%B %d, %Y")
                formatted_date = parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                formatted_date = release_date
            break

    max_sequence_length = None
    seq_length_tag = soup.find("td", string=lambda x: x and "Sequence Length" in x)
    if seq_length_tag:
        max_sequence_length = seq_length_tag.find_next_sibling("td").get_text(
            strip=True
        )

    parameters = None
    parameters_div = soup.find(
        "div", class_="contents", attrs={"data-target": "ModelTensorsParams"}
    )
    if parameters_div:
        model_size_div = parameters_div.find(
            "div", string=lambda x: x and "params" in x
        )
        if model_size_div:
            params_text = (
                model_size_div.get_text(strip=True).replace("params", "").strip()
            )

            match = re.match(r"([0-9.]+)([BKM]?)", params_text)

            if match:
                number_str, suffix = match.groups()
                number = float(number_str)  # Convert the number part to float

                # Convert based on the suffix
                if suffix == "B":
                    parameters = int(
                        number * 1_000_000_000
                    )  # Convert billions to integer
                elif suffix == "M":
                    parameters = int(number * 1_000_000)  # Convert millions to integer
                elif suffix == "K":
                    parameters = int(number * 1_000)  # Convert thousands to integer
                else:
                    parameters = int(number)  # If no suffix, treat as a plain number
            else:
                parameters = params_text

    return {
        "repo_name": repo_name,
        "description": description,
        "release_date": formatted_date,
        "max_sequence_length": max_sequence_length,
        "parameters": parameters,
    }
