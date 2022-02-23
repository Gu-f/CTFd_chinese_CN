from wtforms import BooleanField, RadioField, StringField, TextAreaField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class NotificationForm(BaseForm):
    title = StringField("标题", description="公告标题")
    content = TextAreaField(
        "公告内容",
        description="公告内容，支持HTML和markdown语法.",
    )
    type = RadioField(
        "公告类型",
        choices=[("toast", "右下角小窗提示"), ("alert", "弹窗提示"), ("background", "不提示")],
        default="toast",
        description="用户收到的公告类型",
        validators=[InputRequired()],
    )
    sound = BooleanField(
        "提示音",
        default=True,
        description="当用户收到新公告的时候，播放提示音",
    )
    submit = SubmitField("发布")
