from django.contrib import admin

from .models import Thought, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_thought_count']

    def get_thought_count(self, obj):
        return Thought.objects.filter(tags__in=[obj.id]).count()

    get_thought_count.short_description = 'Thought count'


@admin.register(Thought)
class ThoughtAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'get_text', 'is_editable', 'get_tag_count']
    list_display_links = ['get_text']
    ordering = ['id']

    def get_text(self, obj):
        return f'{obj.text[:50]}...' if len(obj.text) > 50 else obj.text

    def get_tag_count(self, obj):
        return Tag.objects.filter(thought__in=[obj.id]).count()

    get_tag_count.short_description = 'Tag count'
    get_text.short_description = 'Text'
