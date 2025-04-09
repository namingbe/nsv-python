class Reader:
    META_SEPARATOR = '---\n'

    def __init__(self, file_obj):
        self._file_obj = file_obj
        self.version = None
        self.metadata = []
        self._line = 0  # Solely for error reporting
        self._parse_header()

    def _parse_header(self):
        for line in self._file_obj:
            self._line += 1
            if line == Reader.META_SEPARATOR:
                break
            if line == 'v:1.0\n':
                self.version = '1.0'
            self.metadata.append(line[:-1])
        else:
            raise ValueError("Invalid NSV: End of input encountered before end of header")

        if self.version is None:
            raise ValueError("Invalid NSV: Missing version information")

    def __iter__(self):
        return self

    def __next__(self):
        acc = []
        for line in self._file_obj:
            self._line += 1
            if line == '\n':
                return acc
            if line == '\\\n':  # empty cell
                acc.append('')
            else:  # non-empty cell
                if line[-1] == '\n':  # so as not to chop if missing newline at EOF
                    line = line[:-1]
                acc.append(Reader.unescape(line))  # bruh
        # at the end of file
        if acc:
            return acc
        else:  # an empty row would self-report in the cycle body
            raise StopIteration

    @staticmethod
    def unescape(s):
        if s == '\\':
            return ''
        return s.replace("\\n", "\n").replace("\\\\", "\\")  # i know
