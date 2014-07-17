from django.db import models
from django.contrib.auth.models import User

MONTHS = ((1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), 
          (5, 'May'), (6, 'June'), (7, 'July'), (8, 'Aug'), (9, 'Sept'),
          (10, 'Oct'), (11, 'Nov'), (12, 'Dec'))

ALLOCATION = (('PS', 'Personnel Services'),
              ('MOOE', 'Maintenance and Operating Services'),
              ('CO', 'Capital Outlay'))

class Permissions(models.Model):
    action = models.CharField(max_length=10)
    target = models.CharField(max_length=45)

    def __unicode__(self):
        return self.action + ' ' + self.target
        
    class Meta:
        db_table = 'permissions'


class Groups(models.Model):
    name = models.CharField(max_length=45)

    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = 'groups'

class GroupPermissions(models.Model):
    group = models.ForeignKey(Groups)
    permission = models.ForeignKey(Permissions)

    def __unicode__(self):
        return self.group+' '+self.permission

    class Meta:
        db_table = 'group_perm'

class UserGroup(models.Model):
    user = models.OneToOneField(User)
    group = models.ForeignKey(Groups)

    def __unicode__(self):
        return self.user + ' ' + self.group

    class Meta:
        db_table = 'user_group'

class UserActivity(models.Model):
    user = models.ForeignKey(User)
    action = models.CharField(max_length = 100)
    act_date = models.DateTimeField()
    target = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'user_activity'
    
    
class Sector(models.Model):
    name = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'sector'


class Agency(models.Model):
    name = models.CharField(max_length = 200)
    sector = models.ForeignKey(Sector)
    email = models.EmailField()
    acces_key = models.CharField(max_length = 150)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'agency'


class Notification(models.Model):
    agency = models.ForeignKey(Agency)
    date_notify = models.DateField()
    subject = models.CharField(max_length=45)
    msg = models.TextField()

    class Meta:
        db_table = 'notification'

class COSSubmission(models.Model):
    agency = models.ForeignKey(Agency)
    date_submitted = models.DateTimeField()
    
    
    class Meta:
        db_table = 'cos_submission'

class BudgetProposal(models.Model):
    year = models.IntegerField()
    activity = models.CharField(max_length = 200)
    agency = models.ForeignKey(Agency)
    allocation = models.CharField(max_length=4)
    performance_indicator = models.CharField(max_length = 45)
    q1 = models.IntegerField()
    q2 = models.IntegerField()
    q3 = models.IntegerField()
    q4 = models.IntegerField()
    jan = models.DecimalField(max_digits = 12, decimal_places = 2)
    feb = models.DecimalField(max_digits = 12, decimal_places = 2)
    mar = models.DecimalField(max_digits = 12, decimal_places = 2)
    apr = models.DecimalField(max_digits = 12, decimal_places = 2)
    may = models.DecimalField(max_digits = 12, decimal_places = 2)
    jun = models.DecimalField(max_digits = 12, decimal_places = 2)
    jul= models.DecimalField(max_digits = 12, decimal_places = 2)
    aug = models.DecimalField(max_digits = 12, decimal_places = 2)
    sept = models.DecimalField(max_digits = 12, decimal_places = 2)
    oct = models.DecimalField(max_digits = 12, decimal_places = 2)
    nov = models.DecimalField(max_digits = 12, decimal_places = 2)
    dec = models.DecimalField(max_digits = 12, decimal_places = 2)
    total = models.DecimalField(max_digits = 15, decimal_places = 2)
    
    def __unicode__(self):
        return self.activity

    class Meta:
        db_table = 'budget_proposal'
        permissions = (('record_wfp', 'Enter data from WFP'),
                       ('print_report', 'Print Agency WFP Information')
        )
        
    

class WFPData(models.Model):
    year = models.IntegerField()
    activity = models.CharField(max_length = 200)
    agency = models.ForeignKey(Agency)
    allocation = models.CharField(max_length='4', choices=ALLOCATION)
    jan = models.DecimalField(max_digits = 12, decimal_places = 2)
    feb = models.DecimalField(max_digits = 12, decimal_places = 2)
    mar = models.DecimalField(max_digits = 12, decimal_places = 2)
    apr = models.DecimalField(max_digits = 12, decimal_places = 2)
    may = models.DecimalField(max_digits = 12, decimal_places = 2)
    jun = models.DecimalField(max_digits = 12, decimal_places = 2)
    jul= models.DecimalField(max_digits = 12, decimal_places = 2)
    aug = models.DecimalField(max_digits = 12, decimal_places = 2)
    sept = models.DecimalField(max_digits = 12, decimal_places = 2)
    oct = models.DecimalField(max_digits = 12, decimal_places = 2)
    nov = models.DecimalField(max_digits = 12, decimal_places = 2)
    dec = models.DecimalField(max_digits = 12, decimal_places = 2)
    total = models.DecimalField(max_digits = 15, decimal_places = 2)

    def __unicode__(self):
        return self.activity

    class Meta:
        db_table = 'wfp_data'
        permissions = (('record_wfp', 'Enter data from WFP'),
                       ('print_report', 'Print Agency WFP Information')
        )


class PerformanceTarget(models.Model):
    wfp_activity = models.ForeignKey(WFPData)
    indicator = models.CharField(max_length=45)
    jan = models.IntegerField()
    feb = models.IntegerField()
    mar = models.IntegerField()
    apr = models.IntegerField()
    may = models.IntegerField()
    jun = models.IntegerField()
    jul = models.IntegerField()
    aug = models.IntegerField()
    sept = models.IntegerField()
    oct = models.IntegerField()
    nov = models.IntegerField()
    dec = models.IntegerField()

    class Meta:
        db_table = 'performancetarget'
        
    
class AllotmentReleases(models.Model):
    year = models.IntegerField()
    agency = models.ForeignKey(Agency)
    allocation = models.CharField(max_length='4', choices=ALLOCATION)
    ada_no = models.CharField(max_length=5)
    date_release = models.DateField()
    month = models.IntegerField(choices=MONTHS)
    amount_release = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'allotmentreleases'

"""
class FundRelease(models.Model):
    ada = models.IntegerField()
    agency = models.ForeignKey(Agency)
    year = models.IntegerField()
    month = models.IntegerField()
    date_released = models.IntegerField
    allocation = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def unicode(self):
        return unicode(self.ada)
        
    class Meta:
        db_table = 'fund_release'
"""

class MPFRO(models.Model):
    agency = models.ForeignKey(Agency)
    year = models.IntegerField()
    month = models.IntegerField(choices=MONTHS)
    activity = models.OneToOneField(WFPData)
    allot_receive = models.DecimalField(max_digits=15, decimal_places=2)
    incurred = models.DecimalField(max_digits=15, decimal_places=2)
    remaining = models.DecimalField(max_digits=15, decimal_places=2)
    remarks = models.CharField(max_length=200)
    class Meta:
        db_table = 'mpfro'

class MPFROAccomplishment(models.Model):
    mpfro = models.ForeignKey(MPFRO)
    p_target = models.OneToOneField(PerformanceTarget)
    target = models.IntegerField()
    accomplished = models.IntegerField()
    variance = models.IntegerField()
    
    class Meta:
        db_table = 'mpfro_acc'

    
class FundBalances(models.Model):
    year = models.IntegerField()
    agency = models.ForeignKey(Agency)
    ps = models.DecimalField(max_digits=15, decimal_places=2)
    mooe = models.DecimalField(max_digits=15, decimal_places=2)
    co = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'fund_balances'


class MPFRSubmission(models.Model):
    year = models.IntegerField()
    agency = models.ForeignKey(Agency)
    jan = models.DateField(null=True)
    feb = models.DateField(null=True)
    mar = models.DateField(null=True)
    apr = models.DateField(null=True)
    may = models.DateField(null=True)
    jun = models.DateField(null=True)
    jul = models.DateField(null=True)
    aug = models.DateField(null=True)
    sept = models.DateField(null=True)
    oct = models.DateField(null=True)
    nov = models.DateField(null=True)
    dec = models.DateField(null=True)

    class Meta:
        db_table = 'mpfr_submission'


class QuarterlyReq(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'quarterly_req'

class QuarterReqSubmission(models.Model):
    agency = models.ForeignKey(Agency)
    requirement = models.ForeignKey(QuarterlyReq)
    year = models.IntegerField()
    quarter = models.IntegerField()
    date_submitted = models.DateField()

    class Meta:
        db_table = 'quarter_req_submit'
    

class CoRequest(models.Model):
    date_received = models.DateField()
    agency = models.ForeignKey(Agency)
    subject = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    status = models.CharField(max_length=150)

    class Meta:
        db_table = 'co_request'
