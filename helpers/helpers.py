from django.db import connection
import time
from datetime import datetime

def has_permission(user_id, action, target):
    cursor = connection.cursor()
    query = '''SELECT * FROM user_permissions WHERE
    id = %s AND action=%s AND target=%s
    '''
    cursor.execute(query, [user_id, action, target])
    return cursor.fetchone()>0

def get_allowed_tabs(user_id):
    tabs=[{'tag' : 'Home', 'link': '/admin/home'}]
    if has_permission(user_id, 'record', 'user'):
        tabs.append({'tag': 'Users', 'link': '/admin/users'})
    if has_permission(user_id, 'view', 'agency'):
        tabs.append({'tag': 'Agency/Office', 'link': '/admin/agencies'})
    if has_permission(user_id, 'view', 'transaction history'):
        tabs.append({'tag': 'Transaction History', 'link': ''})
    if has_permission(user_id, 'process', 'monthly cash allocation'):
        tabs.append({'tag': 'SMCA', 'link': '/admin/smca'})
    if has_permission(user_id, 'print', 'transaction history'):
        tabs.append({'tag': 'Transaction Summary', 'link': '/history/summary'})
 

    reports = []
    if has_permission(user_id, 'print', 'total releases'):
        reports.append({'tag': 'Total Fund Release', 'link': '/admin/allot_releases'})
        reports.append({'tag': 'Total Monthly Release', 'link': '/admin/total_monthly_release'})
        reports.append({'tag': 'Yearly Local Fund', 'link': '/admin/yearly_fund'})
    if has_permission(user_id, 'print', "running balances"):
        reports.append({'tag': 'Running Balances', 'link': '/agency/fund/running_balances'})
        reports.append({'tag': 'Approved Budget', 'link': '/admin/approved_budget'})
        
    if has_permission(user_id, 'view', "analysis report"):
        pass
    if has_permission(user_id, 'print', "fund distribution"):
        reports.append({'tag': 'Local Fund Distribution', 'link': '/admin/fund_distrib'})
    if has_permission(user_id, 'view', "quarterly reports"):
       pass
    if has_permission(user_id, 'print', 'agencies with complete requirements'):
        reports.append({'tag': 'Agencies w/ Complete Requirements', 'link': '/admin/agencies_with_compreqs'})
    if has_permission(user_id, 'print', 'agencies with incomplete requirements'):
        reports.append({'tag': 'Agencies w/ Incomplete Requirements', 'link': '/admin/agencies_with_increqs'})
    tabs.append({'tag':'Reports', 'menus':reports})
    return tabs


def getAgencyTabs(user_id, agency_id):
    tabs = []
    if has_permission(user_id, 'record', 'agency submitted requirements'):
        tabs.append({'tag' : "Requirements", 'link': '/admin/manage_agency_docs/'+str(agency_id)+'/'})
    if has_permission(user_id, 'record', 'wfp'):
        tabs.append({'tag' : 'WFP', 'link': '/agency/wfp/wfpinfo/'+str(agency_id)+'/'})
    if has_permission(user_id, 'process', 'monthly cash allocation'):
        tabs.append({'tag' : 'Monthly Cash Allocation', 'link': '/agency/fund/monthly_alloc/'+str(agency_id)+'/'})
    if has_permission(user_id, 'print', 'comprehensive performance report'):
        tabs.append({'tag' : 'Monthly Report of Operation', 'link': '/admin/monthly_reports/'+str(agency_id)+'/'})
    if has_permission(user_id, 'record', 'allotment releases'):
        tabs.append({'tag' : 'Allotment Releases', 'link': '/agency/fund/allotment_releases/'+str(agency_id)+'/'})
    if has_permission(user_id, 'record', 'request received'):
        tabs.append({'tag' : 'CO Requests', 'link': '/agency/wfp/co_request/'+str(agency_id)+'/'})
    return tabs
    

def stringify_month(month): # month is an integer starting 1 trough 12
    months = {1:'January', 2: 'February', 3:'March', 4:'April', 
              5:'May', 6:'June', 7:'July', 8:'August', 
              9:'September', 10:'October', 11:'November', 12:'December'
    }
    return months[month]
    
def numify(num):
    if num is None:
        return 0
    else:
        return num


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def quarterofMonth(month):
    '''
    month -> int
    postcondition:
    returns the preceding quarter of the month
    '''
    if month>=1 and month<=3:
        return 4
    elif month>=4 and month<=6:
        return 1
    elif month>=7 and month<=9:
        return 2
    elif month>=10 and month<=12:
        return 3
    else:
        return -1

def strRequiredQuarter(month, year):
    if month>=1 and month<=3:
        return '%s 4th quarter' %(year-1)
    elif month>=4 and month<=6:
        return '%s 1st quarter' %(year) 
    elif month>=7 and month<=9:
        return '%s 2nd' %(year)
    elif month>=10 and month<=12:
        return '%s 3rd' %(year)
    else:
        return ''


def exactQuarterofMonth(month):
    #returns the exact quarter where the month belong
    if month>=1 and month<=3:
        return 1
    elif month>=4 and month<=6:
        return 2
    elif month>=7 and month<=9:
        return 3
    elif month>=10 and month<=12:
        return 4


def getMonthLookup():
    return {1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr',
            5: 'may', 6: 'jun', 7: 'jul', 8: 'aug',
            9: 'sept', 10: 'oct', 11: 'nov', 12: 'dec'}


def getYearsChoices():
    cur_year  = datetime.today().year
    base_year = 2014
    years = []
    while cur_year >= base_year:
        years.append((cur_year, cur_year))
        cur_year-=1

    return tuple(years)

    
