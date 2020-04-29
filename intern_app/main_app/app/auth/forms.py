from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, SelectField, FileField, DateField
from wtforms.validators import DataRequired

class InternProfileForm(FlaskForm):
	company_name = StringField('Company you are joining', validators=[DataRequired()])
	company_website = StringField('Company Website', validators=[DataRequired()])
	city = StringField('City you are interning at', validators=[DataRequired()])
	state = StringField('State you are interning at', validators=[DataRequired()])
	start_date  = DateField('Starting Date', validators=[DataRequired()])
	submit = SubmitField('Complete Profile', render_kw={'class':'btn-primary'})
