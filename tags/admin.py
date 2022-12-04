from django.contrib import admin
from . import models

@admin.register(models.TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ['content_type','object_id','tag_label']
    list_per_page = 10
    list_select_related = ['tag']
    
    @admin.display(ordering= 'tag')
    def tag_label(self,TaggedItem):
        return TaggedItem.tag.label

