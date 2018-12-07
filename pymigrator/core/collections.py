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

    def create_collection(self, field, name=None, value=None):
        """
        :param field: 테이블에 반드시 포함되어 있어야 한다.
        :type  field: string

        :param name: 콜렉션의 이름을 준다. 안 주면 필드값으로 준다. 한 필드에 여러 콜렉션을 생성하고 싶으면 이름으로 구분한다.
        :type  name: string

        :param value: 값은 None, 스칼라값, 정규식, 호출 가능한 객체 중 하나.
                      None 이면 값의 종류별로 모두 골라낸다.
                      정규식은 re.compile() 된 객체이며 .match() 메소드를 통해 매칭되어야 한다.
                      호출 가능한 객체는 객체의 호출 값에 대해 수집 여부를 조사한다. True/False 리턴해야 한다.
                      스칼라값은 해당 값만을 가지도록 한다.
        """
        if field not in self.table.headers():
            raise Exception('Keys does not match to the table.')

        collection = {}

        is_callable = isinstance(value, FunctionType) or isinstance(value, LambdaType)
        is_regex = isinstance(value, _pattern_type)

        for idx, row in enumerate(self.table):
            if value:
                if is_callable:
                    v = row[field]
                    collectible = value(idx, row)
                elif is_regex:
                    v = row[field]
                    collectible = bool(value.match(v))
                else:
                    v = value
                    collectible = row[field] == v
            else:
                v = row[field]
                collectible = True

            if collectible:
                if v not in collection:
                    collection[v] = []
                collection[v].append(idx)

        if name is None:
            name = field

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
