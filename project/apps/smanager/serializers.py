
# Third-Party
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

# Local
from .fields import TimezoneField

from .models import Contest
from .models import Contestant
from .models import Entry
from .models import Session



class ContestSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'contestants': 'apps.smanager.serializers.ContestantSerializer',
    }

    class Meta:
        model = Contest
        fields = (
            'id',
            'url',
            'status',
            'result',
            'group',
            'session',
            'award',
            'contestants',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            # 'contestants',
        ]


class ContestantSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Contestant
        fields = (
            'id',
            'url',
            'status',
            'entry',
            'contest',
            'permissions',
        )


class EntrySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    statelogs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    included_serializers = {
        'contestants': 'apps.smanager.serializers.ContestantSerializer',
        # 'statelogs': 'django_fsm_log.serializers.StateLogSerializer',
        'group': 'apps.bhs.serializers.GroupSerializer',
    }

    class Meta:
        model = Entry
        fields = (
            'id',
            'url',
            'status',
            'is_evaluation',
            'is_private',
            'is_mt',
            'draw',
            'seed',
            'prelim',
            'participants',
            'pos',
            'representing',
            'description',
            'notes',
            'session',
            'group',
            'contestants',
            'permissions',
            'statelogs',
        )

    class JSONAPIMeta:
        included_resources = [
            # 'appearances',
            'contestants',
        ]

    def validate(self, data):
        """Check that the start is before the stop."""
        # if data['is_private'] and data['contestants']:
        #     raise serializers.ValidationError("Can not be private and compete for an award.")
        return data


class SessionSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    included_serializers = {
        'contests': 'apps.smanager.serializers.ContestSerializer',
        'entries': 'apps.smanager.serializers.EntrySerializer',
        # 'rounds': 'api.serializers.RoundSerializer',
    }

    class Meta:
        model = Session
        fields = (
            'id',
            'url',
            'status',
            'kind',
            'is_invitational',
            'footnotes',
            'description',
            'notes',
            'legacy_report',
            'drcj_report',
            'num_rounds',
            'convention',
            'contests',
            'entries',
            'rounds',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            'contests',
            'entries',
            # 'rounds',
        ]
