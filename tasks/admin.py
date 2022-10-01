from django.contrib import admin
from .models import Task
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    #campo de solo lectura
  readonly_fields = ('created', )


admin.site.register(Task, TaskAdmin)