from django.core.management.base import BaseCommand
from party.models import Members


class Command(BaseCommand):
    help = 'Clears old alerts'

    def handle(self, *args, **options):
        ra = int(options['ra'])
        return Members.create_member(ra)

    def add_arguments(self, parser):
        parser.add_argument('ra')
