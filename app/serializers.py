from rest_framework import serializers

from app.models import Product, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'created', 'price', 'lessons_count']

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()
