BEGIN;
INSERT INTO "user" (
  id, username, password,
  first_name, middle_name, last_name,
  polynomial_coef, roles
) VALUES
  (1, 'admin', 'admin', 'Admin', NULL, 'Admin', '{2, 5}', '{"admin", "writer"}'),
  (2, 'writer', 'writer', 'Writer', NULL, 'Writer', '{5, 2}', '{"writer"}')
;
ALTER SEQUENCE user_id_seq RESTART WITH 3;

INSERT INTO "category" (id, name, allowed_roles) VALUES
  (1, 'top_secret', '{"admin"}'),
  (2, 'public', '{"writer", "admin"}')
;
ALTER SEQUENCE category_id_seq RESTART WITH 3;

END;
