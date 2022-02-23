from wtforms import (
    BooleanField,
    HiddenField,
    MultipleFileField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm


class PageEditForm(BaseForm):
    title = StringField(
        "标题", description="该标题将会显示在导航栏中"
    )
    route = StringField(
        "路由",
        description="这是路由指向，你创建的页面可通过该URL路径访问，如设置成 /page 。除此之外你也可以使用链接来链接到该页面。",
    )
    draft = BooleanField("草稿")
    hidden = BooleanField("隐藏")
    auth_required = BooleanField("需要登录后才能访问")
    content = TextAreaField("内容")
    format = SelectField(
        "选择编辑语言",
        choices=[("markdown", "Markdown"), ("html", "HTML")],
        default="markdown",
        validators=[InputRequired()],
        description="用来生成页面的语法格式",
    )


class PageFilesUploadForm(BaseForm):
    file = MultipleFileField(
        "上传文件",
        description="使用 Control键+鼠标左键 或 Cmd键+鼠标左键 进行附加上传多个文件",
        validators=[InputRequired()],
    )
    type = HiddenField("页面类型", default="page", validators=[InputRequired()])
