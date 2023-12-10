from dataclasses import dataclass


@dataclass
class ImageEntity:
    artist_name: str
    prompt_index: str
    filename: str
    url: str
    date_added: str
    tags: list[str]
