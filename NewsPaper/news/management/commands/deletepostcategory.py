from django.core.management.base import BaseCommand, CommandError
from news.models import Post ,Category


class Command(BaseCommand):
    help = 'Удаление новостей из выбранной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы действительно хотите удалить все посты в категории {options["category"]}? yes/no:')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Успешно удалены все новости из категории {category.name}'))

        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не удалось найти категорию {options['category']}'))
