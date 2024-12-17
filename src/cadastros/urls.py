from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import views, viewsets

router = DefaultRouter()

router.register(
    "produto",
    viewset=viewsets.ProdutoViewset,
    basename="produto",
)
router.register(
    "produto-post",
    viewset=viewsets.ProdutoPostViewset,
    basename="produto",
)
router.register(
    "vendedor",
    viewset=viewsets.VendedorViewset,
    basename="vendedor",
)

router.register(
    "equipe-venda",
    viewset=viewsets.EquipeVendaViewset,
    basename="equipe-venda",
)

router.register(
    "loja",
    viewset=viewsets.LojaViewset,
    basename="loja",
)

urlpatterns = []

urlpatterns += router.urls
