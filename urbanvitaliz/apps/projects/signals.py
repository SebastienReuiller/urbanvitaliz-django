import datetime

import django.dispatch
from actstream import action
from actstream.models import action_object_stream
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from notifications import models as notifications_models
from notifications.signals import notify
from urbanvitaliz.apps.reminders import api as reminders_api
from urbanvitaliz.apps.reminders import models as reminders_models
from urbanvitaliz.apps.survey import signals as survey_signals

from . import models
from .utils import (create_reminder, get_collaborators_for_project,
                    get_notification_recipients_for_project,
                    get_project_moderators, get_regional_actors_for_project,
                    get_switchtenders_for_project)

#####
# Projects
#####
project_submitted = django.dispatch.Signal()
project_validated = django.dispatch.Signal()
project_switchtender_joined = django.dispatch.Signal()


@receiver(project_submitted)
def log_project_submitted(sender, submitter, project, **kwargs):
    action.send(project, verb="a été déposé")


@receiver(project_submitted)
def notify_moderators_project_submitted(sender, submitter, project, **kwargs):
    recipients = get_project_moderators()

    # Notify project moderators
    notify.send(
        sender=submitter,
        recipient=recipients,
        verb="a soumis pour modération le projet",
        action_object=project,
        target=project,
        private=True,
    )


@receiver(project_validated)
def log_project_validated(sender, moderator, project, **kwargs):
    action.send(project, verb="a été validé")

    if project.status == "DRAFT" or project.muted:
        return

    # Notify regional actors of a new project
    try:
        owner = auth_models.User.objects.get(email=project.email)
    except auth_models.User.DoesNotExist:
        return

    notify.send(
        sender=owner,
        recipient=get_regional_actors_for_project(project),
        verb="a déposé le projet",
        action_object=project,
        target=project,
        private=True,
    )


@receiver(project_switchtender_joined)
def log_project_switchtender_joined(sender, project, **kwargs):
    recipients = (
        get_regional_actors_for_project(project, allow_national=True)
        | get_collaborators_for_project(project)
    ).distinct()

    for recipient in recipients:
        action.send(
            sender,
            verb="est devenu·e aiguilleur·se sur le projet",
            action_object=project,
            target=project,
        )


@receiver(project_switchtender_joined)
def notify_project_switchtender_joined(sender, project, **kwargs):
    if project.status == "DRAFT" or project.muted:
        return

    recipients = (
        get_regional_actors_for_project(project, allow_national=True)
        | get_collaborators_for_project(project)
    ).distinct()

    # Notify regional actors
    notify.send(
        sender=sender,
        recipient=recipients,
        verb="est devenu·e aiguilleur·se sur le projet",
        action_object=project,
        target=project,
        private=True,
    )


#####
# Reminders
#####
reminder_created = django.dispatch.Signal()


@receiver(reminder_created)
def log_reminder_created(sender, task, project, user, **kwargs):
    if not user.is_staff:
        action.send(
            user,
            verb="a créé un rappel sur l'action",
            action_object=task,
            target=project,
        )


######
# Actions
#####
action_created = django.dispatch.Signal()
action_visited = django.dispatch.Signal()
action_not_interested = django.dispatch.Signal()
action_blocked = django.dispatch.Signal()
action_inprogress = django.dispatch.Signal()
action_already_done = django.dispatch.Signal()
action_done = django.dispatch.Signal()
action_undone = django.dispatch.Signal()
action_commented = django.dispatch.Signal()

# TODO refactor arguements as project is know to task -> f(sender, task , user, **kwargs)


@receiver(action_created)
def log_action_created(sender, task, project, user, **kwargs):
    if task.public is False:
        return

    action.send(user, verb="a recommandé l'action", action_object=task, target=project)


@receiver(action_created)
def notify_action_created(sender, task, project, user, **kwargs):
    if task.public is False:
        return

    if project.status == "DRAFT" or project.muted:
        return

    recipients = get_notification_recipients_for_project(project).exclude(id=user.id)

    notify.send(
        sender=user,
        recipient=recipients,
        verb="a recommandé l'action",
        action_object=task,
        target=project,
        private=True,
    )

    # assign reminder in six weeks
    create_reminder(6 * 7, task, project.email, origin=reminders_models.Mail.STAFF)


@receiver(action_visited)
def log_action_visited(sender, task, project, user, **kwargs):
    if not user.is_staff:
        action.send(user, verb="a visité l'action", action_object=task, target=project)


@receiver(action_not_interested)
def log_action_not_interested(sender, task, project, user, **kwargs):
    if not user.is_staff:
        action.send(
            user,
            verb="n'est pas intéressé·e l'action",
            action_object=task,
            target=project,
        )


@receiver(action_blocked)
def log_action_blocked(sender, task, project, user, **kwargs):
    if not user.is_staff:
        action.send(
            user,
            verb="est bloqué sur l'action",
            action_object=task,
            target=project,
        )


@receiver(action_already_done)
def log_action_already_done(sender, task, project, user, **kwargs):
    if not user.is_staff:
        action.send(
            user, verb="a déjà fait l'action", action_object=task, target=project
        )


@receiver(action_done)
def log_action_done(sender, task, project, user, **kwargs):
    if not user.is_staff:
        action.send(user, verb="a terminé l'action", action_object=task, target=project)


@receiver(action_inprogress)
def log_action_inprogress(sender, task, project, user, **kwargs):
    if not user.is_staff:
        action.send(
            user,
            verb="travaille sur l'action",
            action_object=task,
            target=project,
        )


@receiver(action_undone)
def log_action_undone(sender, task, project, user, **kwargs):
    if not user.is_staff:
        action.send(
            user, verb="a redémarré l'action", action_object=task, target=project
        )


@receiver(action_commented)
def log_action_commented(sender, task, project, user, **kwargs):
    if project.status == "DRAFT" or project.muted:
        return

    action.send(user, verb="a commenté l'action", action_object=task, target=project)


@receiver(action_commented)
def notify_action_commented(sender, task, project, user, **kwargs):
    if project.status == "DRAFT" or project.muted:
        return

    recipients = get_notification_recipients_for_project(project).exclude(id=user.id)

    notify.send(
        sender=user,
        recipient=recipients,
        verb="a commenté l'action",
        action_object=sender,
        target=project,
        private=True,
    )


# In case of deletion
@receiver(pre_delete, sender=models.Note, dispatch_uid="note_hard_delete_logs")
@receiver(pre_save, sender=models.Note, dispatch_uid="note_soft_delete_logs")
def delete_activity_on_note_delete(sender, instance, **kwargs):
    if instance.deleted is False:
        return

    project_ct = ContentType.objects.get_for_model(instance)
    notifications_models.Notification.objects.filter(
        target_content_type=project_ct.pk, target_object_id=instance.pk
    ).delete()

    action_object_stream(instance).delete()


@receiver(
    pre_delete, sender=models.Project, dispatch_uid="project_delete_notifications"
)
def delete_notifications_on_project_delete(sender, instance, **kwargs):
    project_ct = ContentType.objects.get_for_model(instance)
    notifications_models.Notification.objects.filter(
        target_content_type=project_ct.pk, target_object_id=instance.pk
    ).delete()


def delete_task_history(task):
    """Remove all logging history and notification is a task is deleted"""
    task_ct = ContentType.objects.get_for_model(task)
    notifications_models.Notification.objects.filter(
        action_object_content_type_id=task_ct.pk, action_object_object_id=task.pk
    ).delete()

    action_object_stream(task).delete()

    reminders_api.remove_reminder_email(task)


@receiver(pre_save, sender=models.Task, dispatch_uid="task_soft_delete_notifications")
def delete_notifications_on_soft_task_delete(sender, instance, **kwargs):
    if instance.deleted is False:
        return
    delete_task_history(instance)


@receiver(pre_delete, sender=models.Task, dispatch_uid="task_hard_delete_notifications")
def delete_notifications_on_hard_task_delete(sender, instance, **kwargs):
    delete_task_history(instance)


######
# Notes
#####
note_created = django.dispatch.Signal()


@receiver(note_created)
def notify_note_created(sender, note, project, user, **kwargs):
    if note.public is False:
        recipients = get_switchtenders_for_project(project).exclude(id=user.id)
        action.send(
            user, verb="a rédigé une note interne", action_object=note, target=project
        )
    else:
        recipients = get_notification_recipients_for_project(project).exclude(
            id=user.id
        )

    if project.status == "DRAFT" or project.muted:
        return

    notify.send(
        sender=user,
        recipient=recipients,
        verb="a créé une note de suivi",
        action_object=note,
        target=project,
        private=True,
    )


################################################################
# Project Survey events
################################################################
@receiver(
    survey_signals.survey_session_updated,
    dispatch_uid="survey_answer_created_or_updated",
)
def log_survey_session_updated(sender, session, request, **kwargs):
    project = session.project
    user = request.user

    # If we already sent this notification less a day ago, skip it
    one_day_ago = timezone.now() - datetime.timedelta(days=1)
    if session.action_object_actions.filter(
        verb="a mis à jour le questionnaire", timestamp__gte=one_day_ago
    ).count():
        return

    action.send(
        user,
        verb="a mis à jour le questionnaire",
        action_object=session,
        target=session.project,
    )

    recipients = get_switchtenders_for_project(project).exclude(id=user.id)
    notify.send(
        sender=user,
        recipient=recipients,
        verb="a mis à jour le questionnaire",
        action_object=session,
        target=project,
        private=True,
    )


# eof
