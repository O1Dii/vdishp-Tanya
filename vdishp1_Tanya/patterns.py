import pandas as pd

from collections.abc import Iterable, Iterator


class MyIterator(Iterator):
    _position: int = None
    _reverse: bool = False

    def __init__(self, collection: Iterable, reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value


class MyCollection(Iterable):
    def __init__(self, collection: Iterable = []) -> None:
        self._collection = list(collection)

    def __iter__(self) -> MyIterator:
        return MyIterator(self._collection)

    def get_reverse_iterator(self) -> MyIterator:
        return MyIterator(self._collection, True)

    def sort_items(self):
        self._collection.sort()

    def add_item(self, item):
        self._collection.append(item)


class SingletonMeta(type):
    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()

        return self._instance


class DataFrameSingleton(metaclass=SingletonMeta):
    def __init__(self, df=None):
        if df is not None:
            self._df = df

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, df):
        self._df = df


from abc import ABC, abstractmethod


class Bus(ABC):
    @abstractmethod
    def get_df(self) -> pd.DataFrame:
        pass


class BusFromCsv(Bus):
    def get_df(self):
        return pd.read_csv('bus.csv', index_col='номер маршрута')


class BusFromJson(Bus):
    def get_df(self) -> pd.DataFrame:
        df = pd.read_json('bus.json')
        df.index.name = 'номер маршрута'
        return df


class Train(ABC):
    @abstractmethod
    def get_df(self) -> pd.DataFrame:
        pass


class TrainFromCsv(Train):
    def get_df(self) -> pd.DataFrame:
        return pd.read_csv('train.csv', index_col='номер маршрута')


class TrainFromJson(Train):
    def get_df(self) -> pd.DataFrame:
        df = pd.read_json('train.json')
        df.index.name = 'номер маршрута'
        return df


class AbstractFactory(ABC):
    @abstractmethod
    def create_bus(self) -> Bus:
        pass

    @abstractmethod
    def create_train(self) -> Train:
        pass


class CsvFactory(AbstractFactory):
    def create_bus(self) -> BusFromCsv:
        return BusFromCsv()

    def create_train(self) -> TrainFromCsv:
        return TrainFromCsv()


class JsonFactory(AbstractFactory):
    def create_bus(self) -> BusFromJson:
        return BusFromJson()

    def create_train(self) -> TrainFromJson:
        return TrainFromJson()
