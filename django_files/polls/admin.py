from django.contrib import admin

# Register your models here.


from .models import Host, Node, History

admin.site.register(Host)
admin.site.register(Node)
admin.site.register(History)
