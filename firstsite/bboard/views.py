
from django.shortcuts import render


from bboard.models import Bb


def index(request):
    bbs = Bb.objects.order_by('-published')

    return render(request, 'bboard/index.html', {'bbs': bbs})
