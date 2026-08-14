from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import JsonResponse  # 👈 ADD THIS

from .serializers import (
    ClientRegistrationSerializer,
    ClientLoginSerializer,
    ClientSerializer,
    CaseSerializer,
    CaseDetailSerializer,
    DocumentSerializer,
    InternalNoteSerializer,
)
from apps.cases.models import Case, Document, InternalNote
from .telegram import send_telegram_alert


# ===== AUTHENTICATION =====

@api_view(['POST'])
def register(request):
    """Client registration endpoint"""
    serializer = ClientRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': ClientSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """Client login endpoint"""
    serializer = ClientLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': ClientSerializer(user).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    """Get current user profile"""
    serializer = ClientSerializer(request.user)
    return Response(serializer.data)


# ===== CASES =====

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_case(request):
    """Create a new case"""
    serializer = CaseSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        with transaction.atomic():
            case = serializer.save()
            # Trigger Telegram alert
            send_telegram_alert(case)
            return Response(CaseDetailSerializer(case).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_cases(request):
    """Get all cases for the authenticated client"""
    cases = request.user.cases.all()
    serializer = CaseDetailSerializer(cases, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def case_detail(request, case_id):
    """Get a single case with all details"""
    case = get_object_or_404(Case, id=case_id, client=request.user)
    serializer = CaseDetailSerializer(case)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_documents(request, case_id):
    """Upload documents for a case"""
    case = get_object_or_404(Case, id=case_id, client=request.user)
    
    if 'documents' not in request.FILES:
        return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    files = request.FILES.getlist('documents')
    if len(files) == 0:
        return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check file size limit (50MB)
    max_size = 50 * 1024 * 1024
    for f in files:
        if f.size > max_size:
            return Response(
                {'error': f'File {f.name} exceeds 50MB limit'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    created_docs = []
    for file in files:
        doc = Document.objects.create(
            case=case,
            document_type='OTHER',
            file_name=file.name,
            file_url=f'/media/{file.name}',  # Placeholder for local dev
            file_size=file.size,
            uploaded_by=request.user
        )
        created_docs.append(doc)
    
    serializer = DocumentSerializer(created_docs, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_internal_note(request, case_id):
    """Add an internal note to a case (team only)"""
    case = get_object_or_404(Case, id=case_id, client=request.user)
    serializer = InternalNoteSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        note = serializer.save(case=case)
        return Response(InternalNoteSerializer(note).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===== HEALTH CHECK =====

def health_check(request):
    """Simple health check endpoint using JsonResponse (no DRF dependency)"""
    return JsonResponse({'status': 'ok', 'message': 'Veritas Asset Recovery API is running'})