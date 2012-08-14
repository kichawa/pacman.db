import sqlite3
import argparse

class DB(object):
    def __init__(self, db_path):
        self.db_path = db_path

    def get_pkg(self, name):
        with self._db() as db:
            c = db.cursor()
            c.execute("SELECT * FROM packages WHERE name = '%s'" % name)
            """row = None
            for row in c:
                name = row[0]
                filename = row[1]"""
            return c.fetchall()

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

def _example_get(name):
    pkg32 = DB('packages_32.sqlite3')
    pkg = pkg32.get_pkg(name)
    if pkg:
        pkg = pkg.pop()
        return "Name: %s, version: %s." % (pkg[0], pkg[2])
    else:
        print "There is not pkg like %s " % name

def _example_search(pattern):
    pkg32 = DB('packages_32.sqlite3')
    pkgs = pkg32.search_pkg(pattern)
    if pkgs:
        for pkg in pkgs:
            yield pkg[0]
    else:
        print "There is not pkgs contain '%s'" % pattern

def search_print(items):
    packages = []
    for pkg in items:
        packages.append(pkg)
    packages = sorted(packages)
    if packages:
        output = ""
        for pkg in packages:
            output += pkg + ", "
        return "Found: " + output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search db with name of package')
    parser.add_argument('-n', '--name', help='show info about pkg')
    parser.add_argument('-s', '--search', help='show pkgs fit to pattern', nargs='*')

    args = parser.parse_args()

    name = args.name
    search = args.search
    pkgs = []
    if name:
        print _example_get(name)
    if search:
        if len(search) > 3:
            print "Too much patterns"
        else:
            for item in search:
                if len(item) > 2:
                    print search_print(_example_search(item))
                else:
                    print "Your pattern '%s' is too short." % item

