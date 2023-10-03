# encoding: utf-8

"""
Urls for projects application

author  : raphael.marvie@beta.gouv.fr,guillaume.libersat@beta.gouv.fr
created : 2021-05-26 15:54:25 CEST
"""


from django.urls import path

from . import views
from .views import (
    administration,
    detail,
    documents,
    export,
    feeds,
    notes,
    sharing,
)

urlpatterns = [
    path(r"projects/", views.project_list, name="projects-project-list"),
    # projects for switchtenders
    path(
        r"projects/advisor/",
        views.project_list_for_advisor,
        name="projects-project-list-advisor",
    ),
    path(
        r"projects/staff/",
        views.project_list_for_staff,
        name="projects-project-list-staff",
    ),
    path(r"projects/map", views.project_maplist, name="projects-project-list-map"),
    path(
        r"projects/csv",
        export.project_list_export_csv,
        name="projects-project-list-export-csv",
    ),
    path("projects/feed/", feeds.LatestProjectsFeed(), name="projects-feed"),
    path(
        r"project/<int:project_id>/",
        detail.project_detail,
        name="projects-project-detail",
    ),
    path(
        r"project/<int:project_id>/tags",
        detail.project_update_tags,
        name="projects-project-tags",
    ),
    path(
        r"project/<int:project_id>/topics",
        detail.project_create_or_update_topics,
        name="projects-project-topics",
    ),
    path(
        r"project/<int:project_id>/presentation",
        detail.project_overview,
        name="projects-project-detail-overview",
    ),
    path(
        r"project/<int:project_id>/connaissance",
        detail.project_knowledge,
        name="projects-project-detail-knowledge",
    ),
    path(
        r"project/<int:project_id>/documents",
        documents.document_list,
        name="projects-project-detail-documents",
    ),
    path(
        r"project/<int:project_id>/suivi",
        detail.project_internal_followup,
        name="projects-project-detail-internal-followup",
    ),
    path(
        r"project/<int:project_id>/activite",
        detail.project_internal_followup_tracking,
        name="projects-project-detail-internal-followup-tracking",
    ),
    path(
        r"project/<int:project_id>/actions",
        detail.project_actions,
        name="projects-project-detail-actions",
    ),
    path(
        r"project/<int:project_id>/actions/inline",
        detail.project_actions_inline,
        name="projects-project-detail-actions-inline",
    ),
    path(
        r"project/<int:project_id>/conversations",
        detail.project_conversations,
        name="projects-project-detail-conversations",
    ),
    path(
        r"project/<int:project_id>/switchtender/join",
        views.project_switchtender_join,
        name="projects-project-switchtender-join",
    ),
    path(
        r"project/<int:project_id>/observer/join",
        views.project_observer_join,
        name="projects-project-observer-join",
    ),
    path(
        r"project/<int:project_id>/switchtender/leave",
        views.project_switchtender_leave,
        name="projects-project-switchtender-leave",
    ),
    path(
        r"project/partage/<str:project_ro_key>/",
        sharing.project_detail_from_sharing_link,
        name="projects-project-sharing-link",
    ),
    path(
        r"project/<int:project_id>/accept/",
        views.project_accept,
        name="projects-project-accept",
    ),
    path(
        r"project/<int:project_id>/delete/",
        views.project_delete,
        name="projects-project-delete",
    ),
    path(
        r"project/<int:project_id>/conversation/",
        notes.create_public_note,
        name="projects-conversation-create-message",
    ),
    path(
        r"project/<int:project_id>/documents/televerser",
        documents.document_upload,
        name="projects-documents-upload-document",
    ),
    path(
        r"project/<int:project_id>/documents/<int:document_id>/pin-unpin",
        documents.document_pin_unpin,
        name="projects-documents-pin-unpin",
    ),
    path(
        r"project/<int:project_id>/documents/<int:document_id>/delete",
        documents.document_delete,
        name="projects-documents-delete-document",
    ),
    path(
        r"project/<int:project_id>/note/",
        notes.create_private_note,
        name="projects-create-note",
    ),
    path(
        r"note/<int:note_id>/delete/",
        notes.delete_note,
        name="projects-delete-note",
    ),
    path(
        r"note/<int:note_id>/",
        notes.update_note,
        name="projects-update-note",
    ),
    path(
        r"project/<int:project_id>/administration/",
        administration.project_administration,
        name="projects-project-administration",
    ),
    path(
        r"project/<int:project_id>/administration/<int:user_id>/promote/",
        administration.promote_collaborator_as_referent,
        name="projects-project-promote-referent",
    ),
    path(
        r"project/<int:project_id>/administration/access/collectivity/invite",
        administration.access_collaborator_invite,
        name="projects-project-access-collectivity-invite",
    ),
    path(
        r"project/<int:project_id>/administration/access/collectivity/invite/<uuid:invite_id>/resend",
        administration.access_collaborator_resend_invite,
        name="projects-project-access-collectivity-resend-invite",
    ),
    path(
        r"project/<int:project_id>/administration/access/advisor/invite",
        administration.access_advisor_invite,
        name="projects-project-access-advisor-invite",
    ),
    path(
        r"project/<int:project_id>/administration/access/advisor/invite/<uuid:invite_id>/resend",
        administration.access_advisor_resend_invite,
        name="projects-project-access-advisor-resend-invite",
    ),
    path(
        r"project/<int:project_id>/administration/access/invite/<uuid:invite_id>/revoke",
        administration.access_revoke_invite,
        name="projects-project-access-revoke-invite",
    ),
    path(
        r"project/<int:project_id>/administration/access/collectivity/<str:email>/delete",
        administration.access_collaborator_delete,
        name="projects-project-access-collectivity-delete",
    ),
    path(
        r"project/<int:project_id>/administration/access/advisor/<str:email>/delete",
        administration.access_advisor_delete,
        name="projects-project-access-advisor-delete",
    ),
]

# eof
