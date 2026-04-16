from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField('Tên tài khoản', validators=[DataRequired(), Length(3, 80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(6, 128)])
    submit = SubmitField('Đăng ký')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')

class ProfileForm(FlaskForm):
    full_name = StringField('Họ tên', validators=[DataRequired()])
    school = StringField('Trường')
    district = StringField('Quận/Huyện')
    teach_skills = StringField('Kỹ năng mình DẠY được (cách nhau dấu phẩy)')
    learn_skills = StringField('Kỹ năng mình MUỐN HỌC (cách nhau dấu phẩy)')
    bio = TextAreaField('Giới thiệu bản thân')
    submit = SubmitField('Cập nhật profile')