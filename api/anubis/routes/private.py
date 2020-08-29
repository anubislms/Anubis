import traceback
import logging
import json
from typing import List

from flask import request, Blueprint
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_

from anubis.models import Assignment, AssignmentQuestion, AssignedStudentQuestion
from anubis.models import Submission
from anubis.models import User
from anubis.models import db
from anubis.utils.auth import get_token
from anubis.utils.cache import cache
from anubis.utils.data import regrade_submission, is_debug
from anubis.utils.data import success_response, error_response
from anubis.utils.decorators import json_response, json_endpoint
from anubis.utils.elastic import log_endpoint
from anubis.utils.redis_queue import enqueue_webhook_rpc
from dateutil.parser import parse as date_parse, ParserError

private = Blueprint('private', __name__, url_prefix='/private')


def fix_dangling():
    # TODO rewite this
    raise


@cache.memoize(timeout=30)
def stats_for(student_id, assignment_id):
    # TODO rewrite this
    raise


@cache.cached(timeout=30)
def get_students():
    return [s.data for s in User.query.all()]


@private.route('/')
def private_index():
    return 'super duper secret'


if is_debug():
    @private.route('/token/<netid>')
    @json_response
    def private_token_netid(netid):
        user = User.query.filter_by(netid=netid).first()
        if user is None:
            return error_response('User does not exist')
        return success_response(get_token(user.netid))


@private.route('/assignment/sync', methods=['POST'])
@log_endpoint('cli', lambda: 'assignment-sync')
@json_endpoint(required_fields=[('assignment', dict), ('tests', list)])
def private_assignment_sync(assignment_data: dict, tests: List[str]):
    logging.debug("/private/assignment/sync meta: {}".format(json.dumps(assignment_data, indent=2)))
    logging.debug("/private/assignment/sync tests: {}".format(json.dumps(tests, indent=2)))
    # Find the assignment
    a = Assignment.query.filter(
        Assignment.unique_code == assignment_data['unique_code']
    ).first()

    # Attempt to find the class
    c = Class_.query.filter(
        or_(Class_.name == assignment_data["class"],
            Class_.class_code == assignment_data["class"])
    ).first()
    if c is None:
        return error_response('Unable to find class')

    # Check if it exists
    if a is None:
        a = Assignment(unique_code=assignment_data['unique_code'])

    # Update fields
    a.name = assignment_data['name']
    a.hidden = assignment_data['hidden']
    a.description = assignment_data['description']
    a.pipeline_image = assignment_data['pipeline_image']
    a.class_ = c
    try:
        a.release_date = date_parse(assignment_data['release_date'])
        a.due_date = date_parse(assignment_data['due_date'])
        a.grace_date = date_parse(assignment_data['grace_date'])
    except ParserError:
        logging.error(traceback.format_exc())
        return error_response('Unable to parse datetime')

    db.session.add(a)
    db.session.commit()

    for i in AssignmentTest.query.filter(
        and_(AssignmentTest.assignment_id == a.id,
             AssignmentTest.name.notin_(tests))
    ).all():
        db.session.delete(i)
    db.session.commit()

    for test_name in tests:
        at = AssignmentTest.query.filter(
            Assignment.id == a.id,
            AssignmentTest.name == test_name,
        ).join(Assignment).first()

        if at is None:
            at = AssignmentTest(assignment=a, name=test_name)
            db.session.add(at)
            db.session.commit()

    return success_response({
        'assignment': a.data,
    })

@private.route('/dangling')
@log_endpoint('cli', lambda: 'dangling')
@json_response
def private_dangling():
    """
    This route should hand back a json list of all submissions that are dangling.
    Dangling being that we have no netid to match to the github username that
    submitted the assignment.
    """

    dangling = Submission.query.filter(
        Submission.student_id == None,
    ).all()
    dangling = [a.data for a in dangling]

    return success_response({
        "dangling": dangling,
        "count": len(dangling)
    })


@private.route('/regrade/<assignment_name>')
@log_endpoint('cli', lambda: 'regrade')
@json_response
def private_regrade_assignment(assignment_name):
    """
    This route is used to restart / re-enqueue jobs.

    TODO verify fields that this endpoint is processing

    body = {
      netid
    }

    body = {
      netid
      commit
    }
    """
    assignment = Assignment.query.filter_by(
        name=assignment_name
    ).first()

    if assignment is None:
        return error_response('cant find assignment')

    submission = Submission.query.filter_by(
        assignment=assignment
    ).all()

    response = []

    for s in submission:
        res = regrade_submission(s)
        response.append({
            'submission': s.id,
            'commit': s.commit,
            'netid': s.netid,
            'success': res['success'],
        })

    return success_response({'submissions': response})


@private.route('/fix-dangling')
@log_endpoint('cli', lambda: 'fix-dangling')
@json_response
def private_fix_dangling():
    return fix_dangling()


@private.route('/stats/<assignment_name>')
@private.route('/stats/<assignment_name>/<netid>')
@log_endpoint('cli', lambda: 'stats')
@cache.memoize(timeout=60, unless=lambda: request.args.get('netids', None) is not None)
@json_response
def private_stats_assignment(assignment_name, netid=None):
    netids = request.args.get('netids', None)

    if netids is not None:
        netids = json.loads(netids)
    elif netid is not None:
        netids = [netid]
    else:
        netids = list(map(lambda x: x['netid'], get_students()))

    students = get_students()
    students = filter(
        lambda x: x['netid'] in netids,
        students
    )

    bests = {}

    assignment = Assignment.query.filter_by(name=assignment_name).first()
    if assignment is None:
        return error_response('assignment does not exist')

    for student in students:
        submissionid = stats_for(student['id'], assignment.id)
        netid = student['netid']
        if submissionid is None:
            # no submission
            bests[netid] = None
        else:
            submission = Submission.query.filter_by(
                id=submissionid
            ).first()
            build = len(submission.builds) > 0
            best_count = sum(map(lambda x: 1 if x.passed else 0, submission.reports))
            late = 'past due' if assignment.due_date < submission.timestamp else False
            late = 'past grace' if assignment.grace_date < submission.timestamp else late
            bests[netid] = {
                'submission': submission.data,
                'builds': build,
                'reports': [rep.data for rep in submission.reports],
                'total_tests_passed': best_count,
                'repo_url': submission.repo,
                'master': 'https://github.com/{}'.format(
                    submission.repo[submission.repo.index(':') + 1:-len('.git')],
                ),
                'commit_tree': 'https://github.com/{}/tree/{}'.format(
                    submission.repo[submission.repo.index(':') + 1:-len('.git')],
                    submission.commit
                ),
                'late': late
            }
    return success_response({'stats': bests})


from anubis.models import SubmissionTestResult, SubmissionBuild
from anubis.models import AssignmentTest, AssignmentRepo, InClass, Class_

if is_debug():
    @private.route('/seed')
    @json_response
    def private_seed():
        # Yeet
        SubmissionTestResult.query.delete()
        SubmissionBuild.query.delete()
        Submission.query.delete()
        AssignmentRepo.query.delete()
        AssignmentTest.query.delete()
        InClass.query.delete()
        Assignment.query.delete()
        Class_.query.delete()
        User.query.delete()
        db.session.commit()

        # Create
        u = User(netid='jmc1283', github_username='juanpunchman', name='John Cunniff', is_admin=True)
        c = Class_(name='Intro to OS', class_code='CS-UY 3224', section='A', professor='Gustavo')
        ic = InClass(owner=u, class_=c)
        a = Assignment(name='Assignment1: uniq', pipeline_image="registry.osiris.services/anubis/assignment/1",
                       hidden=False, release_date='2020-08-22', due_date='2020-08-22', class_=c, github_classroom_url='')
        at1 = AssignmentTest(name='Long file test', assignment=a)
        at2 = AssignmentTest(name='Short file test', assignment=a)
        r = AssignmentRepo(owner=u, assignment=a, repo_url='https://github.com/juan-punchman/xv6-public.git')
        s1 = Submission(commit='2bc7f8d636365402e2d6cc2556ce814c4fcd1489', state='Enqueued', owner=u, assignment=a, repo=r)
        s2 = Submission(commit='0001', state='Enqueued', owner=u, assignment=a, repo=r)

        # Commit
        db.session.add_all([u, c, ic, a, at1, at2, s1, s2, r])
        db.session.commit()

        # Init models
        s1.init_submission_models()
        s2.init_submission_models()

        enqueue_webhook_rpc(s1.id)

        return {
            'u': u.data,
            'a': a.data,
            's1': s1.data,
        }