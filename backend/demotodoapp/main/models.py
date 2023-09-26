from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Note(models.Model):
    author = models.ForeignKey(
        to=User,
        verbose_name=_("Author"),
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=30,
        verbose_name=_("Name"),
    )

    def __str__(self):
        return "%s (%s)" % (self.name, self.author)

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")


class Todo(models.Model):
    note = models.ForeignKey(
        to=Note,
        verbose_name=_("Note"),
        on_delete=models.CASCADE,
        related_name="todos",
    )

    text = models.CharField(
        max_length=120,
        verbose_name=_("Text"),
    )

    done = models.BooleanField(
        verbose_name=_("Done"),
        default=False,
    )

    def __str__(self):
        if len(self.text) > 20:
            return "%s..." % self.text[:20]

        return self.text

    class Meta:
        verbose_name = _("Todo")
        verbose_name_plural = _("Todos")
