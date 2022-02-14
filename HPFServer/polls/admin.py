from django.contrib import admin
from .models import PollGroup, PollQuestion, PollAnswer, PollVote, Ballot
from core.admin import BaseAdminAccess


class AdminPollAccess(BaseAdminAccess):
    # fields = ("creation_user", "title", "opening_datetime", "closing_datetime", "visibility", "members_only",)
    # readonly_fields = ("creation_user",)
    pass


class AdminPollQuestionAccess(BaseAdminAccess):
    list_display = ("id", "__str__", "type",)
    fields = ("question_text", "poll_group", "max_choices", "type", "opening_datetime", "closing_datetime", "members_only", "visibility",)
    readonly_fields = ("type", "poll_group",)

    def type(self, obj):
        if hasattr(obj, "selection"):
            return "sélection"
        elif hasattr(obj, "chapter"):
            return "chapitre"
        else:
            return "thème"


class AdminPollAnswerAccess(BaseAdminAccess):
    list_display = ("id", "__str__",)


class AdminPollVoteAccess(BaseAdminAccess):
    pass
    # list_display = ("vote_datetime", "poll_answer", "ip_address",)
    # fields = ("user", "ip_address", "poll_answer", "vote_datetime",)
    # readonly_fields = ("user", "ip_address", "poll_answer", "vote_datetime",)


class AdminPollBallotAccess(BaseAdminAccess):
    list_display = ("id", "__str__")
    fields = ("user", "ip_address", "poll_question", "vote_datetime",)
    readonly_fields = ("user", "ip_address", "poll_question", "vote_datetime",)


admin.site.register(PollGroup, AdminPollAccess)
admin.site.register(PollQuestion, AdminPollQuestionAccess)
admin.site.register(PollAnswer, AdminPollAnswerAccess)
admin.site.register(PollVote, AdminPollVoteAccess)
admin.site.register(Ballot, AdminPollBallotAccess)
