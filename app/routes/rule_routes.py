from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required
from app.services import RuleService
from app.forms.rule_forms import RuleCreateForm, RuleEditForm, RuleDeleteConfirm
from app.decorator_method import role_required, permission_required

rule_bp = Blueprint("rules", __name__, url_prefix="/rules")

@rule_bp.route("/")
@login_required
@role_required("Admin", "Expert")
def index():
    rules = RuleService.get_rule_all()
    return render_template("rules/index.html", rules=rules)


@rule_bp.route("/<int:rule_id>/detail")
@login_required
@permission_required("rule.view")
def detail(rule_id: int):
    rule = RuleService.get_rule_by_id(rule_id)
    if rule is None:
        abort(404)
    return render_template("rules/detail.html", rule=rule)


@rule_bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("rule.create")
def create():
    form = RuleCreateForm()
    if form.validate_on_submit():
        data = {
            "rule_id": form.rule_id.data,
            "title": form.title.data,
            "description": form.description.data,
            "category": form.category.data,
            "solution": form.solution.data,
            "confidence": form.confidence.data,           
        }
        fact_ids = form.fact_ids.data or []
        
        rule = RuleService.create_rule(data, fact_ids)
        flash(f"Rule '{rule.rule_id}' was created succesfully.", "success")
        return redirect(url_for("rules.index"))
    return render_template("rules/create.html", form=form)


@rule_bp.route("/<int:rule_id>/edit", methods=["GET", "POST"])
@login_required
@permission_required("rule.edit")
def edit(rule_id: int):
    
    rule = RuleService.get_rule_by_id(rule_id)
    if rule is None: 
        abort(404)
        
    form = RuleEditForm(original_rule=rule, obj=rule)
    if form.validate_on_submit():
        data = {
            "rule_id": form.rule_id.data,
            "title": form.title.data,
            "description": form.description.data,
            "category": form.category.data,
            "solution": form.solution.data,
            "confidence": form.confidence.data,           
        }
        fact_ids = form.fact_ids.data or []
        
        rule = RuleService.update_rule(rule, data, fact_ids)
        flash(f"Rule '{rule.rule_id}' was updated succesfully.", "success")
        return redirect(url_for("rules.index"))
    return render_template("rules/edit.html", form=form, rule=rule)


@rule_bp.route("/<int:rule_id>/delete", methods=["GET"])
@login_required
@permission_required("rule.delete")
def delete_confirm(rule_id: int):
    rule = RuleService.get_rule_by_id(rule_id)
    if rule is None:
        abort(404)
        
    form = RuleDeleteConfirm()
    return render_template("rules/delete_confirm.html", rule=rule, form=form)


@rule_bp.route("/<int:rule_id>/delete", methods=["POST"])
@login_required
@permission_required("rule.delete")
def delete(rule_id: int):
    rule = RuleService.get_rule_by_id(rule_id)
    if rule is None:
        abort(404)
    RuleService.delete_confirm_rule(rule)
    flash("Rule was deleted successfully.", "success")
    return redirect(url_for("rules.index"))
