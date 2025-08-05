from django.shortcuts import render
from .models import Publicacion, Categoria, Etiqueta
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404


# Create your views here.
def index(request):
    return render(request, 'index.html')
def servicios(request):
    return render(request, 'servicios.html')
def equipo(request):
    return render(request, 'equipo.html')
def blog(request):
    publicaciones = Publicacion.objects.filter(es_publicado=True).order_by('-fecha_publicacion')
    recientes = Publicacion.objects.filter(es_publicado=True).order_by('-fecha_publicacion')[:3]
    categorias = Categoria.objects.all()
    etiquetas = Etiqueta.objects.all()
    paginator = Paginator(publicaciones, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {
    'page_obj': page_obj,
    'categorias': categorias,
    'etiquetas': etiquetas,
    'recientes': recientes,
})


def blog_detalles(request, slug):
    publicacion = get_object_or_404(Publicacion, slug=slug, es_publicado=True)

    prev_post = Publicacion.objects.filter(
        es_publicado=True,
        fecha_publicacion__lt=publicacion.fecha_publicacion
    ).order_by('-fecha_publicacion').first()

    next_post = Publicacion.objects.filter(
        es_publicado=True,
        fecha_publicacion__gt=publicacion.fecha_publicacion
    ).order_by('fecha_publicacion').first()

    recientes = Publicacion.objects.filter(es_publicado=True).exclude(slug=slug).order_by('-fecha_publicacion')[:3]
    categorias = Categoria.objects.all()
    etiquetas = Etiqueta.objects.all()

    return render(request, 'blog-detalles.html', {
        'publicacion': publicacion,
        'recientes': recientes,
        'categorias': categorias,
        'etiquetas': etiquetas,
        'prev_post': prev_post,
        'next_post': next_post,
    })

def tag_detail(request, slug):
    etiqueta = get_object_or_404(Etiqueta, slug=slug)
    publicaciones = Publicacion.objects.filter(
        etiquetas=etiqueta,
        es_publicado=True
    ).order_by('-fecha_publicacion')

    recientes = Publicacion.objects.filter(es_publicado=True).exclude(etiquetas=etiqueta)[:3]
    categorias = Categoria.objects.all()
    etiquetas = Etiqueta.objects.all()

    return render(request, 'tag-detail.html', {
        'etiqueta': etiqueta,
        'publicaciones': publicaciones,
        'recientes': recientes,
        'categorias': categorias,
        'etiquetas': etiquetas,
    })