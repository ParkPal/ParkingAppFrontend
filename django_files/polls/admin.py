from django.contrib import admin

# Register your models here.


from .models import Question, Host, Node

admin.site.register(Question)
admin.site.register(Host)
admin.site.register(Node)
