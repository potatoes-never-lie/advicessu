from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from knox.models import AuthToken
from django.http import Http404
from .models import Post, Bookmark
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer, PostSerializer
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponseRedirect

# Create your views here.
@api_view(['GET'])
def HelloAPI(request):
    return Response("hello world!")


class RegistrationAPI(generics.GenericAPIView):
    """
        회원가입을 하는 API
        
        ---
        # 내용
            - username : 이름
            - email : 이메일
            - password : 비밀번호
    """
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
       # if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
       #     body = {"message": "short field"}
       #     return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user),
            }
        )


class LoginAPI(generics.GenericAPIView):
    """
        로그인을 하는 API

        ---
        # 내용
            - email : 이메일
            - password : 비밀번호
    """
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    """
        유저 정보 가져오는 API

        ---
        # 내용
            - username : 이름
            - email : 이메일
            - password : 비밀번호
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class PostListAPI(APIView):
    """
        게시글의 목록을 보여주는 API

        ---
        # 내용
            - title : 글 제목
            - text : 글 내용 
    """
    def post(self, request, format=None):                   #포스트 생성 
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            #serializer.save()
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        queryset=Post.objects.all()                         #포스트 조회
        serializer=PostSerializer(queryset, many=True)
        return Response(serializer.data)


class PostDetailAPI(APIView):
    """
        리스트에서 특정 id를 가지는 게시글을 보여주는 API

        ---
        # 내용
            - title : 글 제목
            - text : 글 내용 
    """
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        post=self.get_object(pk)
        serializer=PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post=self.get_object(pk)
        serializer=PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post=self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostFavoriteAPI(APIView):
    """
        사용자의 스크랩 리스트에서 특정 id를 가지는 게시글을 보여주는 API

        ---
        # 내용
            - title : 글 제목
            - text : 글 내용 
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:   #로그인된 상태이면 
            return HttpResponseForbidden()
        else:
            if 'post_id' in kwargs:
                post_id=kwargs['post_id']
                post=Post.objects.get(pk=post_id)
                user=request.user
                if user in post.favorite.all():
                    post.favorite.remove(user)
                else:
                    post.favorite.add(user)
                return HttpResponseRedirect('/')        #이 부분 체크. 리턴값을 어떻게 해주어야??

class PostFavoriteListAPI(APIView):
    """
        사용자의 스크랩 리스트를 보여주는 API

        ---
        # 내용
            - title : 글 제목
            - text : 글 내용 
    """
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            user=self.request.user
            queryset=user.like_post.all()                     #포스트 조회
            serializer=PostSerializer(queryset, many=True)
            return Response(serializer.data)
