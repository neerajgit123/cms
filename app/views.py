from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_205_RESET_CONTENT, HTTP_400_BAD_REQUEST
from .serializers import UserSerializer, UserUpdateSerializer, PostSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated
from .models import User, Like, Post
from django.db.models import Q

class UserListPostUpdateDeleteView(APIView):
    permission_classes = []
    serialier = UserSerializer
    
    def get(self, request):
        data = User.objects.all()
        if data:
            serializer = self.serialier(data, many=True)
            return Response({"data":serializer.data}, status=HTTP_200_OK)
        else:
            return Response({"data":"No Data Found"}, status=HTTP_204_NO_CONTENT)
    
    def post(self, request):
        serializer = self.serialier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "message":"User Created Successfully!!"}, status=HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
    def patch(self,request):
        self.permission_classes = [IsAuthenticated]
        user_id = self.request.user.id
        obj = User.objects.filter(id=user_id).first()
        serializer = UserUpdateSerializer(instance=obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'message':'User Update Successfully!!'}, status=HTTP_205_RESET_CONTENT)
        return Response({"error":serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        self.permission_classes = [IsAuthenticated]
        user_id = self.request.user.id
        user = User.objects.filter(id=user_id).first()
        user.delete()
        return Response({'data':'User is deleted successfully!!'},status=HTTP_204_NO_CONTENT)    
            
class PostListPostView(APIView):
    permission_classes = []
    serialier = PostSerializer
    
    def get(self, request):
        user = request.user.id
        data = Post.objects.filter(Q(is_soft_deleted=False, publish='public') | Q(is_soft_deleted=False, user=user))
        if data:
            serializer = self.serialier(data, many=True)
            return Response({"data":serializer.data}, status=HTTP_200_OK)
        else:
            return Response({"data":"No Data Found"}, status=HTTP_204_NO_CONTENT)
    
    def post(self, request):
        self.permission_classes = [IsAuthenticated]
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        serializer = self.serialier(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "message":"Post Created Successfully!!"}, status=HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=HTTP_400_BAD_REQUEST)

class PostGetUpdateDeleteView(APIView):
    permission_classes = []
    serialier = PostSerializer
    
    def validate_post(self, user, post_id):
        return Post.objects.filter(id=post_id, user=user, is_soft_deleted=False).first()   

    def get(self, request, post_id):
        
        data = Post.objects.filter(is_soft_deleted=False, id=post_id).first()
        if data:
            serializer = self.serialier(data)
            return Response({"data":serializer.data}, status=HTTP_200_OK)
        else:
            return Response({"data":"No Data Found"}, status=HTTP_204_NO_CONTENT)
    
    def patch(self,request, post_id):
        self.permission_classes = [IsAuthenticated]
        user = self.request.user
        obj = self.validate_post(user, post_id)
        if not obj:
            return Response({"data":"This Post is deleted or Not belongs to you!!"}, status=HTTP_404_NOT_FOUND)
        serializer = self.serialier(instance=obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'message':'Post Update Successfully!!'}, status=HTTP_205_RESET_CONTENT)
        return Response({"error":serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
    def delete(self,request, post_id):
        self.permission_classes = [IsAuthenticated]
        user = self.request.user
        obj = self.validate_post(user, post_id)
        if not obj:
            return Response({"data":"This Post is deleted or Not belongs to you!!"}, status=HTTP_404_NOT_FOUND)
        obj.is_soft_deleted=True
        obj.save()
        return Response({'data':'Post is deleted Successfully!!'}, status=HTTP_204_NO_CONTENT)  

class LikeListPostView(APIView):
    serialier = LikeSerializer
    permission_classes = []

    def get(self, request):
        data = Like.objects.filter(is_soft_deleted=False)
        if data:
            serializer = self.serialier(data, many=True)
            return Response({"data":serializer.data}, status=HTTP_200_OK)
        else:
            return Response({"data":"No Data Found"}, status=HTTP_204_NO_CONTENT)
    
    def post(self, request):
        self.permission_classes = [IsAuthenticated]
        request_data = request.data.copy()
        request_data['user'] = request.user.id

        obj = Like.objects.filter(user=request.user, post__id=int(request_data.get('post'))).first()
        if obj:
            return Response({'data':'You already like this post'}, status=HTTP_400_BAD_REQUEST)
        
        serializer = self.serialier(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "message":"Like Successfully!!"}, status=HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=HTTP_400_BAD_REQUEST)
 
class LikeGetUpdateDeleteView(APIView):
    serialier = LikeSerializer
    permission_classes = []
    
    def get(self, request, like_id):
        data = Like.objects.filter(is_soft_delete=False, id=like_id).first()
        if data:
            serializer = self.serialier(data)
            return Response({"data":serializer.data}, status=HTTP_200_OK)
        else:
            return Response({"data":"No Data Found"}, status=HTTP_204_NO_CONTENT)
 
    def patch(self, request, like_id):
        self.permission_classes = [IsAuthenticated]
        user = self.request.user
        request_data = self.request.data
        obj = Like.objects.filter(id=like_id, user=user, post=int(request_data.get('post'))).first()
        if obj and obj.is_soft_deleted == True:
            obj.is_soft_deleted = False
            obj.save()
            return Response({"data":"You like the post!!"}, status=HTTP_205_RESET_CONTENT)
        elif obj and obj.is_soft_deleted == False:
            obj.is_soft_deleted =True
            obj.save()
            return Response({"data":"You dislike the post!!"}, status=HTTP_404_NOT_FOUND)
        else:
            return Response({"data":"This Like is deleted or Not belongs to you!!"}, status=HTTP_404_NOT_FOUND)
    
    def delete(self, request, like_id):
        self.permission_classes = [IsAuthenticated]
        user = self.request.user
        obj = Like.objects.filter(id=like_id, user=user).first()
        if not obj:
            return Response({"data":"This Like is deleted or Not belongs to you!!"}, status=HTTP_404_NOT_FOUND)
        else:
            obj.delete()
            return Response({"data":"This Like is deleted successfully"}, status=HTTP_204_NO_CONTENT)
            
            
            