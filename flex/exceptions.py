import six
import collections

from flex.utils import (
    is_non_string_iterable,
    prettify_errors,
)

from rest_framework.serializers import ValidationError as DRFValidationError


class ErrorList(list):
    def __init__(self, value=None):
        super(ErrorList, self).__init__()
        if value:
            self.add_error(value)

    def add_error(self, error):
        if is_non_string_iterable(error) and not isinstance(error, collections.Mapping):
            map(self.add_error, error)
        else:
            self.append(error)


class ErrorDict(collections.defaultdict):
    def __init__(self, value=None):
        super(ErrorDict, self).__init__(ErrorList)
        for k, v in (value or {}).items():
            self.add_error(k, v)

    def add_error(self, key, error):
        self[key].add_error(error)


class ValidationError(DRFValidationError):
    def __init__(self, error):
        if not isinstance(error, collections.Mapping) and \
           is_non_string_iterable(error) and \
           len(error) == 1:
            error = error[0]
        self._error = error

        if isinstance(self._error, collections.Mapping):
            self.error_dict = self._error
        elif is_non_string_iterable(self._error):
            self.error_list = self._error

    def __repr__(self):
        return "<type '{0}'>, {1}".format(
            repr(type(self)),
            repr(self.detail),
        )

    def __str__(self):
        return prettify_errors(self._error)

    @property
    def detail(self):
        return self._error

    @property
    def messages(self):
        if isinstance(self._error, six.string_types):
            return [self._error]
        elif isinstance(self._error, collections.Mapping):
            return [self._error]
        return self._error
