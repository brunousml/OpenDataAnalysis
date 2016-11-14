from django.core.management.base import BaseCommand

from data.OpenDataParliamentariansPayments import OpenDataParliamentariansPayments


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Dump open data to local database
        odp = OpenDataParliamentariansPayments()
        odp.dump()
