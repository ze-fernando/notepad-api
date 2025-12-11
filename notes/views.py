from http import HTTPStatus
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import NoteSerializer
from .models import Note


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all(request):
    notes = Note.objects.filter(visible=Note.Visible.PUBLIC)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_by_id(request, id):
    user = request.user
    note = Note.objects.filter(id=id).first()
    if note:

        if note.visible == Note.Visible.PUBLIC or note.user == user:
            serializer = NoteSerializer(note)
            return Response(serializer.data, status=HTTPStatus.OK)

        return Response({'message': 'You cant view this note, its private'}, status=HTTPStatus.UNAUTHORIZED)
    return Response({'message': 'Note not find'}, status=HTTPStatus.NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mine(request):
    user = request.user
    notes = Note.objects.filter(user=user)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    serializer = NoteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    title = serializer.validated_data['title']
    content = serializer.validated_data.get('content', '')
    visible = serializer.validated_data.get('visible', 'private')

    note = Note.objects.create(title=title, content=content, visible=visible, user=request.user)

    return Response(NoteSerializer(note).data, status=HTTPStatus.OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update(request, id):
    serializer = NoteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    title = serializer.validated_data['title']
    content = serializer.validated_data.get('content')
    visible = serializer.validated_data.get('visible')

    note = Note.objects.filter(id=id)
    if not note:
        return Response({'message': 'Note not found or you cannot update it'}, status=HTTPStatus.NOT_FOUND)

    note.update(title=title, content=content, visible=visible)

    return Response(NoteSerializer(note.first()).data, status=HTTPStatus.CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request, id):
    note = Note.objects.filter(id=id).first()
    if note.user != request.user:
        return Response({'message': 'Only onwer can delete this note'}, status=HTTPStatus.UNAUTHORIZED)

    note.delete()

    return Response({'message': 'Note deleted successfully'}, status=HTTPStatus.OK)

