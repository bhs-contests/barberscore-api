# Third-Party
import pytest
from rest_framework.test import APIClient

# Django
from django.test.client import Client

# First-Party
from api.factories import (
    AppearanceFactory,
    AssignmentFactory,
    AwardFactory,
    ChartFactory,
    ContestantFactory,
    ContestFactory,
    ConventionFactory,
    CompetitorFactory,
    EntryFactory,
    GrantorFactory,
    GridFactory,
    GroupFactory,
    MemberFactory,
    OfficeFactory,
    OfficerFactory,
    OrganizationFactory,
    PanelistFactory,
    ParticipantFactory,
    PersonFactory,
    RepertoryFactory,
    RoundFactory,
    ScoreFactory,
    SessionFactory,
    SongFactory,
    UserFactory,
    VenueFactory,
)


@pytest.fixture
def admin_django_client():
    admin = UserFactory(
        is_staff=True,
        is_active=True,
    )
    client = Client()
    client.force_login(admin)
    return client


@pytest.fixture
def admin_api_client():
    admin = UserFactory(
        is_staff=True,
        is_active=True,
    )
    client = APIClient()
    client.force_authenticate(user=admin)
    return client


@pytest.fixture
def user_api_client():
    user = UserFactory(
        is_staff=False,
        is_active=True,
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def anon_api_client():
    client = APIClient()
    return client


@pytest.fixture
def appearance():
    return AppearanceFactory()


@pytest.fixture
def assignment():
    return AssignmentFactory()


@pytest.fixture
def award():
    return AwardFactory()


@pytest.fixture
def chart():
    return ChartFactory()


@pytest.fixture
def contest():
    return ContestFactory()


@pytest.fixture
def contestant():
    return ContestantFactory()


@pytest.fixture
def convention():
    return ConventionFactory()


@pytest.fixture
def competitor():
    return CompetitorFactory()


@pytest.fixture
def entry():
    return EntryFactory()


@pytest.fixture
def grantor():
    return GrantorFactory()


@pytest.fixture
def grid():
    return GridFactory()


@pytest.fixture
def group():
    return GroupFactory()


@pytest.fixture
def member():
    return MemberFactory()


@pytest.fixture
def office():
    return OfficeFactory()


@pytest.fixture
def officer():
    return OfficerFactory()


@pytest.fixture
def organization():
    return OrganizationFactory()


@pytest.fixture
def panelist():
    return PanelistFactory()


@pytest.fixture
def participant():
    return ParticipantFactory()


@pytest.fixture
def person():
    return PersonFactory()


@pytest.fixture
def repertory():
    return RepertoryFactory()


@pytest.fixture
def round():
    return RoundFactory()


@pytest.fixture
def score():
    return ScoreFactory()


@pytest.fixture
def session():
    return SessionFactory()


@pytest.fixture
def song():
    return SongFactory()


@pytest.fixture
def venue():
    return VenueFactory()


@pytest.fixture
def user():
    return UserFactory()
