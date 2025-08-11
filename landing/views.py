from django.shortcuts import render
from .models import Publicacion, Categoria, Etiqueta, Candidato
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


from django.core.mail import EmailMessage
from django.contrib import messages


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
    
    
def guardar_cv(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        cv = request.FILES.get('cv')

        if nombre and correo and telefono and cv:
            # Guardar en la BD
            Candidato.objects.create(
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                cv=cv
            )

            try:
                # 1️⃣ Correo para el administrador
                email_admin = EmailMessage(
                    subject=f"Nuevo CV recibido de {nombre}",
                    body=(
                        f"Se ha recibido un nuevo currículum:\n\n"
                        f"Nombre: {nombre}\n"
                        f"Correo: {correo}\n"
                        f"Teléfono: {telefono}\n"
                    ),
                    from_email="admin@mercadologosholding.com",  # remitente visible
                    to=["admin@mercadologosholding.com"],  # destinatario real
                )
                email_admin.attach(cv.name, cv.read(), cv.content_type)
                email_admin.send()

                # 2️⃣ Correo de confirmación para el candidato
                email_candidato = EmailMessage(
                    subject="Hemos recibido tu CV - Mercadólogos Holding",
                    body=(
                        f"Hola {nombre},\n\n"
                        "Gracias por enviarnos tu currículum. Nuestro equipo lo revisará y "
                        "te contactaremos si tu perfil encaja con nuestras vacantes.\n\n"
                        "Saludos cordiales,\n"
                        "Equipo de Reclutamiento\n"
                        "Mercadólogos Holding"
                    ),
                    from_email="admin@mercadologosholding.com",
                    to=[correo],
                )
                email_candidato.send()

                messages.success(request, 'Tu CV fue enviado con éxito.')
            except Exception as e:
                messages.error(request, f"Ocurrió un error al enviar el correo: {e}")

            return redirect('equipo')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')

    return redirect('equipo')


def enviar_contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        mensaje = request.POST.get('mensaje')

        if nombre and correo and mensaje:
            try:
                # Correo para el administrador
                email_admin = EmailMessage(
                    subject=f"Nuevo mensaje de contacto de {nombre}",
                    body=(
                        f"Has recibido un nuevo mensaje desde el formulario de contacto:\n\n"
                        f"Nombre: {nombre}\n"
                        f"Correo: {correo}\n"
                        f"Mensaje:\n{mensaje}\n"
                    ),
                    from_email="admin@mercadologosholding.com",
                    to=["admin@mercadologosholding.com"],
                )
                email_admin.send()

                # Respuesta automática al usuario
                email_usuario = EmailMessage(
                    subject="Hemos recibido tu mensaje - Mercadólogos Holding",
                    body=(
                        f"Hola {nombre},\n\n"
                        "Gracias por contactarnos. Hemos recibido tu mensaje y "
                        "te responderemos lo antes posible.\n\n"
                        "Saludos,\n"
                        "Equipo Mercadólogos Holding"
                    ),
                    from_email="admin@mercadologosholding.com",
                    to=[correo],
                )
                email_usuario.send()

                messages.success(request, 'Tu mensaje fue enviado con éxito.')
            except Exception as e:
                messages.error(request, f"Ocurrió un error al enviar el mensaje: {e}")
        else:
            messages.error(request, 'Todos los campos son obligatorios.')

    return redirect('index')