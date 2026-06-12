from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	             path('UserLogin.html', views.UserLogin, name="UserLogin"), 
	             path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),
		     path('TrainYolo', views.TrainYolo, name="TrainYolo"),
	             path('TrainGraph', views.TrainGraph, name="TrainGraph"),
	             path('SpeciesDetection', views.SpeciesDetection, name="SpeciesDetection"),
	             path('SpeciesDetectionAction', views.SpeciesDetectionAction, name="SpeciesDetectionAction"),	              	       
]
