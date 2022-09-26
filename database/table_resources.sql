create table if not exists resources (
	id integer primary key,
	moodle_id integer unique,
	course_id integer unique,
	type_id integer unique,
	name text,
	foreign key (course_id) references courses (id)
	foreign key (type_id) references types (id)
);
