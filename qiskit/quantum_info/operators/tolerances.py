# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Tolerances mixin class.
"""

import warnings

from qiskit.exceptions import QiskitError
from qiskit.quantum_info.operators.predicates import ATOL_DEFAULT, RTOL_DEFAULT


class TolerancesMeta(type):
    """Metaclass to handle tolerances"""
    def __init__(cls, *args, **kwargs):
        cls._ATOL_DEFAULT = ATOL_DEFAULT
        cls._RTOL_DEFAULT = RTOL_DEFAULT
        cls._MAX_TOL = 1e-4
        super().__init__(cls, args, kwargs)

    @property
    def atol(cls):
        """The default absolute tolerance parameter for float comparisons."""
        return cls._ATOL_DEFAULT

    def _check_value(cls, value, value_name):
        """Check if value is within valid ranges"""
        if value < 0:
            raise QiskitError(
                "Invalid {} ({}) must be non-negative.".format(value_name, value))
        if value > cls._MAX_TOL:
            raise QiskitError(
                "Invalid {} ({}) must be less than {}.".format(value_name, value, cls._MAX_TOL))

    @atol.setter
    def atol(cls, value):
        """Set the class default absolute tolerance parameter for float comparisons."""
        cls._check_value(value, "atol")  # pylint: disable=no-value-for-parameter
        cls._ATOL_DEFAULT = value

    @property
    def rtol(cls):
        """The relative tolerance parameter for float comparisons."""
        return cls._RTOL_DEFAULT

    @rtol.setter
    def rtol(cls, value):
        """Set the class default relative tolerance parameter for float comparisons."""
        cls._check_value(value, "rtol")  # pylint: disable=no-value-for-parameter
        cls._RTOL_DEFAULT = value


class TolerancesMixin(metaclass=TolerancesMeta):
    """Mixin Class for tolerances"""

    @property
    def atol(self):
        """The default absolute tolerance parameter for float comparisons."""
        return self.__class__.atol

    @property
    def rtol(self):
        """The relative tolerance parameter for float comparisons."""
        return self.__class__.rtol

    @classmethod
    def set_atol(cls, value):
        """Set the class default absolute tolerance parameter for float comparisons.

        DEPRECATED: use operator.atol = value instead
        """
        warnings.warn("`{}.set_atol` method is deprecated, use `{}.atol = "
                      "value` instead.".format(cls.__name__, cls.__name__),
                      DeprecationWarning)
        cls.atol = value

    @classmethod
    def set_rtol(cls, value):
        """Set the class default relative tolerance parameter for float comparisons.

        DEPRECATED: use operator.rtol = value instead
        """
        warnings.warn("`{}.set_rtol` method is deprecated, use `{}.rtol = "
                      "value` instead.".format(cls.__name__, cls.__name__),
                      DeprecationWarning)
        cls.rtol = value
