from django.contrib import admin
from . import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['label']
    search_fields = ['label']
    
    
    
@admin.register(models.TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tag']
    list_display = ['tag']
    list_per_page = 10
    list_select_related = ['tag']
    search_fields = ['tag']
    
    #@admin.display(ordering= 'tag')
    #def tag_label(self,TaggedItem):
    #    return TaggedItem.tag.label

