# Standard Libary
import logging

# Third-Party
import pydf
from django_filters.rest_framework import DjangoFilterBackend
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.utils.text import slugify

# Local
from .backends import CoalesceFilterBackend
from .filters import AssignmentFilter
from .filters import ConventionFilter
from .filters import GroupFilter
from .filters import OfficerFilter
from .filters import ScoreFilter
from .filters import RoundFilter
from .filters import SessionFilter
from .filters import UserFilter
from .filters import StateLogFilter
from .models import Appearance
from .models import Assignment
from .models import Award
from .models import Chart
from .models import Competitor
from .models import Contest
from .models import Contestant
from .models import Convention
from .models import Entry
from .models import Grantor
from .models import Grid
from .models import Group
from .models import Member
from .models import Office
from .models import Officer
from .models import Panelist
from .models import Person
from .models import Repertory
from .models import Round
from .models import Score
from .models import Session
from .models import Song
from .models import User
from .models import Venue
from .serializers import AppearanceSerializer
from .serializers import AssignmentSerializer
from .serializers import AwardSerializer
from .serializers import ChartSerializer
from .serializers import CompetitorSerializer
from .serializers import ContestantSerializer
from .serializers import ContestSerializer
from .serializers import ConventionSerializer
from .serializers import EntrySerializer
from .serializers import GrantorSerializer
from .serializers import GridSerializer
from .serializers import GroupSerializer
from .serializers import MemberSerializer
from .serializers import OfficerSerializer
from .serializers import OfficeSerializer
from .serializers import PanelistSerializer
from .serializers import PersonSerializer
from .serializers import RepertorySerializer
from .serializers import RoundSerializer
from .serializers import ScoreSerializer
from .serializers import SessionSerializer
from .serializers import SongSerializer
from .serializers import StateLogSerializer
from .serializers import UserSerializer
from .serializers import VenueSerializer
from .renderers import PDFRenderer
from .responders import PDFResponse
from .renderers import XLSXRenderer
from .responders import XLSXResponse
from .tasks import create_legacy_report
from .tasks import create_drcj_report
from .tasks import create_contact_report
from .tasks import create_roster_report
from .tasks import create_chart_report


log = logging.getLogger(__name__)


class AppearanceViewSet(viewsets.ModelViewSet):
    queryset = Appearance.objects.select_related(
        'round',
        'competitor',
        'grid',
    ).prefetch_related(
        'songs',
    ).order_by('id')
    serializer_class = AppearanceSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "appearance"

    @action(methods=['post'], detail=True)
    def start(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.start(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def finish(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.finish(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def verify(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.verify(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def confirm(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.confirm(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def include(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.include(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def exclude(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.exclude(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)



class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related(
        'convention',
        'person',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = AssignmentSerializer
    filter_class = AssignmentFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "assignment"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.activate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.deactivate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.select_related(
        'group',
        'parent',
    ).prefetch_related(
        'children',
        'contests',
    ).order_by('status', 'name')
    serializer_class = AwardSerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "award"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.activate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.deactivate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.select_related(
    ).prefetch_related(
        'repertories',
        'songs',
    ).order_by('status', 'title')
    serializer_class = ChartSerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "chart"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.activate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.deactivate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, renderer_classes=[XLSXRenderer])
    def report(self, request):
        xlsx = create_chart_report()
        file_name = 'chart-report'
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'session',
        'award',
        'group',
    ).prefetch_related(
        'contestants',
    ).order_by('id')
    serializer_class = ContestSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "contest"

    @action(methods=['post'], detail=True)
    def include(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.include(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def exclude(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.exclude(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'entry',
        'contest',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = ContestantSerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "contestant"

    @action(methods=['post'], detail=True)
    def include(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.include(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def exclude(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.exclude(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.select_related(
        'venue',
        'group',
    ).prefetch_related(
        'sessions',
        'assignments',
        'grantors',
    ).distinct().order_by('id')
    serializer_class = ConventionSerializer
    filter_class = ConventionFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "convention"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.activate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.deactivate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class CompetitorViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.select_related(
        'session',
        'group',
        'entry',
    ).prefetch_related(
        'appearances',
    ).order_by('id')
    serializer_class = CompetitorSerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "competitor"

    @action(methods=['post'], detail=True)
    def start(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.start(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def finish(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.finish(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def disqualify(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.disqualify(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def scratch(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.scratch(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, renderer_classes=[PDFRenderer])
    def csa(self, request, pk=None):
        competitor = Competitor.objects.get(pk=pk)
        panelists = Panelist.objects.filter(
            kind=Panelist.KIND.official,
            scores__song__appearance__competitor=competitor,
        ).distinct(
            'category',
            'person',
        ).order_by(
            'category',
            'person',
            'person__last_name',
        )
        appearances = competitor.appearances.order_by(
            'num',
        ).prefetch_related(
            'songs',
        )
        songs = Song.objects.select_related(
            'chart',
        ).filter(
            appearance__competitor=competitor,
        ).prefetch_related(
            'scores',
            'scores__panelist__person',
        ).order_by(
            'appearance__round__num',
            'num',
        )
        members = competitor.group.members.select_related(
            'person',
        ).filter(
            status=Member.STATUS.active,
        ).order_by('part')
        context = {
            'competitor': competitor,
            'panelists': panelists,
            'appearances': appearances,
            'songs': songs,
            'members': members,

        }
        rendered = render_to_string('csa.html', context)
        file = pydf.generate_pdf(rendered)
        content = ContentFile(file)
        pdf = content
        file_name = '{0}-ors'.format(
            slugify(
                "{0} {1} {2} CSA".format(
                    competitor.session.convention.name,
                    competitor.session.get_kind_display(),
                    competitor.group.name,
                )
            )
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.select_related(
        'session',
        'group',
        'competitor',
    ).prefetch_related(
        'contestants',
    ).order_by('id')
    serializer_class = EntrySerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "entry"

    @action(methods=['post'], detail=True)
    def build(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.build(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def invite(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.invite(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def withdraw(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.withdraw(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def submit(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.submit(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def approve(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.approve(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class GridViewSet(viewsets.ModelViewSet):
    queryset = Grid.objects.select_related(
        'round',
        'venue',
        'appearance',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = GridSerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "grid"


class GrantorViewSet(viewsets.ModelViewSet):
    queryset = Grantor.objects.select_related(
        'group',
        'convention',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = GrantorSerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "grantor"


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related(
        'parent',
    ).prefetch_related(
        'children',
        'awards',
        'competitors',
        'conventions',
        'entries',
        'members',
        'officers',
        'repertories',
    ).distinct()
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "group"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.activate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.deactivate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, renderer_classes=[XLSXRenderer])
    def roster(self, request, pk=None):
        group = Group.objects.get(pk=pk)
        xlsx = create_roster_report(group)
        file_name = '{0}-roster'.format(
            slugify(
                "{0}".format(
                    group.name,
                )
            )
        )
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related(
        'group',
        'person',
    ).order_by('id')
    serializer_class = MemberSerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "member"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.activate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.deactivate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.select_related(
    ).prefetch_related(
        'officers',
    ).order_by('id')
    serializer_class = OfficeSerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "office"


class OfficerViewSet(viewsets.ModelViewSet):
    queryset = Officer.objects.select_related(
        'office',
        'person',
        'group',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = OfficerSerializer
    filter_class = OfficerFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "officer"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.activate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.deactivate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class PanelistViewSet(viewsets.ModelViewSet):
    queryset = Panelist.objects.select_related(
        'round',
        'person',
    ).prefetch_related(
        'scores',
    ).order_by('id')
    serializer_class = PanelistSerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "panelist"


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.select_related(
        'user',
    ).prefetch_related(
        'assignments',
        'members',
        'officers',
        'panelists',
    ).order_by('id')
    serializer_class = PersonSerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "person"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.activate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.deactivate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class RepertoryViewSet(viewsets.ModelViewSet):
    queryset = Repertory.objects.select_related(
        'group',
        'chart',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = RepertorySerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "repertory"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.activate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.deactivate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.select_related(
        'session',
    ).prefetch_related(
        'appearances',
        'panelists',
        'grids',
    ).distinct().order_by('id')
    serializer_class = RoundSerializer
    filter_class = RoundFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "round"

    @action(methods=['post'], detail=True)
    def build(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.build(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def start(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.start(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def review(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.review(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def verify(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.verify(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def finish(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.finish(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


    @action(methods=['get'], detail=True, renderer_classes=[PDFRenderer])
    def announcements(self, request, pk=None):
        round = Round.objects.get(pk=pk)
        advancers = round.session.competitors.filter(
            status=Competitor.STATUS.started,
        ).order_by('draw')
        contests = round.session.contests.filter(
            status=Contest.STATUS.included,
            award__rounds__lte=round.num,
            award__level__in=[
                Award.LEVEL.championship,
                Award.LEVEL.award,
            ],
        ).order_by('award__tree_sort')
        competitors = round.session.competitors.filter(
            status=Competitor.STATUS.finished,
        ).select_related(
            'group',
        ).order_by(
            '-is_ranked',
            'tot_rank',
            '-tot_points',
        )[:5]
        context = {
            'round': round,
            'advancers': advancers,
            'contests': contests,
            'competitors': competitors,
        }
        rendered = render_to_string('announcements.html', context)
        file = pydf.generate_pdf(rendered)
        content = ContentFile(file)
        pdf = content
        file_name = '{0}-announcements'.format(
            slugify(
                "{0} {1} {2} Announcements".format(
                    round.session.convention.name,
                    round.session.get_kind_display(),
                    round.get_kind_display(),
                )
            )
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=True, renderer_classes=[PDFRenderer])
    def oss(self, request, pk=None):
        round = Round.objects.select_related(
            'session',
            'session__convention',
            'session__convention__venue',
        ).get(pk=pk)
        competitors = round.session.competitors.filter(
            status=Competitor.STATUS.finished,
            appearances__round=round,
        ).select_related(
            'group',
            'entry',
        ).prefetch_related(
            'entry__contestants',
            'entry__contestants__contest',
            'appearances',
            'appearances__round',
            'appearances__songs',
            'appearances__songs__chart',
            'appearances__songs__scores',
            'appearances__songs__scores__panelist',
            'appearances__songs__scores__panelist__person',
        ).order_by(
            '-is_ranked',
            'tot_rank',
            '-tot_points',
        )
        advancers = round.session.competitors.filter(
            status=Competitor.STATUS.started,
        ).select_related(
            'group',
        ).prefetch_related(
            'appearances',
            'appearances__songs',
            'appearances__songs__scores',
            'appearances__songs__scores__panelist',
            'appearances__songs__scores__panelist__person',
        ).order_by(
            'draw',
        )
        contests = round.session.contests.filter(
            status=Contest.STATUS.included,
            # award__rounds__lte=round.num,
            # award__level__in=[
            #     Award.LEVEL.championship,
            #     Award.LEVEL.award,
            # ],
        ).select_related(
            'award',
            'group',
        ).order_by('award__tree_sort')
        panelists = round.panelists.select_related(
            'person',
        ).filter(
            kind=Panelist.KIND.official,
            category__gte=Panelist.CATEGORY.ca,
        ).order_by(
            'category',
            'person__last_name',
            'person__first_name',
        )
        is_multi = bool(round.session.rounds.count() > 1)
        context = {
            'round': round,
            'competitors': competitors,
            'advancers': advancers,
            'panelists': panelists,
            'contests': contests,
            'is_multi': is_multi,
        }
        rendered = render_to_string('oss.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Letter',
            orientation='Portrait',
        )
        content = ContentFile(file)
        pdf = content
        file_name = '{0}-oss'.format(
            slugify(
                "{0} {1} {2} Round".format(
                    round.session.convention.name,
                    round.session.get_kind_display(),
                    round.get_kind_display(),
                )
            )
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


    @action(methods=['get'], detail=True, renderer_classes=[PDFRenderer])
    def sa(self, request, pk=None):
        round = Round.objects.get(pk=pk)
        panelists = Panelist.objects.filter(
            kind__in=[
                Panelist.KIND.official,
                Panelist.KIND.practice,
            ],
            scores__song__appearance__round=round,
        ).select_related(
            'person',
        ).distinct(
        ).order_by(
            'category',
            'person__last_name',
        )
        competitors = round.session.competitors.filter(
            status=Competitor.STATUS.finished,
        ).select_related(
            'group',
        ).prefetch_related(
            'appearances',
            'appearances__songs',
            'appearances__songs__scores',
            'appearances__songs__scores__panelist',
            'appearances__songs__scores__panelist__person',
        ).order_by(
            '-is_ranked',
            '-tot_points',
        )
        context = {
            'round': round,
            'panelists': panelists,
            'competitors': competitors,
        }
        rendered = render_to_string('sa.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Letter',
            orientation='Landscape',
        )
        content = ContentFile(file)
        pdf = content
        file_name = '{0}-sa'.format(
            slugify(
                "{0} {1} {2} Round".format(
                    round.session.convention.name,
                    round.session.get_kind_display(),
                    round.get_kind_display(),
                )
            )
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'song',
        'panelist',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = ScoreSerializer
    filter_class = ScoreFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "score"


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related(
        'convention',
    ).prefetch_related(
        'contests',
        'entries',
        'competitors',
        'rounds',
    ).distinct().order_by('id')
    serializer_class = SessionSerializer
    filter_class = SessionFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "session"

    @action(methods=['post'], detail=True)
    def build(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.build(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def open(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.open(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def close(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.close(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def verify(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.verify(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def start(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.start(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def finish(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.finish(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, renderer_classes=[XLSXRenderer])
    def legacy(self, request, pk=None):
        session = Session.objects.get(pk=pk)
        xlsx = create_legacy_report(session)
        file_name = '{0}-legacy'.format(
            slugify(
                "{0} {1} Session".format(
                    session.convention.name,
                    session.get_kind_display(),
                )
            )
        )
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=True, renderer_classes=[XLSXRenderer])
    def drcj(self, request, pk=None):
        session = Session.objects.get(pk=pk)
        xlsx = create_drcj_report(session)
        file_name = '{0}-drcj'.format(
            slugify(
                "{0} {1} Session".format(
                    session.convention.name,
                    session.get_kind_display(),
                )
            )
        )
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=True, renderer_classes=[XLSXRenderer])
    def contact(self, request, pk=None):
        session = Session.objects.get(pk=pk)
        xlsx = create_contact_report(session)
        file_name = '{0}-contact'.format(
            slugify(
                "{0} {1} Session".format(
                    session.convention.name,
                    session.get_kind_display(),
                )
            )
        )
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=True, renderer_classes=[PDFRenderer])
    def oss(self, request, pk=None):
        session = Session.objects.get(pk=pk)
        competitors = session.competitors.filter(
            status=Competitor.STATUS.finished,
        ).select_related(
            'group',
        ).prefetch_related(
            'appearances',
            'appearances__songs',
            'appearances__songs__scores',
            'appearances__songs__scores__panelist',
            'appearances__songs__scores__panelist__person',
        ).order_by(
            '-is_ranked',
            'tot_rank',
            '-tot_points',
        )
        advancers = session.competitors.filter(
            status=Competitor.STATUS.started,
        ).select_related(
            'group',
        ).prefetch_related(
            'appearances',
            'appearances__songs',
            'appearances__songs__scores',
            'appearances__songs__scores__panelist',
            'appearances__songs__scores__panelist__person',
        ).order_by(
            'draw',
        )
        current = session.rounds.filter(
            status=Round.STATUS.finished,
        ).order_by('num').last().num
        contests = session.contests.filter(
            status=Contest.STATUS.included,
            award__rounds__lte=current,
            award__level__in=[
                Award.LEVEL.championship,
                Award.LEVEL.award,
            ],
        ).select_related(
            'award',
        ).order_by('award__tree_sort')
        panelists = Panelist.objects.filter(
            kind=Panelist.KIND.official,
            round__session=session,
        ).distinct(
            'category',
            'person__last_name',
            'person__first_name',
        ).order_by(
            'category',
            'person__last_name',
            'person__first_name',
        )
        context = {
            'session': session,
            'competitors': competitors,
            'advancers': advancers,
            'panelists': panelists,
            'contests': contests,
        }
        rendered = render_to_string('oss.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Letter',
            orientation='Portrait',
        )
        content = ContentFile(file)
        pdf = content
        file_name = '{0}-oss'.format(
            slugify(
                "{0} {1} Session".format(
                    session.convention.name,
                    session.get_kind_display(),
                )
            )
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


    @action(methods=['get'], detail=True, renderer_classes=[PDFRenderer])
    def sa(self, request, pk=None):
        session = Session.objects.get(pk=pk)
        panelists = Panelist.objects.filter(
            kind__in=[
                Panelist.KIND.official,
                Panelist.KIND.practice,
            ],
            scores__song__appearance__round__session=session,
        ).select_related(
            'person',
        ).distinct(
        ).order_by(
            'category',
            'person__last_name',
        )
        competitors = session.competitors.filter(
            status=Competitor.STATUS.finished,
        ).select_related(
            'group',
        ).prefetch_related(
            'appearances',
            'appearances__songs',
            'appearances__songs__scores',
            'appearances__songs__scores__panelist',
            'appearances__songs__scores__panelist__person',
        ).order_by(
            '-is_ranked',
            '-tot_points',
        )
        context = {
            'session': session,
            'panelists': panelists,
            'competitors': competitors,
        }
        rendered = render_to_string('sa.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Letter',
            orientation='Landscape',
        )
        content = ContentFile(file)
        pdf = content
        file_name = '{0}-sa'.format(
            slugify(
                "{0} {1} Session".format(
                    session.convention.name,
                    session.get_kind_display(),
                )
            )
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.select_related(
        'appearance',
        'chart',
    ).prefetch_related(
        'scores',
    ).order_by('id')
    serializer_class = SongSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "song"


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.select_related(
    ).prefetch_related(
        'conventions',
        'grids',
    ).order_by('name')
    serializer_class = VenueSerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "venue"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related(
        # 'person',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = UserSerializer
    filter_class = UserFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "user"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.activate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.deactivate(by=self.request.user)
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class StateLogViewSet(viewsets.ModelViewSet):
    queryset = StateLog.objects.select_related(
        'content_type',
        'by',
    ).prefetch_related(
    )
    serializer_class = StateLogSerializer
    filter_class = StateLogFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    resource_name = "statelog"
