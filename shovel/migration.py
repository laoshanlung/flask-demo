from shovel import task
import json
import psycopg2
import sys

from schemup import commands
from schemup.dbs import postgres
from schemup.validator import findSchemaMismatches

import config

# TODO: Put into Schemup
class DictSchema(object):
    def __init__(self, path):
        self.versions = json.load(open(path, "r"))

    def getExpectedTableVersions(self):
        return sorted(self.versions.iteritems())

@task
def run(action='nothing'):
    dryRun = action != 'commit'

    dbConfig = config.POSTGRES
    dbConfigParams = {
        "database": dbConfig["database"],
        "host": dbConfig["host"],
        "user": dbConfig["username"],
        "password": dbConfig["password"],
        "port": dbConfig["port"]
    }

    pgConn = psycopg2.connect(**dbConfigParams)

    pgSchema = postgres.PostgresSchema(pgConn, dryRun=dryRun)

    dictSchema = DictSchema("schema/versions.json")

    pgSchema.ensureSchemaTable()

    # Ensure current DB's integrity
    schemaMismatches = findSchemaMismatches(pgSchema)
    if schemaMismatches:
        print "Real schema & 'schemup_tables' are out of sync"
        for mismatch in schemaMismatches:
            print mismatch, "\n"
        sys.exit(1)

    commands.load('schema/migrations')
    sqls = commands.upgrade(pgSchema, dictSchema)

    if dryRun and sqls:
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        for sql in sqls: print sql
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        sys.exit(1)

    commands.validate(pgSchema, dictSchema)
