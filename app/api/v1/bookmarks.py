from fastapi import APIRouter


bookmark_router = APIRouter(prefix="/bookmarks")

@bookmark_router.get("/{user_id}")
async def list_bookmarks_by_user(user_id: int):
  return "hello bookarks"



@bookmark_router.post("/{user_id}")
async def create_bookmarks_by_user(user_id: int):
  pass

# response_model=PetOut
# return await pet_crud.select_pets_by_user_id(user_id)
# return await pet_crud.insert_pet_by_user_id(item, user_id)
  
  

