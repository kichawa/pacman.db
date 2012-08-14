import sqlite3

#TODO:
#m2m or json with pkg_id
#depends (in db)
#optdepends (in db)
#conflicts (out of scope)
#provides (out of scope)
#{'': '', '%DEPENDS%': '', '%CONFLICTS%': '', '%OPTDEPENDS%': '', '%PROVIDES%': ''}

class DB(object):
    def __init__(self, db_path):
        self.db_path = db_path

    def get_pkg(self, name):
        with self._db() as db:
            c = db.cursor()
            c.execute("SELECT * FROM packages WHERE name = '%s'" % name)
            for row in c:
                name = row[0]
                filename = row[1]
                print name, filename
            db.commit()

    def _db(self):
        return sqlite3.connect(self.db_path)

def _example(name):
    pkg32 = DB('packages_32.sqlite3')
    pkg32.get_pkg(name)

if __name__ == '__main__':
    _example('linux')
