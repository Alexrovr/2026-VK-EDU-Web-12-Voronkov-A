from django.shortcuts import render

# Генерируем тестовые данные пользователей
USERS = [
    {
        'id': i,
        'username': f'user{i}',
        'email': f'user{i}@example.com',
        'avatar': 'img/default-avatar.png',
        'bio': f'Я участник форума, интересуюсь программированием'
    } for i in range(1, 10)
]

def login_view(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def profile(request, user_id):
    user = next((u for u in USERS if u['id'] == user_id), None)
    return render(request, 'profile.html', {'user': user, 'popular_tags': ['python', 'django', 'javascript', 'react', 'css']})
