from account.decorators import super_admin_required
from judge.tasks import judge_task
from problem.models import Problem
# from judge.dispatcher import JudgeDispatcher
from utils.api import APIView
from ..models import Submission


class SubmissionRejudgeAPI(APIView):
    @super_admin_required
    def get(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Parameter error, id is required")
        try:
            submission = Submission.objects.select_related("problem").get(id=id, contest_id__isnull=True)
        except Submission.DoesNotExist:
            return self.error("Submission does not exists")
        submission.statistic_info = {}
        submission.save()

        judge_task.delay(submission.id, submission.problem.id)
        return self.success()


class ProblemRejudgeAPI(APIView):
    @super_admin_required
    def get(self, request):
        problem_id = request.GET.get("problem_id")
        if not problem_id:
            return self.error("Parameter error, problem id is required")
        try:
            problem = Problem.objects.get(id=problem_id, contest_id__isnull=True)
        except Problem.DoesNotExist:
            return self.error("Problem does not exists")
        try:
            submissions = Submission.objects.filter(problem_id=problem_id, contest_id__isnull=True)
        except Submission.DoesNotExist:
            return self.error("Submission does not exists")
        for submission in submissions:
            submission.statistic_info = {}
            submission.save()
            judge_task.delay(submission.id, submission.problem.id)
        return self.success()


class ContestProblemRejudgeAPI(APIView):
    @super_admin_required
    def get(self, request):
        # -- todo -- ?????? I don't know why two field is swapped?
        problem_id = request.GET.get("contest_id")
        contest_id = request.GET.get("problem_id")
        if (not problem_id) or (not contest_id):
            return self.error("Parameter error, id is required")
        try:
            problem = Problem.objects.select_related("contest").get(_id=problem_id, contest_id=contest_id)
        except Problem.DoesNotExist:
            return self.error("Problem does not exists Contest: %s, Problem: %s" % (contest_id, problem_id))
        try:
            submissions = Submission.objects.filter(problem_id=problem.id, contest_id=problem.contest_id)
        except Submission.DoesNotExist:
            return self.error("Submission does not exists")
        for submission in submissions:
            submission.statistic_info = {}
            submission.save()
            judge_task.delay(submission.id, submission.problem.id)
        return self.success()
