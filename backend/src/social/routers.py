from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.auth_config import current_active_verified_user
from ..auth.models import User
from ..db import get_async_session
from .models import Post
from .schemas import PostCreate

router = APIRouter()


@router.get("/my_posts/")
async def get_my_posts(
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Post).where(Post.author_id == user.id)
        result = await session.execute(query)
        return {
            "status": status.HTTP_200_OK,
            "data": result.scalars().all(),
            "details": None
        }
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "details": str(error),
            },
        )


@router.get("/")
@cache(expire=600)
async def get_all_posts(
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Post)
        result = await session.execute(query)
        return {
            "status": status.HTTP_200_OK,
            "data": result.scalars().all(),
            "details": None
        }
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "details": str(error),
            },
        )


@router.post("/")
async def add_post(
    new_post: PostCreate,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        data = new_post.model_dump()
        data['author_id'] = user.id
        post = insert(Post).values(data).returning(Post.id)
        result = await session.execute(post)
        data['id'] = result.fetchone()[0]
        await session.commit()
        return {
            "status": status.HTTP_200_OK,
            "data": data,
            "details": None
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "details": 'Название статьи должно быть уникально!'
            },
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "details": str(error)
            },
        )


@router.get("/{post_id}/")
async def get_post_by_id(
    post_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Post).where(Post.id == post_id)
        post = await session.execute(query)
        existing_post = post.scalar_one_or_none()
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "details": "Поста с данным id не существует."
                },
            )
        return {
            "status": status.HTTP_200_OK,
            "data": existing_post,
            "details": None
        }
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "details": str(error),
            },
        )


@router.patch("/{post_id}/")
async def patch_post(
    post_id: int,
    new_post: PostCreate,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Post).where(Post.id == post_id)
        post = await session.execute(query)
        existing_post = post.scalar_one_or_none()
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "details": "Поста с данным id не существует."
                },
            )
        if existing_post.author != user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "status": status.HTTP_403_FORBIDDEN,
                    "data": None,
                    "details": "Изменять можно только свои посты."
                },
            )
        data = new_post.model_dump()
        existing_post.title = data['title']
        existing_post.slug = data['slug']
        existing_post.text = data['text']

        await session.commit()

        return {
            "status": status.HTTP_200_OK,
            "data": data,
            "details": None
        }
    except HTTPException as http_error:
        raise http_error
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "details": 'Название статьи должно быть уникально!'
            },
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "details": str(error)
            },
        )


@router.delete("/{post_id}/")
async def delete_post(
    post_id: int,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Post).where(Post.id == post_id)
        post = await session.execute(query)
        existing_post = post.scalar_one_or_none()
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "details": "Поста с данным id не существует."
                },
            )
        if existing_post.author != user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "status": status.HTTP_403_FORBIDDEN,
                    "data": None,
                    "details": "Изменять можно только свои посты."
                },
            )
        await session.delete(existing_post)
        await session.commit()

        return {
            "status": status.HTTP_200_OK,
            "data": f"Пост c id={post_id} удалён.",
            "details": None
        }
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "details": str(error)
            },
        )


@router.post("/like/{post_id}/")
async def add_like_unlike(
    post_id: int,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Post).where(Post.id == post_id)
        post = await session.execute(query)
        result = post.scalar_one_or_none()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "details": "Поста с данным id не существует."
                },
            )
        if result.author == user:
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail={
                    "status": status.HTTP_423_LOCKED,
                    "data": None,
                    "details": "Лайки своих постов запрещены."
                },
            )
        like = await result.like_post(session, user)
        like.update({'post_id': post_id})
        return {
            "status": status.HTTP_200_OK,
            "data": like,
            "details": None
        }
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "details": str(error)
            },
        )
