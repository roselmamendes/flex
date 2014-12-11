import pytest

from flex.exceptions import ValidationError
from flex.decorators import (
    skip_if_not_of_type,
    rewrite_reserved_words,
    translate_validation_error,
)
from flex.constants import (
    NUMBER,
)

from django.core.exceptions import ValidationError as DjangoValidationError


#
# skip_if_not_of_type tests
#
@pytest.mark.parametrize(
    'v',
    (0, 1, 2, -2, 0.0, 1.0, 2.0, -2.0),
)
def test_type_enforcement_accepts_valid_types(v):
    @skip_if_not_of_type(NUMBER)
    def fn(value):
        return True

    assert fn(v) is True


@pytest.mark.parametrize(
    'v',
    (True, False, '', None, [], {}, 'abcd', ['a'], {'a': 1}),
)
def test_type_enforcement_detects_invalid_types(v):
    @skip_if_not_of_type(NUMBER)
    def fn(value):
        raise Exception('should not happen')

    fn(v)


#
# rewrite_reserved_words tests
#
def test_rewrite_of_reserved_word_in():
    @rewrite_reserved_words
    def fn(**kwargs):
        assert 'in_' not in kwargs
        assert 'in' in kwargs

    fn(in_=True)


#
# translate_validation_error tests
#
def test_flex_validation_error_is_untouched():
    err = ValidationError('foo')

    @translate_validation_error
    def fn():
        raise err

    try:
        fn()
    except Exception as raised_err:
        assert err is raised_err


def test_django_validation_error_is_converted():
    err = DjangoValidationError('foo')

    @translate_validation_error
    def fn():
        raise err

    try:
        fn()
    except Exception as raised_err:
        assert err is not raised_err
        assert isinstance(raised_err, ValidationError)
