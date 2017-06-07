import json


class ConversionIndex(object):
    def __init__(self, index_name=''):
        self.o2t = {}
        self.t2o = {}
        self.name = index_name

    def set_index(self, origin_index, target_index):
        self.o2t[origin_index] = target_index
        self.t2o[target_index] = origin_index

    def get_origin_by_target(self, target_index):
        return self.t2o[target_index]

    def is_origin_indexed(self, origin_index):
        return origin_index in self.o2t

    def get_target_by_origin(self, origin_index):
        return self.o2t[origin_index]

    def is_target_indexed(self, target_index):
        return target_index in self.t2o

    def reset(self):
        self.o2t = None
        self.t2o = None
        self.name = None

    def dump(self, file_name):
        obj = {
            'name': self.name,
            'o2t':  self.o2t,
            't2o':  self.t2o,
        }
        with open(file_name, 'w') as fp:
            json.dump(obj, fp)

    @staticmethod
    def load(file_name):
        with open(file_name, 'r') as fp:
            idx = ConversionIndex()
            obj = json.load(fp)
            idx.name = obj['name']
            idx.o2t = obj['o2t']
            idx.t2o = obj['t2o']

        return idx
