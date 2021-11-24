#!/bin/bash
set -e

clickhouse client -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS movies_db ON CLUSTER project_cluster;
    CREATE TABLE IF NOT EXISTS movies_db.events (
      finished_at Int64,
      movie_id_user_id String,
      event_datetime DateTime
    ) Engine=MergeTree() ORDER BY event_datetime;
EOSQL