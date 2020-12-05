# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

try:
    from trytond.modules.iversta_tryton.tests.test_iversta_tryton import suite  # noqa: E501
except ImportError:
    from .test_iversta_tryton import suite

__all__ = ['suite']
