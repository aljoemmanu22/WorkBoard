# views.py
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

# Register View (unchanged)
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow registration without authentication

# Login View (updated)
class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to log in
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        is_admin = serializer.validated_data['is_admin']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'is_admin': is_admin
        })

# Logout View (unchanged)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import WorkBoard, Task, WorkBoardUserRole
from .serializers import WorkBoardSerializer, WorkBoardCreateSerializer, TaskSerializer, WorkBoardUserRoleSerializer

# List all work boards or create a new one
class WorkBoardListCreateView(ListCreateAPIView):
    queryset = WorkBoard.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WorkBoardCreateSerializer
        return WorkBoardSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# Retrieve, update, or delete a specific work board
class WorkBoardDetailView(RetrieveUpdateDestroyAPIView):
    queryset = WorkBoard.objects.all()
    serializer_class = WorkBoardSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        board = get_object_or_404(WorkBoard, pk=self.kwargs['pk'])
        # Additional permission logic can be added here for ownership, roles, etc.
        return board


# Create or list tasks for a specific board
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list_create(request, board_id):
    board = get_object_or_404(WorkBoard, pk=board_id)

    if request.method == 'GET':
        tasks = board.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(work_board=board)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update or delete a specific task
class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        return task

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



# Assign user roles to a board
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_user_role(request, board_id):
    board = get_object_or_404(WorkBoard, pk=board_id)
    serializer = WorkBoardUserRoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(work_board=board)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List users and their roles for a board
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def board_user_roles(request, board_id):
    board = get_object_or_404(WorkBoard, pk=board_id)
    roles = board.user_roles.all()
    serializer = WorkBoardUserRoleSerializer(roles, many=True)
    return Response(serializer.data)
