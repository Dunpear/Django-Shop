from rest_framework import serializers
from .models import SocialMedia, SiteRules, SiteSettings, RepetitiveQuestions, Advantages


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'


class SiteRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteRules
        fields = '__all__'


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'


class RepetitiveQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepetitiveQuestions
        fields = '__all__'



class AdvantagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advantages
        fields = '__all__'