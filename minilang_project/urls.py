from django.urls import path, include

urlpatterns = [
    # REMOVER la línea del admin:
    # path('admin/', admin.site.urls),
    path('', include('minilang_app.urls')),
]