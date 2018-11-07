from rest_framework import serializers
from .models import Image, FavouriteList


class ImageSerializer(serializers.ModelSerializer):

    favourite = serializers.SerializerMethodField('add_favourite')

    def add_favourite(self, obj):
        favList = self.context.get("fav_list")
        if favList and str(obj.id) in favList:
            return "yes"
        return "no"

    class Meta:
        model = Image
        fields = ('__all__')
