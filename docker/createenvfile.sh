#!/usr/bin/env sh

echo "$MODE" > .env-non-dev
echo "$LOG_LEVEL" > .env-non-dev
echo "$SENTRY_DSN" > .env-non-dev
echo ""> .env-non-dev
echo "$DB_PORT" > .env-non-dev
echo "$DB_USER" > .env-non-dev
echo "$DB_PASS" > .env-non-dev
echo "$DB_NAME" > .env-non-dev
echo ""> .env-non-dev
echo "$TEST_DB_PORT" > .env-non-dev
echo "$TEST_DB_USER" > .env-non-dev
echo "$TEST_DB_PASS" > .env-non-dev
echo "$TEST_DB_NAME" > .env-non-dev
echo ""> .env-non-dev
echo "$POSTGRES_USER" > .env-non-dev
echo "$POSTGRES_PASSWORD" > .env-non-dev
echo ""> .env-non-dev
echo "$ALGORITHM" > .env-non-dev
echo ""> .env-non-dev
echo "$REDIS_PORT" > .env-non-dev
echo ""> .env-non-dev
echo "$SMTP_PORT" > .env-non-dev
echo "$SMTP_USER" > .env-non-dev
echo "$SMTP_PASSWORD=" > .env-non-dev
