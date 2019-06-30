from account.decorators import super_admin_required
from judge.tasks import judge_task
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
            # 增加contest内rejudge
            submission = Submission.objects.select_related("problem").get(id=id)
            # submission = Submission.objects.select_related("problem").get(id=id, contest_id__isnull=True)
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
            return self.error("Parameter error, id is required")
        try:
            submissions = Submission.objects.filter(problem_id=problem_id, contest_id__isnull=True)
        except Submission.DoesNotExist:
            return self.error("Problem does not exists")
        for submission in submissions.objects.all():
            submission.statistic_info = {}
            submission.save()
            judge_task.delay(submission.id, submission.problem.id)
        return self.success()


class ContestProblemRejudgeAPI(APIView):
    @super_admin_required
    def get(self, request):
        problem_id = request.GET.get("problem_id")
        contest_id = request.GET.get("contest_id")
        if (not problem_id) or (not contest_id):
            return self.error("Parameter error, id is required")
        try:
            submissions = Submission.objects.filter(problem_id=problem_id, contest_id=contest_id)
        except Submission.DoesNotExist:
            return self.error("Problem does not exists")
        for submission in submissions.objects.all():
            submission.statistic_info = {}
            submission.save()
            judge_task.delay(submission.id, submission.problem.id)
        return self.success()
