from flask import Blueprint, request, Response
from app.models.task import Task
from ..db import db
from datetime import datetime
from sqlalchemy import desc
from .route_utilities import validate_model, create_model, get_models_with_filters, send_slack_bot_message

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@bp.get("")
def get_all_tasks():
    sort_parameter = request.args.get('sort')
    query = db.select(Task)

    if sort_parameter == "desc":
        query = query.order_by(desc(Task.title))
    else:
        query = query.order_by(Task.title)
    
    tasks = db.session.scalars(query)
    task_response = [task.to_dict() for task in tasks]
    return task_response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def patch_task_to_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    slack_message = f"Someone just completed the tast {task.title}"
    send_slack_bot_message(slack_message)

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def patch_task_to_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = False
    db.session.commit()
    return Response(status=204, mimetype="application/json")