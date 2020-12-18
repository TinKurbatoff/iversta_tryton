# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import iversta_tryton as iversta

__all__ = ['register']


def register():
    Pool.register(
        iversta.IverstaAssessments,
        iversta.AssessmentChain,
        iversta.AssessmentImage,
        iversta.LoginsToApp,
        module='iversta_tryton', type_='model')
    Pool.register(
        module='iversta_tryton', type_='wizard')
    Pool.register(
        module='iversta_tryton', type_='report')
