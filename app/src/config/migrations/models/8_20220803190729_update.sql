-- upgrade --
ALTER TABLE "user" ADD "password" VARCHAR(360);
ALTER TABLE "user" DROP COLUMN "username";
ALTER TABLE "user" DROP COLUMN "password_hash";
ALTER TABLE "user" ALTER COLUMN "email" TYPE VARCHAR(360) USING "email"::VARCHAR(360);
CREATE UNIQUE INDEX "uid_user_email_1b4f1c" ON "user" ("email");
-- downgrade --
DROP INDEX "idx_user_email_1b4f1c";
ALTER TABLE "user" ADD "username" VARCHAR(20) NOT NULL UNIQUE;
ALTER TABLE "user" ADD "password_hash" VARCHAR(128);
ALTER TABLE "user" DROP COLUMN "password";
ALTER TABLE "user" ALTER COLUMN "email" TYPE VARCHAR(30) USING "email"::VARCHAR(30);
