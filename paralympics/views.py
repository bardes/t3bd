from django.shortcuts import render
from .models import Delegacao, Atleta, Esporte
from django.http import Http404

def ranking(request):
    p = Delegacao.objects.Ranking()

    return render(request, 'paralympics/ranking.html', {'paises': p})

def atleta(request, id):
    a = Atleta.objects.Info(id)
    if not a:
        raise Http404("Atleta não existe!")

    context = {}
    context['atleta'] = a
    context['medalhas'] = Atleta.objects.Medalhas(id)
    return render(request, 'paralympics/atleta.html', context)

def atletas(request):
    context = {}
    deleg = request.GET.get('d', '')
    genero = request.GET.get('g', '')
    esporte = request.GET.get('e', '')

    context['atletas'] = Atleta.objects.Filtra(deleg, genero, esporte)
    context['delegacoes'] = Delegacao.objects.List()
    context['esportes'] = Esporte.objects.List()

    return render(request, 'paralympics/atletas.html', context)
