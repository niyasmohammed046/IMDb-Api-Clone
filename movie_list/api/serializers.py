#serializers.ModelSerializer

from rest_framework import serializers
from movie_list.models import WatchList ,StreamingPlatform ,Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ('watchlist',)
        #fields = '__all__'


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True,read_only=True)

    class Meta:
        model = WatchList
        fields = '__all__'


class StreamingPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"

# class StreamingPlatformSerializer(serializers.HyperlinkedModelSerializer):
#     # watchlist = WatchListSerializer(many=True, read_only= True)   #this method will show all the details
#     # watchlist = serializers.StringRelatedField(many=True)  # this will show what we give in the string
#     watchlist = serializers.HyperlinkedRelatedField(
#         many=True,
#         read_only=True,
#         lookup_field='id',
#         view_name= "movie-detail"  # this is what we write in the urls name
#     ) 

#     class Meta:
#         model = StreamingPlatform
#         fields = '__all__'


#serializers.Serializer

# from rest_framework import serializers
# from movie_list.models import Movie


# def check_length_of_description(value):
#     if len(value) < 10:
#         raise serializers.ValidationError("description must be less than 10 words")
#     else:
#         return value

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     name = serializers.CharField()
#     description = serializers.CharField(validators=[check_length_of_description])
#     active = serializers.BooleanField()

#     def create(self,validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self,instance,validated_data):
#         instance.name = validated_data.get('name',instance.name)
#         instance.description = validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active',instance.active)
#         instance.save()
#         return instance
    

#     def validate_name(self,value):  #field level validation
#         if len(value) < 3:
#             raise serializers.ValidationError("Name is too short")
#         else:
#             return value
        
#     def validate(self,data):     #object level validation
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("description must be different from the name")
#         else:
#             return data