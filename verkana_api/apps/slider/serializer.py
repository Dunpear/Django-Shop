from rest_framework import serializers
from .models import Slider, SliderItem


class SliderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SliderItem
        fields = '__all__'


class SliderSerializer(serializers.ModelSerializer):
    slider_items = SliderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Slider
        fields = ['id', 'title', 'register_date', 'delay', 'auto_play', 'is_active', 'slider_items']
