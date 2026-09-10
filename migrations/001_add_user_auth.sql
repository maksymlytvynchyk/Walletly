-- Run this once in DBeaver for an existing development database.
-- Existing legacy users need to be recreated through the new registration form.
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS full_name VARCHAR(127) NOT NULL DEFAULT '';
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS phone VARCHAR(20) NOT NULL DEFAULT '';
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email VARCHAR(255) NOT NULL DEFAULT '';
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS birth_date DATE;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255) NOT NULL DEFAULT '';
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS access_token VARCHAR(255);

UPDATE "user" SET phone = login WHERE phone = '';
UPDATE "user" SET email = CONCAT('legacy-', id, '@example.invalid') WHERE email = '';

CREATE UNIQUE INDEX IF NOT EXISTS ix_user_phone ON "user" (phone);
CREATE UNIQUE INDEX IF NOT EXISTS ix_user_email ON "user" (email);
CREATE UNIQUE INDEX IF NOT EXISTS ix_user_access_token ON "user" (access_token);
