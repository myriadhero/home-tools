from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    todo_verb = models.CharField(max_length=50, help_text="verb, eg 'To Watch'")
    done_verb = models.CharField(
        max_length=50, help_text="verb, past tense, eg 'Watched'"
    )

    def get_chosen(self):
        return JarItem.chosen.filter(category=self).first()

    def get_todo(self):
        return JarItem.todo.filter(category=self)

    def get_done(self):
        return JarItem.done.filter(category=self)

    def has_jar_items(self):
        return self.get_todo().exists()

    def choose_random(self):
        chosen_item = self.get_chosen()
        # prevent picking if exists
        if chosen_item:
            return chosen_item

        random_item: JarItem = self.get_todo().order_by("?").first()
        if random_item:
            random_item.choose()
        return random_item

    def make_chosen_done(self):
        chosen_item: JarItem = self.get_chosen()
        if chosen_item:
            chosen_item.mark_done()

    def get_absolute_url(self):
        return reverse("jar:jar", kwargs={"category": self.slug})


class ChosenManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_chosen=True, is_done=False)


class TodoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_done=False, is_chosen=False)


class DoneManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_done=True, is_chosen=False)


class JarItem(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    is_chosen = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    done_date = models.DateField(default=timezone.now)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )

    objects = models.Manager()
    chosen = ChosenManager()
    done = DoneManager()
    todo = TodoManager()

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=("slug", "category"), name="Category-slug constraint"
            )
        ]

    def choose(self):
        chosen = JarItem.chosen.filter(category=self.category).first()
        if chosen:
            chosen.put_back()
        self.is_chosen = True
        self.save()

    def put_back(self):
        self.is_chosen = False
        self.save()

    def mark_done(self):
        self.is_chosen = False
        self.is_done = True
        self.done_date = timezone.now()
        self.save()

    def mark_undone(self):
        self.is_done = False
        self.save()

    def toggle_done(self):
        if self.is_done:
            self.mark_undone()
        else:
            self.mark_done()

    def save(self, *args, **kwargs):
        self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug = self.slug or slugify(self.name)

        if (
            not JarItem.objects.filter(category=self.category, slug=self.slug)
            .exclude(pk=self.pk)
            .exists()
        ):
            return base_slug

        main_piece, delim, last_piece = base_slug.rpartition("-")

        counter = int(last_piece) + 1 if last_piece.isdigit() else 1
        base_slug = main_piece

        slug = f"{base_slug}-{counter}"

        while JarItem.objects.filter(slug=slug, category=self.category).exists():
            counter += 1
            slug = f"{base_slug}-{counter}"

        return slug
