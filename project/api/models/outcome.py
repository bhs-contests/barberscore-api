
# Standard Library
import logging
import uuid

# Third-Party
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum, Q, Avg, F

log = logging.getLogger(__name__)


class Outcome(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    num = models.IntegerField(
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )

    legacy_num = models.IntegerField(
        blank=True,
        null=True,
    )

    legacy_name = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )

    # FKs
    round = models.ForeignKey(
        'Round',
        related_name='outcomes',
        on_delete=models.CASCADE,
    )

    award = models.ForeignKey(
        'cmanager.award',
        related_name='outcomes',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='outcomes',
    )

    # Methods
    def get_name(self):
        Group = apps.get_model('bhs.group')
        Panelist = apps.get_model('api.panelist')
        if self.round.kind != self.round.KIND.finals and not self.award.is_single:
            return "(Result determined in Finals)"
        if self.award.level == self.award.LEVEL.deferred:
            return "(Result determined post-contest)"
        if self.award.level in [self.award.LEVEL.manual, self.award.LEVEL.raw, self.award.LEVEL.standard]:
            return "MUST ENTER WINNER MANUALLY"
        # if self.award.level == self.award.LEVEL.raw:
        #     group_ids = Group.objects.filter(
        #         appearances__contenders__outcome=self,
        #     ).values_list('id', flat=True)
        #     group = Group.objects.filter(
        #         id__in=group_ids,
        #     ).annotate(
        #         avg=Avg(
        #             'appearances__songs__scores__points',
        #             filter=Q(
        #                 appearances__round__session=self.round.session,
        #                 appearances__songs__scores__panelist__kind=Panelist.KIND.official,
        #             ),
        #         ),
        #         base=Avg(
        #             'appearances__base',
        #             filter=Q(
        #                 appearances__round__session=self.round.session,
        #             ),
        #         ),
        #         diff=F('avg') - F('base'),
        #         sng=Sum(
        #             'appearances__songs__scores__points',
        #             filter=Q(
        #                 appearances__songs__scores__panelist__kind=Panelist.KIND.official,
        #                 appearances__songs__scores__panelist__category=Panelist.CATEGORY.singing
        #             ),
        #         ),
        #         per=Sum(
        #             'appearances__songs__scores__points',
        #             filter=Q(
        #                 appearances__songs__scores__panelist__kind=Panelist.KIND.official,
        #                 appearances__songs__scores__panelist__category=Panelist.CATEGORY.performance
        #             ),
        #         ),
        #     ).filter(
        #         diff__gt=0,
        #     ).order_by(
        #        '-diff',
        #     ).first()
        #     try:
        #         winner = group.name
        #     except AttributeError:
        #         winner = "(No Award Winner)"
        #     return winner
        # if self.award.level == self.award.LEVEL.standard:
        #     group_ids = Group.objects.filter(
        #         appearances__contenders__outcome=self,
        #     ).values_list('id', flat=True)
        #     groups = Group.objects.filter(
        #         id__in=group_ids,
        #     ).annotate(
        #         score=Avg(
        #             'appearances__songs__scores__points',
        #             filter=Q(
        #                 appearances__round__session=self.round.session,
        #                 appearances__songs__scores__panelist__kind=Panelist.KIND.official,
        #             ),
        #         ),
        #         base=Avg(
        #             'appearances__base',
        #             filter=Q(
        #                 appearances__round__session=self.round.session,
        #             ),
        #         ),
        #     )
        #     totals = groups.aggregate(
        #         Avg('score'),
        #         Avg('base'),
        #     )
        #     winner = groups.annotate(
        #         score_ratio=F('score') / totals['score__avg'],
        #         base_ratio=F('base') / totals['base__avg'],
        #         diff=F('score_ratio') - F('base_ratio'),
        #     ).order_by(
        #         '-diff',
        #     ).first().name
        if self.award.level == self.award.LEVEL.qualifier:
            threshold = self.award.threshold
            group_ids = Group.objects.filter(
                appearances__contenders__outcome=self,
            ).values_list('id', flat=True)
            qualifiers = Group.objects.filter(
                id__in=group_ids,
            ).annotate(
                avg=Avg(
                    'appearances__songs__scores__points',
                    filter=Q(
                        appearances__round__session=self.round.session,
                        appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    ),
                ),
            ).filter(
                avg__gte=threshold,
            ).order_by(
                'name',
            ).values_list('name', flat=True)
            if qualifiers:
                return ", ".join(qualifiers)
            return "(No Qualifiers)"
        if self.award.level in [self.award.LEVEL.championship, self.award.LEVEL.representative]:
            winner = Group.objects.filter(
                appearances__contenders__outcome=self,
            ).annotate(
                tot=Sum(
                    'appearances__songs__scores__points',
                    filter=Q(
                        appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    ),
                ),
                sng=Sum(
                    'appearances__songs__scores__points',
                    filter=Q(
                        appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                        appearances__songs__scores__panelist__category=Panelist.CATEGORY.singing
                    ),
                ),
                per=Sum(
                    'appearances__songs__scores__points',
                    filter=Q(
                        appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                        appearances__songs__scores__panelist__category=Panelist.CATEGORY.performance
                    ),
                ),
            ).earliest(
                '-tot',
                '-sng',
                '-per',
            )
            if winner:
                return str(winner.name)
            return "(No Recipient)"
        raise RuntimeError("Level mismatch")

    # Internals
    class Meta:
        unique_together = (
            ('round', 'award',),
            ('round', 'num',),
        )

    class JSONAPIMeta:
        resource_name = "outcome"

    def __str__(self):
        return str(self.id)

    def clean(self):
        pass

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return any([
            self.round.status == self.round.STATUS.published,
            self.round.session.convention.assignments.filter(
                person__user=request.user,
                status__gt=0,
                category__lte=10,
            ),
        ])


    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_round_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.round.session.convention.assignments.filter(
                    person__user=request.user,
                    status__gt=0,
                    category__lte=10,
                ),
                self.round.status < self.round.STATUS.verified,
            ]),
        ])
