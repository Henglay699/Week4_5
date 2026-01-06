from .user_routes import user_bp
from .auth_routes import auth_bp
from .role_routes import role_bp
from .rule_routes import rule_bp
from .fact_routes import fact_bp
from .diagnosis_routes import diag_bp
from .permission_routes import permission_bp

__all__=[
    "user_bp",
    "auth_bp",
    "permission_bp",
    "role_bp",
    "rule_bp",
    "fact_bp",
    "diag_bp",
]