from shortener.utils import MsgOk, url_count_changer
from shortener.models import ShortenedUrls, Users
from shortener.urls.serializers import UserSerializer, UrlListSerializer, UrlCreateSerializer
from django.contrib.auth.models import User, Group
from django.http.response import Http404
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import renderer_classes

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ShortenedUrls.objects.order_by("-created_at")
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        #POST
        serializer = UrlCreateSerializer(data=request.data)
        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)
            return Response(UrlListSerializer(rtn).data, status=status.HTTP_201_CREATED)
        pass

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk).first()
        serializer = UrlListSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, requset, pk=None):
        pass

    @renderer_classes([JSONRenderer])
    def destroy(self, request, pk=None):
        #DELETE
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        return MsgOk()  

    def list(self, request):
        # GET ALL
        queryset = self.get_queryset().all()
        serializer = UrlListSerializer(queryset, many=True)
        return Response(serializer.data)