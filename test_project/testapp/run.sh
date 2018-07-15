#!/usr/bin/env bash

alembic upgrade head

flask run --host=0.0.0.0
