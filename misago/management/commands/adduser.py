from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from optparse import make_option
from misago.models import Role, User

class Command(BaseCommand):
    args = 'username email password'
    help = 'Creates new user account'
    option_list = BaseCommand.option_list + (
        make_option('--admin',
            action='store_true',
            dest='admin',
            default=False,
            help='Make a new user an administrator'),
        )

    def handle(self, *args, **options):
        if len(args) < 3:
            raise CommandError('adduser requires exactly three arguments: user name, e-mail address and password')

        # Set user
        try:
            new_user = User.objects.create_user(args[0], args[1], args[2])
        except ValidationError as e:
            raise CommandError("New user cannot be created because of following errors:\n\n%s" % '\n'.join(e.messages))

        # Set admin role
        if options['admin']:
            new_user.roles.add(Role.objects.get(_special='admin'))
            new_user.make_acl_key(True)
            new_user.save(force_update=True)

        if options['admin']:
            self.stdout.write('Successfully created new administrator "%s"' % args[0])
        else:
            self.stdout.write('Successfully created new user "%s"' % args[0])
        self.stdout.write('\n\nNew user should use "%s" e-mail address and "%s" password to sign in.\n' % (args[1], args[2]))
