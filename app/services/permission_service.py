from typing import List, Optional
from app.models.permission import Permission
from extensions import db

class PermissionService:

    @staticmethod
    def get_permission_all(search_query: str = "", page: int = 1, per_page: int = 10):
        query = Permission.query.order_by(Permission.code.asc())
        
        if search_query:
            query = query.filter(Permission.code.contains(search_query) | Permission.name.contains(search_query))
        
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def count_permissions() -> int:
        return Permission.query.count()
    
    @staticmethod
    def get_permission_by_id(permission_id: int) -> Optional[Permission]:
        return Permission.query.get(permission_id)

    @staticmethod
    def create_permission(data: dict) -> Permission:
        perm = Permission()
        perm.code = data["code"]
        perm.name = data["name"]
        perm.module = data.get("module", "General")
        perm.description = data.get("description") or ""

        db.session.add(perm)
        db.session.commit()
        return perm
    
    @staticmethod
    def update_permission(permission: Permission, data: dict) -> Permission:
        permission.code = data["code"]
        permission.name = data["name"]
        permission.module = data.get("module", "General")
        permission.description = data.get("description") or ""
        
        db.session.add(permission)
        db.session.commit()
        return permission
    
    @staticmethod
    def delete_permission(permission: Permission) -> None:
        db.session.delete(permission)
        db.session.commit()