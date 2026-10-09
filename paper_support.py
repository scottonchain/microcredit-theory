"""Shared CSV input and LaTeX-table output; numerical models remain in their papers."""
import csv
from pathlib import Path


class PaperTables:
    def __init__(self, output, source, header):
        self.output = Path(output)
        self.source = Path(source)
        self.header = header

    def read(self, name, base=None):
        with (Path(base) if base is not None else self.source).joinpath(name).open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def write_tex(self, name, lines):
        with (self.output / name).open("w", encoding="utf-8") as handle:
            handle.write(self.header)
            for line in lines:
                handle.write(line + " \\\\\n")

    def write_csv(self, name, header, data):
        with (self.output / name).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
            writer.writerows(data)
