from sqlalchemy import select
from typing import Sequence, Mapping
from db import SessionLocal, init_db
from models import User, Comment
from sqlalchemy.orm import selectinload


# CREATE TABLE users (
# 	id INTEGER NOT NULL,
# 	name VARCHAR(100) NOT NULL,
# 	email VARCHAR(200) NOT NULL,
# 	PRIMARY KEY (id)
# )


def add_user(user: Mapping[str, str]):
    from sqlalchemy.exc import IntegrityError
    with SessionLocal() as s:
        try:
            u = User(name=user.get("name"), email=user.get("email"))
            s.add(u)
            s.commit()
            s.refresh(u)
            return u
        except IntegrityError:
            s.rollback()
            raise


def get_users() -> Sequence[User]:
    with SessionLocal() as s:
        result = select(User).order_by(User.id)
        return s.execute(result).scalars().all()


def get_user_by_email(email: str) -> User | None:
    with SessionLocal() as s:
        result = select(User).options(selectinload(User.comments)).where(User.email == email)
        return s.execute(result).scalar_one_or_none()


def add_comment(user_id: int, text: str):
    with SessionLocal() as s:
        comment = Comment(text=text, user_id=user_id)
        s.add(comment)
        s.commit()
        s.refresh(comment)
        return comment


if __name__ == "__main__":
    init_db(reset=True)

    for x in range(5):
        user = {
            "name": f"user{x}",
            "email": f"email{x}@email.com"
        }
        new_user = add_user(user)
        add_comment(new_user.id, "This is my first comment!")
    print([u.email for u in get_users()])
    user = get_user_by_email("email0@email.com")

    for c in user.comments:
        print(f"User {user.name} said:", c.text)
