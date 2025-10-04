from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'created_at', 'deadline')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'closed_at')
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description')
        }),
        ('Даты', {
            'fields': ('created_at', 'deadline', 'closed_at')
        }),
        ('Приоритет и статус', {
            'fields': ('priority', 'status')
        }),
    )