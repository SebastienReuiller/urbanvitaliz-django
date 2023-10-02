# encoding: utf-8

"""
Forms for projects application

author  : raphael.marvie@beta.gouv.fr,guillaume.libersat@beta.gouv.fr
created : 2021-12-14 10:36:20 CEST
"""


from django import forms
from markdownx.fields import MarkdownxFormField

from . import models

##################################################
# Notes
##################################################


class NoteForm(forms.ModelForm):
    """Generic Note creation/edition"""

    class Meta:
        model = models.Note
        fields = ["content"]

    content = MarkdownxFormField()


class StaffNoteForm(NoteForm):
    class Meta:
        model = models.Note
        fields = ["content"]


class PrivateNoteForm(forms.ModelForm):
    """Private Note creation"""

    class Meta:
        model = models.Note
        fields = ["content"]


class PublicNoteForm(forms.ModelForm):
    """Public Note creation"""

    class Meta:
        model = models.Note
        fields = ["content"]


##################################################
# Project
##################################################
class ProjectForm(forms.ModelForm):
    """Form for updating the base information of a project"""

    postcode = forms.CharField(max_length=5, required=False, label="Code Postal")
    insee = forms.CharField(max_length=5, required=False, label="Code Insee")

    class Meta:
        model = models.Project
        fields = [
            "name",
            "postcode",
            "insee",
            "location",
            "description",
        ]


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = ["the_file", "the_link", "description"]


class ProjectTagsForm(forms.ModelForm):
    """Form for tags creation/update"""

    class Meta:
        model = models.Project
        fields = ["tags"]


class TopicForm(forms.Form):
    """Form for handling a topic"""

    name = forms.CharField(max_length=32, required=False, label="Thème")


class ProjectTopicsForm(forms.ModelForm):
    """Form for topics creation/update"""

    class Meta:
        model = models.Project
        fields = ["advisors_note"]


# eof
