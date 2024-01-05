# dop_be

## Creating an Environment
With a basic understanding of what the environment is, we can create one using alembic init. This will create an environment using the “generic” template:
```commandline
cd /path/to/yourproject
source /path/to/yourproject/.venv/bin/activate   # assuming a local virtualenv
alembic init alembic
```
Where above, the init command was called to generate a migrations directory called alembic:
```commandline
Creating directory /path/to/yourproject/alembic...done
Creating directory /path/to/yourproject/alembic/versions...done
Generating /path/to/yourproject/alembic.ini...done
Generating /path/to/yourproject/alembic/env.py...done
Generating /path/to/yourproject/alembic/README...done
Generating /path/to/yourproject/alembic/script.py.mako...done
Please edit configuration/connection/logging settings in
'/path/to/yourproject/alembic.ini' before proceeding.
```

Alembic also includes other environment templates. These can be listed out using the list_templates command:
```commandline
alembic list_templates
Available templates:

async - Generic single-database configuration with an async dbapi.
multidb - Rudimentary multi-database configuration.
generic - Generic single-database configuration.

Templates are used via the 'init' command, e.g.:

  alembic init --template generic ./scripts
```

For starting up with just a single database and the generic configuration, setting up the SQLAlchemy URL is all that’s needed:
```commandline
sqlalchemy.url = postgresql://scott:tiger@localhost/test
```

## Create a Migration Script
```commandline
$ alembic revision -m "create account table"
Generating /path/to/yourproject/alembic/versions/1975ea83b712_create_accoun
t_table.py...done
```
A new file 1975ea83b712_create_account_table.py is generated. Looking inside the file:
```doctest
"""create account table

Revision ID: 1975ea83b712
Revises:
Create Date: 2011-11-08 11:40:27.089406

"""

# revision identifiers, used by Alembic.
revision = '1975ea83b712'
down_revision = None
branch_labels = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    pass

def downgrade():
    pass
```

## Running our First Migration
```commandline
$ alembic upgrade head
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade None -> 1975ea83b712
```

## Getting Information
With a few revisions present we can get some information about the state of things.
First we can view the current revision:
```commandline
$ alembic current
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
Current revision for postgresql://scott:XXXXX@localhost/test: 1975ea83b712 -> ae1027a6acf (head), Add a column
```
head is displayed only if the revision identifier for this database matches the head revision.
We can also view history with alembic history; the --verbose option (accepted by several commands, including history, current, heads and branches) will show us full information about each revision:
```commandline
$ alembic history --verbose

Rev: ae1027a6acf (head)
Parent: 1975ea83b712
Path: /path/to/yourproject/alembic/versions/ae1027a6acf_add_a_column.py

    add a column

    Revision ID: ae1027a6acf
    Revises: 1975ea83b712
    Create Date: 2014-11-20 13:02:54.849677

Rev: 1975ea83b712
Parent: <base>
Path: /path/to/yourproject/alembic/versions/1975ea83b712_add_account_table.py

    create account table

    Revision ID: 1975ea83b712
    Revises:
    Create Date: 2014-11-20 13:02:46.257104
```
- reference: 
  - https://alembic.sqlalchemy.org/en/latest/tutorial.html
  - https://blog.jerrycodes.com/multiple-heads-in-alembic-migrations/
### Create system settings table
- Require:
```commandline
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```
Init system_settings_table:
```commandline
insert into system_settings (id, is_maintain)
values (uuid_generate_v4(), false)
```


