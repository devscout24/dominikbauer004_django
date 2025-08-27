from django.shortcuts import render
from rest_framework.permissions import AllowAny,IsAuthenticated
from apps.Authentication.views import BaseAPIView
from .models import NewsPortal
from rest_framework import status
from .serializers import NewsPortalSerializer
# Create your views here.\
    
class NewsPortalListView(BaseAPIView):
    permission_classes= [IsAuthenticated]
    
    def get(self, request):
        try:
            news= NewsPortal.objects.all()
            serializer = NewsPortalSerializer(news, context={'request': request}, many=True)

            
            return self.success_response("News Articles Retrieved Successfully", data= serializer.data)
        
        except Exception as e:
            return self.error_response("Failed to retrieve news", data= {"error": str(e)},
                                       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR )


class UserNewsView(BaseAPIView):
    permission_classes= [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            news= NewsPortal.objects.get(pk=pk)
            serializer= NewsPortalSerializer(news, context={'request': request})
            
            return self.success_response(
                "News featch successfully!",
                data= serializer.data,
            ) 
        except Exception as e:
            return self.error_response(
                "Failed to featch news",
                data= {"error": str(e)}
            )    