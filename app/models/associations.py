from extensions import db

user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
)

role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True),
)

rule_facts = db.Table(
    "rule_facts",
    db.Column("rule_id", db.Integer, db.ForeignKey("rules.id"), primary_key=True),
    db.Column("fact_id", db.Integer, db.ForeignKey("facts.id"), primary_key=True),
) 

# user_rules = db.Table(
#     "user_rules",
#     db.Column("user_id", db.Integer, db.Foreign("users.id"), primary_key=True),
#     db.Column("rule_id", db.Integer, db.Foreign("rules.id"), primary_key=True)
#     )

# user_facts = db.Table(
#     "user_facts",
#     db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
#     db.Column("facts_id", db.Integer, db.ForeignKey("facts.id"), primary_key=True)
# )

