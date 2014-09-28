from django.db import models
from django.contrib.auth.models import User

MONTHS = ((1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), 
          (5, 'May'), (6, 'June'), (7, 'July'), (8, 'Aug'), (9, 'Sept'),
          (10, 'Oct'), (11, 'Nov'), (12, 'Dec'))

ALLOCATION = (('PS', 'Personnel Services'),
              ('MOOE', 'Maintenance and Operating Services'),
              ('CO', 'Capital Outlay'))

PROG = (('GASS', 'General Administration and Support Services'),
        ('SO', 'Support to Operations'),
        ('O', 'Operations'))

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
    name   = models.CharField(max_length = 200)
    sector = models.ForeignKey(Sector)
    email  = models.EmailField()
    a_type = models.IntegerField(choices=((1, 'Locally Funded'),
                                          (2, 'Line Agencies')))

    parent_key    = models.IntegerField(default=0)
    acces_key     = models.CharField(max_length = 150)

    

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'agency'


class Notification(models.Model):
    agency      = models.ForeignKey(Agency)
    date_notify = models.DateField()
    subject     = models.CharField(max_length=45)
    msg         = models.TextField()

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
    program = models.CharField(max_length = 100)
    activity = models.CharField(max_length = 200)
    agency = models.ForeignKey(Agency)
    allocation = models.CharField(max_length=4, choices=ALLOCATION)
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
    total = models.DecimalField(max_digits = 12, decimal_places = 2)

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
    jan = models.IntegerField(default=0)
    jan_acc = models.IntegerField(default=0)
    feb = models.IntegerField(default=0)
    feb_acc = models.IntegerField(default=0)
    mar = models.IntegerField(default=0)
    mar_acc = models.IntegerField(default=0)
    apr = models.IntegerField(default=0)
    apr_acc = models.IntegerField(default=0)
    may = models.IntegerField(default=0)
    may_acc = models.IntegerField(default=0)
    jun = models.IntegerField(default=0)
    jun_acc = models.IntegerField(default=0)
    jul = models.IntegerField(default=0)
    jul_acc = models.IntegerField(default=0)
    aug = models.IntegerField(default=0)
    aug_acc = models.IntegerField(default=0)
    sept = models.IntegerField(default=0)
    sept_acc = models.IntegerField(default=0)
    oct = models.IntegerField(default=0)
    oct_acc = models.IntegerField(default=0)
    nov = models.IntegerField(default=0)
    nov_acc = models.IntegerField(default=0)
    dec = models.IntegerField(default=0)
    dec_acc = models.IntegerField(default=0)

    class Meta:
        db_table = 'performancetarget'

class PerformanceReport(models.Model):
    activity = models.ForeignKey(WFPData)
    month = models.IntegerField()
    year = models.IntegerField()
    received = models.DecimalField(max_digits=12, decimal_places=2)
    incurred = models.DecimalField(max_digits=12, decimal_places=2)
    remarks = models.CharField(max_length=200)

    class Meta:
        db_table = 'performance_report'
        
    
class AllotmentReleases(models.Model):
    year = models.IntegerField()
    agency = models.ForeignKey(Agency)
    allocation = models.CharField(max_length='4', choices=ALLOCATION)
    ada_no = models.CharField(max_length=5)
    date_release = models.DateField()
    month = models.IntegerField(choices=MONTHS)
    amount_release = models.DecimalField(max_digits=15, decimal_places=2)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'allotmentreleases'


#monthly performance and financial report of operation
class MPFRO(models.Model):
    agency = models.ForeignKey(Agency)
    year = models.IntegerField()
    month = models.IntegerField(choices=MONTHS)
    activity = models.OneToOneField(WFPData)
    allot_received = models.DecimalField(max_digits=15, decimal_places=2)
    incurred = models.DecimalField(max_digits=15, decimal_places=2)
    remaining = models.DecimalField(max_digits=15, decimal_places=2)
    remarks = models.CharField(max_length=200)
    class Meta:
        db_table = 'mpfro'

    
class FundBalances(models.Model):
    year = models.IntegerField()
    agency = models.ForeignKey(Agency)
    ps = models.DecimalField(max_digits=15, decimal_places=2)
    mooe = models.DecimalField(max_digits=15, decimal_places=2)
    co = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'fund_balances'


class MonthlyReqSubmitted(models.Model):
    year = models.IntegerField()
    agency = models.ForeignKey(Agency)
    date_submitted = models.DateTimeField()
    month = models.IntegerField()
    user = models.ForeignKey(User)
    
    class Meta:
        db_table = 'monthly_req_submitted'


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
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'quarter_req_submitted'
    

class CoRequest(models.Model):
    date_received = models.DateField()
    agency = models.ForeignKey(Agency)
    subject = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    status = models.CharField(max_length=150)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'co_request'
