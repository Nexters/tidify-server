from app.models.models.bookmarks import BookmarkCreateRequest, BookmarkWithMeta
from core.utils import opengraph


def get_bookmark_info_with_og(bookmark_in: BookmarkCreateRequest) -> BookmarkWithMeta:
    domain = opengraph.get_domain(bookmark_in.url)
    soup = opengraph.get_page(bookmark_in.url)

    title = bookmark_in.title if bookmark_in.title else opengraph.get_og_title(soup)
    return BookmarkWithMeta(
            url=bookmark_in.url,
            title=title,
            favicon_url=opengraph.get_favicon(soup, domain),
            og_url=opengraph.get_og_image_url(soup)
    )
