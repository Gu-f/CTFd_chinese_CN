from wtforms import BooleanField, FileField, SelectField, StringField, TextAreaField
from wtforms.fields.html5 import IntegerField, URLField
from wtforms.widgets.html5 import NumberInput

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.utils.csv import get_dumpable_tables


class ResetInstanceForm(BaseForm):
    accounts = BooleanField(
        "账户",
        description="删除所有用户和团队帐户及其关联信息",
    )
    submissions = BooleanField(
        "提交",
        description="删除所有提交，提交获得的分数或进度",
    )
    challenges = BooleanField(
        "挑战", description="删除所有挑战相关数据"
    )
    pages = BooleanField(
        "页面", description="删除所有页面及其关联文件"
    )
    notifications = BooleanField(
        "公告", description="删除所有公告"
    )
    submit = SubmitField("重置 CTF")


class AccountSettingsForm(BaseForm):
    domain_whitelist = StringField(
        "账户邮箱白名单",
        description="都好分隔的电子邮件域名，用户可在该域中注册 (e.g. ctfd.io, gmail.com, yahoo.com)",
    )
    team_creation = SelectField(
        "团队创建",
        description="控制用户是否可以创建自己的团队(仅限团队模式)",
        choices=[("true", "开启"), ("false", "关闭")],
        default="true",
    )
    team_size = IntegerField(
        widget=NumberInput(min=0),
        description="每个团队的用户数量(仅限团队模式)",
    )
    num_teams = IntegerField(
        "队伍总数",
        widget=NumberInput(min=0),
        description="最大队伍数量(仅限团队模式)",
    )
    verify_emails = SelectField(
        "验证邮箱",
        description="控制用户在正常参与之前必须验证邮箱",
        choices=[("true", "开启"), ("false", "关闭")],
        default="false",
    )
    team_disbanding = SelectField(
        "团队解散",
        description="控制是否允许队长解散自己的团队",
        choices=[
            ("inactive_only", "为不活动的团队启用"),
            ("disabled", "关闭"),
        ],
        default="inactive_only",
    )
    name_changes = SelectField(
        "名称更改",
        description="控制用户和团队是否可以更改其名称",
        choices=[("true", "开启"), ("false", "关闭")],
        default="true",
    )
    incorrect_submissions_per_min = IntegerField(
        "flag提交保护",
        widget=NumberInput(min=1),
        description="每分钟允许提交flag的限制数量 (默认: 10)",
    )

    submit = SubmitField("更新")


class ExportCSVForm(BaseForm):
    table = SelectField("数据库表", choices=get_dumpable_tables())
    submit = SubmitField("下载 CSV")


class ImportCSVForm(BaseForm):
    csv_type = SelectField(
        "CSV 类型",
        choices=[("users", "用户"), ("teams", "团队"), ("challenges", "挑战")],
        description="CSV数据类型",
    )
    csv_file = FileField("CSV 文件", description="CSV 文件内容")


class LegalSettingsForm(BaseForm):
    tos_url = URLField(
        "服务条款地址",
        description="托管在其他位置的服务条款文档或URL地址",
    )
    tos_text = TextAreaField(
        "服务条款", description="服务条款页面上显示的内容",
    )
    privacy_url = URLField(
        "隐私政策",
        description="托管在其他位置的隐私政策或URL地址",
    )
    privacy_text = TextAreaField(
        "隐私政策", description="隐私政策页面上显示的内容",
    )
    submit = SubmitField("更新")
