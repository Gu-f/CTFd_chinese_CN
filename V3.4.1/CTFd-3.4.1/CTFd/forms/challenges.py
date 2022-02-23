from wtforms import MultipleFileField, SelectField, StringField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class ChallengeSearchForm(BaseForm):
    field = SelectField(
        "搜索字段",
        choices=[
            ("name", "挑战名称"),
            ("id", "ID"),
            ("category", "挑战类别"),
            ("type", "挑战类型"),
        ],
        default="name",
        validators=[InputRequired()],
    )
    q = StringField("参数", validators=[InputRequired()])
    submit = SubmitField("搜索")


class ChallengeFilesUploadForm(BaseForm):
    file = MultipleFileField(
        "上传文件",
        description="使用 Control键+鼠标左键 或 Cmd键+鼠标左键 进行附加上传多个文件.",
        validators=[InputRequired()],
    )
    submit = SubmitField("上传")
