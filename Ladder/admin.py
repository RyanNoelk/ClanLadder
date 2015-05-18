from django.contrib import admin
from MatchHistory.models import Player_History
from Ladder.models import Player


class PlayerHistoryInline(admin.TabularInline):
    model = Player_History
    extra = 0
    
class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['Name']}),
        (None,               {'fields': ['Country']}),
        (None,               {'fields': ['Race']}),
    ]
    inlines = [PlayerHistoryInline]
    list_display = ('Name', 'Points')
    
admin.site.register(Player, PlayerAdmin)
