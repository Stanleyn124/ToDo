from django.contrib import admin

# Register your models here.


from .models import Tag, List, Task, UpdateMessage, Priority, Status

admin.site.register(Tag)
admin.site.register(List)
admin.site.register(Task)
admin.site.register(UpdateMessage)
admin.site.register(Priority)
admin.site.register(Status)
