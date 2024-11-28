from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from .forms import UserCreateForm
from .models import User, Ranking, UserHistory, Waste, ScanningStatistics
from django.db import IntegrityError
from .utils import decrypt_message
import json
from datetime import datetime
from django.db import models
import random


@login_required
def custom_logout(request):
    logout(request)
    return redirect('home.index')


def custom_login(request):
    viewData = {}
    viewData["title"] = "Iniciar Sesión"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "Login", "route": "accounts.login"},
    ]
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {"viewData": viewData})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            viewData["error"] = 'El nombre de usuario o la contraseña no son correctos.'
            return render(request, 'accounts/login.html', {"viewData": viewData})
        else:
            login(request, user)
            next_route = request.GET.get('next')
            if next_route:
                try:
                    return redirect(next_route)
                except:
                    pass
            return redirect('home.index')


def signup(request):
    viewData = {}
    viewData["title"] = "Registro"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "Signup", "route": "accounts.signup"},
    ]

    if request.method == 'GET':
        viewData["form"] = UserCreateForm()
        return render(request, 'accounts/signup.html', {"viewData": viewData})
    else:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email'],
                    experience_points=0
                )
                user.save()
                login(request, user)
                return redirect('home.index')
            except IntegrityError as error:
                viewData["error"] = [error]
        else:
            error_list = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_list.append(error)

            viewData["error"] = error_list

        viewData["form"] = form
        return render(request, 'accounts/signup.html', {"viewData": viewData})


@login_required
def profile(request):
    if request.method == 'POST' and request.FILES.get('profile_pic'):
        request.user.profile_picture = request.FILES.get('profile_pic')
        request.user.save()
        return redirect('accounts.profile')

    viewData = {}
    viewData["title"] = "Perfil"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "My Account", "route": "accounts.index"},
        {"name": "Profile", "route": "accounts.profile"},
    ]
    viewData["user"] = request.user
    user_points = request.user.experience_points
    user_ranking = Ranking.objects.filter(from_points__lte=user_points, to_points__gte=user_points).first()
    viewData["ranking"] = user_ranking
    return render(request, 'accounts/profile.html', {"viewData": viewData})


@login_required
def index(request):
    viewData = {}
    viewData["title"] = "Mi cuenta"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "My Account", "route": "accounts.index"},
    ]
    return render(request, 'accounts/index.html', {"viewData": viewData})


@login_required
def rankings(request):
    viewData = {}
    viewData["title"] = "Divisiones"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "My Account", "route": "accounts.index"},
        {"name": "Rankings", "route": "accounts.rankings"},
    ]
    viewData["rankings"] = Ranking.objects.order_by('-level')
    user_points = request.user.experience_points
    user_ranking = Ranking.objects.filter(from_points__lte=user_points, to_points__gte=user_points).first()
    pending_points = (user_ranking.to_points - user_points) + 1
    progress_percentage = 100 * (1 - (pending_points / (user_ranking.to_points + 1 - user_ranking.from_points)))
    viewData["user_points"] = user_points
    viewData["user_ranking_name"] = user_ranking.name
    viewData["user_pending_points"] = pending_points
    viewData["user_progress_percentage"] = round(progress_percentage)

    return render(request, 'accounts/rankings.html', {"viewData": viewData})


@login_required
def redemption(request, encrypted_message):
    viewData = {}
    viewData["title"] = "Redención de puntos"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "My Account", "route": "accounts.index"},
        {"name": "Redemption", "route": "accounts.redemption"},
    ]

    try:
        code = decrypt_message(encrypted_message)
        code.user = request.user
        code.save()

        gained_points = 1

        if (code.success == "1"):
            gained_points = 5

        UserHistory.objects.create(
            type_of_activity='QR_SCAN',
            accumulated_points=gained_points,
            user=request.user
        )

        request.user.experience_points += gained_points
        request.user.save()

        viewData["gained_points"] = gained_points
        viewData["success"] = "El código ha sido redimido con éxito."
    except:
        viewData["error"] = "Código inválido."

    return render(request, 'accounts/redemption.html', {"viewData": viewData})


@login_required
def stats(request):
    viewData = {}
    viewData["title"] = "My Stats"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "My Account", "route": "accounts.index"},
        {"name": "Stats", "route": "accounts.stats"},
    ]
    scanning_entries = ScanningStatistics.objects.filter(user=request.user).order_by('-scan_date')
    total_co2 = scanning_entries.aggregate(total_co2=models.Sum('co2_saved'))
    
    # Calculamos el porcentaje (1kg = 100%)
    total_co2_value = total_co2['total_co2'] or 0
    co2_percentage = total_co2_value * 100
    
    co2_percentage_str = f"{min(round(co2_percentage, 1), 100):.1f}".replace(',', '.')

    viewData["scanning_entries"] = scanning_entries
    viewData["total_co2"] = total_co2_value
    viewData["co2_percentage"] = co2_percentage_str  
    return render(request, 'accounts/stats.html', {"viewData": viewData})


@login_required
def upload_json(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        json_file = request.FILES['json_file']
        try:
            data = json.load(json_file)
            print(data)
            for item in data:
                Waste.objects.create(
                    iteration=item[0],
                    date=datetime.strptime(item[1], '%d/%m/%Y/%H:%M:%S').strftime('%Y-%m-%d'),
                    name_ima_before=item[2],
                    name_ima_after=item[3],
                    mode=item[4],
                    folder=item[5],
                    res=item[6],
                    rec=item[7],
                    ecological_point=item[8],
                    model_version=item[9],
                    success=item[10]
                )
            return redirect(request.META.get('HTTP_REFERER', '/'))
        except json.JSONDecodeError:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def experience_points(request):
    viewData = {}
    viewData["title"] = "My Experience"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "My Account", "route": "accounts.index"},
        {"name": "Experience", "route": "accounts.experience"},
    ]
    scanning_entries = ScanningStatistics.objects.filter(user=request.user).order_by('-scan_date')
    total_experience = scanning_entries.aggregate(total_experience=models.Sum('experience'))
    viewData["scanning_entries"] = scanning_entries
    viewData["total_experience"] = total_experience['total_experience'] or 0
    return render(request, 'accounts/experience.html', {"viewData": viewData})

def waste_quiz(request):
    questions = [
        {"question": "Where should you dispose of a plastic bottle?", "options": ["Black Bin", "White Bin", "Green Bin"], "answer": "White Bin"},
        {"question": "Where should you dispose of food scraps?", "options": ["Black Bin", "White Bin", "Green Bin"], "answer": "Green Bin"},
        {"question": "Where should you dispose of a newspaper?", "options": ["Black Bin", "White Bin", "Green Bin"], "answer": "White Bin"},
        {"question": "Where should you dispose of a broken glass?", "options": ["Black Bin", "White Bin", "Green Bin"], "answer": "Black Bin"},
        {"question": "Where should you dispose of a used tissue?", "options": ["Black Bin", "White Bin", "Green Bin"], "answer": "Black Bin"},
        {"question": "Where should you dispose of a cardboard box?", "options": ["Black Bin", "White Bin", "Green Bin"], "answer": "White Bin"},
        {"question": "Where should you dispose of coffee grounds?", "options": ["Black Bin", "White Bin", "Green Bin"], "answer": "Green Bin"},
        {"question": "Where should you dispose of a candy wrapper?", "options": ["Black Bin", "White Bin", "Green Bin"], "answer": "Black Bin"},
        {"question": "Where should you dispose of a magazine?", "options": ["Black Bin", "White Bin", "Green Bin"], "answer": "White Bin"},
        {"question": "Where should you dispose of yard waste?", "options": ["Black Bin", "White Bin", "Green Bin"], "answer": "Green Bin"},
    ]

    if request.method == 'POST':
        feedback = []
        all_correct = True
        
        for i, question in enumerate(request.session['quiz_questions']):
            user_answer = request.POST.get(f'question_{i+1}')
            correct_answer = question['answer']
            
            if user_answer != correct_answer:
                all_correct = False
                feedback.append({
                    'question': question['question'],
                    'user_answer': user_answer,
                    'correct_answer': correct_answer
                })
        
        return render(request, 'accounts/quiz_result.html', {
            'all_correct': all_correct,
            'feedback': feedback
        })

    selected_questions = random.sample(questions, 3)
    request.session['quiz_questions'] = selected_questions
    return render(request, 'accounts/quiz.html', {'questions': selected_questions})