from django.urls import path, re_path
from django.views.generic.dates import WeekArchiveView
from django.views.generic.edit import CreateView

from bboard.models import Bb
from bboard.views import index, by_rubric, BbCreateView, add_save, add, add_and_save, practice, detail, BbByRubricView, \
    IndexListView, BbDetailView, BbAddView, BbIndexView, BbMonthArchiveView, BbRedirectView

vals = {'name': 'by_index',
        'beaver': 'beaver - это бобер!'
}

urlpatterns = [
    path('', index, name='index'),
    #path('', BbIndexView.as_view(), name='index'),
    #path('<int:rubric_id>/', by_rubric, vals, name='by_rubric'),
    path('<int:rubric_id>/', BbByRubricView.as_view, name='by_rubric'),
    # path('add/', BbCreateView.as_view(), name='add'),
    # path('add/save/', add_save, name='add_save'),
    # path('add/', add, name='add'),
    # path('add/', add_and_save, name='add'),
    #path('text/', practice, name='practice'),
    path('read/<int:rec_id>/', detail, name='read'),
    #path('add/', BbCreateView.as_view(), name='add'),
    path('add/', BbAddView.as_view(), name='add'),
    path('detail/<int:pk/', BbDetailView.as_view(), name='detail'),
    path('<int:year>/<int:month>/', BbMonthArchiveView.as_view()),
    path('<int:year>/week/<int:week>/', WeekArchiveView.as_view(
        model=Bb, date_field='published', context_object_name='bbs')),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/',
         BbRedirectView.as_view(), name='old_detail'),
    ]
# urlpatterns = [
#     re_path(r'^$', index, name='index'),
#     re_path(r'^(?P<rubric_id>[0-9]*)/$', by_rubric, vals, name='by_rubric'),
#     re_path(r'^add/$', BbCreateView.as_view(), name='add'),
# ]