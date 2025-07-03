from django.shortcuts import render


def home(request):
    context = {
        'title': 'Welcome to My Portfolio',
        'welcome_message': 'Hello! I am a passionate developer who loves creating amazing web applications.'
    }
    return render(request, 'pages/home.html', context)
