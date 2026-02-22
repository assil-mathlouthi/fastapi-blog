from fastapi import APIRouter
from fastapi import HTTPException, status
from database import SessionDep
from models import Post, User
from schemas import PostCreate, PostResponse, PostUpdate
from sqlalchemy import select
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("", response_model=list[PostResponse])
async def get_posts(db: SessionDep):
    result = await db.execute(select(Post).options(selectinload(Post.author)))
    posts = result.scalars().all()
    return posts

@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
async def create_post(post: PostCreate, db: SessionDep):
    user = await db.get(User, post.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    new_post = Post(**post.model_dump())
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post,attribute_names=["author"])
    return new_post


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: SessionDep):
    post = await db.get(Post, post_id,options=[selectinload(Post.author)])
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")

@router.put("/{post_id}", response_model=PostResponse)
async def update_post_full(post_id: int,post_data : PostCreate, db: SessionDep):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    if post_data.user_id != post.user_id:
        user =  await db.get(User, post_data.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    post.title = post_data.title
    post.content = post_data.content
    post.user_id = post_data.user_id
    await db.commit()
    await db.refresh(post,attribute_names=["author"])
    return post


@router.patch("/{post_id}", response_model=PostResponse)
async def update_post_partial(post_id: int,post_data : PostUpdate, db: SessionDep):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    
    update_data = post_data.model_dump(exclude_unset=True)
    for attr , value in update_data.items():
        setattr(post,attr,value)
    
    await db.commit()
    await db.refresh(post,attribute_names=["author"])
    return post

@router.delete("/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id:int, db: SessionDep):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    await db.delete(post)
    await db.commit()