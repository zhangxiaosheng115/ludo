# coding=utf-8


class SqlModelMixin(object):

    def to_dict(self):
        result_dict = self.__dict__.copy()
        result_dict.pop('_sa_instance_state', '')
        return result_dict