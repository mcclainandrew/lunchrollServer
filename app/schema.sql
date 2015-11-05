drop table if exists Users;
create table Users (
  userID integer primary key autoincrement,
  username text not null,
  password text not null,
  email text not null
);
drop table if exists Groups;
create table Groups (
  groupID integer primary key autoincrement,
  userID integer not null,
  name text not null,
  users text
);
drop table if exists Preferences;
create table Preferences (
  preferenceID integer primary key autoincrement,
  userID integer not null,
  genrePreferenceID integer not null
);
drop table if exists GenrePreferences;
create table GenrePreferences (
  genrePreferenceID integer primary key autoincrement,
  asian integer not null,
  mexican integer not null,
  american integer not null,
  italian integer not null,
  indian integer not null,
  greek integer not null
);
