from wtforms import (
    FileField,
    HiddenField,
    PasswordField,
    RadioField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

from CTFd.constants.themes import DEFAULT_THEME
from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.utils.config import get_themes


class SetupForm(BaseForm):
    ctf_name = StringField(
        "竞赛名称", description="您的CTF竞赛主名称"
    )
    ctf_description = TextAreaField(
        "竞赛描述", description="您的CTF竞赛描述"
    )
    user_mode = RadioField(
        "模式选择",
        choices=[("teams", "团队赛"), ("users", "个人赛")],
        default="teams",
        description="控制比赛形式是以团队为单位进行竞赛，还是以个人为单位进行竞赛",
        validators=[InputRequired()],
    )

    name = StringField(
        "管理员用户名",
        description="管理员账户自己的用户名",
        validators=[InputRequired()],
    )
    email = EmailField(
        "管理员邮箱",
        description="管理员账户自己的邮箱",
        validators=[InputRequired()],
    )
    password = PasswordField(
        "管理员密码",
        description="管理员账户的密码",
        validators=[InputRequired()],
    )

    ctf_logo = FileField(
        "Logo",
        description="网站的Logo(徽标)，不是CTF名称. 用作主页按钮.",
    )
    ctf_banner = FileField("Banner", description="主页的Banner(横幅图片).")
    ctf_small_icon = FileField(
        "网站小图标",
        description="用户浏览器标签左侧显示的图标(favicon),只能是PNG图片。并且大小必须是32x32px",
    )
    ctf_theme = SelectField(
        "主题",
        description="CTFd使用的主题",
        choices=list(zip(get_themes(), get_themes())),
        default=DEFAULT_THEME,
        validators=[InputRequired()],
    )
    theme_color = HiddenField(
        "主题颜色",
        description="主题使用的用于控制界面美观的颜色，需要主题支持才能生效。(可选)",
    )

    start = StringField(
        "开始时间", description="CTF竞赛的开始时间. (可选)."
    )
    end = StringField(
        "结束时间", description="CTF竞赛的结束时间. (可选)."
    )
    submit = SubmitField("完成")
