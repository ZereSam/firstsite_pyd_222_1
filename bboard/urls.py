from django.urls import path, re_path

from bboard.views import index, by_rubric, BbCreateView, add_save, add, add_and_save, practice, detail

vals = {'name': 'by_index',
        'beaver': 'beaver - это бобер!'
}

urlpatterns = [
    path('', index, name='index'),
    path('<int:rubric_id>/', by_rubric, vals, name='by_rubric'),
    # path('add/', BbCreateView.as_view(), name='add'),
    # path('add/save/', add_save, name='add_save'),
    # path('add/', add, name='add'),
    path('add/', add_and_save, name='add'),
    path('text/', practice, name='practice'),
    path('read/<int:rec_id>/', detail, name='read')
]
# urlpatterns = [
#     re_path(r'^$', index, name='index'),
#     re_path(r'^(?P<rubric_id>[0-9]*)/$', by_rubric, vals, name='by_rubric'),
#     re_path(r'^add/$', BbCreateView.as_view(), name='add'),
# ]