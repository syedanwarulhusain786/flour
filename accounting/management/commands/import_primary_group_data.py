import json
from django.core.management.base import BaseCommand
from accounting.models import Primary_Group, Group

class Command(BaseCommand):
    help = 'Import primary group and group data from JSON'

    def handle(self, *args, **options):
        with open(r'C:\Users\Java_Shabi\OneDrive\Desktop\travel\travel erp latest\erp\accounting\management\commands\ledger_group.json', 'r') as file:
            data = json.load(file)

            for primary_group_data in data['primary_groups']:
                primary_group = Primary_Group.objects.create(
                    # primary_group_number=primary_group_data['id'],
                    primary_group_name=primary_group_data['name'],
                    primary_group_type=primary_group_data['name'],
                    
                )

                for group_data in primary_group_data['groups']:
                    Group.objects.create(
                        primary_group=primary_group,
                        # group_number=group_data['id'],
                        group_name=group_data['name']
                    )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
