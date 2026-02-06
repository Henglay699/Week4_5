from typing import List, Optional
from app.models.user import User
from app.models.role import Role
from extensions import db

class UserService:
    @staticmethod
    def get_all(search_query: str = "", page: int = 1, per_page: int = 10):
        query = User.query.order_by(User.id.desc())
        if search_query:
            query = query.filter(
                db.or_(
                    User.username.contains(search_query),
                    User.email.contains(search_query),
                    User.full_name.contains(search_query)
                )
            )
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def count_all_users() -> int:
        return User.query.count()
        
    @staticmethod
    def count_active_users() -> int:
        return User.query.filter_by(is_active=True).count()
    
    @staticmethod
    def count_inactive_users() -> int:
        return User.query.filter_by(is_active=False).count()

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return User.query.get(user_id)

    @staticmethod
    def create(data: dict, password: str, role_id: Optional[int]=None) -> User:
        user = User(
        username=data["username"], # type: ignore
        email=data["email"], # type: ignore
        full_name=data["full_name"] , # type: ignore
        is_active=data.get("is_active", True) # type: ignore
        )
        user.set_password(password)

        if role_id:
            role = db.session.get(Role, role_id) 
            if role:
                user.roles = [role] # type: ignore

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user: User, data: dict, password: Optional[str] = None, role_id: Optional[int]=None) -> User:
        user.username = data["username"]
        user.email = data["email"]
        user.full_name = data["full_name"]
        user.is_active = data.get("is_active", True) # type: ignore

        if password:
            user.set_password(password)

        if role_id:
            roles  = db.session.get(Role, role_id)
            if roles:
                user.roles = [roles] # type: ignore

        db.session.commit()
        return user

    @staticmethod
    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()
