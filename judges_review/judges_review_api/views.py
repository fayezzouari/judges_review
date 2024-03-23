from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from requests import auth
from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from . import forms
from .serializers import JudgementSerializer, UserLoginSerializer, UserSerializer
from .models import Judgement, Project
from .forms import AssignJudgeProject, AddProject, UserRegistrationForm, ProjectSearchForm
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login, logout


# Create your views here.
#   @permission_classes([IsAuthenticated])
class JudgesView(viewsets.ModelViewSet):
    def get(self, request):
        form = ProjectSearchForm(request.POST)

        queryset = Judgement.objects.filter(judge=request.user.id)
        projects = Project.objects.values_list('id', 'name')
        users_data = []
        i=0
        print(request.user)
        for project in projects:

            try:
                if queryset[i].project_id.id == project[0] :
                    user_data = {
                        'id': project[0],
                        'name': project[1],
                        'score': queryset[i].score,
                    }
                    i+=1
                    users_data.append(user_data)
            except:
                break
        return render(request, 'dashboard.html',{'projects':users_data, 'user': request.user, 'form': form})


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "User Does not exist!"
                }
            }

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Login successful
                # You can perform additional actions here like setting session data
                login(request, user)
                if request.user.is_superuser:
                    return redirect('../project-scores/')
                return redirect('../dashboard/')
            else:
                # Authentication failed
                return redirect('../login/')

        # Invalid input data
        return redirect('../login/')

class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            logout(request)
            return redirect('../login')
        except:
            return Response({'error': 'Something went wrong'})


class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']

                # Create user
                user = User.objects.create_user(username=username, password=password, email=email)

                # Assign user to a specific group
                group_name = 'Judge'  # Change this to the desired group name
                try:
                    group = Group.objects.get(name=group_name)
                    group.user_set.add(user)
                except Group.DoesNotExist:
                    # Handle group not found error
                    pass

                # Redirect to success page or any other desired page
                return HttpResponseRedirect('judges_space/login/')  # Change this to your success URL

        else:
            form = UserRegistrationForm()

        return render(request, 'registration/register.html', {'form': form})


class AddProjectCreateView(generics.CreateAPIView):
    def post(self, request):
        form = AddProject(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            name = form.cleaned_data['name']
            item= Project(id=id, name=name)
            item.save()
            return redirect('../judge-to-project/')


class AssignJudgeToProject(generics.CreateAPIView):
    serializer_class = JudgementSerializer
    def post(self, request):
        form = AssignJudgeProject(request.POST)
        if form.is_valid():
            project_id = form.cleaned_data['project_id']
            judge = form.cleaned_data['judge']
            item = Judgement(project_id=project_id, judge=judge)
            item.save()
            return redirect('../add-project/')


def judges_login_view(request):
    return render(request, 'login.html')


def add_project(request):
    form = AddProject(request.POST)
    return render(request, 'add-project.html',  {'form' : form})


def assign_judge_project(request):
    form = AssignJudgeProject(request.POST)
    return render(request, 'assign-judge-project.html', {'form' : form})


def judges_register(request):
    form = UserRegistrationForm(request.POST)
    return render(request, 'register.html', {'form': form})


def project_search(request):
    if request.method == 'POST':
        form = ProjectSearchForm(request.POST)
        if form.is_valid():
            project_id = form.cleaned_data['project_id']
            # Perform search query to find the project with the specified ID
            projects = Project.objects.filter(id=project_id)
            return render(request, 'search_results.html', {'projects': projects, 'searched_id': project_id})

    return render(request, 'dashboard.html')


def project_board(request, project_id):
    project = Project.objects.get(id=project_id)
    # Logic to display the board for judging the project
    return render(request, 'project_board.html', {'project': project})

class GradeProject(APIView):
    serializer_class = JudgementSerializer
    def post(self,request, project_id):
        instance = Judgement.objects.get(project_id=project_id, judge= request.user)

        form = forms.GradeProject(request.POST)
        if form.is_valid():
            presentation = form.cleaned_data['presentation']
            prototype = form.cleaned_data['prototype']
            #business_plan = form.cleaned_data['business_plan']
            idea = form.cleaned_data['idea']
            score = presentation + prototype  + idea
            setattr(instance, 'score', score)  # Update the score field value
            instance.save()
            return redirect('../../../dashboard/')


# views.py

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def project_scores(request):
    projects = Project.objects.all()
    judges = User.objects.filter(groups__name='Judge')
    project_scores = []
    for project in projects:
        scores = {}
        scores['project'] = project
        scores['judges'] = {}
        for judge in judges:
            try:
                score = Judgement.objects.get(project_id=project.id, judge=judge)
                scores['judges'][judge.username] = score.score
            except Judgement.DoesNotExist:
                continue
        project_scores.append(scores)

    return render(request, 'projects_scores.html', {'project_scores': project_scores})
