from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group 

##################################################################################
# Command that creates default groups such as Member, Board Member, Committee Member, and Admin
# @author E.M.A. Arts
# @since 22 DEC 2019
# Reference: https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/
##################################################################################

class Command(BaseCommand):
    help = 'Creates default groups such as (Board) Member or Admin'

    # Default groups to create
    def get_default_groups(self):
        return [
            {'name': 'Admin'},
            {'name': 'Moderator'},
            {'name': 'Member'},
            {'name': 'Board Member'},
            {'name': 'Committee Member'},
        ]

    def handle(self, *args, **options):
        sCreatedGroups = []
        for group in self.get_default_groups():
            # Check if another group with the same name already exists
            if Group.objects.filter(name=group.get('name')).exists():
                self.stdout.write(self.style.WARNING('Group "%s" already existed' % group.get('name')))
                continue
            
            # Create the group
            sCreatedGroups.append(group.get('name'))
            pGroup = Group.objects.create(**group)
        
        # Print a termination message
        if sCreatedGroups:
            self.stdout.write(self.style.SUCCESS('Successfully created groups "%s"' % ', '.join(sCreatedGroups)))
        else:
            self.stdout.write(self.style.WARNING('All default groups already existed.'))
