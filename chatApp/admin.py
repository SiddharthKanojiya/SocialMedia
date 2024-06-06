from django.contrib import admin
from chatApp.models import Mychats,Mygroup,Mygroupchats
# Register your models here.

@admin.register(Mychats)
class MychatAdmin(admin.ModelAdmin):
    list_display = ('id','me','frnd','chats')


admin.site.register(Mygroup)
admin.site.register(Mygroupchats)