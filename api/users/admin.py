from django.contrib import admin

from api.users.models import Profile, Follow

class ProfileAdmin(admin.ModelAdmin):

	def first_name(self, the_profile):
		if the_profile.user:
			return '{}'.format(
				the_profile.user.first_name
			)
		return None

	def last_name(self, the_profile):
		if the_profile.user:
			return '{}'.format(the_profile.user.last_name)
		return None

	def email(self, the_profile):
		if the_profile.user:
			return '{}'.format(the_profile.user.email)
		return None

	list_display = (
		'id',
		'first_name',
		'last_name',
		'email'
	)

class FollowAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'user',
		'target',
		'created_at'
	)

admin.site.register(Follow, FollowAdmin)
admin.site.register(Profile, ProfileAdmin)