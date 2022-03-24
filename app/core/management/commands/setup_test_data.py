import random

from django.db import transaction
from django.core.management.base import BaseCommand

from clients.constants import CommunicationTypes
from clients.models import (
    Client,
    ClientContact,
    ClientCommunication,
    ClientAddress
)
from clients.factories import (
    IndividualClientFactory,
    CompanyClientFactory,
    ClientContactFactory,
    ClientCommunicationFactory,
    ClientAddressFactory
)
from core.models import User
from notes.factories import NoteFactory
from notes.models import Note


CLIENT_COUNT = 500
CLIENT_FACTORY_TYPES = (IndividualClientFactory, CompanyClientFactory)


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Initializing...")
        models = [
            Client,
            ClientContact,
            Note,
            ClientCommunication,
            ClientAddress
        ]
        clients = []
        users = [None, ]
        for user in User.objects.all():
            users.append(user)
        self.stdout.write("Removing Previously Generated Data...")
        for m in models:
            m.objects.all().delete()
        self.stdout.write("Generating Clients...")
        for i in range(CLIENT_COUNT):
            client = random.choice(CLIENT_FACTORY_TYPES)()
            clients.append(client)
            for i in range(random.randrange(1, 5)):
                ClientContactFactory(client=client)
            for i in range(random.randrange(0, 15)):
                NoteFactory(client=client)
            for i in range(random.randrange(0, 10)):
                ClientCommunicationFactory(
                    contact=random.choice(client.contacts.all()),
                    client=client,
                    communication_type=random.choice(
                        CommunicationTypes.COMMUNICATION_TYPE_CHOICES
                    )[0]
                )
            for i in range(random.randrange(1, 3)):
                ClientAddressFactory(
                    client=client,
                    description="Warehouse"
                )
            assigned_user = random.choice(users)
            if assigned_user:
                client.assigned_users.add(assigned_user)
        self.stdout.write("Data Generation Complete.")
