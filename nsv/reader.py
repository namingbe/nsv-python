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
                if acc:  # end of row
                    return acc
                else:  # maybe empty row
                    self._line += 1
                    if next(self._file_obj) == '\n':  # definitely empty row
                        return []
                    else:
                        raise ValueError(f"Invalid NSV: Unexpected newline at line {self._line}")
            if line == '\\\n':  # empty cell
                acc.append('')
            else:  # non-empty cell
                acc.append(line[:-1])  # bruh
        # at the end of file
        if acc:
            return acc
        raise StopIteration
