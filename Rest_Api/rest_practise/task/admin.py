from django.contrib import admin

# Register your models here.
from .models import TaskList, Task, Attachment

class TaskListAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_on', 'house', 'created_by', 'status')
    search_fields = ('name', 'description')
    list_filter = ('created_on', 'house', 'created_by', 'status')

admin.site.register(TaskList, TaskListAdmin)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_on', 'task_list', 'created_by', 'status')
    search_fields = ('name', 'description')
    list_filter = ('created_on', 'task_list', 'created_by', 'status')

admin.site.register(Task, TaskAdmin)

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_on', 'task')
    search_fields = ('task__name',)
    list_filter = ('created_on', 'task')

admin.site.register(Attachment, AttachmentAdmin)
