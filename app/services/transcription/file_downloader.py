import requests
import tempfile


def download_file(url: str) -> str:

    response = requests.get(url)

    response.raise_for_status()

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    temp_file.write(response.content)
    temp_file.close()

    return temp_file.name