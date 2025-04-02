class Writer:
    META_SEPARATOR = '---'

    def __init__(self, file_obj, version='1.0', metadata=()):
        self._file_obj = file_obj
        self.version = version
        self.metadata = metadata
        self._write_header()

    def _write_header(self):
        if self.version == '1.0':
            self._file_obj.write("v:1.0\n")
        else:
            raise ValueError("Invalid version number")
        self._file_obj.write('\n'.join(self.metadata))
        self._file_obj.write(f'\n{Writer.META_SEPARATOR}\n')

    def write_elem(self, elem):
        if elem != '':
            chunk = ''.join(f'{Writer.escape(str(line))}\n' if line else '\\\n' for line in elem)
            self._file_obj.write(chunk)
        else:
            self._file_obj.write('\n')
        self._file_obj.write('\n')

    def write_elems(self, elems):
        for elem in elems:
            self.write_elem(elem)

    @staticmethod
    def escape(s):
        if s == '':
            return '\\'
        return s.replace("\\", "\\\\").replace("\n", "\\n")  # i know
