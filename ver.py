import sqlite3

import pkglist



class DB(object):
    def __init__(self, db_path):
        self.db_path = db_path

    def create(self):
        with self._db() as db:
            c = db.cursor()
            try:
                c.execute('''
                CREATE TABLE packages(
                    name VARCHAR(128) PRIMARY KEY,
                    license VARCHAR(32),
                    builddate INT
                )
                ''')
            except sqlite3.OperationalError:
                pass
            db.commit()

    def add_or_update(self, **p):
        p = self._prepare_pkg(p)
        with self._db() as db:
            c = db.cursor()
            c.execute('SELECT 1 FROM packages WHERE name=:name', p)
            if c.fetchall():
                c.execute('''
                UPDATE
                    packages
                SET
                    license=:license,
                    builddate=:builddate
                WHERE
                    name=:name
                ''', p)
            else:
                c.execute('''
                INSERT INTO
                    packages(name, license, builddate)
                VALUES
                    (:name, :license, :builddate)
                ''', p)
            db.commit()

    def _db(self):
        return sqlite3.connect(self.db_path)

    def _prepare_pkg(self, p):
        p['builddate'] = int(p['builddate'])
        p['license'] = p.get('license', '')
        return p


def _example():
    pkg32 = DB('packages_32.sqlite3')
    pkg32.create()
    repo = pkglist.Repo('/var/lib/pacman/sync/core.db')
    for pkg in repo.packages():
        pkg32.add_or_update(**pkg)

if __name__ == '__main__':
    _example()