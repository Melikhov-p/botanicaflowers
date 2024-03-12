from django.contrib import admin
from chats.models import Chat, Message


class ChatAdmin(admin.ModelAdmin):
    list_display = ('client', 'start_time', 'closed')
    list_editable = ('closed', )


class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'text', 'sended_at')
    list_filter = ('chat', 'sender')
    search_fields = ('chat', 'sender')


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
