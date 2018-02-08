# Standard Libary
import uuid

# Third-Party
from cloudinary.models import CloudinaryField
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.db import models
from django.utils.html import format_html
from django.utils.timezone import now

# First-Party
from api.tasks import create_variance_report


class Appearance(TimeStampedModel):
    """
    An appearance of a competitor on stage.

    The Appearance is meant to be a private resource.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (2, 'published', 'Published',),
        (5, 'verified', 'Verified',),
        (10, 'started', 'Started',),
        (20, 'finished', 'Finished',),
        (30, 'confirmed', 'Confirmed',),
        (40, 'flagged', 'Flagged',),
        (50, 'scratched', 'Scratched',),
        (60, 'cleared', 'Cleared',),
        (90, 'announced', 'Announced',),
        (95, 'archived', 'Archived',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    num = models.IntegerField(
        null=True,
        blank=True,
    )

    draw = models.IntegerField(
        null=True,
        blank=True,
    )

    actual_start = models.DateTimeField(
        help_text="""
            The actual appearance window.""",
        null=True,
        blank=True,
    )

    actual_finish = models.DateTimeField(
        help_text="""
            The actual appearance window.""",
        null=True,
        blank=True,
    )

    variance_report = CloudinaryField(
        null=True,
        blank=True,
        editable=False,
    )

    # Privates
    rank = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    per_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    tot_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    per_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    tot_score = models.FloatField(
        null=True,
        blank=True,
    )

    # Appearance FKs
    round = models.ForeignKey(
        'Round',
        related_name='appearances',
        on_delete=models.CASCADE,
    )

    competitor = models.ForeignKey(
        'Competitor',
        related_name='appearances',
        on_delete=models.CASCADE,
    )

    # Appearance Internals
    class JSONAPIMeta:
        resource_name = "appearance"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = "{0} {1}".format(
            self.round,
            self.competitor.group.nomen,
        )
        super().save(*args, **kwargs)

    def variance_report_link(self):
        if self.variance_report:
            return format_html(
                '<a href="{0}">File Link</a>',
                self.variance_report.url,
            )
        else:
            return None

    # Methods
    def calculate(self):
        self.mus_points = self.songs.filter(
            scores__kind=10,
            scores__category=30,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']
        self.per_points = self.songs.filter(
            scores__kind=10,
            scores__category=40,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']
        self.sng_points = self.songs.filter(
            scores__kind=10,
            scores__category=50,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

        self.tot_points = self.songs.filter(
            scores__kind=10,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']
        self.mus_score = self.songs.filter(
            scores__kind=10,
            scores__category=30,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']
        self.per_score = self.songs.filter(
            scores__kind=10,
            scores__category=40,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']
        self.sng_score = self.songs.filter(
            scores__kind=10,
            scores__category=50,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']
        self.tot_score = self.songs.filter(
            scores__kind=10,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    # Appearance Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return request.user.is_scoring_manager

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        assi = bool(self.competitor.session.convention.assignments.filter(
            person__user=request.user,
            status__gt=0,
        ))
        return assi

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return request.user.is_scoring_manager

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        assi = bool(self.competitor.session.convention.assignments.filter(
            person__user=request.user,
            status__gt=0,
        ))
        return assi

    # Transitions
    @fsm_log_by
    @transition(field=status, source=[STATUS.new], target=STATUS.started)
    def start(self, *args, **kwargs):
        self.actual_start = now()
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.started], target=STATUS.finished)
    def finish(self, *args, **kwargs):
        self.actual_finish = now()
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.finished, STATUS.confirmed], target=STATUS.confirmed)
    def confirm(self, *args, **kwargs):
        for song in self.songs.all():
            song.calculate()
            variance = song.check_variance()
            if variance:
                create_variance_report(self)
                return
        self.variance_report = None
        self.calculate()
        return

    # @fsm_log_by
    # @transition(field=status, source=[STATUS.], target=STATUS.announced)
    # def announce(self, *args, **kwargs):
    #     return