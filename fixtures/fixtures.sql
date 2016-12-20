BEGIN;
INSERT INTO "user" (
  id, username, password,
  first_name, middle_name, last_name,
  polynomial_coef, roles
) VALUES
  (1, 'batman', 'batman', 'Bruce', NULL, 'Wayne', '{1, 1, 1}', '{"admin", "writer"}'),
  (2, 'robin', 'robin', 'Dick', NULL, 'Grayson', '{2, 5}', '{"writer"}')
;
ALTER SEQUENCE user_id_seq RESTART WITH 3;

INSERT INTO "category" (id, name, allowed_roles) VALUES
  (1, 'top_secret', '{"admin"}'),
  (2, 'public', '{"writer", "admin"}')
;
ALTER SEQUENCE category_id_seq RESTART WITH 3;

INSERT INTO "note" (id, author_id, category_id, title, "text") VALUES
  (1, 1, 1, 'How to stop Superman',
   '<p>Kryptonite, the fictional mineral that conveniently takes away all of Sups super powers.</p>' ||
    '<p>Kryptonite is not the only weakness Superman has. The fight itself is essentially a ruse to distract Superman, ' ||
    'while Catwoman, under Batman’s orders, kidnaps Lois Lane, Superman/Clark Kent’s love. Batman then plans to have Catwoman ' ||
    'drop Lois Lane off a skyscraper in plain view of Superman. Upon seeing the love of his life falling to her death, Superman ' ||
    'snaps out of Poison Ivy’s mind control and rescues Lois, flying her to safety.</p>'
  ),
  (2, 2, 2, 'Who is batman?', '<p>I spent a lot of time trying to figure out who batman is. Until he took me under his protection, until he cared after me.</p> ' ||
                              '<b>Because batman is Bruce Wayne!</p>')
;
ALTER SEQUENCE note_id_seq RESTART WITH 3;
END;
