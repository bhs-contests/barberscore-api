from __future__ import division

from django.core.exceptions import ValidationError

from django.utils import timezone

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import (
    RegexValidator,
)


class Contestant(models.Model):
    """
    Contestants.

    This class represents a particular contestant.  Historical information
    is not maintained.
    """

    QUARTET = 1
    CHORUS = 2

    CONTESTANT_CHOICES = (
        (QUARTET, "Quartet"),
        (CHORUS, "Chorus"),
    )

    contestant_type = models.IntegerField(
        help_text="""
            The type of contestant, either chorus or quartet.""",
        choices=CONTESTANT_CHOICES,
        default=QUARTET,
    )

    name = models.CharField(
        help_text="""
            The name of the contestant.""",
        max_length=200,
    )

    slug = models.SlugField(
        help_text="""
            The slug, generated in a signal from the name field.""",
        max_length=200,
        unique=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the contestant.""",
        max_length=200,
        blank=True,
    )

    website = models.URLField(
        help_text="""
            The website URL of the contestant.""",
        blank=True,
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the contestant.""",
        blank=True,
    )

    twitter = models.CharField(
        help_text="""
            The twitter handle (in form @twitter_handle) of the contestant.""",
        blank=True,
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'@([A-Za-z0-9_]+)',
                message="""
                    Must be a single Twitter handle
                    in the form `@twitter_handle`.
                """,
            ),
        ],
    )

    email = models.EmailField(
        help_text="""
            The contact email of the contestant.""",
        blank=True,
    )

    phone = models.CharField(
        help_text="""
            The contact phone number of the contestant.""",
        max_length=20,
        blank=True,
    )

    director = models.CharField(
        help_text="""
            The name of the director(s) of the chorus.""",
        max_length=200,
        blank=True,
    )

    lead = models.CharField(
        help_text="""
            The name of the quartet lead.""",
        max_length=50,
        blank=True,
    )

    tenor = models.CharField(
        help_text="""
            The name of the quartet tenor.""",
        max_length=50,
        blank=True,
    )

    baritone = models.CharField(
        help_text="""
            The name of the quartet baritone.""",
        max_length=50,
        blank=True,
    )

    bass = models.CharField(
        help_text="""
            The name of the quartet bass.""",
        max_length=50,
        blank=True,
    )

    district = models.CharField(
        help_text="""
            The abbreviation of the district the
            contestant is representing.""",
        max_length=50,
        blank=True,
    )

    prelim = models.FloatField(
        help_text="""
            The prelim score of the contestant.""",
        null=True,
        blank=True,
    )

    picture = models.ImageField(
        help_text="""
            The 'official' picture of the contestant.""",
        blank=True,
        null=True,
    )

    blurb = models.TextField(
        help_text="""
            A blurb describing the contestant.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    @property
    def next_performance(self):
        return self.performances.order_by('stagetime').first()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contestant', args=[str(self.slug)])

    class Meta:
        ordering = ['contestant_type', 'name']


class Contest(models.Model):
    """
    Contests.

    This class represents a particular contest.
    """

    QUARTET = 1
    CHORUS = 2
    COLLEGIATE = 3
    SENIOR = 4

    CONTEST_TYPE_CHOICES = (
        (QUARTET, 'Quartet'),
        (CHORUS, 'Chorus'),
        (COLLEGIATE, 'Collegiate'),
        (SENIOR, 'Senior'),
    )

    contest_type = models.IntegerField(
        help_text="""
            The contest type:  Quartet, Chorus, Collegiate or Senior.""",
        choices=CONTEST_TYPE_CHOICES,
        default=QUARTET,
    )

    INTERNATIONAL = 1
    DISTRICT = 2
    DIVISION = 3

    CONTEST_LEVEL_CHOICES = (
        (INTERNATIONAL, 'International'),
        # (DISTRICT, 'District'),
        # (DIVISION, 'Division'),
    )

    contest_level = models.IntegerField(
        help_text="""
            The contest level:  International, District, etc..
            Currently only International is supported.""",
        choices=CONTEST_LEVEL_CHOICES,
        default=INTERNATIONAL,
    )

    year = models.CharField(
        help_text="""
            The year of the contest, as a Char.""",
        default='2014',
        max_length=4,
    )

    slug = models.SlugField(
        help_text="""
            The slug of the contest type.""",
        max_length=200,
        unique=True,
    )

    def __unicode__(self):
        return '{0} {1} {2}'.format(
            self.year,
            self.get_contest_level_display(),
            self.get_contest_type_display(),
        )

    class Meta:
        ordering = (
            '-year',
            'contest_level',
            'contest_type',
        )


class Performance(models.Model):
    """
    Performances.

    This class represents the join of a contestant and a contest.
    Each performance consists of two songs in a contest round.  Rounds
    are only applicable to the quartet contest in the context, but the
    field is included for data architecture consistency.
    """

    QUARTERS = 1
    SEMIS = 2
    FINALS = 3

    CONTEST_ROUND_CHOICES = (
        (QUARTERS, 'Quarter-Finals'),
        (SEMIS, 'Semi-Finals'),
        (FINALS, 'Finals'),
    )

    ONE = 1
    TWO = 2

    SESSION_CHOICES = (
        (ONE, "Session #1"),
        (TWO, "Session #2"),
    )

    contest = models.ForeignKey(
        Contest,
        help_text="""
            The contest for this particular performance.""",
        related_name='performances',
    )

    contestant = models.ForeignKey(
        Contestant,
        help_text="""
            The contestant for this particular performance.""",
        related_name='performances',
    )

    contest_round = models.IntegerField(
        help_text="""
            The performance contest round.""",
        choices=CONTEST_ROUND_CHOICES,
        default=FINALS,
    )

    appearance = models.IntegerField(
        help_text="""
            The appearance order, within a given round.""",
    )

    stagetime = models.DateTimeField(
        help_text="""
            The approximate stagetime of the performance, in
            the local time of the venue.  NOTE: for usage purposes,
            the default is the current time.  However, this must
            eventually be overwritten with the actual stagetime.""",
        default=timezone.now,
    )

    session = models.IntegerField(
        help_text="""
            The session number.""",
        default=ONE,
        choices=SESSION_CHOICES,
    )

    song1 = models.CharField(
        help_text="""
            The title of the first song of the performance.""",
        blank=True,
        max_length=200,
    )

    mus1 = models.IntegerField(
        help_text="""
            The raw music score of the first song.""",
        blank=True,
        null=True,
    )

    prs1 = models.IntegerField(
        help_text="""
            The raw presentation score of the first song.""",
        blank=True,
        null=True,
    )

    sng1 = models.IntegerField(
        help_text="""
            The raw singing score of the first song.""",
        blank=True,
        null=True,
    )

    song2 = models.CharField(
        help_text="""
            The title of the second song of the performance.""",
        blank=True,
        max_length=200,
    )

    mus2 = models.IntegerField(
        help_text="""
            The raw music score of the second song.""",
        blank=True,
        null=True,
    )

    prs2 = models.IntegerField(
        help_text="""
            The raw presentation score of the second song.""",
        blank=True,
        null=True,
    )

    sng2 = models.IntegerField(
        help_text="""
            The raw singing score of the second song.""",
        blank=True,
        null=True,
    )

    men_on_stage = models.IntegerField(
        help_text="""
            The number of men on stage (relevant for chorus only.)""",
        blank=True,
        null=True,
    )

    # DENORMALIZED VALUES
    # The following values are denormalized, and the default population
    # happens via pre-save signals.  This allows for manual correction
    # as needed.
    song1_score = models.FloatField(
        help_text="""
            The percentile score of the first song.""",
        blank=True,
        null=True,
    )

    song2_score = models.FloatField(
        help_text="""
            The percentile score of the second song.""",
        blank=True,
        null=True,
    )

    performance_score = models.FloatField(
        help_text="""
            The percentile score of the performance (both songs).""",
        blank=True,
        null=True,
    )

    total_score = models.FloatField(
        help_text="""
            The running percentile score of performances to date
            by this particular contestant.""",
        blank=True,
        null=True,
    )

    place = models.IntegerField(
        help_text="""
            The ordinal placement of the contestant in this
            particular contest.""",
        blank=True,
        null=True,
    )

    def clean(self):
        """
        Multi-field (ie, model) validation.
        """
        if self.contest.contest_type != Contest.QUARTET and self.contest_round != self.FINALS:
            raise ValidationError(
                """Only Quartets have Quarter- and Semi-Final Rounds."""
            )
        if (self.contest.contest_type != Contest.CHORUS and self.contestant.contestant_type == Contestant.CHORUS) or (self.contest.contest_type == Contest.CHORUS and self.contestant.contestant_type != Contestant.CHORUS):
            raise ValidationError(
                    """Contestant and Contest mismatch: {contestant_type} != {contest_type}""".format(
                        contestant_type=self.contestant.get_contestant_type_display(),
                        contest_type=self.contest.get_contest_type_display(),
                    ),
                code='type_mismatch',
                params={
                    'contestant_type': self.contestant.get_contestant_type_display(),
                    'contest_type': self.contest.get_contest_type_display(),
                }
            )

    def __unicode__(self):
        return '{0}, {1}'.format(
            self.contestant,
            self.get_contest_round_display(),
        )

    class Meta:
        ordering = (
            'contest',
            'contest_round',
            'appearance',
        )
        unique_together = (
            'contest',
            'contest_round',
            'appearance',
        )
