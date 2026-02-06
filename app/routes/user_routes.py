from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    abort,
)
from app.forms.user_forms import UserCreateForm, UserEditForm, UserConfirmDeleteForm
from flask_login import login_required
from app.services.user_service import UserService
from app.decorator_method import role_required, permission_required

user_bp = Blueprint("users", __name__, url_prefix="/users")

@user_bp.route("/")
@login_required
@role_required("Admin")
def index():
    search_query = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    pagination = UserService.get_all(search_query=search_query, page=page)
    return render_template("users/index.html", 
                           users=pagination.items, 
                           pagination=pagination,
                           search_query=search_query)


@user_bp.route("/<int:user_id>")
@login_required
@permission_required("user.view")
def detail(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)
    return render_template("users/detail.html", user=user)

@user_bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("user.create")
def create():
    form = UserCreateForm()
    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data, 
            "is_active": form.is_active.data,
        }
        password = str(form.password.data)
        role_id = form.role_id.data or None
        
        user = UserService.create(data, password, role_id)
        flash(f"User '{user.username}' was created successfully.", "success")
        return redirect(url_for("users.index"))
    
    return render_template("users/create.html", form=form)


@user_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@permission_required("user.edit")
def edit(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)

    form = UserEditForm(original_user=user, obj=user)

    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data,
        }
        password = form.password.data or None
        role_id = form.role_id.data or None

        UserService.update(user, data, password, role_id)
        flash(f"User '{user.username}' was updated successfully.", "success")
        return redirect(url_for("users.detail", user_id=user.id))

    return render_template("users/edit.html", form=form, user=user)

@user_bp.route("/<int:user_id>/delete")
@login_required
@permission_required("user.delete")
def delete_confirm(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)
    form = UserConfirmDeleteForm()
    return render_template("users/delete_confirm.html", user=user, form=form)

@user_bp.route("/<int:user_id>/delete", methods=["POST"])
@login_required
@permission_required("user.delete")
def delete(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)

    UserService.delete(user)
    flash("User was deleted successfully.", "success")
    return redirect(url_for("users.index"))
