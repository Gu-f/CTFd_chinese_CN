from wtforms import RadioField, StringField, TextAreaField
from wtforms.fields.html5 import IntegerField

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class AwardCreationForm(BaseForm):
    name = StringField("奖项名称")
    value = IntegerField("分值")
    category = StringField("类别")
    description = TextAreaField("描述")
    submit = SubmitField("创建")
    icon = RadioField(
        "勋章",
        choices=[
            ("", "None"),
            ("shield", "Shield"),
            ("bug", "Bug"),
            ("crown", "Crown"),
            ("crosshairs", "Crosshairs"),
            ("ban", "Ban"),
            ("lightning", "Lightning"),
            ("skull", "Skull"),
            ("brain", "Brain"),
            ("code", "Code"),
            ("cowboy", "Cowboy"),
            ("angry", "Angry"),
        ],
    )
