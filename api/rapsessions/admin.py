from django.contrib import admin

from api.rapsessions.models import RapSession, Like, Beat, Rapback

class RapSessionAdmin(admin.ModelAdmin):

	list_display = (
		'id',
		'title',
		'created_at'
	)

# class ClipAdmin(admin.ModelAdmin):
# 	list_display = (
# 		'id',
# 		'creator',
# 		'session',
# 		'clip_num',
# 	)

class LikeAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'user',
		'session',
		'created_at'
	)

class BeatAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title'
    )

class RapbackAdmin(admin.ModelAdmin):
    list_display = (
        'original',
        'response',
        'created_at'
    )

# class BattleVoteAdmin(admin.ModelAdmin):
# 	list_display = (
# 		'id',
# 		'battle',
# 		'is_for_creator'
# 	)

admin.site.register(RapSession, RapSessionAdmin)
# admin.site.register(Clip, ClipAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Beat, BeatAdmin)
admin.site.register(Rapback, RapbackAdmin)
# admin.site.register(BattleVote, BattleVoteAdmin)