# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    # Add any other custom fields

from django.db import models
from django.contrib.auth import get_user_model

# Custom User model (inherited from AbstractUser)
User = get_user_model()

class WorkBoard(models.Model):
    """
    Model representing a Work Board. 
    A Work Board contains tasks categorized into 'ToDo', 'In Progress', and 'Completed'.
    """
    title = models.CharField(max_length=255, help_text="Title of the Work Board", unique=True)
    description = models.TextField(blank=True, null=True, help_text="Optional description of the Work Board")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_boards")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    """
    Model representing a task in a Work Board. 
    A task can be assigned to users and moved between statuses: ToDo, In Progress, Completed.
    """
    TODO = 'ToDo'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    
    STATUS_CHOICES = [
        (TODO, 'ToDo'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]

    title = models.CharField(max_length=255, help_text="Title of the Task")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the Task")
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=TODO)
    work_board = models.ForeignKey(WorkBoard, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# User role model for task board permissions
class WorkBoardUserRole(models.Model):
    """
    Model to define user roles for each Work Board.
    """
    OWNER = 'Owner'
    COLLABORATOR = 'Collaborator'
    VIEWER = 'Viewer'

    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (COLLABORATOR, 'Collaborator'),
        (VIEWER, 'Viewer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="board_roles")
    work_board = models.ForeignKey(WorkBoard, on_delete=models.CASCADE, related_name="user_roles")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=VIEWER)

    class Meta:
        unique_together = ('user', 'work_board')

    def __str__(self):
        return f'{self.user.username} - {self.role} on {self.work_board.title}'
