from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('me/', views.me, name='me'),
    
    # Cases
    path('cases/', views.create_case, name='create_case'),
    path('cases/my/', views.my_cases, name='my_cases'),
    path('cases/<uuid:case_id>/', views.case_detail, name='case_detail'),
    path('cases/<uuid:case_id>/upload/', views.upload_documents, name='upload_documents'),
    path('cases/<uuid:case_id>/notes/', views.add_internal_note, name='add_internal_note'),
    
    # Health
    path('health/', views.health_check, name='health_check'),
]