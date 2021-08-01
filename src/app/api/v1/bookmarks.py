from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from starlette.requests import Request  # noqa

from app.models.models.bookmarks import BookmarkListResponse, BookmarkResponse, BookmarkCreateRequest, \
    BookmarkUpdateRequest
from app.crud import bookmark_crud
from core.errors import exceptions
from core.utils.query_utils import to_dict
from database.conn import db
from database.schema import Bookmarks

bookmark_router = APIRouter(prefix="/bookmarks")
__valid_id = Path(..., title="The ID of bookmark to get", ge=1)


@bookmark_router.get("/", response_model=BookmarkListResponse)
async def list_bookmarks_by_member(
        request: Request,
        session: Session = Depends(db.session)
) -> BookmarkListResponse:
    """
    curl -X 'GET' \
      'http://0.0.0.0:8080/api/v1/bookmarks/' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer
      eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
      .eyJpZCI6MSwiZW1haWwiOiJtaW5rajE5OTJAZ21haWwuY29tIiwibmFtZSI6Imxlb28uaiIsInByb2ZpbGVfaW1nIjoiaHR0cDovL2sua2FrYW9jZG4ubmV0L2RuL2hFUTBLL2J0cmFzVmFWaldHL2VLeHN4RHRteXllM2dBQWRLVWFQQTEvaW1nXzY0MHg2NDAuanBnIiwic25zX3R5cGUiOiJrYWthbyJ9.sN2znQnLSvoUoOT08qhtXARKiEBaJGRulxKPY1-4MhI'
    """
    # TODO: pagination
    bookmarks = await bookmark_crud.get_bookmarks_by_user_id(session, user_id=request.state.user.id)
    return BookmarkListResponse(
            bookmarks=[BookmarkResponse(id=bookmark.id,
                                        user_id=bookmark.user_id,
                                        title=bookmark.title,
                                        url=bookmark.url) for bookmark in bookmarks],
            bookmarks_count=len(bookmarks)
    )


@bookmark_router.post("/", response_model=BookmarkResponse, status_code=201)
async def create_bookmark(
        request: Request,
        bookmark_in: BookmarkCreateRequest,
        session: Session = Depends(db.session)
) -> BookmarkResponse:
    """
    curl -X 'POST' \
      'http://0.0.0.0:8080/api/v1/bookmarks/' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer
      eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
      .eyJpZCI6MSwiZW1haWwiOiJtaW5rajE5OTJAZ21haWwuY29tIiwibmFtZSI6Imxlb28uaiIsInByb2ZpbGVfaW1nIjoiaHR0cDovL2sua2FrYW9jZG4ubmV0L2RuL2hFUTBLL2J0cmFzVmFWaldHL2VLeHN4RHRteXllM2dBQWRLVWFQQTEvaW1nXzY0MHg2NDAuanBnIiwic25zX3R5cGUiOiJrYWthbyJ9.sN2znQnLSvoUoOT08qhtXARKiEBaJGRulxKPY1-4MhI' \
      -H 'Content-Type: application/json' \
      -d '{
      "title": "네이버",
      "url": "www.naver.com"
    }'
    """
    user_id = request.state.user.id
    bookmark = await bookmark_crud.create_bookmark(session, user_id, bookmark_in)
    return BookmarkResponse(**to_dict(bookmark))


@bookmark_router.patch("/{bookmark_id}", response_model=BookmarkResponse, status_code=201)
async def update_bookmark(
        request: Request,
        bookmark_in: BookmarkUpdateRequest,
        bookmark_id: int = __valid_id,
        session: Session = Depends(db.session)
) -> BookmarkResponse:
    """
    curl -X 'PATCH' \
      'http://0.0.0.0:8080/api/v1/bookmarks/3' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer
      eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
      .eyJpZCI6MSwiZW1haWwiOiJtaW5rajE5OTJAZ21haWwuY29tIiwibmFtZSI6Imxlb28uaiIsInByb2ZpbGVfaW1nIjoiaHR0cDovL2sua2FrYW9jZG4ubmV0L2RuL2hFUTBLL2J0cmFzVmFWaldHL2VLeHN4RHRteXllM2dBQWRLVWFQQTEvaW1nXzY0MHg2NDAuanBnIiwic25zX3R5cGUiOiJrYWthbyJ9.sN2znQnLSvoUoOT08qhtXARKiEBaJGRulxKPY1-4MhI' \
      -H 'Content-Type: application/json' \
      -d '{
      "title": "kakao",
      "url": "www.kakao.com"
    }'
    """
    user_id = request.state.user.id
    bookmark = bookmark_crud.update_bookmark(session, user_id, bookmark_id, bookmark_in)
    return BookmarkResponse(**to_dict(bookmark))


@bookmark_router.delete("/{bookmark_id}", status_code=204)
async def delete_bookmark(
        bookmark_id: int = __valid_id,
        session: Session = Depends(db.session)
) -> None:
    """
    curl -X 'DELETE' \
      'http://0.0.0.0:8080/api/v1/bookmarks/3' \
      -H 'Authorization: Bearer
      eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
      .eyJpZCI6MSwiZW1haWwiOiJtaW5rajE5OTJAZ21haWwuY29tIiwibmFtZSI6Imxlb28uaiIsInByb2ZpbGVfaW1nIjoiaHR0cDovL2sua2FrYW9jZG4ubmV0L2RuL2hFUTBLL2J0cmFzVmFWaldHL2VLeHN4RHRteXllM2dBQWRLVWFQQTEvaW1nXzY0MHg2NDAuanBnIiwic25zX3R5cGUiOiJrYWthbyJ9.sN2znQnLSvoUoOT08qhtXARKiEBaJGRulxKPY1-4MhI' \
      -H 'accept: */*'
    """
    bookmark = Bookmarks.filter(session=session, id=bookmark_id)
    if not bookmark.first():
        raise exceptions.BookmarkNotFoundException(bookmark_id=bookmark_id)
    bookmark.delete(auto_commit=True)
