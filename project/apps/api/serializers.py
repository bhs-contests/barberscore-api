from rest_framework_json_api import serializers

import six
import pytz

from django.core.exceptions import (
    ValidationError,
)

from drf_haystack.serializers import (
    HaystackSerializerMixin,
)

from drf_extra_fields.fields import (
    DateTimeRangeField,
    DateRangeField,
)

from .models import (
    Award,
    Chapter,
    Contest,
    Contestant,
    Convention,
    Group,
    Judge,
    Organization,
    Performance,
    Performer,
    Person,
    Round,
    Score,
    Session,
    Setlist,
    Role,
    Song,
    Venue,
)


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')


class AwardSerializer(serializers.ModelSerializer):
    # organization = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Award
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'organization',
        )


class ChapterSerializer(serializers.ModelSerializer):
    # organization = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Chapter
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'organization',
        )


class ContestSerializer(serializers.ModelSerializer):
    # session = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )
    # performances = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Contest
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            # 'champion',
            'contestants',
            'award',
            'session',
            # 'parent',
            # 'children',
        )


class ContestantSerializer(serializers.ModelSerializer):
    # performer = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Contestant
        fields = (
            'id',
            'url',
            'name',
            'slug',
            'status',
            'rank',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'performer',
            'contest',
        )


class ConventionSerializer(serializers.ModelSerializer):
    # organization = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # sessions = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )
    date = DateRangeField()

    class Meta:
        model = Convention
        fields = (
            'id',
            'url',
            'name',
            'slug',
            'status',
            'season',
            'level',
            'division',
            'date',
            'venue',
            'year',
            'organization',
            'drcj',
            'sessions',
            'human_date',
        )
        # lookup_field = 'slug'


class GroupSerializer(serializers.ModelSerializer):

    # performers = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Group
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'kind',
            'chapter',
            'organization',
            'performers',
        )
        read_only_fields = [
            'picture',
        ]


class GroupSearchSerializer(HaystackSerializerMixin, GroupSerializer):
    class Meta(GroupSerializer.Meta):
        search_fields = [
            "text",
            "name",
        ]


class JudgeSerializer(serializers.ModelSerializer):
    # scores = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )
    # session = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )
    # person = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Judge
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'person',
            'category',
            'designation',
            'kind',
            'slot',
            'status',
            'session',
            'scores',
        )


class OrganizationSerializer(serializers.ModelSerializer):
    # children = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )
    # parent = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Organization
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            # 'kind',
            'long_name',
            'parent',
            'children',
            # 'performers',
        )
        read_only_fields = [
            'picture',
        ]


class PerformanceSerializer(serializers.ModelSerializer):
    # performer = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # round = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # songs = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # start_dt = serializers.Field()

    scheduled = DateTimeRangeField()
    actual = DateTimeRangeField()

    class Meta:
        model = Performance
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'slot',
            'start_dt',
            'scheduled',
            'actual',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'round',
            'performer',
            'songs',
        )


class PerformerSerializer(serializers.ModelSerializer):
    # session = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # organization = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # performances = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Performer
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'organization',
            'picture',
            'seed',
            'prelim',
            'rank',
            'men',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'delta_score',
            'delta_place',
            'session',
            'group',
            'performances',
            'roles',
            'contestants',
        )
        read_only_fields = [
            'picture',
        ]


class PersonSerializer(serializers.ModelSerializer):
    # catalogs = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # choruses = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )
    # quartets = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # sessions = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Person
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            # 'kind',
            # 'catalogs',
            'roles',
            'panels',
            'conventions',
        )
        read_only_fields = [
            'picture',
        ]


class PersonSearchSerializer(HaystackSerializerMixin, GroupSerializer):
    class Meta(PersonSerializer.Meta):
        search_fields = [
            "text",
            "name",
        ]


class RoundSerializer(serializers.ModelSerializer):
    # session = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )
    # performances = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Round
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'kind',
            'session',
            'performances',
        )


class ScoreSerializer(serializers.ModelSerializer):
    # song = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # judge = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Score
        fields = [
            'id',
            'url',
            'slug',
            'name',
            'song',
            'judge',
            'points',
            'status',
            'kind',
        ]


class SessionSerializer(serializers.ModelSerializer):
    # convention = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # rounds = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # judges = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # performers = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Session
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'kind',
            'convention',
            'administrator',
            'aca',
            'rounds',
            'performers',
            'contests',
            'judges',
        )


class SetlistSerializer(serializers.ModelSerializer):
    # convention = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # rounds = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # judges = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # performers = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Setlist
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'chart',
            'performer',
        )


class RoleSerializer(serializers.ModelSerializer):
    # performer = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )
    # person = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Role
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'performer',
            'person',
            'part',
        )


class SongSerializer(serializers.ModelSerializer):
    # chart = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # catalog = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # performance = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # scores = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Song
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'order',
            'title',
            'status',
            'is_parody',
            'chart',
            'performance',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'scores',
        )


class VenueSerializer(serializers.ModelSerializer):
    # catalogs = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # songs = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )
    timezone = TimezoneField()

    class Meta:
        model = Venue
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'timezone',
            'conventions',
        )
