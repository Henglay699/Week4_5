from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from app.models import Fact
from app.forms.diagnosis_forms import DiagnosisForm
from app.services.diagnosis_service import DiagnosisService

diag_bp = Blueprint("diagnosis", __name__, url_prefix="/diagnosis")

@login_required
@diag_bp.route("/", methods=["GET", "POST"])
def diagnose():
    form = DiagnosisForm()
    results = None
    
    if form.validate_on_submit():
        # form.fact_ids.data will be a list of integers [1, 2, 5]
        selected_ids = form.fact_ids.data
        if selected_ids:
            results = DiagnosisService.perform_diagnosis(selected_ids)
            flash("Issues is found", "success")
    
    return render_template("diagnosis/index.html", form=form, results=results)