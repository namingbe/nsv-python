class Writer:
    META_SEPARATOR = '---'

    def __init__(self, file_obj, version='1.0', metadata=()):
        self._file_obj = file_obj
        self.version = version
        self.metadata = metadata
        self._write_header()
        self._at_start = True

    def _write_header(self):
        if self.version == '1.0':
            self._file_obj.write("v:1.0\n")
        else:
            raise ValueError("Invalid version number")
        for line in self.metadata:
            self._file_obj.write(f'{line}\n')
        self._file_obj.write(f'{Writer.META_SEPARATOR}\n')

    def write_row(self, row):
        if self._at_start:
            self._at_start = False
        else:
            # print(repr('\n'))
            self._file_obj.write('\n')
        if row:
            chunk = ''.join(f'{Writer.escape(str(cell))}\n' if cell else '\\\n' for cell in row)
            # print(repr(chunk))
            self._file_obj.write(chunk)
        else:
            # print(repr('\n'))
            self._file_obj.write('\n')

    def write_rows(self, rows):
        for row in rows:
            self.write_row(row)

    @staticmethod
    def escape(s):
        if s == '':
            return '\\'
        return s.replace("\\", "\\\\").replace("\n", "\\n")  # i know
