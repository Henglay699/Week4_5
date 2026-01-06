from .user_forms import UserCreateForm, UserEditForm, UserConfirmDeleteForm
from .role_forms import RoleCreateForm, RoleEditForm, RoleConfirmDeleteForm 
from .rule_forms import RuleCreateForm, RuleEditForm, RuleDeleteConfirm
from .fact_forms import FactCreateForm, FactEditForm, FactDeleteConfirm
from .diagnosis_forms import DiagnosisForm
from .permission_forms import (
    PermissionCreateForm, 
    PermissionEditForm,
    PermissionConfirmDeleteForm)

__all__ = [
    "UserCreateForm",
    "UserEditForm",
    "UserConfirmDeleteForm",
    "RoleCreateForm",
    "RoleEditForm",
    "RoleConfirmDeleteForm",
    "PermissionCreateForm",
    "PermissionEditForm",
    "PermissionConfirmDeleteForm",
    "RuleCreateForm",
    "RuleEditForm",
    "RuleDeleteConfirm",
    "FactCreateForm",
    "FactEditForm",
    "FactDeleteConfirm",
    "DiagnosisForm",
]