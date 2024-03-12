from django.contrib import admin
from client.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'last_login')
    search_fields = ('phone',)

    def last_login(self, obj):
        return obj.user.last_login


admin.site.register(Client, ClientAdmin)
