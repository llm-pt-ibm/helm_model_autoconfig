import requests
from bs4 import BeautifulSoup


def get_huggingface_model_info(model_url):
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
            parameters = (
                model_size_div.get_text(strip=True).replace("params", "").strip()
            )

    return {
        "repo_name": repo_name,
        "description": description,
        "release_date": release_date,
        "max_sequence_length": max_sequence_length,
        "parameters": parameters,
    }
