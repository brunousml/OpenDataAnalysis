from django.core.management.base import BaseCommand

from data.OpenDataParliamentary import OpenDataParliamentaryBrJsonParser
from senate.models import Parliamentary, ParliamentaryIdentification, State


def get_parliamentary_identification(parliamentary):

    parser = OpenDataParliamentaryBrJsonParser(parliamentary)

    parliamentary_identification = ParliamentaryIdentification.objects.filter(
        name=parser.get_parliamentary_node('NomeParlamentar')
    )

    if not parliamentary_identification:
        # Get State
        state = State.objects.filter(slug=parser.get_parliamentary_node('UfParlamentar'))
        if not state:
            state = State(slug=parser.get_parliamentary_node('UfParlamentar'))
            state.save()
        else:
            state = state[0]

        # Create Parliamentary
        parliamentary_identification = ParliamentaryIdentification(
            code=parser.get_parliamentary_node('CodigoParlamentar'),
            name=parser.get_parliamentary_node('NomeParlamentar'),
            full_name=parser.get_parliamentary_node('NomeCompletoParlamentar'),
            gender=parser.get_parliamentary_node('SexoParlamentar'),
            salutation=parser.get_parliamentary_node('FormaTratamento'),
            url_photo=parser.get_parliamentary_node('UrlFotoParlamentar'),
            url_page=parser.get_parliamentary_node('UrlPaginaParlamentar'),
            email=parser.get_parliamentary_node('EmailParlamentar'),
            acronym_party=parser.get_parliamentary_node('SiglaPartidoParlamentar'),
            state=state,

        )
        parliamentary_identification.save()
    else:
        parliamentary_identification = parliamentary_identification[0]

    return parliamentary_identification


class Command(BaseCommand):
    def handle(self, *args, **options):
        parliamentarians = OpenDataParliamentaryBrJsonParser.get_parliamentarians()

        for parliamentary in parliamentarians:
            self.stdout.write(
                self.style.SUCCESS(unicode(parliamentary[u'IdentificacaoParlamentar'][u'NomeCompletoParlamentar'])))

            p_identification = get_parliamentary_identification(parliamentary)
            parliamentary = Parliamentary.objects.filter(identification=p_identification)

            if not parliamentary:
                parliamentary = Parliamentary(identification=p_identification)
            else:
                parliamentary = parliamentary[0]

            parliamentary.save()

