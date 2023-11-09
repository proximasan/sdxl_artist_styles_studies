from functools import cache
import json
from pathlib import Path
import unicodedata
import os
import csv
from typing import Literal, Optional, Tuple

from app.entitites import ImageEntity


@cache
def get_image_dict_from_json() -> dict[str, str]:
    """Get the image dictionary from the index.json file.

    Returns:
        dict[str, str]: A dictionary of image filenames and their corresponding dates.
    """
    index_json_path = Path("static/index.json").resolve()
    with open(index_json_path, "r") as f:
        json_data = json.load(f)
    return json_data["images"]


def normalize_nfc(string: str) -> str:
    """Normalize a string to NFC.

    Args:
        string (str): The string to normalize.

    Returns:
        str: The normalized string.
    """
    return unicodedata.normalize("NFC", string)


@cache
def get_artist_tags() -> Tuple[dict[str, list[str]], set[str]]:
    """Get artist tags from the CSV file.

    Returns:
        Tuple[dict[str, list[str]], set[str]]: A tuple containing a dictionary of artist tags and a set of unrecognized artists.
    """
    artist_tags = {}
    unrecognized_artists = set()

    # Read from local CSV file
    with open(
        "static/SDXL Image Synthesis Style Studies Database (Copy of The List) - Artists.csv",
        "r",
        encoding="utf-8",
    ) as f:
        csv_reader = csv.reader(f)

        for index, row in enumerate(csv_reader):
            # Skip header rows as needed
            if index < 3:
                continue

            if len(row) >= 4:
                artist_fields = [field.strip() for field in row[:2]]
                artist_name = f"{artist_fields[1]} {artist_fields[0]}"
                artist_name = normalize_nfc(artist_name)  # Normalize artist name

                # Check if artist is unrecognized
                if row[3].strip().lower() == "no":
                    unrecognized_artists.add(artist_name)
                else:
                    tags_column = row[7] if len(row) > 7 else ""
                    artist_tags[artist_name] = [
                        tag.strip()
                        for tag in tags_column.split(",")
                        if tag.strip() not in ["", "-"]
                    ]

                # Add alternative artist names with a space instead of a hyphen
                if len(row) >= 7:
                    alternative_name = artist_name.replace("-", " ")
                    alternative_name = normalize_nfc(
                        alternative_name
                    )  # Normalize alternative name
                    tags_column = row[7] if len(row) > 7 else ""
                    if alternative_name not in artist_tags:
                        artist_tags[alternative_name] = [
                            tag.strip()
                            for tag in tags_column.split(",")
                            if tag.strip() not in ["", "-"]
                        ]

    return artist_tags, unrecognized_artists


def get_all_tags(artist_tags: dict[str, list[str]]) -> list[str]:
    """Get all tags from the artist tags dictionary.

    Args:
        artist_tags (dict[str, list[str]]): The artist tags dictionary.

    Returns:
        list[str]: A list of all tags.
    """
    all_tags = set()
    for tags in artist_tags.values():
        all_tags.update(tags)
    all_tags.add("#unrecognized")  # Add the "unrecognized" tag
    return sorted(list(all_tags))


@cache
def get_images_data(
    letter: Optional[str] = None,
    tag: Optional[str] = None,
    sort_by: Literal["alphabetical", "recent"] = "alphabetical",
    search_query: bool = False,
) -> list[ImageEntity]:
    """Get the images data.

    Args:
        letter (Optional[str], optional): Letter to search by. Defaults to None.
        tag (Optional[str], optional): Tag to search by. Defaults to None.
        sort_by (Literal[&quot;alphabetical&quot;, &quot;recent&quot;], optional): Sort for the list. Defaults to "alphabetical".
        search_query (bool, optional): Search query. Defaults to False.

    Returns:
        list[ImageEntity]: A list of ImageEntity objects.
    """
    images_data: list[ImageEntity] = []
    artist_tags, unrecognized_artists = get_artist_tags()

    image_date_map = get_image_dict_from_json()

    for filename, date_added in image_date_map.items():
        normalized_filename = normalize_nfc(filename)  # Normalize filename
        if (
            normalized_filename.endswith(".jpg") or normalized_filename.endswith(".png")
        ) and "_0" in normalized_filename:
            artist_name = (
                " ".join(normalized_filename.split("_")[:-1])
                .replace("-", " ")
                .replace("  ", " ")
            )
            artist_name = normalize_nfc(artist_name)  # Normalize artist name
            prompt_index = normalized_filename.split("_")[-1].split(".")[0]

            # Use local file path instead of URL
            image_path = os.path.join("/static/grids/", normalized_filename)
            tags = artist_tags.get(artist_name, [])

            if artist_name in unrecognized_artists:
                tags.append("#unrecognized")

            images_data.append(
                ImageEntity(
                    artist_name=artist_name,
                    prompt_index=prompt_index,
                    filename=normalized_filename,
                    url=image_path,
                    date_added=date_added,
                    tags=tags,
                )
            )

    if tag:
        if tag == "#unrecognized":
            images_data = [
                image
                for image in images_data
                if image.artist_name in unrecognized_artists
            ]
        else:
            tag = tag.lower().strip()  # Clean and format the tag for comparison
            images_data = [
                image
                for image in images_data
                if any(t.lower().strip() == tag for t in image.tags)
            ]
            images_data = [
                image
                for image in images_data
                if image.artist_name not in unrecognized_artists
            ]
    elif sort_by != "recent" and not search_query:
        # Filter out unrecognized artists only if no tag is provided and it's not a recent sort and no search query is present
        images_data = [
            image
            for image in images_data
            if image.artist_name not in unrecognized_artists
        ]

    if letter:
        images_data = [
            image
            for image in images_data
            if image.artist_name.split()[-1][0].upper() == letter.upper()
        ]

    if sort_by == "alphabetical":
        images_data.sort(key=lambda x: x.artist_name.split()[-1])
    elif sort_by == "recent":
        images_data.sort(key=lambda x: x.date_added, reverse=True)

    return images_data


@cache
def get_total_image_count_from_json() -> int:
    """Get the total image count from the index.json file.

    Returns:
        int: The total image count.
    """
    image_date_map = get_image_dict_from_json()
    return sum(
        bool((filename.endswith((".jpg", ".png")) and "_0" in filename))
        for filename in image_date_map
    )


def filter_by_artist(
    search_query: str, images_data: list[ImageEntity]
) -> list[ImageEntity]:
    """Filter images by artist name.

    Args:
        search_query (str): The search query.
        images_data (list[ImageEntity]): The list of images.

    Returns:
        list[ImageEntity]: The filtered list of images.
    """
    return [
        image
        for image in images_data
        if search_query.lower() in image.artist_name.lower()
    ]


def check_grids_folder_exists() -> bool:
    """Check if the grids folder exists.

    Returns:
        bool: True if the grids folder exists, False otherwise.
    """
    return Path("static/grids/").resolve().exists()


def download_grid_file():
    """Download the grid file from HuggingFace Hub."""
    if not check_grids_folder_exists():
        Path("static/grids/").resolve().mkdir(parents=True, exist_ok=True)
        from huggingface_hub import snapshot_download

        snapshot_download(
            repo_id="parrotzone/sdxl-1.0", repo_type="dataset", local_dir="static/"
        )
