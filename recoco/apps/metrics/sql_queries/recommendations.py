from django.db.models import When, Case, QuerySet, Count, Q, F, BooleanField


from recoco.apps.tasks.models import Task

from ..utils import hash_field, display_value


def get_queryset(site_id: int) -> QuerySet:
    return (
        Task.objects.exclude(project__exclude_stats=True)
        .filter(site__pk=site_id)
        .order_by("created_on")
        .annotate(hash=hash_field("id", salt="task"))
        .annotate(project_hash=hash_field("project__id", salt="project"))
        .annotate(status_name=display_value(Task.STATUS_CHOICES, "status"))
        .annotate(created_by_hash=hash_field("created_by", salt="user"))
        .annotate(
            with_resource=Case(
                When(resource__isnull=True, then=False),
                default=True,
                output_field=BooleanField(),
            ),
        )
        .annotate(
            comment_count=Count(
                "followups", filter=~Q(followups__comment=""), distinct=True
            ),
            member_comment_count=Count(
                "followups",
                filter=Q(followups__who__in=F("project__members"))
                & ~Q(followups__comment=""),
                distinct=True,
            ),
            advisor_comment_count=Count(
                "followups",
                filter=Q(followups__who__in=F("project__switchtenders"))
                & ~Q(followups__comment=""),
                distinct=True,
            ),
        )
        .values(
            "hash",
            "public",
            "project_hash",
            "created_by_hash",
            "created_on",
            "status_name",
            "comment_count",
            "member_comment_count",
            "advisor_comment_count",
            "visited",
            "with_resource",
            "topic__name",
        )
    )
