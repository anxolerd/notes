create table "user" (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  first_name TEXT NOT NULL,
  middle_name TEXT,
  last_name TEXT NOT NULL,
  polynomial_coef INTEGER[] NOT NULL,
  roles TEXT[]
);


create table "category" (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  allowed_roles TEXT[]
);


create table "note" (
  id SERIAL PRIMARY KEY,
  author_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  text TEXT NOT NULL
);

alter table "user" add constraint "ix_user_username_uniq" unique (username);
alter table "category" add constraint "ix_category_name_uniq" unique (name);
alter table "note" add constraint "note_author_id_fkey" foreign key (author_id) references "user" (id);
alter table "note" add constraint "note_category_id_fkey" foreign key (category_id) references "category" (id);
