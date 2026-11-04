#!/usr/bin/env bash
# Usage: source dbt_env.sh
# Activates the dbt Python environment and loads Snowflake settings from ../.env
source "$(dirname "${BASH_SOURCE[0]:-$0}")/.venv/bin/activate"
set -a
source "$(dirname "${BASH_SOURCE[0]:-$0}")/../.env"
set +a
echo "dbt environment ready: $(which dbt)"
