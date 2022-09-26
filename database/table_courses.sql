create table if not exists courses (
	id integer primary key,
	moodle_id integer unique,
	name text
);
