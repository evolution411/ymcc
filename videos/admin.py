from django.contrib import admin
from .models import Video, VideoComment

class VideoAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
	list_display = ('commentPoster', 'commentText', 'video', 'commentDate', 'active')
	list_filter = ('active', 'commentDate')
	search_field = ('commentPoster', 'commentText')
	actions = ['approve_comments']

	def approve_comment(self, request, queryset):
		queryset.update(active=True)


admin.site.register(Video, VideoAdmin)
admin.site.register(VideoComment, CommentAdmin)
# Register your models here.
