from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import TaskSerializer,UserSerializer
from api.models import Tasks
from django.contrib.auth.models import User

from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.decorators import action
from rest_framework import authentication,permissions


# Create your views here.
class TaskView(APIView):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        qs=Tasks.objects.get(id=id) 
        serializer=TaskSerializer(qs,many=False)
        return Response(data=serializer.data) 
    def delete(self,request,*args,**kw):
        id=kw.get("id") 
        Tasks.objects.get(id=id).delete()
        return Response(data="deleted")
    def put(self,request,*args,**kw):
        id=kw.get("id")
        obj=Tasks.objects.get(id=id)
        serializer=TaskSerializer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)    



class TaskViewsetView(ViewSet):
    def list(self,request,*args,**kw):
        qs=Tasks.objects.all()
        serializer=TaskSerializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self,request,*args,**kw):
        serializer=TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:     
            return Response(data=serializer.errors)
    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Tasks.objects.get(id=id) 
        serializer=TaskSerializer(qs,many=False)
        return Response(data=serializer.data) 


    def upadate(self,request,*args,**kw):
        id=kw.get("pk")
    
        obj=Tasks.objects.get(id=id)
        serializer=TaskSerializer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)    

    def destroy(self,request,*args,**kw):
        id=kw.get("pk") 
        Tasks.objects.get(id=id).delete()
        return Response(data="deleted")

class TaskModelViewsetView(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    serializer_class=TaskSerializer
    queryset=Tasks.objects.all()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def list(self, request, *args, **kw):
        qs=Tasks.objects.filter(user=request.user)
        serializer=TaskSerializer(qs,many=True)
        return Response(data=serializer.data)
            
    
    # def create(self, request, *args, **kw):
    #     serializer=TaskSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(User=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)            


#localhost:8000/api/v1/tasks/finished_tasks
    @action(methods=["GET"],detail=False)    
    def finished_tasks(self,request,*args,**kw):
        qs=Tasks.objects.filter(status=True)
        serializer=TaskSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["GET"],detail=False)    
    def pending_tasks(self,request,*args,**kw):
        qs=Tasks.objects.filter(status=False)
        serializer=TaskSerializer(qs,many=True)
        return Response(data=serializer.data)
    @action(methods=["POST"],detail=True) 
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        Tasks.objects.filter(id=id).update(status=True) 
        return Response(data="status updated")
        
        

class UserView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            usr=User.objects.create_user(**serializer.validated_data)
            serializer=UserSerializer(usr,many=False)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)    

  

        
    
  