from pytest import raises

from pysdvu.error import BaseError


def test_baseerror():
    with raises(BaseError):
        raise BaseError()
