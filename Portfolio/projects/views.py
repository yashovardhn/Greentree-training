from django.shortcuts import render, get_object_or_404
from .models import Project


def project_index(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
        'title': 'My Projects'
    }
    return render(request, 'projects/project_index.html', context)


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    context = {
        'project': project,
        'title': project.title
    }
    return render(request, 'projects/project_detail.html', context)
