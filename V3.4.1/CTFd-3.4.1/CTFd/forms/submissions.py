from wtforms import SelectField, StringField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class SubmissionSearchForm(BaseForm):
    field = SelectField(
        "Search Field",
        choices=[
            ("provided", "提交者"),
            ("id", "ID"),
            ("account_id", "账户ID"),
            ("challenge_id", "挑战者ID"),
            ("challenge_name", "用户名称"),
        ],
        default="provided",
        validators=[InputRequired()],
    )
    q = StringField("参数", validators=[InputRequired()])
    submit = SubmitField("搜索")
