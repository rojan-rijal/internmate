from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, SelectField, FileField, DateField
from wtforms.validators import DataRequired

"""
@@Class_name: InternProfileForm
@@Class_Description: This function inherits types and functions from FlaskForm. This is a form
				design that is implemented for user inputs. It is used in auth/views.py for /complete/profile
				endpoint. When a new user signs up, they are requested to put their internship information
				to better use the system.
@@CODEOWNERS: Rojan Rijal
@@Last_Update_Date: April 22, 2020
"""
class InternProfileForm(FlaskForm):
	company_name = StringField('Company you are joining', validators=[DataRequired()])
	company_website = StringField('Company Website', validators=[DataRequired()])
	city = StringField('City you are interning at', validators=[DataRequired()])
	state = StringField('State you are interning at', validators=[DataRequired()])
	start_date  = DateField('Starting Date: (YYYY-DD-MM)', validators=[DataRequired()])
	submit = SubmitField('Complete Profile', render_kw={'class':'btn-primary'})
