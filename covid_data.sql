-- -------------------------------------------------------------
-- TablePlus 3.9.1(342)
--
-- https://tableplus.com/
--
-- Database: psu_covid_dash_checker.sqlite3
-- Generation Time: 2020-09-22 20:18:03.2780
-- -------------------------------------------------------------


CREATE TABLE covid_data (
	update_time real PRIMARY KEY,
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

