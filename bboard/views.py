from django.db.models import Min, Max, Count, Q, Sum, IntegerField, Avg
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, Http404, StreamingHttpResponse, FileResponse, \
    JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from bboard.forms import BbForm
from bboard.models import Bb, Rubric


def count_bb():
    result = {}
    for r in Rubric.objects.annotate(num_bbs=Count('bb')):
        result.update({r.pk: r.num_bbs})
    return result


def print_request_fields(request):
    for attr in dir(request):
        value = getattr(request, attr)
        print(f"{attr}:  {value}")


class BbCreateView(CreateView):
    template_name = 'bboard/add_form.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()

        return context


def index_resp(request):
    resp = HttpResponse("Здесь будет", content_type='text/plain; charset=utf-8')
    resp.write(' главная')
    resp.writelines((' страница', ' сайта'))
    resp['keywords'] = 'Python, Django'
    return resp


class IndexListView(ListView):
    template_name = 'bboard/index.html'
    model = Bbcontext_object_name = 'bbs'

    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['min_price'], context['max_price'], context['diff_price'] = self.get_price_aggregates()
        context['count_bb'] = BbCreateView().count_bb()
        return context

    def get_price_aggregates(self):
        result = Bb.objects.aggregate(
            min_price=Min('price'),
            max_price=Max('price'),
            diff_price=Max('price') - Min('price')
        )
        return result.get('min_price'), result.get('max_price'), result.get('diff_price')


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    template = get_template('bboard/index.html')
    # return HttpResponse(template.render(context, request))
    return HttpResponse(render_to_string('bboard/index.html', context, request))
    #data = {'title': 'Мотоцикл', 'content': 'Старый', 'price': 10000.0}
    #return JsonResponse(data)

#def index(request):
#    resp_content = ('Здесь будет', ' главная', ' страница', ' сайта')
 #   resp = StreamingHttpResponse(resp_content,
 #                                content_type='text/plain; charset=utf-8')
 #   return resp


def practice(request):
    prac = HttpResponse('It is normal', content_type='text/plain; charset=utf-8')
    prac.write(' to')
    prac.writelines((' love', ' flowers'))
    prac['keywords'] = 'Python, Django'
    return prac


def index_old(request):
    bbs = Bb.objects.order_by('-published')
    rubrics = Rubric.objects.all()

    # min_price = Bb.objects.aggregate(Min('price'))
    # max_price = Bb.objects.aggregate(mp=Max('price'))
    result = Bb.objects.aggregate(min_price=Min('price'),
                                  max_price=Max('price'),
                                  diff_price=Max('price') - Min('price'))

    # for r in Rubric.objects.annotate(cnt=Count('bb',
    #                                  filter=Q(bb__price__gt=1000))):
                                     # min=Min('bb__price')).filter(cnt__gt=0):

        # print(r.name, ': ', r.min, sep='')
        # print(r.name, ': ', r.min, sep='')

    # print(
    #     Bb.objects.aggregate(
    #         sum=Sum(
    #             'price', output_field=IntegerField(),
    #                              filter=Q(rubric__name='Бытовая техника'))))

    print(
        Bb.objects.aggregate(
            avg=Avg(
                'price', output_field=IntegerField(),
                filter=Q(rubric__name='Сельхозтехника'),
            distinct=False  # если True, то только уникальное
     )))

    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        # 'min_price': min_price.get('price__min'),
        # 'max_price': max_price.get('mp'),
        'min_price': result.get('min_price'),
        'max_price': result.get('max_price'),
        'diff_price': result.get('diff_price'),
        'count_bb': count_bb(),
    }
    return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id, **kwargs):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)

    print(kwargs.get('name'), kwargs.get('beaver'))

    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        'current_rubric': current_rubric,
        'count_bb': count_bb(),
        # 'name': kwargs.get('name'),
        'kwargs': kwargs,

    }
    current_rubric = Rubric()
    try:
        current_rubric = Rubric.objects.get(pk=rubric_id)
    except current_rubric.DoesNotExist:
        return HttpResponseNotFound('Такой рубрики не существует')


#     return HttpResponse(...)


# class BbByRubricView(TemplateView):
#     template_name = 'bboard/by_rubric.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
#         context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
#         context['rubrics'] = Rubric.objects.all()
#         return context


def add(request):
    bbf = BbForm()
    context = {'form': bbf}
    return render(request, 'bboard/add_form.html', context)


def add_save(request):
    bbf = BbForm(request.POST)

    if bbf.is_valid():
        bbf.save()

        return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
    else:
        context = {'form': bbf}
        return render(request, 'bboard/add_form.html', context)


def add_and_save(request):
    if request.method == 'POST':

        bbf = BbForm(request.POST)

        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/add_form.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'bboard/add_form.html', context)


# def detail(request, bb_id):
#     try:
#         bb = Bb.objects.get(pk=bb_id)
#     except Bb.DoesNotExist:
#         # return HttpResponseNotFound('Такого объявления не существует')
#         return Http404('Такого объявления не существует')
#     return HttpResponse(...)


def detail(request, rec_id):
    bb = get_object_or_404(Bb, pk=rec_id)
    bbs = get_list_or_404(Bb, pk=bb.rubric.pk)
    context = {'bb': bb, 'bbs': bbs}
    return HttpResponse(render_to_string('bboard/detail.html', context, request))


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context


class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('bboard:by_rubric',
                       kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})




