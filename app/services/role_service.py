from typing import List , Optional
from app.models.role import Role
from app.models.permission import Permission
from extensions import db

class RoleService:

    @staticmethod
    def get_role_all(search_query: str = "", page: int = 1, per_page: int = 10):
        query = Role.query.order_by(Role.name.asc())
        if search_query:
            query = query.filter(Role.name.contains(search_query))
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def count_roles() -> int:
        return Role.query.count()

    @staticmethod
    def get_role_by_id(role_id: int) ->  Optional[Role]:
        return Role.query.get(role_id)
    
    @staticmethod
    def create_role(data: dict, permission_ids: Optional[List[int]]) -> Role:
        role = Role()
        role.name = data["name"]
        role.description = data.get("description") or ""

        if permission_ids:
            permissions = db.session.scalars(
                db.select(Permission).filter(
                    Permission.id.in_(permission_ids)
                )
            ).all()

            role.permissions = permissions  # type: ignore

        db.session.add(role)
        db.session.commit()
        return role
    
    @staticmethod
    def update_role(role: Role, data: dict, permission_ids: Optional[List[int]] = None) -> Role:
        role.name = data["name"]
        role.description = data.get("description") or ""

        if permission_ids is not None:
            perms = []
            if permission_ids:
                perms = db.session.scalars(
                    db.select(Permission).filter(
                        Permission.id.in_(permission_ids)
                    )
                ).all()

            role.permissions = perms # type: ignore
        db.session.add(role)
        db.session.commit()
        return role
    
    @staticmethod
    def delete_role(role: Role) -> None:
        db.session.delete(role)
        db.session.commit()
        
    