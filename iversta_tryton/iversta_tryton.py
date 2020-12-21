from trytond.model import ModelView
from trytond.model import ModelSQL
from trytond.model import (ModelStorage, fields)


import os.path


__all__ = [ 'IverstaAssessments',
            'AssessmentChain'
            'AssessmentImage',
            'LoginsToApp'
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
    images = fields.One2Many('iversta.image', 'assessment', string = 'All images', help = "All assessment images taken in this session")
    images_previous = fields.One2Many('iversta.image', 'next_to_compare', string = 'Previous set', help = "All assessment images taken in the previous session")
    # previous_set = fields.One2One('iversta.assessment-iversta.assessment', origin = 'next_set', target = 'next_set_chain', string = 'Previous session', help = "Link to the previous session")
    # next_set = fields.One2One('iversta.assessment-iversta.assessment', origin = 'previous_set', target = 'previous_set_chain', string = 'Next session', help = "Link to the previous session")
    # ———————————————————— Function fields —————————————————————————

    # ———————————————————— Plain fields ————————————————————————————
    last_photo_date = fields.Char('Last image timestamp', readonly = True, help = 'Time of the last photo taken')
    assess_datetime = fields.DateTime("Assessed on",
        context={'date_format':'%b %d, %Y', 'time_fromat':'%I:%M:%s %p'},
        #format='%I:%M %p',
        required=False,
        readonly = True,)
    license_plate = fields.Char('License plate',  readonly = True, help = '1-8 chars, car license plate like XXX-XXX')#: (16 chars)
    VIN = fields.Char('VIN', size=17, required = False,  readonly = True, help = 'VIN is 17-char string');
    rental_file_num = fields.Char('Rental file #', size=64,  readonly = True, help = 'Format: IVR-xxxxx-YYZ-xx'); #: 64 chars 
    odosize = fields.Numeric('Odometer', help = 'Type the most recent odometer measure' )#: (long integer) #// number
    images_qty = fields.Integer('Images',  readonly = True,)#: (integer) // if needed?
    damages_qty = fields.Integer('Damages', readonly = True,)#: (integer) // if needed?
    session_uuid = fields.Char('Uniquie session ID', size=40, readonly = True, help = 'UUID example: b6d6d0be-1a67-4adc-b5a2-e6a6d1a8310d'); #: 64 chars 
    comments = fields.Text('Comments',  help = 'Any comments to a session'); #: 64 chars 
    check_in_out = fields.Selection([
                ('I', 'Car Check In'),
                ('O', 'Car Check Out'),
                ('U', 'Undefined'),],
                'Session type (CheckIn|CheckOut)', readonly = True, help ='Inspection at CheckIn or CheckOut')

    
    @staticmethod
    def default_check_in_out():
        if len(images)>0:
            return images[0].check_in_out
        return 'U'

    
class AssessmentChain(ModelSQL, ModelView):
    # description (mandatory on first declaration)
    'Chaining Assessments'

    # Internal class name. Always used as a reference inside Tryton
    # default: '<module_name>.<class_name>' on Tryton
    # becomes '<module_name>_<class_name>' in the database
    __name__ = 'iversta.assessment-iversta.assessment'
    # previous_set_chain = fields.One2One('iversta.assessment-iversta.assessment', origin = 'next_set_chain', target = 'next_set', string = 'Previous session', help = "Link to the previous session")
    # next_set_chain = fields.One2One('iversta.assessment-iversta.assessment', origin = 'previous_set_chain', target = 'previous_set', string = 'Previous session', help = "Link to the previous session")

###############################################################################################################
###### ———————————————————-   IMAGES 
###############################################################################################################

class AssessmentImage(ModelSQL, ModelView):
     #docstring for AssessmentImage
    'Image of Assessment'

    # Internal class name. Always used as a reference inside Tryton
    # default: '<module_name>.<class_name>' on Tryton
    # becomes '<module_name>_<class_name>' in the database
    __name__ = 'iversta.image'

    # ———————————————- One2Many Many2One fields ——————————————————————————
    assessment = fields.Many2One('iversta.assessment', string = 'Most recent set', ondelete='SET NULL', required=False,  help = 'The full set of assesment images')
    next_to_compare = fields.Many2One('iversta.assessment', string = 'Next set to comare to', ondelete='SET NULL', required=False,  help = 'The full set of assesment images')

    # ———————————————————— Plain fields ————————————————————————————
    license_plate = fields.Char('License plate', readonly = True, help = '1-8 chars, car license plate like XXX-XXX')#: (16 chars)
    VIN = fields.Char('VIN', size=17, required = False, readonly = True, help = 'VIN is 17-char string');
    rental_file_num = fields.Char('Rental file #', readonly = True, size=64, help = 'Firmat: IVR-xxxxx-YYZ-xx'); #: 64 chars 
    odosize = fields.Numeric('Odometer', help = 'Type the most recent odometer measure' )#: (long integer) #// number
    image_num_in_set = fields.Char('Num in sequence', help = 'Image number in a sequence')#: (16 chars)
    damage_image_num_in_set = fields.Char('Damage in sequence', help = 'Image number in a damage sequence')#: (16 chars)
    filename = fields.Char('File Name', readonly=True)
    file_id = fields.Char('Ext file id', readonly=False)
    session_uuid = fields.Char('Uniquie session ID', size=40, readonly = True, help = 'UUID example: b6d6d0be-1a67-4adc-b5a2-e6a6d1a8310d'); #: 64 chars 
    recorded_date = fields.Char('Photo Timestamp', readonly = True, help = 'Time of photo taken by device')
    date_taken = fields.DateTime('Image taken on', readonly = True,
        context={'date_format':'%b %d, %Y', 'time_fromat':'%I:%M:%s %p'},)
    image_type = fields.Selection([
                ('O', 'Overview'),
                ('D', 'Damage')],
                 'Type of photo', readonly = True, help ='A general view or a close damage view')
    check_in_out = fields.Selection([
                ('I', 'Car Check In'),
                ('O', 'Car Check Out')],
                 'Session type (CheckIn|CheckOut)', readonly = True, help ='When photo is taken CheckIn|CheckOut')
    comments = fields.Text('Comments',  help = 'Any comments to the image'); #: 64 chars 

    # ——— BINARY FIELD 
    image = fields.Binary('File', readonly=False, filename='filename')#, file_id = 'file_id')

    @staticmethod
    def default_image_type():
        return 'O'

    @staticmethod
    def default_check_in_out():
        return 'I'


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
    __name__ = 'iversta.logins-to-app'

    # ———————————————- One2Many Many2One fields ——————————————————————————

    # ———————————————————— Plain fields ————————————————————————————
    login =  fields.Char('Login', help = 'User login')#:
    full_name =  fields.Char('Full name', help = 'A full name of a user')#:
    token_issued = fields.Char('New token issued', help = 'A new token issued for a new login')#:
    token_used = fields.Char('Token used', help = 'Current token used to login')#:
    user_id = fields.Numeric('Tryton ID in Tryton', help = 'DB id in Tryton DB')#
    #= fields.Char('Login Result', help = 'Login result')#:
    login_result = fields.Selection([
                ('S', 'Sucessful'),
                ('U', 'Failed')],
                 'Login Result', help ='Result of login attempt')
        
    @staticmethod
    def default_login_result():
        return 'U'


