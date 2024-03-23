from django.urls import path
from . import views

urlpatterns = [

    path('', views.index_view, name="index-view"),

    path('dashboard/', views.JudgesView.as_view({'get': 'get'}), name="dashboard" ),
    path('login/', views.judges_login_view, name="login-view"),
    path('logout/', views.LogoutView.as_view(), name="logout-view"),
    path('register/', views.judges_register, name="register-view"),
    path('search/', views.project_search, name='project-search'),
    path('project-scores/', views.project_scores, name='project-scores'),
    path('submit-register/', views.UserRegistrationAPIView.as_view(), name="register-sub"),
    path('submit-login/', views.LoginView.as_view(), name='login-submition'),
    path('submit-add-project/', views.AddProjectCreateView.as_view(), name="add-project"),
    path('submit-judge-project/', views.AssignJudgeToProject.as_view(), name="judge-project"),

    path('add-project/', views.add_project, name="add_project"),
    path('judge-to-project/', views.assign_judge_project, name="judge-project"),
    path('project/<str:project_id>/board/', views.project_board, name='project_board'),
    path('project/<str:project_id>/grading/', views.GradeProject.as_view(),name="grading"),
]