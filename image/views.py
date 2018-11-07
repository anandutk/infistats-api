from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .models import Image, FavouriteList
from .serializers import ImageSerializer
from datetime import datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import time


# Create your views here.



class AllImages(APIView):
    def get(self, request):
        return GetObjects(request)


class ALlImagesWithRange(APIView):
    def get(self, request, start_ind, end_ind):
        filter = {}
        return GetObjects(request, filter, int(start_ind), int(end_ind))


class ImagesCategoryWithRange(APIView):
    def get(self, request, category, start_ind, end_ind):
        filter = {'image_category': category}
        return GetObjects(request,filter, int(start_ind), int(end_ind))

class ImagesCategory(APIView):
    def get(self, request, category):
        filter = {'image_category': category}
        return GetObjects(request,filter)

class ImagesTagWithRange(APIView):
    def get(self, request, tag, start_ind, end_ind):
        filter = {'image_tags__contains': tag}
        return GetObjects(request,filter, int(start_ind), int(end_ind))

class ImagesTag(APIView):
    def get(self, request, tag):
        filter = {'image_tags__contains': tag}
        return GetObjects(request,filter)

"""
class CategoryLatest(APIView):
    def get(self, request):
        #filter = {'image_category': category}
        #return GetObjects(request,filter)
        #Score.objects.annotate(max_date=Max('student__score__date')).filter(date=F('max_date'))
        #return Response(Image.objects.values('image_category', 'image_file'))
        #return Response(Image.objects.annotate(max_date=Max('image_category__image_file__date')).filter(date=F('max_date')))
        #return Response(Image.objects.annotate(max_date=Max('date')).filter(date=F('max_date')))
        #return Response(Image.objects.values('image_category').annotate(max_date=Max('date')).filter(date=F('max_date')).values('image_category'))
        #return Response(Image.objects.values('image_category').annotate(max_date=Max('date')).filter(date=F('max_date')).values('image_category','image_file', 'date','max_date'))
        #Model.objects.values('category').annotate(max_pubdate=Max('pubdate')).order_by()
        #return Response(Image.objects.values('image_category').annotate(max_date=Max('id')).values('image_category', 'image_file', 'date', 'max_date'))
        return Response(
            (Image.objects.values('image_category').annotate(max_date=Max('date'))))
"""

class AllCategory(APIView):
    def get(self, request):
        return Response(set(Image.objects.values_list('image_category', flat=True)))

class AllTag(APIView):
    def get(self, request):
        img_tags = Image.objects.values_list('image_tags', flat=True)
        tags = []
        for t in img_tags:
            tags.extend(t.split(','))
        tags = filter(None,map(lambda x: x.strip(),tags))

        return Response(set(tags))

class ImagesCount(APIView):
    def get(self, request):

        count = Image.objects.all().count()

        #serializer = ImageSerializer(images, many=True)
        return Response(count)

class ImagesCountAfterTime(APIView):
    def get(self, request,timeStamp):
        t = time.localtime(float(timeStamp))
        count = Image.objects.order_by('-date').filter(date__gte = datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min)).count()
        #serializer = ImageSerializer(images, many=True)
        return Response(count)

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class UpdateFavourite(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        data = request.data
        #print data

        if data.has_key("device_id") and data.has_key("image_id") and  data.has_key("favourite"):
            try:
                favObj = FavouriteList.objects.get(device_id = data["device_id"])
                if favObj:
                    favList = set(favObj.favouriteList.split(','))
                    if data["image_id"] in favList and data["favourite"] == "no":
                        favList.remove(data["image_id"])
                        if '' in favList: favList.remove('')
                        favObj.favouriteList = ','.join(favList)
                        favObj.save()
                    elif not data["image_id"] in favList and data["favourite"] == "yes":
                        favList.add(data["image_id"])
                        if '' in favList: favList.remove('')
                        favObj.favouriteList = ','.join(favList)
                        favObj.save()
            except FavouriteList.DoesNotExist:
                if data["favourite"] == "yes":
                    favObj = FavouriteList(device_id=data["device_id"], favouriteList=data["image_id"])
                    favObj.save()

            return Response("success")
        else:
            raise ParseError("Didn't get expected data")


def GetObjects(request, filter = None, start_ind = 0, end_ind = 9):
    if request.GET.has_key('device_id'):
        device_id = request.GET["device_id"]
    else:
        device_id = None

    if start_ind > end_ind:
        raise ParseError("Requested range is not proper")
    # Debug
    #print "Start: " + str(start_ind) + " End: " + str(end_ind)
    #filter = {'{0}_{1}'.format('image', 'category'): 'cat1'}
    #filter = {'image_category': 'cat2'}

    resp_data = {}

    try:
        favObj = FavouriteList.objects.get(device_id=device_id)
        favList = favObj.favouriteList.split(',')
        if '' in favList:
            favList.remove('')
    except FavouriteList.DoesNotExist:
        favList = None
    if request.GET.has_key('favourite'):
        if favList:
            if not filter:
                filter = {}
            filter['pk__in'] = favList
        else:
            resp_data['MetaData'] = {'TotalCount': 0,
                                     'StartInd': -1,
                                     'EndInd': -1
                                     }
            return Response(resp_data)

    if filter:
        totalCnt = Image.objects.filter(**filter ).count()
        images = Image.objects.filter(**filter ).order_by('-id')[start_ind:(end_ind + 1)]
    else:
        totalCnt = Image.objects.all().count()
        images = Image.objects.all().order_by('-id')[start_ind:(end_ind + 1)]
    #ret_hdr = {'count': images.count()}

    #serializer = ImageSerializer(images, many=True,context={'device_id': device_id})
    serializer = ImageSerializer(images, many=True,context={'fav_list': favList})

    if start_ind >= totalCnt:
        raise ParseError("No data available")
    if end_ind >= totalCnt:
        end_ind = totalCnt -1
    resp_data['MetaData'] = {'TotalCount': totalCnt,
                              'StartInd':start_ind,
                              'EndInd':end_ind
                              }
    resp_data['Payload'] = serializer.data
    return Response(resp_data)