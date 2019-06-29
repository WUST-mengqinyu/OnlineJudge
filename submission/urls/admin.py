from django.conf.urls import url

from ..views.admin import SubmissionRejudgeAPI, ProblemRejudgeAPI, ContestProblemRejudgeAPI

urlpatterns = [
    url(r"^submission/rejudge?$", SubmissionRejudgeAPI.as_view(), name="submission_rejudge_api"),
    url(r"^submission/problem_rejudge?$", ProblemRejudgeAPI.as_view(), name="submission_rejudge_api"),
    url(r"^submission/contest_problem_rejudge?$", ContestProblemRejudgeAPI.as_view(), name="submission_rejudge_api"),
]
