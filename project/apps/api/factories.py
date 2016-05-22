from factory.django import (
    DjangoModelFactory,
)

from factory import (
    SubFactory,
    PostGenerationMethodCall,
)

from datetime import datetime

from psycopg2.extras import DateTimeTZRange

from apps.api.models import (
    Award,
    Certification,
    Chapter,
    Chart,
    Contest,
    Contestant,
    Convention,
    Group,
    Judge,
    Member,
    Organization,
    Performance,
    Performer,
    Person,
    Role,
    Round,
    Score,
    Session,
    Song,
    Submission,
    User,
    Venue,
)


# Users
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User


class AdminFactory(UserFactory):
    email = 'admin@barberscore.com'
    password = PostGenerationMethodCall('set_password', 'password')
    name = 'Admin User'
    is_staff = True


class PublicFactory(UserFactory):
    email = 'user@barberscore.com'
    password = PostGenerationMethodCall('set_password', 'password')
    name = 'Public User'


# Awards
class AwardFactory(DjangoModelFactory):
    class Meta:
        model = Award
    status = Award.STATUS.active


class InternationalQuartetAward(AwardFactory):
    kind = Award.KIND.quartet
    championship_season = Award.SEASON.international
    championship_rounds = 3
    is_primary = True
    is_qualification_required = True
    qualifier_season = Award.SEASON.spring
    qualifier_rounds = 2
    threshold = 76
    minimum = 70
    advance = 73
    organization = SubFactory(
        'apps.api.factories.InternationalFactory'
    )


class InternationalChorusAward(AwardFactory):
    kind = Award.KIND.chorus
    championship_season = Award.SEASON.international
    championship_rounds = 1
    is_primary = True
    is_qualification_required = True
    qualifier_season = Award.SEASON.fall
    qualifier_rounds = 1
    organization = SubFactory(
        'apps.api.factories.InternationalFactory'
    )


class InternationalSeniorsAward(AwardFactory):
    kind = Award.KIND.seniors
    championship_season = Award.SEASON.midwinter
    championship_rounds = 1
    is_primary = True
    is_qualification_required = True
    qualifier_season = Award.SEASON.spring
    qualifier_rounds = 1
    organization = SubFactory(
        'apps.api.factories.InternationalFactory'
    )


class InternationalYouthAward(AwardFactory):
    kind = Award.KIND.youth
    championship_season = Award.SEASON.international
    championship_rounds = 1
    is_primary = True
    is_qualification_required = True
    qualifier_season = Award.SEASON.spring
    qualifier_rounds = 1
    threshold = 73
    minimum = 61
    advance = 70
    organization = SubFactory(
        'apps.api.factories.InternationalFactory'
    )


class DistrictQuartetAward(AwardFactory):
    kind = Award.KIND.quartet
    championship_season = Award.SEASON.fall
    championship_rounds = 2
    is_primary = True
    # is_qualification_required = True
    # qualifier_season = Award.SEASON.spring
    # qualifier_rounds = 2
    # threshold = 76
    # minimum = 70
    # advance = 73
    organization = SubFactory(
        'apps.api.factories.DistrictFactory'
    )


class DistrictChorusAward(AwardFactory):
    kind = Award.KIND.chorus
    championship_season = Award.SEASON.spring
    championship_rounds = 1
    is_primary = True
    # is_qualification_required = True
    # qualifier_season = Award.SEASON.fall
    # qualifier_rounds = 1
    organization = SubFactory(
        'apps.api.factories.DistrictFactory'
    )


class DistrictSeniorsAward(AwardFactory):
    kind = Award.KIND.seniors
    championship_season = Award.SEASON.fall
    championship_rounds = 1
    is_primary = True
    # is_qualification_required = True
    # qualifier_season = Award.SEASON.spring
    # qualifier_rounds = 1
    organization = SubFactory(
        'apps.api.factories.DistrictFactory'
    )


class DistrictYouthAward(AwardFactory):
    kind = Award.KIND.youth
    championship_season = Award.SEASON.fall
    championship_rounds = 1
    is_primary = True
    # is_qualification_required = True
    # qualifier_season = Award.SEASON.spring
    # qualifier_rounds = 1d
    # threshold = 73
    # minimum = 61
    # advance = 70
    organization = SubFactory(
        'apps.api.factories.DistrictFactory'
    )


class DivisionQuartetAward(AwardFactory):
    kind = Award.KIND.quartet
    championship_season = Award.SEASON.spring
    championship_rounds = 2
    is_primary = True
    is_qualification_required = False
    organization = SubFactory(
        'apps.api.factories.DivisionFactory'
    )


class DivisionChorusAward(AwardFactory):
    kind = Award.KIND.chorus
    championship_season = Award.SEASON.spring
    championship_rounds = 1
    is_primary = True
    is_qualification_required = False
    organization = SubFactory(
        'apps.api.factories.DivisionFactory'
    )


class DivisionSeniorsAward(AwardFactory):
    kind = Award.KIND.seniors
    championship_season = Award.SEASON.spring
    championship_rounds = 1
    is_primary = True
    is_qualification_required = False
    organization = SubFactory(
        'apps.api.factories.DivisionFactory'
    )


class DivisionYouthAward(AwardFactory):
    kind = Award.KIND.youth
    championship_season = Award.SEASON.spring
    championship_rounds = 1
    is_primary = True
    is_qualification_required = False
    organization = SubFactory(
        'apps.api.factories.DivisionFactory'
    )


# Chapters
class ChapterFactory(DjangoModelFactory):
    class Meta:
        model = Chapter
    status = Chapter.STATUS.active
    code = 'Z-999'


class DistrictChapterFactory(ChapterFactory):
    name = 'Test District Chapter'
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


class AffiliateChapterFactory(ChapterFactory):
    name = 'Test Affiliate Chapter'
    organization = SubFactory(
        'apps.api.factories.AffiliateFactory',
    )


# Charts
class ChartFactory(DjangoModelFactory):
    class Meta:
        model = Chart

    title = 'The Old Songs'


# Groups
class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    status = Group.STATUS.active

    name = 'Test Quartet'
    kind = Group.KIND.quartet
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


class QuartetFactory(DjangoModelFactory):
    class Meta:
        model = Group

    status = Group.STATUS.active

    name = 'Test Quartet'
    kind = Group.KIND.quartet
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


class ChorusFactory(DjangoModelFactory):
    class Meta:
        model = Group

    status = Group.STATUS.active

    name = 'Test Chorus'
    kind = Group.KIND.chorus
    chapter = SubFactory(
        'apps.api.factories.ChapterFactory'
    )
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


# Organizations
class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    status = Organization.STATUS.active


class InternationalFactory(OrganizationFactory):
    level = Organization.LEVEL.international
    kind = Organization.KIND.international
    name = 'Test Interational'
    short_name = 'TI'
    long_name = 'International'
    parent = None


class DistrictFactory(OrganizationFactory):
    level = Organization.LEVEL.district
    kind = Organization.KIND.district
    name = 'Test District'
    short_name = 'TDI'
    long_name = 'District'
    parent = SubFactory(
        'apps.api.factories.InternationalFactory',
    )


class DivisionFactory(OrganizationFactory):
    level = Organization.LEVEL.division
    kind = Organization.KIND.division
    name = 'Test Division'
    short_name = 'TDV'
    long_name = 'Test'
    parent = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


class NoncompFactory(OrganizationFactory):
    level = Organization.LEVEL.district
    kind = Organization.KIND.noncomp
    name = 'Frank Thorne District'
    short_name = 'TNC'
    long_name = 'Frank Thorne'
    parent = SubFactory(
        'apps.api.factories.InternationalFactory',
    )


class AffiliateFactory(OrganizationFactory):
    level = Organization.LEVEL.district
    kind = Organization.KIND.affiliate
    name = 'Test Affiliate'
    short_name = 'TAF'
    long_name = 'Affiliate'
    parent = SubFactory(
        'apps.api.factories.InternationalFactory',
    )


# Persons
class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    name = 'Test Person'
    status = Person.STATUS.active


# Venues
class VenueFactory(DjangoModelFactory):
    class Meta:
        model = Venue
        django_get_or_create = (
            'location',
            'city',
            'state',
            'timezone',
        )
    location = 'Nashville Convention Center'
    city = 'Nashville'
    state = 'Tennessee'
    timezone = 'US/Central'


# Judges
class JudgeFactory(DjangoModelFactory):
    class Meta:
        model = Judge

    category = Judge.CATEGORY.admin
    kind = Judge.KIND.official
    session = SubFactory(
        'apps.api.factories.SessionFactory'
    )
    certification = SubFactory(
        'apps.api.factories.CertificationFactory'
    )


# Certifications
class CertificationFactory(DjangoModelFactory):
    class Meta:
        model = Certification

    status = Certification.STATUS.active
    category = Certification.CATEGORY.admin
    person = SubFactory(
        'apps.api.factories.PersonFactory'
    )


# Submissions
class SubmissionFactory(DjangoModelFactory):
    class Meta:
        model = Submission

    status = Submission.STATUS.new
    performer = SubFactory(
        'apps.api.factories.PerformerFactory'
    )
    chart = SubFactory(
        'apps.api.factories.ChartFactory'
    )


# Members
class MemberFactory(DjangoModelFactory):
    class Meta:
        model = Member

    status = Member.STATUS.active
    chapter = SubFactory(
        'apps.api.factories.ChapterFactory'
    )
    person = SubFactory(
        'apps.api.factories.PersonFactory'
    )


# Roles
class RoleFactory(DjangoModelFactory):
    class Meta:
        model = Role

    status = Role.STATUS.active
    person = SubFactory(
        'apps.api.factories.PersonFactory'
    )
    part = Role.PART.tenor
    group = SubFactory(
        'apps.api.factories.QuartetFactory'
    )


class TenorFactory(DjangoModelFactory):
    class Meta:
        model = Role

    status = Role.STATUS.active
    person = SubFactory(
        'apps.api.factories.PersonFactory'
    )
    part = Role.PART.tenor
    group = SubFactory(
        'apps.api.factories.QuartetFactory'
    )


# Conventions
class ConventionFactory(DjangoModelFactory):
    class Meta:
        model = Convention

    status = Convention.STATUS.new
    venue = SubFactory(
        'apps.api.factories.VenueFactory'
    )


class SummerConventionFactory(ConventionFactory):
    kind = Convention.KIND.international
    season = Convention.SEASON.international
    risers = [13, ]
    year = 2016
    date = DateTimeTZRange(
        lower=datetime(2016, 07, 01, 12, 00),
        upper=datetime(2016, 07, 04, 12, 00),
        bounds='[)',
    )
    organization = SubFactory(
        'apps.api.factories.InternationalFactory',
    )


class MidwinterConventionFactory(ConventionFactory):
    kind = Convention.KIND.international
    season = Convention.SEASON.midwinter
    risers = [0, ]
    year = 2016
    date = DateTimeTZRange(
        lower=datetime(2016, 01, 29, 12, 00),
        upper=datetime(2016, 01, 30, 12, 00),
        bounds='[)',
    )
    organization = SubFactory(
        'apps.api.factories.InternationalFactory',
    )


class SpringConventionFactory(ConventionFactory):
    kind = Convention.KIND.district
    season = Convention.SEASON.spring
    risers = [5, 7, 9, ]
    year = 2016
    date = DateTimeTZRange(
        lower=datetime(2016, 04, 01, 12, 00),
        upper=datetime(2016, 04, 02, 12, 00),
        bounds='[)',
    )
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


class FallConventionFactory(ConventionFactory):
    kind = Convention.KIND.district
    season = Convention.SEASON.fall
    risers = [5, 7, 9, ]
    year = 2016
    date = DateTimeTZRange(
        lower=datetime(2016, 10, 01, 12, 00),
        upper=datetime(2016, 10, 02, 12, 00),
        bounds='[)',
    )
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


class RegionalConventionFactory(ConventionFactory):
    kind = Convention.KIND.fwdnenw
    season = Convention.SEASON.spring
    risers = [5, 7, 9, ]
    year = 2016
    date = DateTimeTZRange(
        lower=datetime(2016, 04, 01, 12, 00),
        upper=datetime(2016, 04, 02, 12, 00),
        bounds='[)',
    )
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


# Sessions
class SessionFactory(DjangoModelFactory):
    class Meta:
        model = Session
        django_get_or_create = (
            'kind',
        )
    status = Session.STATUS.new


class InternationalQuartetSession(SessionFactory):
    kind = Session.KIND.quartet
    convention = SubFactory(
        'apps.api.factories.SummerConvention',
    )


class InternationalChorusSession(SessionFactory):
    kind = Session.KIND.chorus
    convention = SubFactory(
        'apps.api.factories.SummerConvention',
    )


class InternationalSeniorsSession(SessionFactory):
    kind = Session.KIND.seniors
    convention = SubFactory(
        'apps.api.factories.MidwinterConvention',
    )


class InternationalYouthSession(SessionFactory):
    kind = Session.KIND.youth
    convention = SubFactory(
        'apps.api.factories.SummerConvention',
    )


class QuartetSession(SessionFactory):
    kind = Session.KIND.quartet


class DistrictChorusSession(SessionFactory):
    kind = Session.KIND.chorus


# Contests
class ContestFactory(DjangoModelFactory):
    class Meta:
        model = Contest

    status = Contest.STATUS.new
    cycle = 2016
    session = SubFactory(
        'apps.api.factories.SessionFactory'
    )
    award = SubFactory(
        'apps.api.factories.AwardFactory'
    )


# Rounds
class RoundFactory(DjangoModelFactory):
    class Meta:
        model = Round

    status = Round.STATUS.new
    kind = Round.KIND.finals
    num = 1
    session = SubFactory(
        'apps.api.factories.SessionFactory'
    )


# Performers
class PerformerFactory(DjangoModelFactory):
    class Meta:
        model = Performer
        django_get_or_create = (
            'status',
        )
    status = Performer.STATUS.new
    # representing = SubFactory(
    #     'apps.api.factories.DistrictFactory'
    # )
    session = SubFactory(
        'apps.api.factories.SessionFactory'
    )
    group = SubFactory(
        'apps.api.factories.QuartetFactory'
    )


# Contestants
class ContestantFactory(DjangoModelFactory):
    class Meta:
        model = Contestant

    status = Contestant.STATUS.new
    performer = SubFactory(
        'apps.api.factories.PerformerFactory'
    )
    contest = SubFactory(
        'apps.api.factories.ContestFactory',
    )


# Performances
class PerformanceFactory(DjangoModelFactory):
    class Meta:
        model = Performance

    status = Performance.STATUS.new
    performer = SubFactory(
        'apps.api.factories.PerformerFactory',
    )
    round = SubFactory(
        'apps.api.factories.RoundFactory',
        # session=Iterator(Session.objects.all())
    )


# Songs
class SongFactory(DjangoModelFactory):
    class Meta:
        model = Song

    status = Performance.STATUS.new
    order = 1
    performance = SubFactory(
        'apps.api.factories.PerformanceFactory',
    )
    submission = SubFactory(
        'apps.api.factories.SubmissionFactory',
        # performer=Iterator(Performer.objects.all())
    )


# Scores
class ScoreFactory(DjangoModelFactory):
    class Meta:
        model = Score

    status = Score.STATUS.new
    judge = SubFactory(
        'apps.api.factories.JudgeFactory',
    )
    song = SubFactory(
        'apps.api.factories.SongFactory',
        # performer=Performer.objects.all().first()
    )
    category = 1
    kind = 10
