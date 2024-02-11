from django.contrib import admin

from .models import *


class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ["course_code", "course_title", "question"]
    

admin.site.register(UserProfile)
admin.site.register(StudyGroup)
admin.site.register(Resources)
admin.site.register(QuizQuestion, QuizQuestionAdmin)
admin.site.register(Quiz)
