
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from app.decorator_method.role_perm_decorator import role_required
from app.services.user_service import UserService
from app.services.role_service import RoleService
from app.services.permission_service import PermissionService
from app.services.rule_service import RuleService
from app.services.fact_service import FactService


dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
@login_required
@role_required('Admin')
@dashboard_bp.route('/')
def index():
    user_count = UserService.count_all_users()
    user_inactive = UserService.count_inactive_users()
    user_is_active = UserService.count_active_users()
    role_count = RoleService.count_roles()
    permission_count = PermissionService.count_permissions()
    rule_count = RuleService.count_rules()
    fact_count = FactService.count_facts()

    return render_template('dashboard/dashboard.html',
                            user_count=user_count,
                            user_is_active=user_is_active,
                            user_inactive=user_inactive,
                            role_count=role_count,
                            permission_count=permission_count,
                            rule_count=rule_count,
                            fact_count=fact_count)