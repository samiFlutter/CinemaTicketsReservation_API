import imp
from pickle import PUT
import stat
from webbrowser import get
from django.http import Http404
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import JsonResponse


from project.settings import REST_FRAMEWORK
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GuestSerializer, MovieSerializer, PostSerializer, ResevationSerializer
from django.http import Http404
from rest_framework import generics, mixins,viewsets
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated



# without REST and no model  query


def no_rest_no_model(request):
    guests = [{"id": 1, "name": "omer", "mobile": 132},
              {"id": 2, "name": "yassin", "mobile": 999}]

    return JsonResponse(guests, safe=False)

# without REST and from model  query


def no_rest_from_model(request):

    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response, safe=False)

# GET POST


@api_view(['GET', 'POST'])
def FBV_List(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST
    if request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

# PUT GET DELETE


@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):

    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    # PUT
    if request.method == 'PUT':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # delete
    if request.method == 'DELETE':

        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CBV class based view
# 4.1 list and  Create == GET and POST


class CBV_List(APIView):

    def get(self, request):
        guestes = Guest.objects.all()
        serializer = GuestSerializer(guestes, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.data,
            status=status.HTTP_400_BAD_REQUEST
        )

# 4.2 GET PUT DELETE class based view  --pk


class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
            print('try is good ')
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# mixins list
class mixins_list(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
    ):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)

  

class mixins_pk(mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):
        def get(self,request,pk):
            return self.retrieve(request)

        def put(self,request):
            return self.update(request)

        def delete(self,request):
            return self.destroy(request)
       


# generics 
# 6
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # ca pour demander le mot de passe et user name when you want to excute this 
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    # ca pour demander token when you want to excute this 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
# 6.1
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

# 7 viewsets 
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class viewssets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ['movie']
class viewssets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ResevationSerializer



# 8 find movie
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        movie = request.data['movie'],
        hall = request.data['hall']
    )
    serializer = MovieSerializer(movies,many=True)
    return Response(serializer.data)
# 9 create new reservation
@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        movie = request.data['movie'],
        hall = request.data['hall']
    )

    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie=movie
    reservation.save()
    return Response(status=status.HTTP_201_CREATED)
    


# working on permissions edite 
# 10 post author editor  
from .permissions import IsAuthorOrReadOnly
from .models import Post
class  Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
