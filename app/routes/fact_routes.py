from flask import Blueprint, url_for, redirect, flash, render_template, abort
from flask_login import login_required
from app.decorator_method import role_required, permission_required
from app.forms.fact_forms import FactCreateForm, FactDeleteConfirm, FactEditForm
from app.services.fact_service import FactService

fact_bp = Blueprint("facts", __name__, url_prefix="/facts")

@fact_bp.route("/")
@login_required
@role_required("Admin", "Expert")
def index():
    facts = FactService.get_fact_all()
    return render_template("facts/index.html", facts=facts)


@fact_bp.route("/<int:fact_id>/detail")
@login_required
@permission_required("fact.view")
def detail(fact_id: int):
    fact = FactService.get_fact_by_id(fact_id)
    if fact is None:
        abort(404)
    return render_template("facts/detail.html", fact=fact)


@fact_bp.route("/create", methods=["GET", "POST"])
@login_required 
@permission_required("fact.create")
def create():
    form = FactCreateForm()
    if form.validate_on_submit():
        data = {
            "name": form.name.data
        }
        FactService.create_fact(data)
        flash("fact created successfully.", "success")
        return redirect(url_for("facts.index"))
        
    return render_template("facts/create.html", form=form)


@fact_bp.route("/<int:fact_id>/edit", methods=["GET", "POST"])
@login_required
@permission_required("fact.edit")
def edit(fact_id: int):
    fact = FactService.get_fact_by_id(fact_id)
    if fact is None:
        abort(404)
        
    form = FactEditForm(original_fact=fact, obj=fact)
    if form.validate_on_submit():
        data = {
            "name": form.name.data
        }
        FactService.update_fact(fact, data)
        flash("facts updated successfully.", "success")
        return redirect(url_for("facts.index"))
    return render_template("facts/edit.html", form=form, fact=fact)


@fact_bp.route("/<int:fact_id>/delete", methods=["GET"])
@login_required
@permission_required("fact.delete")
def delete_confirm(fact_id: int):
    fact = FactService.get_fact_by_id(fact_id)
    if fact is None:
        abort(404)
    
    form = FactDeleteConfirm()
    return render_template("facts/delete_confirm.html", form=form, fact=fact)


@fact_bp.route("/<int:fact_id>/delete", methods=["POST"])
@login_required
@permission_required("fact.delete")
def delete(fact_id: int):
    fact = FactService.get_fact_by_id(fact_id)
    if fact is None:
        abort(404)
        
    FactService.delete_confirm_fact(fact)
    flash("fact was deleted successfully.", "success")
    return redirect(url_for("facts.index")) 