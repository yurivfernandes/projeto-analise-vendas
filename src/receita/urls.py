from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import views

router = DefaultRouter()
urlpatterns = [
    path('consolidacao/load/',
         view=views.LoadConsolidacaoView.as_view(),
         name='consolidacao-load'),
    path('consolidacao-vendedor/painel/',
         view=views.ConsolidacaoVendedorAnaliseMensal.as_view(),
         name='consolidacao-vendedor-painel'),
    path('consolidacao-produto/painel/',
         view=views.ConsolidacaoProdutoAnaliseMensal.as_view(),
         name='consolidacao-produto-painel'),
    path('consolidacao-loja/painel/',
         view=views.ConsolidacaoLojaAnaliseMensal.as_view(),
         name='consolidacao-loja-painel')
]
urlpatterns += router.urls
