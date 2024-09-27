from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, WorkBoardListCreateView, WorkBoardDetailView, task_list_create, TaskDetailView, assign_user_role, board_user_roles


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('boards/', WorkBoardListCreateView.as_view(), name='board-list-create'),
    path('boards/<int:pk>/', WorkBoardDetailView.as_view(), name='board-detail'),

    # Task routes
    path('boards/<int:board_id>/tasks/', task_list_create, name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    # WorkBoard role management
    path('boards/<int:board_id>/assign-role/', assign_user_role, name='assign-user-role'),
    path('boards/<int:board_id>/roles/', board_user_roles, name='board-user-roles'),
]
