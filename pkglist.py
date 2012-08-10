import tarfile


class Repo(object):
    def __init__(self, path):
        self.path = path

    def _packages(self):
        with tarfile.open(self.path) as tar:
            for member in tar.getmembers():
                if not member.name.endswith('/desc'):  # and not member.name.endswith('/depends'):
                    continue
                tarfd = tar.extractfile(member)
                yield tarfd.read()

    def _parse_package_file(self, raw):
        pkg = {}
        chunks = raw.split('\n\n')
        for chunk in chunks:
            try:
                splited = chunk.split('\n')
                #print splited
                l = len(splited)
                typename = splited[0]
                value = []
                for i in range(1, l):
                    value.append(splited[i])
                #typename, value = chunk.split('\n')
            except ValueError:
                continue
            pkg[typename[1:-1].lower()] = ", ".join(value)
            #pkg[typename[1:-1].lower()] = value
        return pkg

    def packages(self):
        for raw in self._packages():
            yield self._parse_package_file(raw)


def _example():
    r = Repo('core.db')
    #i = 0
    for pkg in r.packages():
        print pkg
        #i += 1
        #print i
        """if pkg['name'] == 'wget':
            for info, name in pkg.iteritems():
                print info, name"""

if __name__ == '__main__':
    _example()
