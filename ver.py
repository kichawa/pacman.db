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
                    filename VARCHAR(256),
                    version VARCHAR(64),
                    desc TEXT,
                    groups VARCHAR(64),
                    csize INT,
                    isize INT,
                    md5sum TEXT,
                    url TEXT,
                    license VARCHAR(32),
                    arch VARCHAR(6),
                    builddate TIMESTAMP,
                    packager TEXT,
                    replaces VARCHAR(128)
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
                    filename=:filename),
                    version=:version,
                    desc=:desc,
                    groups=:groups,
                    csize=:csize,
                    isize=:isize,
                    md5sum=:md5sum,
                    url=:url,
                    license=:license,
                    arch=:arch,
                    builddate=:builddate,
                    packager=:packager,
                    replaces=:replaces
                WHERE
                    name=:name
                ''', p)
            else:
                c.execute('''
                INSERT INTO
                    packages(name, filename, version, desc, groups,
                        isize, csize, md5sum, url, license, arch,
                        builddate, packager, replaces)
                VALUES
                    (:name, :filename, :version, :desc, :groups,
                        :isize, :csize, :md5sum, :url, :license, :arch,
                        :builddate, :packager, :replaces)
                ''', p)
            db.commit()

    def _db(self):
        return sqlite3.connect(self.db_path)

    def _prepare_pkg(self, p):
        p['builddate'] = int(p['builddate'])
        p['license'] = p.get('license', '')
        p['groups'] = p.get('groups', '')
        p['packager'] = p['packager'].decode("utf-8")
        if not 'replaces' in p:
            p['replaces'] = ""
        return p


def _example():
    pkg32 = DB('packages_32.sqlite3')
    pkg32.create()
    repo = pkglist.Repo('/var/lib/pacman/sync/core.db')
    for pkg in repo.packages():
        pkg32.add_or_update(**pkg)

if __name__ == '__main__':
    _example()
