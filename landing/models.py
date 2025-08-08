from django.db import models


from django.urls import reverse


class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('blog:category_detail', args=[self.slug])


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('blog:tag_detail', args=[self.slug])


class Publicacion(models.Model):
    titulo = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    autor = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='blog_posts')
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name='posts')
    etiquetas = models.ManyToManyField(Etiqueta, related_name='posts', blank=True)
    imagen = models.ImageField(upload_to='blog/images/')
    contenido = models.TextField()
    extracto = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField()
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    es_publicado = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # Auto-generate extracto if not provided
        if not self.extracto:
            self.extracto = self.contenido[:200] + '...'
        super().save(*args, **kwargs)


class Candidato(models.Model):
    nombre = models.CharField(max_length=255)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    cv = models.FileField(upload_to='cvs/')
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.correo}"
