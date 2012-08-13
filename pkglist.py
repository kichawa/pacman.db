import tarfile


class Repo(object):
    def __init__(self, path):
        self.path = path

    def _packages(self):
        with tarfile.open(self.path) as tar:
            pkg = {}
            for member in tar.getmembers():
                splited = member.name.split('/')
                if not splited[0] in pkg:
                    pkg[splited[0]] = {} 
                if len(splited) > 1:
                    parse = self._parse_package_file(tar.extractfile(member).read())
                    if splited[1] == 'desc':
                        pkg[splited[0]]['desc'] = parse
                    elif splited[1] == 'depends':
                        pkg[splited[0]]['depends'] = parse
                    else:
                        continue
            yield pkg
    
    def _parse_package_file(self, raw):
        chunks = raw.split('\n\n')
        pkg = {}
        for chunk in chunks:
            try:
                splited = chunk.split('\n')
                l = len(splited)
                typename = splited[0]
                value = []
                for i in range(1, l):
                    value.append(splited[i])
            except ValueError:
                continue
            pkg[typename[1:-1].lower()] = ", ".join(value)
        return pkg

    def packages(self):
        return self._packages()


def _example():
    r = Repo('core.db')
    for pkg in r.packages():
        pkg

if __name__ == '__main__':
    _example()
