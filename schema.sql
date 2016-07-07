drop table if exists ingredients;
create table ingredients (
  id integer primary key autoincrement,
  name text not null,
  calories integer not null,
  protein integer not null,
  carbs integer not null,
  fat integer not null,
  fiber integer not null,
  serving_size text not null
);