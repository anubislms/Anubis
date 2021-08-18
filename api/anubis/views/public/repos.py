from datetime import datetime

from flask import Blueprint

from anubis.models import Assignment, AssignmentRepo
from anubis.utils.auth.http import require_user
from anubis.utils.auth.user import current_user
from anubis.utils.http.decorators import json_response
from anubis.utils.http.https import success_response, error_response, req_assert
from anubis.utils.lms.repos import get_repos
from anubis.utils.lms.courses import is_course_admin
from anubis.utils.github.repos import create_assignment_repo

repos_ = Blueprint("public-repos", __name__, url_prefix="/public/repos")


@repos_.get('')
@repos_.get("/")
@repos_.get("/list")
@require_user()
@json_response
def public_repos_list():
    """
    Get all unique repos for a user

    :return:
    """

    # Get all repos for the user
    repos = get_repos(current_user.id)

    # Pass them back
    return success_response({"repos": repos})


@repos_.post('/create/<string:assignment_id>')
@require_user()
@json_response
def public_repos_create(assignment_id: str):
    """
    Get all unique repos for a user

    :return:
    """

    assignment: Assignment = Assignment.query.filter(
        Assignment.id == assignment_id,
    ).first()

    # Verify assignment exists
    req_assert(assignment is not None, message='Assignment does not exist')

    # If it has not been released, make sure the current user is an admin
    if assignment.release_date < datetime.now():
        req_assert(is_course_admin(assignment.course_id, current_user.id), message='Assignment does not exist')

    repo = create_assignment_repo(assignment, current_user)

    req_assert(repo.repo_created, message='Repo could not be created')
    req_assert(repo.collaborator_configured, message='Student could not be added as a collaborator to repo')

    # Pass them back
    return success_response({"repo": repo.data})


