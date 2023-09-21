from flask import Flask, render_template, request
import os
import csv
import json
import unicodedata

class Config():
    SECURE_SSL_REDIRECT = True

app = Flask(__name__)
app.config.from_object(Config)

def normalize_nfc(string):
    return unicodedata.normalize('NFC', string)

def get_artist_tags():
    artist_tags = {}
    unrecognized_artists = set()
    
    # Read from local CSV file
    with open("static/SDXL Image Synthesis Style Studies Database (Copy of The List) - Artists.csv", 'r', encoding='utf-8') as f:
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
                    artist_tags[artist_name] = [tag.strip() for tag in tags_column.split(",") if tag.strip() not in ["", "-"]]

                # Add alternative artist names with a space instead of a hyphen
                if len(row) >= 7:
                    alternative_name = artist_name.replace("-", " ")
                    alternative_name = normalize_nfc(alternative_name)  # Normalize alternative name
                    tags_column = row[7] if len(row) > 7 else ""
                    if alternative_name not in artist_tags:
                        artist_tags[alternative_name] = [tag.strip() for tag in tags_column.split(",") if tag.strip() not in ["", "-"]]
    
    return artist_tags, unrecognized_artists

def get_all_tags(artist_tags):
    all_tags = set()
    for tags in artist_tags.values():
        all_tags.update(tags)
    all_tags.add("#unrecognized")  # Add the "unrecognized" tag
    return sorted(list(all_tags))

def get_images_data(letter=None, tag=None, sort_by='alphabetical', search_query=None):
    images_data = []
    artist_tags, unrecognized_artists = get_artist_tags()
    
    with open("static/index.json", "r") as f:
        json_data = json.load(f)

    # Extract image filenames and dates from the JSON data
    image_date_map = json_data["images"]

    for filename, date_added in image_date_map.items():
        normalized_filename = normalize_nfc(filename)  # Normalize filename
        if (normalized_filename.endswith(".jpg") or normalized_filename.endswith(".png")) and "_0" in normalized_filename:
            artist_name = " ".join(normalized_filename.split("_")[:-1]).replace("-", " ").replace("  ", " ")
            artist_name = normalize_nfc(artist_name)  # Normalize artist name
            prompt_index = normalized_filename.split("_")[-1].split(".")[0]
            
            # Use local file path instead of URL
            image_path = os.path.join("/static/grids/", normalized_filename)
            tags = artist_tags.get(artist_name, [])
            
            if artist_name in unrecognized_artists:
                tags.append("#unrecognized")
                
            images_data.append({
                "artist_name": artist_name,
                "prompt_index": prompt_index,
                "filename": normalized_filename,
                "url": image_path,
                "date_added": date_added,
                "tags": tags
            })

    if tag:
        if tag == "#unrecognized":
            images_data = [image for image in images_data if image["artist_name"] in unrecognized_artists]
        else:
            tag = tag.lower().strip()  # Clean and format the tag for comparison
            images_data = [image for image in images_data if any(t.lower().strip() == tag for t in image["tags"])]
            images_data = [image for image in images_data if image["artist_name"] not in unrecognized_artists]

    elif not tag and sort_by != 'recent' and not search_query:
        # Filter out unrecognized artists only if no tag is provided and it's not a recent sort and no search query is present
        images_data = [image for image in images_data if image["artist_name"] not in unrecognized_artists]

    if letter:
        images_data = [image for image in images_data if image["artist_name"].split()[-1][0].upper() == letter.upper()]

    if sort_by == 'alphabetical':
        images_data.sort(key=lambda x: x["artist_name"].split()[-1])
    elif sort_by == 'recent':
        images_data.sort(key=lambda x: x["date_added"], reverse=True)

    return images_data


def get_total_image_count_from_json():
    with open("static/index.json", "r") as f:
        json_data = json.load(f)

    # Extract image filenames from the JSON data
    image_date_map = json_data["images"]

    total_images = 0

    for filename in image_date_map:
        if (filename.endswith(".jpg") or filename.endswith(".png")) and "_0" in filename:
            total_images += 1

    return total_images


@app.route('/recent')
def recent():
    tag = request.args.get("tag")
    total_image_count = get_total_image_count_from_json()
    images_data = get_images_data(sort_by='recent')
    artist_tags, _ = get_artist_tags()
    return render_template("index.html", images_data=images_data, all_tags=get_all_tags(artist_tags), tag=tag, unique_artist_count=len(set(artist_tags.keys())), total_image_count=total_image_count)
    
@app.route("/")
def index():
    total_image_count = get_total_image_count_from_json()
    search_query = request.args.get("search")
    tag = request.args.get("tag")
    
    # Pass the search_query to the get_images_data function
    images_data = get_images_data(tag=tag, search_query=search_query)

    if search_query:
        images_data = [image for image in images_data if search_query.lower() in image["artist_name"].lower()]

    artist_tags, _ = get_artist_tags()
    return render_template("index.html", images_data=images_data, all_tags=get_all_tags(artist_tags), tag=tag, unique_artist_count=len(set(artist_tags.keys())), total_image_count=total_image_count)
    
@app.route("/alphabetical/<string:letter>")
def alphabetical(letter):
    total_image_count = get_total_image_count_from_json()
    search_query = request.args.get("search")
    tag = request.args.get("tag")
    images_data = get_images_data(letter, tag=tag)

    if search_query:
        images_data = [image for image in images_data if search_query.lower() in image["artist_name"].lower()]

    artist_tags, _ = get_artist_tags()
    return render_template("index.html", images_data=images_data, all_tags=get_all_tags(artist_tags), tag=tag, unique_artist_count=len(set(artist_tags.keys())), total_image_count=total_image_count)

@app.route("/<string:artist_name>")
def artist_view(artist_name):
    total_image_count = get_total_image_count_from_json()
    artist_tags, _ = get_artist_tags()
    images_data = get_images_data(tag=None)  # Get data for all images
    images_data = [image for image in images_data if image["artist_name"].lower() == artist_name.lower()]
  
    return render_template("artist.html", artist_name=artist_name, images_data=images_data, all_tags=get_all_tags(artist_tags), unique_artist_count=len(set(artist_tags.keys())), total_image_count=total_image_count)
if __name__ == "__main__":
    app.run(debug=False)