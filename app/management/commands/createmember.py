from django.core.management.base import BaseCommand
from party.models import Members


class Command(BaseCommand):
    help = 'Manually add member to party'

    def add_arguments(self, parser):
        parser.add_argument('ra', )

    def handle(self, *args, **options):
        member = Members.create_member(int(args[0]))
        if member is not None:
            print("Member created")
        else:
            print("RA not registered")
        return
