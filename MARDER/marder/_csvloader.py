"""CSV loader."""
import csv
from errno import EPERM
from os import strerror
import numpy as np
from typing import Any, List, Literal, TextIO, Tuple
import numpy.typing as npt
from tempfile import TemporaryFile
from _csv import Reader
import re

type _Array2D[TValue] = np.ndarray[
    Tuple[int, int],
    np.dtype[TValue]
]


def _load_csv_as_reader(
    file: TextIO
) -> Reader:
    """Automatically formatted csv reader generator.

    Parameters
    ----------
    file : TextIO

    Returns
    -------
    result : Reader

    Raises
    ------
    PermissionError
        When the operation is not allowed.
    """
    if ((not file.readable()) or (not file.seekable())):
        raise PermissionError(strerror(EPERM))
    file.seek(0)
    dialect = csv.Sniffer().sniff(file.read(1024))
    file.seek(0)
    result: Reader = csv.reader(file, dialect=dialect)
    return result


def load_csv_as_matrix(
    file: TextIO,
    skipfirstln: bool = True
) -> _Array2D[np.floating[Any]]:
    """Converts CSV file to an ``ndarray``.

    Parameters
    ----------
    file : TextIO
        The csv file to be loaded.
    skipfirstln : bool, default True
        Indicates whether loader should skip the first line as a title row.

    Returns
    -------
    array : An 2-d array.
        The converted result.

    Raises
    ------
    PermissionError
        When the read operation is not supported
        for the given IO.
    """
    try:
        reader = _load_csv_as_reader(file)
    except PermissionError as e:
        raise e.with_traceback()
    data: List[List[float]] = list()
    for row in reader:
        if (reader.line_num == 1 and skipfirstln):
            continue
        try:
            floatedrow: List[float] = [
                float(t) for t in row
            ]
            data.append(floatedrow)
        except ValueError as e:
            raise e.with_traceback()
        except Exception as err:
            raise err.with_traceback()
        except BaseException as be:
            exit(0)

    array: _Array2D = np.array(data)
    return array


def load_csv_as_tex(
    file: TextIO
) -> str:
    """Returns a table in LaTeX format.

    Parameters
    ----------
    file : TextIO
        The csv file to be converted.

    Returns
    -------
    result : str
        The LaTeX table code.

    Raises
    ------
    PermissionError
        When the file cannot be read.
    """
    try:
        reader = _load_csv_as_reader(file)
    except PermissionError as err:
        raise err.with_traceback()

    with TemporaryFile('w+t', encoding='utf_8_sig', newline='\r\n') as tf:
        heading: List[str] = [
            '\\begin{table}[tp]\n',
            '    \\begin{talltblr}[\n',
            '        caption = {},\n',
            '        label = {}\n',
            '        note{a} = {}\n',
            '    ]{\n',
            '        colspec = {@{}\n'
        ]
        for row in reader:
            if (reader.line_num == 1):
                cols: List[
                    Literal['            S\n']
                ] = ['            S\n'] * len(row)
                heading += cols
                heading.append('        @{}}\n')
                heading.append('    }\n')
                tf.writelines(heading)
                frow = (
                    ' ' * 8
                    ) + (
                        '} &\n' + (
                            ' ' * 8
                        ) + '{'
                    ).join(row) + '}\\\\\n'
                tf.write(frow)
                continue
            pattern = r'\-?\d+\.?\d*(\(\d+\))?(e\-?\d+)?'
            reg = re.compile(pattern)
            drow: List[str] = list()
            for item in row:
                if (reg.fullmatch(item) is None):
                    drow.append(f'{{{item}}}')
                else:
                    drow.append(item)
            tf.write(
                (' ' * 8) + ' & '.join(drow) + '\\\\\n'
            )
        footer: Tuple[
            Literal['    \\end{talltblr}\n'],
            Literal['\\end{table}']
        ] = (
            '    \\end{talltblr}\n',
            '\\end{table}'
        )
        tf.writelines(footer)
        tf.seek(0)
        result = tf.read()
    return result


def load_headers(
    file: TextIO
) -> List[str]:
    """Gets the header row of the csv.

    Parameters
    ----------
    file : TextIO
        The csv file.
    """
