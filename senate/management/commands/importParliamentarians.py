from django.core.management.base import BaseCommand

from data.ParliamentaryParser import OpenDataParliamentariansParser


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Dump open data to local database
        odp = OpenDataParliamentariansParser()
        odp.dump()
