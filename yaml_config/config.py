from os import path

from no_config import Config


@Config
class Teach:
    name = None
    age = None


@Config
class Student:
    name = None
    age = None


@Config
class DatalabMarker:
    debug = None
    DEVICE = None
    MODEL_CACHE_DIR = None


if __name__ == '__main__':
    Config.init(file_path='./config.yaml')
    print(Teach.name)
    print(Student.name)
    print(DatalabMarker.debug)
