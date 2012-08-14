import sqlite3
import pkglist

#TODO:
#m2m or json with pkg_id
#depends
#optdepends
#conflicts
#provides
#{'': '', '%DEPENDS%': '', '%CONFLICTS%': '', '%OPTDEPENDS%': '', '%PROVIDES%': ''}

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
                    sha256sum TEXT,
                    pgpsig TEXT,
                    url TEXT,
                    license VARCHAR(32),
                    arch VARCHAR(6),
                    builddate TIMESTAMP,
                    packager TEXT,
                    replaces VARCHAR(128),
                    depends TEXT
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
                    filename=:filename,
                    version=:version,
                    desc=:desc,
                    groups=:groups,
                    csize=:csize,
                    isize=:isize,
                    md5sum=:md5sum,
                    sha256sum=:sha256sum,
                    pgpsig=:pgpsig,
                    url=:url,
                    license=:license,
                    arch=:arch,
                    builddate=:builddate,
                    packager=:packager,
                    replaces=:replaces,
                    depends=:depends
                WHERE
                    name=:name
                ''', p)
            else:
                c.execute('''
                INSERT INTO
                    packages(name, filename, version, desc, groups,
                        isize, csize, md5sum, sha256sum, pgpsig, url, license, arch,
                        builddate, packager, replaces, depends)
                VALUES
                    (:name, :filename, :version, :desc, :groups,
                        :isize, :csize, :md5sum, :sha256sum, :pgpsig, :url, :license, :arch,
                        :builddate, :packager, :replaces, :depends)
                ''', p)
            db.commit()

    def _db(self):
        return sqlite3.connect(self.db_path)

    def _prepare_pkg(self, pkg): #packages):
        pp = pkg['desc']
        pp['builddate'] = int(pp['builddate'])
        pp['license'] = pp.get('license', '')
        pp['groups'] = pp.get('groups', '')
        pp['packager'] = pp['packager'].decode("utf-8")
        if not 'replaces' in pp:
            pp['replaces'] = ""
        pp['depends'] = pkg['depends']
        return pp


def _example():
    pkg32 = DB('packages_32.sqlite3')
    pkg32.create()
    repo = pkglist.Repo('core.db')
    for packages in repo.packages():
        for name, pkg in packages.iteritems():
            pkg32.add_or_update(**pkg)

if __name__ == '__main__':
    _example()
