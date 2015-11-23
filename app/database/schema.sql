drop table if exists Users;
create table Users (
  userId integer primary key autoincrement,
  username text not null,
  password text not null,
  email text not null
);
drop table if exists Groups;
create table Groups (
  groupId integer primary key autoincrement,
  userId integer not null,
  name text not null,
  users text
);
drop table if exists Preferences;
create table Preferences (
  preferenceId integer primary key autoincrement,
  userId integer not null,
  genrePreferenceId integer not null
);
drop table if exists GenrePreferences;
create table GenrePreferences (
  genrePreferenceId integer primary key autoincrement,
  asian integer not null,
  mexican integer not null,
  american integer not null,
  italian integer not null,
  indian integer not null,
  greek integer not null
);
drop table if exists Friends;
create table Friends (
  userId integer not null,
  friendId integer not null
);