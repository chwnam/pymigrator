import re
from types import FunctionType, LambdaType

from .tables import Table

_pattern_type = re.compile('t').__class__


class FieldValueGroupCollection(object):
    """
    테이블에서 특정 필드-값을 가진 개체를 그룹화한다.
    """

    def __init__(self, table):
        """
        :param table:
        :type  table: Table
        """
        self.table = table
        self.collections = {}

    def create_collection(self, name, **kwargs):
        """
        :param name: 콜렉션의 이름
        :type  name: string

        :param kwargs: 키는 테이블에 정의된 필드 이름,
                       값은 None, 스칼라값, 정규식, 호출 가능한 객체 중 하나.
                       None 이면 값의 종류별로 모두 골라낸다.
                       정규식은 re.compile() 된 객체이며 .match() 메소드를 통해 매칭되어야 한다.
                       호출 가능한 객체는 객체의 호출 값에 대해 수집 여부를 조사한다. True/False 리턴해야 한다.
                       스칼라값은 해당 값만을 가지도록 한다.
        """
        keys = sorted(kwargs.keys())
        for key in keys:
            if key not in self.table.headers():
                raise Exception('Keys does not match to the table.')

        collection = {}
        is_callable = {}
        is_regex = {}

        for key in keys:
            value = kwargs[key]
            is_callable[key] = isinstance(value, FunctionType) or isinstance(value, LambdaType)
            is_regex[key] = isinstance(value, _pattern_type)

        for idx, row in enumerate(self.table):
            collectible = True

            for key in keys:
                value = kwargs[key]
                if value:
                    if is_callable:
                        collectible = value(idx, row)
                    elif is_regex:
                        collectible = bool(value.match(v))
                    else:
                        collectible = row[key] == value
                    if not collectible:
                        break

            if collectible:
                key = '-'.join(['%s:%s' % (k, row[k]) for k in keys])
                if key not in collection:
                    collection[key] = []
                collection[key].append(idx)

        self.collections[name] = collection

    def get_collection(self, name):
        """
        이름으로 콜렉션을 찾는다.
        :param name:
        :return:
        """
        if not self.has_collection(name):
            return None

        return self.collections[name]

    def has_collection(self, name):
        return name in self.collections
