# Standard Libary
import logging
import django_rq
import json

# Django
from django.apps import apps
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import URLValidator
from django.core.validators import validate_email
from django.db import IntegrityError
from django.db.models import Manager
from django.forms.models import model_to_dict
from django.utils.timezone import now
from api.tasks import get_accounts
from api.tasks import delete_account

log = logging.getLogger(__name__)

validate_url = URLValidator()

validate_twitter = RegexValidator(
    regex=r'@([A-Za-z0-9_]+)',
    message="""
        Must be a single Twitter handle
        in the form `@twitter_handle`.
    """,
)


class LowMemberManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group__kind__gt=30)


class GroupManager(Manager):
    def update_or_create_from_structure(self, structure, is_object=False):
        # Map between object/instance
        if is_object:
            mc_pk = structure[0]
            raw_name = structure[1]
            preferred_name = structure[2]
            chorus_name = structure[3]
            status = structure[4]
            kind = structure[5]
            start_date = structure[6]
            email = structure[7]
            phone = structure[8]
            website = structure[9]
            facebook = structure[10]
            twitter = structure[11]
            bhs_id = structure[12]
            parent = structure[13]
            code = structure[14]
        else:
            mc_pk = str(structure.id)
            raw_name = structure.name
            preferred_name = structure.preferred_name
            chorus_name = structure.chorus_name
            status = structure.status.name
            kind = structure.kind
            start_date = structure.established_date
            email = structure.email
            phone = structure.phone
            website = structure.website
            facebook = structure.facebook
            twitter = structure.twitter
            bhs_id = structure.bhs_id
            parent = str(structure.parent.id)
            code = structure.chapter_code

        # Transform as needed
        name = raw_name.strip() if raw_name else ''
        preferred_name = "{0} (NAME APPROVAL PENDING)".format(preferred_name) if preferred_name else ''
        chorus_name = chorus_name.strip() if chorus_name else ''
        kind = getattr(
            self.model.KIND,
            kind.replace('chapter', 'chorus').replace('group', 'noncomp')
        )
        email = email.strip()
        phone = phone.strip()
        website = website.strip()
        facebook = facebook.strip()
        twitter = twitter.strip()
        mem_status = getattr(self.model.MEM_STATUS, status.replace("-", "_"))
        status = getattr(self.model.STATUS, status, self.model.STATUS.inactive)
        code = code.strip() if code else ''

        # Construct the group name
        if kind == self.model.KIND.quartet:
            # If the name has not been assigned, use preferred. Otherwise, call unknown.
            if not name:
                name = preferred_name if preferred_name else 'UNKNOWN'
        elif kind == self.model.KIND.chorus:
            name = chorus_name if chorus_name else 'UNKNOWN'
        else:
            name = name if name else 'UNKNOWN'

        # Clean email
        try:
            validate_email(email)
        except ValidationError:
            email = ""

        # Clean website
        try:
            validate_url(website)
        except ValidationError:
            website = ""

        # Clean facebook
        try:
            validate_url(facebook)
        except ValidationError:
            facebook = ""

        # Clean twitter
        if '@' in twitter:
            if '/' in twitter:
                twitter = twitter.rpartition("/")[2]
            else:
                twitter = twitter
        else:
            if '/' in twitter:
                twitter = twitter.rpartition('/')[2]
            else:
                twitter = "@{0}".format(twitter)
        try:
            validate_twitter(twitter)
        except ValidationError:
            twitter = ""

        # Monkey-patch for the AIC
        if str(bhs_id) in self.model.AIC:
            status = getattr(self.model.STATUS, 'aic')
            name = self.model.AIC[str(bhs_id)]
        defaults = {
            'name': name,
            'status': status,
            'kind': kind,
            'start_date': start_date,
            'email': email,
            'phone': phone,
            'website': website,
            'facebook': facebook,
            'twitter': twitter,
            'code': code,
            'bhs_id': bhs_id,
            'mem_status': mem_status,
        }
        group, created = self.get_or_create(
            mc_pk=mc_pk,
            kind=kind,
        )

        # set prior values
        prior = model_to_dict(
            group,
            fields=[
                'name',
                'status',
                'kind',
                'start_date',
                'email',
                'phone',
                'website',
                'facebook',
                'twitter',
                'code',
                'bhs_id',
                'mem_status',
            ],
        )

        # update the group to new values
        for key, value in defaults.items():
            setattr(group, key, value)

        # Set parent on create only
        if created:
            if kind == self.model.KIND.chorus:
                kind = self.model.KIND.chapter
                name = raw_name.strip() if raw_name else 'UNKNOWN'
                parent = self.model.get_or_create(
                    name=name,
                    code=code,
                    bhs_id=bhs_id,
                    kind=kind,
                )
            else:
                parent = self.get(mc_pk=parent)
            group.parent = parent
            group.save()

        # Build the diff from prior to new
        diff = {}
        for key, value in prior.items():
            if defaults[key] != value:
                if key == 'status':
                    diff[key] = self.model.STATUS[value]
                elif key == 'kind':
                    diff[key] = self.model.KIND[value]
                elif key == 'mem_status':
                    try:
                        diff[key] = self.model.MEM_STATUS[value]
                    except KeyError:
                        diff[key] = None
                elif key == 'start_date':
                    try:
                        diff[key] = value.strftime('%Y-%d-%m')
                    except AttributeError:
                        diff[key] = None
                else:
                    diff[key] = value

        # Bypass if not dirty
        if not diff:
            return group, None

        # Set the transition description
        if group.status == group.STATUS.new:
            description = json.dumps({'status': 'New'})
        else:
            description = json.dumps(diff)

        # Transition as appropriate
        if status == self.model.STATUS.active:
            group.activate(
                description=description,
            )
        elif status == self.model.STATUS.inactive:
            group.deactivate(
                description=description,
            )
        elif status == self.model.STATUS.aic:
            pass
        else:
            raise ValueError('Unknown status')

        # Finally, save the record
        group.save()
        return group, created

    def sort_tree(self):
        self.all().update(tree_sort=None)
        root = self.get(kind=self.model.KIND.international)
        i = 1
        root.tree_sort = i
        root.save()
        for child in root.children.order_by('kind', 'name'):
            i += 1
            child.tree_sort = i
            child.save()
            for grandchild in child.children.filter(
                kind=self.model.KIND.division,
            ).order_by('kind', 'name'):
                i += 1
                grandchild.tree_sort = i
                grandchild.save()
        orgs = self.filter(
            kind__in=[
                self.model.KIND.chapter,
                self.model.KIND.chorus,
                self.model.KIND.quartet,
            ]
        ).order_by(
            'kind',
            'name',
        )
        for org in orgs:
            i += 1
            org.tree_sort = i
            org.save()
        return

    def denormalize(self):
        groups = self.all()
        for group in groups:
            group.denormalize()
            group.save()
        return


class MemberManager(Manager):
    def update_from_join(self, join, is_object=False):
        # Map variables
        if is_object:
            mc_pk = join[0]
            structure = join[1]
            person = join[2]
            inactive_date = join[3]
            inactive_reason = join[4]
            part = join[5]
            sub_status = join[6]
            current_through = join[7]
            established_date = join[8]
            mem_code = join[9]
            mem_status = join[10]
        else:
            mc_pk = str(join.id)
            structure = str(join.structure.id)
            person = str(join.subscription.human.id)
            inactive_date = join.inactive_date
            inactive_reason = join.inactive_reason
            part = join.vocal_part
            sub_status = join.subscription.status
            current_through = join.subscription.current_through
            established_date = join.established_date
            mem_code = join.membership.code
            mem_status = join.membership.status.name

        # Set variables
        status = self.model.STATUS.inactive if inactive_date else self.model.STATUS.active

        sub_status = getattr(
            self.model.SUB_STATUS,
            sub_status if sub_status else '',
            None,
        )

        part = getattr(
            self.model.PART,
            part.strip().lower() if part else '',
            None,
        )

        inactive_reason = getattr(
            self.model.INACTIVE_REASON,
            inactive_reason.strip().replace("-", "_").replace(" ", "") if inactive_reason else '',
            None,
        )

        mem_code = getattr(
            self.model.MEM_CODE,
            mem_code if mem_code else '',
            None,
        )

        mem_status = getattr(
            self.model.MEM_STATUS,
            mem_status.strip().replace("-", "_") if mem_status else '',
            None,
        )

        # Get the related fields
        Group = apps.get_model('api.group')
        group = Group.objects.get(
            mc_pk=structure,
        )
        Person = apps.get_model('api.person')
        person = Person.objects.get(
            mc_pk=person,
        )

        # get or create
        member, created = self.get_or_create(
            person=person,
            group=group,
        )

        # Skip duplicates
        if str(member.mc_pk) == mc_pk:
            return 'Skipped'

        # Instantiate prior values dictionary
        prior = {}
        if member.mc_pk:
            prior['mc_pk'] = str(member.mc_pk)
        if member.sub_status:
            prior['sub_status'] = member.get_sub_status_display()
        if member.current_through:
            prior['current_through'] = member.current_through.strftime('%Y-%m-%d')
        if member.established_date:
            prior['established_date'] = member.established_date.strftime('%Y-%m-%d')
        if member.inactive_date:
            prior['inactive_date'] = member.inactive_date.strftime('%Y-%m-%d')
        if member.inactive_reason:
            prior['inactive_reason'] = member.get_inactive_reason_display()
        if member.part:
            prior['part'] = member.get_part_display()
        if member.mem_code:
            prior['mem_code'] = member.get_mem_code_display()
        if member.mem_status:
            prior['mem_status'] = member.get_mem_status_display()

        # Update the fields
        member.mc_pk = mc_pk
        member.inactive_date = inactive_date
        member.inactive_reason = inactive_reason
        member.part = part
        member.sub_status = sub_status
        member.current_through = current_through
        member.established_date = established_date
        member.mem_code = mem_code
        member.mem_status = mem_status

        # Build the diff from prior to new
        diff = {}
        if prior.get('mc_pk') != str(mc_pk):
            diff['mc_pk'] = getattr(prior, 'mc_pk', None)

        inactive_date_string = inactive_date.strftime('%Y-%m-%d') if inactive_date else None
        if prior.get('inactive_date') != inactive_date_string:
            diff['inactive_date'] = inactive_date_string

        if prior.get('inactive_reason') != inactive_reason:
            diff['inactive_reason'] = getattr(prior, 'inactive_reason', None)

        part_string = self.model.PART[part] if part else None
        if prior.get('part') != part_string:
            diff['part'] = part_string

        sub_status_string = self.model.SUB_STATUS[sub_status] if sub_status else None
        if prior.get('sub_status') != sub_status_string:
            diff['sub_status'] = sub_status_string

        current_through_string = current_through.strftime('%Y-%m-%d') if current_through else None
        if prior.get('current_through') != current_through_string:
            diff['current_through'] = current_through_string

        established_date_string = established_date.strftime('%Y-%m-%d') if established_date else None
        if prior.get('established_date') != established_date_string:
            diff['established_date'] = established_date_string

        mem_code_string = self.model.MEM_CODE[mem_code] if mem_code else None
        if prior.get('mem_code') != mem_code_string:
            diff['mem_code'] = mem_code_string

        mem_status_string = self.model.MEM_STATUS[mem_status] if mem_status else None
        if prior.get('mem_status') != mem_status_string:
            diff['mem_status'] = mem_status_string

        # Set the transition description
        if member.status == member.STATUS.new:
            description = json.dumps({'status': 'New'})
        else:
            description = json.dumps(diff)

        # Transition as appropriate
        if status == self.model.STATUS.active:
            member.activate(
                description=description,
            )
        elif status == self.model.STATUS.inactive:
            member.deactivate(
                description=description,
            )
        else:
            raise ValueError('Unknown status')
        # Finally, save the record.
        member.save()
        return 'Updated'


class OfficerManager(Manager):
    def update_from_role(self, role, is_object=False):
        # Map
        if is_object:
            mc_pk = role[0]
            office = role[1]
            group = role[2]
            person = role[3]
            start_date = role[4]
            end_date = role[5]
        else:
            mc_pk = str(role.id)
            office = role.name
            group = str(role.structure.id)
            person = str(role.human.id)
            start_date = role.start_date
            end_date = role.end_date

        today = now().date()
        if end_date:
            if end_date < today:
                status = self.model.STATUS.inactive
            else:
                status = self.model.STATUS.active
        else:
            status = self.model.STATUS.active

        # Get group
        Group = apps.get_model('api.group')
        group = Group.objects.get(mc_pk=group)
        # Get person
        Person = apps.get_model('api.person')
        person = Person.objects.get(mc_pk=person)
        # Get office
        Office = apps.get_model('api.office')
        office = Office.objects.get(name=office)

        # get or create
        officer, created = self.get_or_create(
            person=person,
            group=group,
            office=office,
        )
        # Skip duplicates
        if str(officer.mc_pk) == mc_pk:
            return 'Skipped'

        # Instantiate prior values dictionary
        prior = {}
        if officer.mc_pk:
            prior['mc_pk'] = str(officer.mc_pk)
        if officer.start_date:
            prior['start_date'] = officer.start_date.strftime('%Y-%m-%d')
        if officer.end_date:
            prior['end_date'] = officer.end_date.strftime('%Y-%m-%d')

        # Update the fields
        officer.mc_pk = mc_pk
        officer.start_date = start_date
        officer.end_date = end_date

        # Build the diff from prior to new
        diff = {}

        if prior.get('mc_pk') != mc_pk:
            diff['mc_pk'] = prior.get('mc_pk')

        start_date_string = start_date.strftime('%Y-%m-%d') if start_date else None
        if prior.get('start_date') != start_date_string:
            diff['start_date'] = prior.get('start_date')

        end_date_string = end_date.strftime('%Y-%m-%d') if end_date else None
        if prior.get('end_date') != end_date_string:
            diff['end_date'] = prior.get('end_date')

        # Set the transition description
        if officer.status == officer.STATUS.new:
            description = json.dumps({'status': 'New'})
        else:
            description = json.dumps(diff)

        # Transition as appropriate
        if status == self.model.STATUS.active:
            officer.activate(
                description=description,
            )
        elif status == self.model.STATUS.inactive:
            officer.deactivate(
                description=description,
            )
        else:
            raise ValueError('Unknown status')
        # Finally, save the record.
        officer.save()
        return 'Updated'


class PersonManager(Manager):
    def update_or_create_from_human(self, human, is_object=False):
        # Map between object/instance
        if is_object:
            mc_pk = human[0]
            first_name = human[1]
            middle_name = human[2]
            last_name = human[3]
            nick_name = human[4]
            email = human[5]
            birth_date = human[6]
            phone = human[7]
            cell_phone = human[8]
            work_phone = human[9]
            bhs_id = human[10]
            gender = human[11]
            part = human[12]
        else:
            mc_pk = str(human.mc_pk)
            first_name = human.first_name
            middle_name = human.middle_name
            last_name = human.last_name
            nick_name = human.nick_name
            email = human.email
            birth_date = human.birth_date
            phone = human.phone
            cell_phone = human.cell_phone
            work_phone = human.work_phone
            bhs_id = human.bhs_id
            gender = human.gender
            part = human.part

        # Same logic regardless of inbound form
        first_name = first_name.strip()
        try:
            middle_name = middle_name.strip()
        except AttributeError:
            middle_name = ""
        last_name = last_name.strip()
        try:
            nick_name = nick_name.replace("'", "").replace('"', '').replace("(", "").replace(")", "").strip()
        except AttributeError:
            nick_name = ""
        if nick_name == first_name:
            nick_name = ""
        if email:
            email = email.strip()
            try:
                validate_email(email)
            except ValidationError:
                email = None
        else:
            email = None
        if not phone:
            phone = ''
        if not cell_phone:
            cell_phone = ''
        if not work_phone:
            work_phone = ''
        if gender:
            gender = getattr(self.model.GENDER, gender.casefold(), None)
        else:
            gender = None
        if part:
            part = getattr(self.model.PART, part.casefold(), None)
        else:
            part = None
        # Set default; subscriptions updates it.
        defaults = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'nick_name': nick_name,
            'email': email,
            'birth_date': birth_date,
            'phone': phone,
            'cell_phone': cell_phone,
            'work_phone': work_phone,
            'bhs_id': bhs_id,
            'gender': gender,
            'part': part,
        }
        try:
            person, created = self.update_or_create(
                mc_pk=mc_pk,
                defaults=defaults,
            )
        except IntegrityError:
            defaults['mc_pk'] = mc_pk
            defaults.pop('bhs_id', None)
            try:
                person, created = self.update_or_create(
                    bhs_id=bhs_id,
                    defaults=defaults,
                )
            except IntegrityError:
                defaults['mc_pk'] = mc_pk
                defaults['bhs_id'] = bhs_id
                defaults.pop('email', None)
                person, created = self.update_or_create(
                    email=email,
                    defaults=defaults,
                )
        return person, created

    def update_from_subscription(self, subscription, is_object=False):
        # Map between object/instance
        if is_object:
            mc_pk = subscription[0]
            human = subscription[1]
            current_through = subscription[2]
            status = subscription[3]
        else:
            mc_pk = str(subscription.id)
            human = str(subscription.human.id)
            current_through = subscription.current_through
            status = subscription.status

        status = getattr(
            self.model.STATUS,
            status,
            self.model.STATUS.inactive,
        )
        person = self.get(
            mc_pk=human,
        )
        # Instantiate prior values dictionary
        prior = {}
        prior['status'] = person.get_status_display()
        prior['current_through'] = person.current_through.strftime('%Y-%m-%d') if person.current_through else None

        # Update
        person.current_through = current_through

        # Build the diff from prior to new
        diff = {}
        if person.status != status:
            diff['status'] = prior['status']
        current_through_string = current_through.strftime('%Y-%m-%d') if current_through else None
        if prior.get('current_through') != current_through_string:
            diff['current_through'] = prior['current_through']
        if diff:
            diff['mc_pk'] = mc_pk

        if not diff:
            return 'Skipped'

        # Set the transition description
        if person.status == person.STATUS.new:
            description = json.dumps({'status': 'New'})
        else:
            description = json.dumps(diff)

        if status == self.model.STATUS.active:
            person.activate(
                description=description,
            )
        elif status == self.model.STATUS.inactive:
            person.deactivate(
                description=description,
            )
        else:
            raise ValueError('Unknown status')
        person.save()
        return 'Updated'

    def update_users(self, cursor=None):
        # Get Base - currently only active officers persons
        Officer = apps.get_model('api.officer')
        persons = self.filter(
            officers__status=Officer.STATUS.active,
            status=self.model.STATUS.active,
            email__isnull=False,
        ).distinct()
        if cursor:
            persons = persons.filter(
                modified__gt=cursor,
            )
        # Return as objects
        persons = persons.values_list(
            'id',
                'email',
            'status',
        )
        User = apps.get_model('api.user')
        for person in persons:
            django_rq.enqueue(
                User.objects.update_or_create_from_person,
                person,
                is_object=True,
            )
        return persons.count()


class UserManager(BaseUserManager):
    def update_or_create_from_person(self, person, is_object=False):
        # mapping
        Person = apps.get_model('api.person')
        if is_object:
            person_pk = str(person[0])
            name = person[1]
            email = person[2]
            status = person[3]
        else:
            person_pk = str(person.pk)
            name = person.full_name
            email = person.email
            status = person.status

        # really clean email
        email = email.lower()

        defaults = {
            'name': name,
            'email': email,
            'status': status,
        }
        person = Person.objects.get(
            id=person_pk,
        )
        try:
            user = self.get(
                person=person,
            )
            created = False
        except self.model.DoesNotExist:
            user = self.create(
                email=email,
                name=name,
                person=person,
            )
            user.set_unusable_password()
            created = True

        # set prior values
        prior = model_to_dict(
            user,
            fields=[
                'name',
                'email',
                'status',
            ],
        )

        # Update to new values
        user.email = email
        user.name = name

        # Build the diff from prior to new
        diff = {}
        for key, value in prior.items():
            if defaults[key] != value:
                diff[key] = value

        if not diff:
            return user, None

        # Set the transition description
        if user.status == user.STATUS.new:
            description = json.dumps({'status': 'New'})
        else:
            description = json.dumps(diff)

        # Transition as appropriate
        if status == self.model.STATUS.active:
            user.activate(
                description=description,
            )
        elif status == self.model.STATUS.inactive:
            user.deactivate(
                description=description,
            )
        # Finally, return the user
        user.save(using=self._db)
        return user, created

    def delete_orphans(self):
        accounts = get_accounts()
        users = list(self.filter(
            account_id__isnull=False
        ).values_list('account_id', flat=True))
        i = 0
        for account in accounts:
            if account['account_id'] not in users:
                i += 1
                delete_account.delay(account['account_id'])
        return i

    def create_user(self, email, **kwargs):
        user = self.model(
            email=email,
            **kwargs
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
