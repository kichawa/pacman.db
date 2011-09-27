import tarfile


class Repo(object):
    def __init__(self, path):
        self.path = path

    def _packages(self):
        with tarfile.open(self.path) as tar:
            for member in tar.getmembers():
                if not member.name.endswith('/desc'):
                    continue
                tarfd = tar.extractfile(member)
                yield tarfd.read()

    def _parse_package_file(self, raw):
        pkg = {}
        chunks = raw.split('\n\n')
        for chunk in chunks:
	    try:
                typename, value = chunk.split('\n')
            except ValueError:
                continue
            pkg[typename[1:-1].lower()] = value
        return pkg

    def packages(self):
        for raw in self._packages():
            yield self._parse_package_file(raw)


def _example():
    r = Repo('/var/lib/pacman/sync/core.db')
    for pkg in r.packages():
        print pkg

if __name__ == '__main__':
    _example()
