from django.db import models
from django.conf import settings


class Projects(models.Model):
    TYPE_PROJECT = (
        ('BackEnd', 'BackEnd'),
        ('FrontEnd', 'FrontEnd'),
        ('IOS', 'IOS'),
        ('Android', 'Android'),
    )
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=8192)
    type = models.CharField(max_length=20, default='BackEnd', choices=TYPE_PROJECT)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Projects'


class Contributors(models.Model):
    ROLE = (
        ('Responsable', 'Responsable'),
        ('Dev', 'Dev'),
    )

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    permission = models.CharField(max_length=20)
    role = models.CharField(max_length=128,default='Dev', blank=True, choices=ROLE)

    def __str__(self):
        return "{} à contribuer au projet : {}".format(self.user, self.project)

    class Meta:
        verbose_name_plural = 'Contributors'


class Issues(models.Model):
    STATUS = (
        ('Début', 'Début'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
    )
    TAG = (
        ('Tâche', 'Tâche'),
        ('Bug', 'Bug'),
        ('Amélioration', 'Amélioration'),
    )
    PRIORITY = (
        ('Faible', 'Faible'),
        ('Moyen', 'Moyen'),
        ('Elevé', 'Elevé'),
    )
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=500)
    tag = models.CharField(max_length=20, default='Tâche', choices=TAG)
    priority = models.CharField(max_length=20, default='Moyen', choices=PRIORITY)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='En cours', choices=STATUS)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Auteur')
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Contributeur')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Issues'


class Comments(models.Model):
    description = models.CharField(max_length=500)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} a commenter l'issue {}".format(self.author, self.issue[:10])

    class Meta:
        verbose_name_plural = 'Comments'
