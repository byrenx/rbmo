
--- use for getting the sum of fund release to a agency for a specific
--- program or activity, year and allocation
select sum(amount) from fund_releases 
where budgetallocation_id in (select id from budget_allocation where agency_id=1 and year=2014 and allocation_id=1) 
