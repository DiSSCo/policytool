from django.db import models

from common.models import Institution
from policy.utils import available_language_codes


class Service(models.Model):
    """
    DiSSCo service to which policies may apply.
    """
    # the name of the service
    name = models.TextField()
    # a short description of the service and its scope
    description = models.TextField(blank=True)
    # service URL (could be the service's homepage or another page of additional info)
    url = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class ServiceComponent(models.Model):
    """
    Component of a DiSSCo service relating to a more specific part of a workflow.
    """
    # the name of the service component
    name = models.TextField()
    # a short description of the service component
    description = models.TextField(blank=True)
    # the component this service belongs to
    service = models.ForeignKey(Service, related_name='components', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name} [{self.service}]'


class PolicyCategory(models.Model):
    """
    High level policy category referring to a number of related policy areas.
    """
    # the name of the policy category
    name = models.TextField()
    # a summary of the policy areas covered by the policy category
    scope = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class PolicyArea(models.Model):
    """
    Policy classification representing a specific area or theme.
    """
    # the name of the policy area
    name = models.TextField()
    # a number assigned to the policy area for administrative purposes
    number = models.IntegerField()
    # a summary of the scope of policy that is covered by the policy area
    scope = models.TextField(blank=True)
    # the category this policy area belongs to
    category = models.ForeignKey(PolicyCategory, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name} [{self.category}]'


# define the options for the component type
class PolicyComponentType(models.TextChoices):
    BOOL = 'bool'
    NUMBER = 'number'
    OPTION_SINGLE = 'option'
    OPTION_MULTIPLE = 'options'

    @property
    def requires_options(self) -> bool:
        return self in (PolicyComponentType.OPTION_SINGLE, PolicyComponentType.OPTION_MULTIPLE)


class PolicyComponent(models.Model):
    """
    Granular policy element within the policy area.
    """

    # the name of the policy component
    name = models.TextField()
    question = models.TextField()
    order = models.IntegerField(default=0)
    # a short and informative description of the policy component
    description = models.TextField(blank=True)
    # the type of data representing the component
    type = models.TextField(choices=PolicyComponentType.choices)
    # the policy area this component belongs to
    policy_area = models.ForeignKey(PolicyArea, related_name='components', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name}, {self.type} on {self.policy_area}'

    def get_type(self) -> PolicyComponentType:
        return PolicyComponentType(self.type)

    def is_option_based(self) -> bool:
        return self.get_type().requires_options


class PolicyComponentOption(models.Model):
    """
    Controlled vocabulary term for options relating to policy components. For example, one of a list
    of licenses that might be applied to collections data, or one of a list of exceptions to Open
    Data policy.
    """
    value = models.TextField()
    order = models.IntegerField(default=0)
    # the component this option belongs to
    policy_component = models.ForeignKey(PolicyComponent, related_name='options',
                                         on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Option: {self.value} on {self.policy_component}'


class InstitutionPolicyArea(models.Model):
    """
    Institutional summary of the existence, status and availability of policy documentation for the
    policy area.
    """

    # policy implementation status choices
    class PolicyImplementationStatus(models.TextChoices):
        # TODO: do we need more options here?
        DOCUMENTED = 'documented'
        UNDOCUMENTED = 'undocumented'
        NOT_IN_PLACE = 'not_in_place'

    # a name for the policy
    name = models.TextField()
    # whether the institution has a formally documented policy, undocumented procedure, or nothing
    # at all
    status = models.TextField(choices=PolicyImplementationStatus.choices)
    # date that the document was written
    documentation_date = models.DateTimeField(blank=True, null=True)
    # date that the documentation is next due to be reviewed
    documentation_next_review_date = models.DateTimeField(blank=True, null=True)
    # whether the documentation is public or has been released for internal use only
    # TODO: should this be a choice?
    documentation_public = models.TextField(blank=True)
    # whether the institution is willing and able to openly share the policy documentation
    # TODO: should this be a choice?
    documentation_shareable = models.TextField(blank=True)
    # details of one or more documents provided that are relevant to the subject. This may include
    # file/document names, links to online documentation, and details of the relevant sections
    # within the documentation if required. The same documentation may cover more than one of the
    # policy subjects
    documentation_details = models.TextField()
    # a summary of the policy, if documentation isn't available or can't be shared
    policy_summary = models.TextField(blank=True)
    # any additional notes relevant to the information or its use
    additional_notes = models.TextField(blank=True)
    # the institution this policy belongs to
    institution = models.ForeignKey(Institution, related_name='policies', on_delete=models.CASCADE)
    # the policy area this policy applies to
    policy_area = models.ForeignKey(PolicyArea, on_delete=models.CASCADE)


class InstitutionPolicyOwner(models.Model):
    # TODO: should this have other info like contact info?
    # TODO: should we link to users if we can?
    name = models.TextField()
    # TODO: should this be a choice?
    role = models.TextField()
    # the institutional policy area this owner presides over
    institution_policy_area = models.ForeignKey(InstitutionPolicyArea, related_name='owners',
                                                on_delete=models.CASCADE)


class InstitutionPolicyLanguage(models.Model):
    """
    Language(s) in which the policy documentation has been written.
    """
    code = models.TextField(choices=sorted(available_language_codes().items()))
    institution_policy_area = models.ForeignKey(InstitutionPolicyArea, related_name='languages',
                                                on_delete=models.CASCADE)


class InstitutionPolicyComponent(models.Model):
    """
    Value representing the status of a specific institution with respect to a specific policy
    component.
    """
    value = models.TextField(blank=True)
    chosen_options = models.ManyToManyField(PolicyComponentOption)
    comment = models.TextField(blank=True)
    institution = models.ForeignKey(Institution, related_name='components',
                                    on_delete=models.CASCADE)
    policy_component = models.ForeignKey(PolicyComponent,
                                         related_name='institution_policy_components',
                                         on_delete=models.CASCADE)


class InstitutionResponse(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    policy_area = models.ForeignKey(PolicyArea, on_delete=models.CASCADE)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institution', 'policy_area'],
                                    name='unique_policy_response'),
        ]


class Rule(models.TextChoices):
    EQUAL = 'equal'
    OR = 'or'


class ServicePolicyMapping(models.Model):
    """
    Value and rules representing the requirement of a specific service component with respect to a
    specific policy component.
    """
    # the service component this mapping applies to
    service_component = models.ForeignKey(ServiceComponent, on_delete=models.CASCADE)
    # the policy component this mapping applies to
    policy_component = models.ForeignKey(PolicyComponent, on_delete=models.CASCADE)
    # the rule that defines how this mapping is validated
    rule = models.TextField(choices=Rule.choices)
    allowed_value = models.TextField(blank=True)
    allowed_options = models.ManyToManyField(PolicyComponentOption)

    def get_rule(self) -> Rule:
        return Rule(self.rule)
