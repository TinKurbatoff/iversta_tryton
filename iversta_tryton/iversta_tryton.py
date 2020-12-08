from trytond.model import ModelView
from trytond.model import ModelSQL
from trytond.model import (ModelStorage, fields)


import os.path


__all__ = [ 'IverstaAssessments',
            'AssessmentImage',
            ] 

module_path = os.path.dirname(__file__)


###########################  Class describes Vehicle ###############################
class IverstaAssessments(ModelSQL, ModelView):
    # description (mandatory on first declaration)
    'Assessments'

    # Internal class name. Always used as a reference inside Tryton
    # default: '<module_name>.<class_name>' on Tryton
    # becomes '<module_name>_<class_name>' in the database
    __name__ = 'iversta.assessment'


    # ———————————————- One2Many Many2One fields ——————————————————————————
    images = fields.One2Many('iversta.image', 'assessment', 'All images')
    # ———————————————————— Function fields —————————————————————————

    # ———————————————————— Plain fields ————————————————————————————
    assess_datetime = fields.DateTime("Assessed on",
        context={'date_format':'%b %d, %Y', 'time_fromat':'%I:%M:%s %p'},
        #format='%I:%M %p',
        required=False,
        )
    license_plate = fields.Char('License plate', help = '1-8 chars, car license plate like XXX-XXX')#: (16 chars)
    VIN = fields.Char('VIN', size=17, required = False, help = 'VIN is 17-char string');
    rental_file_num = fields.Char('Rental file #', size=64, help = 'Format: IVR-xxxxx-YYZ-xx'); #: 64 chars 
    odosize = fields.Numeric('Odometer', help = 'Type the most recent odometer measure' )#: (long integer) #// number
    images_qty = fields.Integer('Images')#: (integer) // if needed?
    damages_qty = fields.Integer('Damages')#: (integer) // if needed?
    
class AssessmentImage(ModelSQL, ModelView):
     #docstring for AssessmentImage
    'Image of Assessment'

    # Internal class name. Always used as a reference inside Tryton
    # default: '<module_name>.<class_name>' on Tryton
    # becomes '<module_name>_<class_name>' in the database
    __name__ = 'iversta.image'

    # ———————————————- One2Many Many2One fields ——————————————————————————
    assessment = fields.Many2One('iversta.assessment','Assessment set', ondelete='RESTRICT', select=True)

    # ———————————————————— Plain fields ————————————————————————————
    license_plate = fields.Char('License plate', help = '1-8 chars, car license plate like XXX-XXX')#: (16 chars)
    VIN = fields.Char('VIN', size=17, required = False, help = 'VIN is 17-char string');
    rental_file_num = fields.Char('Rental file #', size=64, help = 'Firmat: IVR-xxxxx-YYZ-xx'); #: 64 chars 
    odosize = fields.Numeric('Odometer', help = 'Type the most recent odometer measure' )#: (long integer) #// number
    image = fields.Binary('File', readonly=True, filename='filename')
    filename = fields.Char('File Name', readonly=True)
    date_taken = fields.DateTime('Image taken on',
        context={'date_format':'%b %d, %Y', 'time_fromat':'%I:%M:%s %p'},)

'''
class SaleLineTax(ModelSQL):
    'Sale Line - Tax'
    __name__ = 'sale.line-account.tax'
    _table = 'sale_line_account_tax'
    line = fields.Many2One('sale.line', 'Sale Line', ondelete='CASCADE',
            select=True, required=True)
    tax = fields.Many2One('account.tax', 'Tax', ondelete='RESTRICT',
            select=True, required=True)

'''

class LoginsToApp(ModelSQL, ModelView):
     #docstring for AssessmentImage
    'Registrations to mobile App'

    # Internal class name. Always used as a reference inside Tryton
    # default: '<module_name>.<class_name>' on Tryton
    # becomes '<module_name>_<class_name>' in the database
    __name__ = 'iversta.regstoapp'

    # ———————————————- One2Many Many2One fields ——————————————————————————

    # ———————————————————— Plain fields ————————————————————————————
    login =  fields.Char('Login', help = 'User login')#:
    full_name =  fields.Char('Full name', help = 'A full name of a user')#:
    token_issued = fields.Char('New token issued', help = 'A new token issued for a new login')#:
    token_used = fields.Char('Token used', help = 'Current token used to login')#:
    user_id = fields.Numeric('Tryton ID in Tryton', help = 'DB id in Tryton DB')#
    #= fields.Char('Login Result', help = 'Login result')#:
    login_result  = fields.Selection([
                ('S', 'Manual'),
                ('U', 'On Order Processed')],
                 'Login Result', help ='Result of login attempt')
        
    @staticmethod
    def default_login_result():
        return 'U'


