import logging
import json
import pickle
from pathlib import Path
from typing import Union
from collections import OrderedDict

# import pandas as pd

logger = logging.getLogger(__name__)
DEFAULT_ENCODING = 'utf-8'
# CSV_ENCODING = 'cp950'
#
#
# def save_csv(data, path, exist_ok=True, mode='w', encoding=DEFAULT_ENCODING, **kwargs) -> None:
#     path = _prepare_write_path(path, exist_ok)
#     if not isinstance(data, pd.DataFrame):
#         data = pd.DataFrame(data)
#     data.to_csv(path, mode=mode, encoding=encoding, **kwargs)
#
#
# def read_csv(path, encoding=DEFAULT_ENCODING, sep=',', **kwargs) -> pd.DataFrame:
#     path = _prepare_read_path(path)
#     if path:
#         return pd.read_csv(path, sep=sep, encoding=encoding, **kwargs)
#
#
# def read_table(path, encoding=DEFAULT_ENCODING, sep='\t', **kwargs) -> pd.DataFrame:
#     path = _prepare_read_path(path)
#     if path:
#         return pd.read_table(path, sep=sep, encoding=encoding, **kwargs)


def read_json(path: Union[str, Path], encoding=DEFAULT_ENCODING, **kwargs) -> dict:
    path = _prepare_read_path(path)
    if path:
        with path.open(encoding=encoding, **kwargs) as f_in:
            return json.load(f_in, object_pairs_hook=OrderedDict)


def save_json(data: dict, path: Union[str, Path], encoding=DEFAULT_ENCODING, **kwargs) -> None:
    with open(path, 'w', encoding=encoding, **kwargs) as f_out:
        json.dump(data, f_out, ensure_ascii=False, indent=2)


def load_pickle(path, **kwargs):
    path = _prepare_read_path(path)
    if path:
        if 'mode' in kwargs:
            kwargs.pop('mode')
            logger.warning('Use "rb" as pickle file mode')
        with path.open('rb', **kwargs) as f_in:
            return pickle.load(f_in)


def save_pickle(data, path, exist_ok=True, **kwargs) -> None:
    path = _prepare_write_path(path, exist_ok)
    if 'mode' in kwargs:
        kwargs.pop('mode')
        logger.warning('Use "wb" as pickle file mode')
    with path.open('wb') as f_out:
        pickle.dump(data, f_out)


def save_list_as_txt(data: list, path, exist_ok=True, encoding=DEFAULT_ENCODING, **kwargs) -> None:
    path = _prepare_write_path(path, exist_ok)
    data = [str(i) for i in data]
    path.write_text('\n'.join(data), encoding=encoding, **kwargs)


def load_list_from_txt(path: Union[str, Path], inner_type=str, encoding=DEFAULT_ENCODING) -> list:
    return_list = []

    path = _prepare_read_path(path)
    if path:
        with path.open(encoding=encoding) as f:
            for line in f.readlines():
                return_list.append(inner_type(line.replace('\n', '')))
    else:
        logger.exception(f'FileNotFound: "{path}", return empty list')

    return return_list


def get_file_name(path: Union[str, Path], with_suffix=False) -> str:
    path = _formatted_path(path)
    if with_suffix:
        return path.name
    else:
        return path.stem


def _prepare_read_path(path: Union[str, Path]) -> Union[Path, None]:
    path = _formatted_path(path)
    if not path.exists():
        logger.exception(f'[FileNotFound]: "{path}"')
        return None
    return path


def _prepare_write_path(path: Union[str, Path], exist_ok=False) -> Path:
    path = _formatted_path(path)
    path.touch(exist_ok=exist_ok)
    return path


def _formatted_path(path: Union[str, Path]) -> Path:
    if isinstance(path, str):
        path = Path(path)
    return path
