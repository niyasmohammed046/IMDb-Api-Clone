from rest_framework import serializers
from movie_list.models import WatchList ,StreamingPlatform ,Review



class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ('watchlist',)

class WatchListSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = WatchList
        fields = '__all__'

class StreamingPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"