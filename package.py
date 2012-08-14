import sqlite3
import argparse

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
            row = None
            for row in c:
                name = row[0]
                filename = row[1]
            return row

    def search_pkg(self, name):
        with self._db() as db:
            c = db.cursor()
            c.execute('''SELECT * FROM packages WHERE name LIKE "%%%s%%"''' % name)
            #row = None
            #for row in c:
            #    name = row[0]
            #    filename = row[1]
            return c.fetchall()

    def _db(self):
        return sqlite3.connect(self.db_path)

def _example(name):
    pkg32 = DB('packages_32.sqlite3')
    pkg = pkg32.get_pkg(name)
    if pkg:
        print pkg
    else:
        print "There is not pkg like %s " % name

def _example_search(pattern):
    pkg32 = DB('packages_32.sqlite3')
    pkgs = pkg32.search_pkg(pattern)
    if pkgs:
        for pkg in pkgs:
            print pkg
    else:
        print "There is not pkgs contain '%s'" % pattern

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Search db with name of package')
    parser.add_argument('-n', '--name', help='show info about pkg')
    parser.add_argument('-s', '--search', help='show pkgs fit to patterns')

    args = parser.parse_args()

    name = args.name
    search = args.search
    if name:
        _example(name)
    if search:
        _example_search(search)
        
