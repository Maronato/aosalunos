from django.conf.urls import url
from party import views


urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='party_index'),

    url(r'^promises/$', views.promises, name='party_promises'),
    url(r'^add-promise/$', views.add_promises, name='party_add_promises'),
    url(r'^edit-promise/$', views.edit_promises, name='party_edit_promises'),
    url(r'^delete-promise/$', views.delete_promises, name='party_delete_promises'),

    url(r'^texts/$', views.texts, name='party_texts'),

    url(r'^profile/$', views.profile, name='party_profile'),
    url(r'^blog/$', views.blog, name='party_blog'),
]
