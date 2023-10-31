from litestar import Request, Router, get
from litestar.response import Template

from app.utils import (
    filter_by_artist,
    get_all_tags,
    get_artist_tags,
    get_images_data,
    get_total_image_count_from_json,
)


@get("/recent")
async def recent(request: Request) -> Template:
    tag = request.query_params.get("tag")
    total_image_count = get_total_image_count_from_json()
    images_data = get_images_data(sort_by="recent")
    artist_tags, _ = get_artist_tags()
    return Template(
        template_name="index.html",
        context={
            "images_data": images_data,
            "all_tags": get_all_tags(artist_tags),
            "tag": tag,
            "unique_artist_count": len(set(artist_tags.keys())),
            "total_image_count": total_image_count,
        },
    )


@get("/")
async def index(request: Request) -> Template:
    total_image_count = get_total_image_count_from_json()
    search_query = request.query_params.get("search")
    tag = request.query_params.get("tag")

    # Pass the search_query to the get_images_data function
    images_data = get_images_data(tag=tag, search_query=search_query)

    if search_query:
        images_data = filter_by_artist(search_query, images_data)

    artist_tags, _ = get_artist_tags()
    return Template(
        "index.html",
        context={
            "images_data": images_data,
            "all_tags": get_all_tags(artist_tags),
            "tag": tag,
            "unique_artist_count": len(set(artist_tags.keys())),
            "total_image_count": total_image_count,
        },
    )


@get("/alphabetical/{letter:str}")
async def alphabetical(letter: str, request: Request) -> Template:
    total_image_count = get_total_image_count_from_json()
    search_query = request.query_params.get("search")
    tag = request.query_params.get("tag")
    images_data = get_images_data(letter, tag=tag)

    if search_query:
        images_data = filter_by_artist(search_query, images_data)

    artist_tags, _ = get_artist_tags()
    return Template(
        "index.html",
        context={
            "images_data": images_data,
            "all_tags": get_all_tags(artist_tags),
            "tag": tag,
            "unique_artist_count": len(set(artist_tags.keys())),
            "total_image_count": total_image_count,
        },
    )


# @get("/{artist_name:str}")
# def artist_view(artist_name: str) -> Template:
#     total_image_count = get_total_image_count_from_json()
#     artist_tags, _ = get_artist_tags()
#     images_data = get_images_data(tag=None)  # Get data for all images
#     images_data = [
#         image for image in images_data if image.artist_name.lower() == artist_name.lower()
#     ]

#     return Template(
#         "artist.html",
#         context={
#             "artist_name": artist_name,
#             "images_data": images_data,
#             "all_tags": get_all_tags(artist_tags),
#             "unique_artist_count": len(set(artist_tags.keys())),
#             "total_image_count": total_image_count,
#         },
#     )


# router = Router("/", route_handlers=[index, recent, alphabetical, artist_view])
router = Router("/", route_handlers=[index, recent, alphabetical])
