from django.db.models import (CASCADE, DateTimeField, ForeignKey, Model, CharField, TextChoices, TextField)
from django.contrib.auth.models import User

class Note(Model):
    class Visible(TextChoices):
        PUBLIC = 'public', 'Public'
        PRIVATE = 'private', 'Private'


    user = ForeignKey(User, on_delete=CASCADE, related_name='notes')
    title = CharField(max_length=255)
    visible = CharField(choices=Visible.choices, default=Visible.PRIVATE, max_length=255)
    content = TextField(blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

