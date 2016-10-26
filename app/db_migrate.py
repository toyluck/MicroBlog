#!/usr/bin/python3.5
import imp
from config import SQLALCHEMY_MIGRATE_REPO
from config import SQLALCHEMY_DATABASE_URL
from migrate.versioning import api

from app import db

# get the  version of current db
v = api.db_version(SQLALCHEMY_DATABASE_URL, SQLALCHEMY_MIGRATE_REPO)
# new migrate
migrate = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migrate.py' % (v + 1))
# new temp_module for new migrate
temp_module = imp.new_module('old_model')
# the old model
old_model = api.create_model(SQLALCHEMY_MIGRATE_REPO, SQLALCHEMY_DATABASE_URL)
# exec the method of new model
exec(old_model, temp_module)

script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URL, SQLALCHEMY_MIGRATE_REPO,
                                          temp_module.meta,
                                          db.metadata)
open(migrate, "wt").write(script)

api.upgrade(SQLALCHEMY_DATABASE_URL, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URL, SQLALCHEMY_MIGRATE_REPO)
print("New migarate saved as  "+ migrate)

print("Current version is " +v)
