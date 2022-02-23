from wtforms import PasswordField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.forms.users import (
    attach_custom_user_fields,
    attach_registration_code_field,
    build_custom_user_fields,
    build_registration_code_field,
)


def RegistrationForm(*args, **kwargs):
    class _RegistrationForm(BaseForm):
        name = StringField("用户名", validators=[InputRequired()])
        email = EmailField("邮箱", validators=[InputRequired()])
        password = PasswordField("密码", validators=[InputRequired()])
        submit = SubmitField("注册")

        @property
        def extra(self):
            return build_custom_user_fields(
                self, include_entries=False, blacklisted_items=()
            ) + build_registration_code_field(self)

    attach_custom_user_fields(_RegistrationForm)
    attach_registration_code_field(_RegistrationForm)

    return _RegistrationForm(*args, **kwargs)


class LoginForm(BaseForm):
    name = StringField("用户名或邮箱", validators=[InputRequired()])
    password = PasswordField("密码", validators=[InputRequired()])
    submit = SubmitField("登录")


class ConfirmForm(BaseForm):
    submit = SubmitField("重新发送重置密码邮件")


class ResetPasswordRequestForm(BaseForm):
    email = EmailField("邮箱", validators=[InputRequired()])
    submit = SubmitField("发送")


class ResetPasswordForm(BaseForm):
    password = PasswordField("新密码", validators=[InputRequired()])
    submit = SubmitField("重置")
