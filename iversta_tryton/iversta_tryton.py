from trytond.model import ModelView
from trytond.model import ModelSQL
from trytond.model import (ModelStorage, fields)
from trytond.pool import PoolMeta, Pool
from time import time

import os.path


__all__ = [ 'IverstaAssessments',
            'AssessmentImage',
            'LoginsToApp'
            ] 

module_path = os.path.dirname(__file__)


###########################  Class describes Vehicle ###############################
class IverstaAssessments(ModelSQL, ModelView):
    # description (mandatory on first declaration)
    'Inspections'

    # Internal class name. Always used as a reference inside Tryton
    # default: '<module_name>.<class_name>' on Tryton
    # becomes '<module_name>_<class_name>' in the database
    __name__ = 'iversta.assessment'

    # ———————————————- One2Many Many2One fields ——————————————————————————
    images = fields.One2Many('iversta.image', 'assessment', string = 'All images', help = "All inspections images taken in this session")
    images_previous = fields.One2Many('iversta.image', 'next_to_compare', string = 'Previous set', help = "All inspection images taken in the previous session")
    # previous_set = fields.One2One('iversta.assessment-iversta.assessment', origin = 'next_set', target = 'next_set_chain', string = 'Previous session', help = "Link to the previous session")
    # next_set = fields.One2One('iversta.assessment-iversta.assessment', origin = 'previous_set', target = 'previous_set_chain', string = 'Next session', help = "Link to the previous session")
    # ———————————————————— Function fields —————————————————————————

    # ———————————————————— Plain fields ————————————————————————————
    last_photo_date = fields.Char('Last image timestamp', readonly = False, help = 'Time of the last photo taken')
    assess_datetime = fields.DateTime("Received on",
        context={'date_format':'%b %d, %Y', 'time_fromat':'%I:%M:%s %p'},
        #format='%I:%M %p',
        required=False,
        readonly = False,)
    license_plate = fields.Char('License plate',  readonly = False, help = '1-8 chars, car license plate like XXX-XXX')#: (16 chars)
    VIN = fields.Char('VIN', size=17, required = False,  readonly = False, help = 'VIN is 17-char string');
    rental_file_num = fields.Char('Rental file #', size=64,  readonly = False, help = 'Format: IVR-xxxxx-YYZ-xx'); #: 64 chars 
    odosize = fields.Numeric('Odometer', help = 'Type the most recent odometer measure' )#: (long integer) #// number
    images_qty = fields.Integer('Images',  readonly = False,)#: (integer) // if needed?
    damages_qty = fields.Integer('Damages', readonly = False,)#: (integer) // if needed?
    session_uuid = fields.Char('Uniquie session ID', size=40, readonly = False, help = 'UUID example: b6d6d0be-1a67-4adc-b5a2-e6a6d1a8310d'); #: 64 chars 
    comments = fields.Text('Comments',  help = 'Any comments to a session'); #: 64 chars 
    check_in_out = fields.Selection([
                ('I', 'Car Check In'),
                ('O', 'Car Check Out'),
                ('U', 'Undefined'),],
                'Session type (CheckIn|CheckOut)', readonly = False, help ='Inspection at CheckIn or CheckOut')

    @staticmethod
    def default_check_in_out():
        if len(images)>0:
            return images[0].check_in_out
        return 'U'

    
###############################################################################################################
###### ———————————————————-   IMAGES 
###############################################################################################################

class AssessmentImage(ModelSQL, ModelView):
     #docstring for AssessmentImage
    'Image of Inspection'

    # Internal class name. Always used as a reference inside Tryton
    # default: '<module_name>.<class_name>' on Tryton
    # becomes '<module_name>_<class_name>' in the database
    __name__ = 'iversta.image'

    # ———————————————- One2Many Many2One fields ——————————————————————————
    assessment = fields.Many2One('iversta.assessment', string = 'Most recent set', ondelete='SET NULL', required=False,  help = 'The full set of inspection images')
    next_to_compare = fields.Many2One('iversta.assessment', string = 'Next set to comare to', ondelete='SET NULL', required=False,  help = 'The full set of inspection images')

    # ———————————————————— Plain fields ————————————————————————————
    license_plate = fields.Char('License plate', readonly = False, help = '1-8 chars, car license plate like XXX-XXX')#: (16 chars)
    VIN = fields.Char('VIN', size=17, required = False, readonly = False, help = 'VIN is 17-char string');
    rental_file_num = fields.Char('Rental file #', readonly = False, size=64, help = 'Firmat: IVR-xxxxx-YYZ-xx'); #: 64 chars 
    odosize = fields.Numeric('Odometer', help = 'Type the most recent odometer measure' )#: (long integer) #// number
    image_num_in_set = fields.Char('Position in sequence', help = 'Image number in a sequence')#: (16 chars)
    damage_image_num_in_set = fields.Char('Damage in sequence', help = 'Image number in a damage sequence')#: (16 chars)

    file_id = fields.Char('Ext file id', readonly=False)
    session_uuid = fields.Char('Uniquie session ID', size=40, readonly = False, help = 'UUID example: b6d6d0be-1a67-4adc-b5a2-e6a6d1a8310d'); #: 64 chars 
    recorded_date = fields.Char('Photo Timestamp', readonly = False, help = 'Time of photo taken by device')
    date_taken = fields.DateTime('Image taken on', readonly = False,
        context={'date_format':'%b %d, %Y', 'time_fromat':'%I:%M:%s %p'},)
    image_type = fields.Selection([
                ('O', 'Overview'),
                ('D', 'Damage')],
                 'Type of photo', readonly = False, help ='A general view or a close damage view')
    check_in_out = fields.Selection([
                ('I', 'Car Check In'),
                ('O', 'Car Check Out')],
                 'Session type (CheckIn|CheckOut)', readonly = False, help ='When photo is taken CheckIn|CheckOut')
    comments = fields.Text('Comments',  help = 'Any comments to the image'); #: 64 chars 
    view_name = fields.Char('View name')
    view_name_func = fields.Function(fields.Char('View name (generated)'),'get_view_name')

    # ——— BINARY FIELD 
    overlay_image  = fields.Binary('Overlay image', readonly=False, filename='overlay_filename') #, file_id = 'file_id')
    overlay_filename = fields.Char('Overlay filename', help = 'Filename for overlay')

    image = fields.Binary('Photo', readonly=False, filename='filename')#, file_id = 'file_id')
    image_func = fields.Function(fields.Binary('Photo with overlay', readonly=False ), 'get_image_with_overlay_text')#))
    filename = fields.Char('File Name', readonly=False)
    svg_image = fields.Binary('SVG overlay', readonly=False, filename='svg_filename')#, file_id = 'file_id')
    svg_filename = fields.Char('File Name', readonly=False)

    image_to_compare = fields.Function(fields.Binary('Previous photo', readonly=False ), 'get_image_from_previous_set')#))
    # image_to_compare_func = fields.Function(fields.Binary('Previous photo', readonly=False ), 'get_image_from_previous_set')#))

    @staticmethod
    def default_image_type():
        return 'O'

    @staticmethod
    def default_check_in_out():
        return 'I'

    def get_view_name(self, name):
        View_names = ['Front view', 'Front-Driver side', 'Rear-Driver side',  'Rear view', 'Rear-Passenger side', 'Front-Passenger side', 'Odometer'];
        try:
            _view_name = View_names[int(self.image_num_in_set)]
        except Exception as e:
            _view_name = f'{e}'
        return _view_name

    def place_text_over_image(self,image_data,text, shift_y=0):
        # shift_y — vertical alignment for multi-row text
        from PIL import Image
        from PIL import ImageFont
        from PIL import ImageDraw 
        from io import BytesIO

        
        x, y = 10, 10+shift_y
        fontcolor = (255, 184, 0)
        shadowcolor = "black"
        # text = "AFTER"
        # img = Image.open("sample_in.jpg")
        # img = Image.frombytes(mode='RGBA',size=(1024,768),data=self.image, decoder_name='raw')
        try:
            img = Image.open(BytesIO(image_data))
            # img.thumbnail((1024,768), Image.ANTIALIAS)
            draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        # font = ImageFont.truetype("sans-serif.ttf", 16)
        # draw.text((x, y),"Sample Text",(r,g,b))
            font_path="/usr/local/lib/python3.7/dist-packages/werkzeug/debug/shared/ubuntu.ttf"
            font = ImageFont.truetype(font_path, 122)
            font_shadow = ImageFont.truetype(font_path, 122)
            draw.text((x-2, y-2), text, font=font_shadow, fill=shadowcolor)
            draw.text((x+2, y-2), text, font=font_shadow, fill=shadowcolor)
            draw.text((x-2, y+2), text, font=font_shadow, fill=shadowcolor)
            draw.text((x-2, y-2), text, font=font_shadow, fill=shadowcolor)
            draw.text((x, y),text, fontcolor, font=font)
        # roi_img.save(img_byte_arr, format='PNG')
            buf = BytesIO()
            img.save(buf, format='JPEG', compress_level=1)
            return buf.getvalue()
        except Exception as e:
            # raise(e)
            pass
        return image_data



    def get_image_from_previous_set(self,name):
        text_on_image_list = {'I':'CHECK-IN', 'O':'CHECK-OUT'}
        text_on_image =text_on_image_list['O']
        image_data =''
        pool = Pool()
        Inspection = pool.get('iversta.assessment')
        Image=pool.get('iversta.image')
        if self.assessment: # If this image belongs to inspection
            if self.assessment.images_previous: # ...and that inspection has images from the previous inspection
                for i in range(len(self.assessment.images_previous)): # iterate through all images in that previous inspection
                    # and that previous inspection has image of the same overlay:
                    if (self.image_num_in_set == self.assessment.images_previous[i].image_num_in_set):
                        if (self.assessment.images_previous[i].filename[-3:]!='svg'):
                            # >>> TO DO  <<<  # check if that is a damage view or overview?
                            image_data = self.assessment.images_previous[i].image # take this image to show...
                            text_on_image = text_on_image_list[self.assessment.images_previous[i].check_in_out] # select the text depends on moment of inspection
                        else:
                            image_data = self.assessment.images_previous[i-1].image # if it is svg — the previous is an actual image.
                            text_on_image = text_on_image_list[self.assessment.images_previous[i-1].check_in_out] # select the text depends on moment of inspection
        return self.place_text_over_image(image_data, text_on_image, shift_y=0) # return image with selected text

    def get_image_with_overlay_text(self,name):
        text_on_image_list = {'I':'CHECK-IN', 'O':'CHECK-OUT'}
        # start_time = time() # calculate execution time
        text_on_image = text_on_image_list[self.check_in_out]
        # time_txt =  f"--- {round(time() - start_time,4)} seconds ---" 
        # img_data = self.place_text_over_image(img_data, time_txt, 120)
        return self.place_text_over_image(self.image, text_on_image, shift_y=0)

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


