/*group inserts*/
insert into permissions(action, target) VALUES
('add', 'agency'), -- 1
('edit', 'agency'), -- 2
('delete', 'agency'), -- 3
('view', 'agency information'), -- 4
('view', 'agency submitted documents'), -- 5
('add', 'agency submitted documents'), -- 6
('delete', 'agency submitted documents'),-- 7
('add', 'agency approved budget'), -- 8
('edit', 'agency approved budget'), -- 9
('delete', 'agency approved budget'), -- 10
('view', 'agency approved budget'), -- 11
('add', 'fund request'), -- 12
('edit', 'fund request'), -- 13
('delete', 'fund request'), -- 14
('view', 'running balances'), -- 15
('print', 'running balances'), -- 16
('view', 'status of allotment releases'), -- 17
('print', 'status of allotment releases'), -- 18
('view', 'total releases'), -- 19
('print', 'total releases'), -- 20
('view', 'monthly reports'), -- 21
('print', 'monthly reports'), -- 22
('view', 'quarterly report'), -- 23
('print', 'quarterly report'), -- 24
('view', 'transaction history'), -- 25
('delete', 'transaction history'), -- 26
('view', 'analysis report'), -- 27
('print', 'analysis report'), -- 28
('print', 'fund utilization'), -- 29
('view', 'fund utilization'), -- 30
('add', 'user'), -- 31
('edit', 'user'), -- 32
('view', 'user'); -- 33



insert into groups(name) VALUES
('Recording Officer'),
('BEAM'),
('BPAC'),
('Administrator');


insert into group_perm(group_id, permission_id) VALUES
/*recording officer*/
(1, 4),
(1, 5),
(1, 6),
(1, 11),
(1, 7),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 19),
(1, 20),
(1, 21),
(1, 22),
(1, 23),
(1, 24),
(1, 27),
(1, 28),
/*BEAM*/
(2, 4),
(2, 5),
(2, 8),
(2, 9),
(2, 10),
(2, 11),
(2, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 19),
(1, 20),
(1, 21),
(1, 22),
(1, 23),
(1, 24),
(1, 27),
(1, 28),
/*BPAC*/
(3, 4),
(3, 5),
(3, 11),
(3, 27),
(3, 28),
(3, 29),
(3, 30),
/*administrative director*/
(4, 1),
(4, 2),
(4, 3),
(4, 4),
(4, 5),
(4, 6),
(4, 7),
(4, 8),
(4, 9),
(4, 10),
(4, 11),
(4, 12),
(4, 13),
(4, 14),
(4, 15),
(4, 16),
(4, 17),
(4, 18),
(4, 19),
(4, 20),
(4, 21),
(4, 22),
(4, 23),
(4, 24),
(4, 25),
(4, 26),
(4, 27),
(4, 28),
(4, 29),
(4, 30),
(4, 31),
(4, 32),
(4, 33);


insert into sector(name) values
('Environmental Conservation & Mgt & Human Settlement'),
('Regional Legislative Services'),
('Administrative & Financial management Services'),
('Health Services'),
('Education, Science & Technology'),
('Livelihood, Social Welfare and Protection Services'),
('Employment Promotion & Development & Industrial Peace'),
('Trade Industry & Investment Development'),
('Transportation & Communication Regulation Services'),
('Road Network, Public Infra & Other Development');

insert into quarterly_req(name)
values
('Statement of Allotment, Obligation and balances'),
('Status of Funds'),
('Reports of Detailed Disbursement'),
('Narrative Accomplishment Reports');



/*views*/
CREATE VIEW user_permissions AS
SELECT auth_user.id, auth_user.username,
	groups.name, permissions.action, permissions.target
FROM auth_user
       INNER JOIN user_group ON
       user_group.user_id=auth_user.id
       INNER JOIN groups ON 
       groups.id = user_group.group_id
       INNER JOIN group_perm ON
       group_perm.group_id=groups.id
       INNER JOIN permissions ON 
       permissions.id=group_perm.permission_id;


create view total_approved_budget
as
select allocation_id, agency_id, year, sum(jan) as jan, sum(feb) as feb,
       sum(mar) as mar, sum(apr) as apr, sum(may) as may,
       sum(jun) as jun, sum(jul) as jul, sum(aug) as aug,
       sum(sept) as sept, sum(oct) as oct, sum(nov) as nov,
       sum(`dec`) as `dec`
from wfp_data group by year, allocation_id, agency_id;


create view total_release_util
as
SELECT year, agency_id, allocation_id, month, sum(amount_release) as total_release, sum(amount_utilize) as total_utilize
from fund_rel_util
group by agency_id, allocation_id, month, year;



---triggers
DELIMITER $$

CREATE TRIGGER add_balance
  AFTER INSERT ON wfp_data
  FOR EACH ROW
BEGIN
  DECLARE row_count INTEGER;
  DECLARE alloc VARCHAR(4);

  SELECT COUNT(*)
  INTO row_count
  FROM fund_balances
  WHERE year=NEW.year AND agency_id=NEW.agency_id;

  SELECT name INTO alloc
  FROM allocation WHERE id=NEW.allocation_id;

  IF row_count > 0 AND strcmp(alloc,'PS') > -1 THEN
     UPDATE fund_balances
     SET ps = ps + (NEW.jan+New.feb+NEW.mar+NEW.apr+NEW.may+NEW.jun+NEW.jul+NEW.aug+NEW.sept+NEW.oct+NEW.nov+NEW.dec)
     WHERE agency_id=NEW.agency_id AND year=NEW.year;
  ELSE IF row_count > 0 AND strcmp(alloc,'MOOE') > -1  THEN
     UPDATE fund_balances
     SET mooe = mooe + (NEW.jan+New.feb+NEW.mar+NEW.apr+NEW.may+NEW.jun+NEW.jul+NEW.aug+NEW.sept+NEW.oct+NEW.nov+NEW.dec)
     WHERE agency_id=NEW.agency_id AND year=NEW.year;
  ELSE IF row_count > 0 AND strcmp(alloc,'CO') > -1  THEN
     UPDATE fund_balances
     SET co = co + (NEW.jan+New.feb+NEW.mar+NEW.apr+NEW.may+NEW.jun+NEW.jul+NEW.aug+NEW.sept+NEW.oct+NEW.nov+NEW.dec)
     WHERE agency_id=NEW.agency_id AND year=NEW.year;
  ELSE if row_count <= 0 and strcmp(alloc,'PS') > -1  THEN
     INSERT INTO fund_balances
     (year, agency_id, ps, mooe, co)
     VALUES(NEW.year, NEW.agency_id, (NEW.jan+New.feb+NEW.mar+NEW.apr+NEW.may+NEW.jun+NEW.jul+NEW.aug+NEW.sept+NEW.oct+NEW.nov+NEW.dec), 0, 0);
  ELSE IF row_count<=0 AND strcmp(alloc,'MOOE') > -1  THEN
     INSERT INTO fund_balances
     (year, agency_id, ps, mooe, co)
     VALUES(NEW.year, NEW.agency_id, 0, (NEW.jan+New.feb+NEW.mar+NEW.apr+NEW.may+NEW.jun+NEW.jul+NEW.aug+NEW.sept+NEW.oct+NEW.nov+NEW.dec), 0);
  ELSE
     INSERT INTO fund_balances
     (year, agency_id, ps, mooe, co)
     VALUES(NEW.year, NEW.agency_id, 0, 0, (NEW.jan+New.feb+NEW.mar+NEW.apr+NEW.may+NEW.jun+NEW.jul+NEW.aug+NEW.sept+NEW.oct+NEW.nov+NEW.dec));
  END IF;

END$$
