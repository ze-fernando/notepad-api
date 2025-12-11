from rest_framework.serializers import CharField, ModelSerializer, Serializer

from .models import Note

class NoteSerializer(ModelSerializer):
    title = CharField(required=True)
    content = CharField(required=False, allow_blank=True)
    visible = CharField(required=False, allow_blank=True)

    class Meta:
        model = Note
        fields = [
            'id',
            'user',
            'title',
            'visible',
            'content',
            'created_at',
            'updated_at',
        ]

        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
