from django.contrib import admin

from api.feedback.models import FeedbackMessage

class FeedbackMessageAdmin(admin.ModelAdmin):
	list_display = (
		'creator',
		'created_at',
		'was_read'
	)

admin.site.register(FeedbackMessage, FeedbackMessageAdmin)