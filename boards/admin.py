from django.contrib import admin
from .models import CustomUser, WorkBoard, Task, WorkBoardUserRole

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(WorkBoard)
admin.site.register(Task)
admin.site.register(WorkBoardUserRole)


