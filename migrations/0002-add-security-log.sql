CREATE TABLE security_log (
  id           SERIAL PRIMARY KEY,
  date_created TIMESTAMP NOT NULL,
  user_id      INTEGER   NOT NULL,
  event_type   INTEGER   NOT NULL,
  is_safe      BOOLEAN   NOT NULL,
  metadata     JSONB
);

ALTER TABLE security_log ADD CONSTRAINT security_log_user_id_fkey
FOREIGN KEY (user_id) REFERENCES "user" (id);
