-- -------------------------------------------------------------
-- TablePlus 3.9.1(342)
--
-- https://tableplus.com/
--
-- Database: psu_covid_dash_checker.sqlite3
-- Generation Time: 2020-09-26 14:49:38.7860
-- -------------------------------------------------------------


CREATE TABLE covid_data (
update_time real NOT NULL default current_timestamp PRIMARY KEY,
overall_total_positive INTEGER,
overall_current_active integer,
overall_cases_no_longer_active integer,
overall_persons_currently_in_quarantine integer,
overall_persons_currently_in_isolation integer,
ondemand_total_tests_performed integer,
ondemand_total_positive_cases integer,
ondemand_total_awaiting_results integer,
random_total_tests_performed integer,
random_total_positive_cases integer,
random_total_awaiting_results integer
);

INSERT INTO "covid_data" ("update_time", "overall_total_positive", "overall_current_active", "overall_cases_no_longer_active", "overall_persons_currently_in_quarantine", "overall_persons_currently_in_isolation", "ondemand_total_tests_performed", "ondemand_total_positive_cases", "ondemand_total_awaiting_results", "random_total_tests_performed", "random_total_positive_cases", "random_total_awaiting_results") VALUES
('2020-09-23 00:38:27', '1665', '613', '1052', '58', '111', '8308', '1457', '364', '15237', '208', '389'),
('2020-09-25 01:05:28', '1665', '613', '1052', '58', '111', '8308', '1457', '364', '15237', '208', '389'),
('2020-09-25 16:20:42', '2123', '819', '1304', '57', '143', '10558', '1892', '515', '17425', '231', '458');
