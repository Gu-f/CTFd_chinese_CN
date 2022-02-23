from marshmallow import ValidationError, post_dump, pre_load, validate
from marshmallow.fields import Nested
from marshmallow_sqlalchemy import field_for
from sqlalchemy.orm import load_only

from CTFd.models import UserFieldEntries, UserFields, Users, ma
from CTFd.schemas.fields import UserFieldEntriesSchema
from CTFd.utils import get_config, string_types
from CTFd.utils.crypto import verify_password
from CTFd.utils.email import check_email_is_whitelisted
from CTFd.utils.user import get_current_user, is_admin
from CTFd.utils.validators import validate_country_code


class UserSchema(ma.ModelSchema):
    class Meta:
        model = Users
        include_fk = True
        dump_only = ("id", "oauth_id", "created", "team_id")
        load_only = ("password",)

    name = field_for(
        Users,
        "name",
        required=True,
        allow_none=False,
        validate=[
            validate.Length(min=1, max=128, error="用户名不能为空")
        ],
    )
    email = field_for(
        Users,
        "email",
        allow_none=False,
        validate=[
            validate.Email("电子邮件必须是正确的电子邮件地址"),
            validate.Length(min=1, max=128, error="电子邮件地址不能为空"),
        ],
    )
    website = field_for(
        Users,
        "website",
        validate=[
            # This is a dirty hack to let website accept empty strings so you can remove your website
            lambda website: validate.URL(
                error="网站必须是以http或https开头的正确URL",
                schemes={"http", "https"},
            )(website)
            if website
            else True
        ],
    )
    country = field_for(Users, "country", validate=[validate_country_code])
    password = field_for(Users, "password", required=True, allow_none=False)
    fields = Nested(
        UserFieldEntriesSchema, partial=True, many=True, attribute="field_entries"
    )

    @pre_load
    def validate_name(self, data):
        name = data.get("name")
        if name is None:
            return
        name = name.strip()

        existing_user = Users.query.filter_by(name=name).first()
        current_user = get_current_user()
        if is_admin():
            user_id = data.get("id")
            if user_id:
                if existing_user and existing_user.id != user_id:
                    raise ValidationError(
                        "用户名已经被使用", field_names=["name"]
                    )
            else:
                if existing_user:
                    if current_user:
                        if current_user.id != existing_user.id:
                            raise ValidationError(
                                "用户名已经被使用", field_names=["name"]
                            )
                    else:
                        raise ValidationError(
                            "用户名已经被使用", field_names=["name"]
                        )
        else:
            if name == current_user.name:
                return data
            else:
                name_changes = get_config("name_changes", default=True)
                if bool(name_changes) is False:
                    raise ValidationError(
                        "用户名更改被禁用", field_names=["name"]
                    )
                if existing_user:
                    raise ValidationError(
                        "用户名更改被禁用", field_names=["name"]
                    )

    @pre_load
    def validate_email(self, data):
        email = data.get("email")
        if email is None:
            return
        email = email.strip()

        existing_user = Users.query.filter_by(email=email).first()
        current_user = get_current_user()
        if is_admin():
            user_id = data.get("id")
            if user_id:
                if existing_user and existing_user.id != user_id:
                    raise ValidationError(
                        "邮箱地址已经被使用", field_names=["email"]
                    )
            else:
                if existing_user:
                    if current_user:
                        if current_user.id != existing_user.id:
                            raise ValidationError(
                                "邮箱地址已经被使用",
                                field_names=["email"],
                            )
                    else:
                        raise ValidationError(
                            "邮箱地址已经被使用", field_names=["email"]
                        )
        else:
            if email == current_user.email:
                return data
            else:
                confirm = data.get("confirm")

                if bool(confirm) is False:
                    raise ValidationError(
                        "请确认您当前的密码", field_names=["confirm"]
                    )

                test = verify_password(
                    plaintext=confirm, ciphertext=current_user.password
                )
                if test is False:
                    raise ValidationError(
                        "当前密码输入错误", field_names=["confirm"]
                    )

                if existing_user:
                    raise ValidationError(
                        "邮箱地址已经被使用", field_names=["email"]
                    )
                if check_email_is_whitelisted(email) is False:
                    raise ValidationError(
                        "只有如下电子邮件地址可以注册 {domains} ".format(
                            domains=get_config("domain_whitelist")
                        ),
                        field_names=["email"],
                    )
                if get_config("verify_emails"):
                    current_user.verified = False

    @pre_load
    def validate_password_confirmation(self, data):
        password = data.get("password")
        confirm = data.get("confirm")
        target_user = get_current_user()

        if is_admin():
            pass
        else:
            if password and (bool(confirm) is False):
                raise ValidationError(
                    "请确认您当前的密码", field_names=["confirm"]
                )

            if password and confirm:
                test = verify_password(
                    plaintext=confirm, ciphertext=target_user.password
                )
                if test is True:
                    return data
                else:
                    raise ValidationError(
                        "当前密码输入错误", field_names=["confirm"]
                    )
            else:
                data.pop("password", None)
                data.pop("confirm", None)

    @pre_load
    def validate_fields(self, data):
        """
        This validator is used to only allow users to update the field entry for their user.
        It's not possible to exclude it because without the PK Marshmallow cannot load the right instance
        """
        fields = data.get("fields")
        if fields is None:
            return

        current_user = get_current_user()

        if is_admin():
            user_id = data.get("id")
            if user_id:
                target_user = Users.query.filter_by(id=data["id"]).first()
            else:
                target_user = current_user

            # We are editting an existing user
            if self.view == "admin" and self.instance:
                target_user = self.instance
                provided_ids = []
                for f in fields:
                    f.pop("id", None)
                    field_id = f.get("field_id")

                    # # Check that we have an existing field for this. May be unnecessary b/c the foriegn key should enforce
                    field = UserFields.query.filter_by(id=field_id).first_or_404()

                    # Get the existing field entry if one exists
                    entry = UserFieldEntries.query.filter_by(
                        field_id=field.id, user_id=target_user.id
                    ).first()
                    if entry:
                        f["id"] = entry.id
                        provided_ids.append(entry.id)

                # Extremely dirty hack to prevent deleting previously provided data.
                # This needs a better soln.
                entries = (
                    UserFieldEntries.query.options(load_only("id"))
                    .filter_by(user_id=target_user.id)
                    .all()
                )
                for entry in entries:
                    if entry.id not in provided_ids:
                        fields.append({"id": entry.id})
        else:
            provided_ids = []
            for f in fields:
                # Remove any existing set
                f.pop("id", None)
                field_id = f.get("field_id")
                value = f.get("value")

                # # Check that we have an existing field for this. May be unnecessary b/c the foriegn key should enforce
                field = UserFields.query.filter_by(id=field_id).first_or_404()

                # Get the existing field entry if one exists
                entry = UserFieldEntries.query.filter_by(
                    field_id=field.id, user_id=current_user.id
                ).first()

                if field.required is True and value.strip() == "":
                    raise ValidationError(
                        f"字段 '{field.name}' 是必须的", field_names=["fields"]
                    )

                if field.editable is False and entry is not None:
                    raise ValidationError(
                        f"字段 '{field.name}' 无法被编辑",
                        field_names=["fields"],
                    )

                if entry:
                    f["id"] = entry.id
                    provided_ids.append(entry.id)

            # Extremely dirty hack to prevent deleting previously provided data.
            # This needs a better soln.
            entries = (
                UserFieldEntries.query.options(load_only("id"))
                .filter_by(user_id=current_user.id)
                .all()
            )
            for entry in entries:
                if entry.id not in provided_ids:
                    fields.append({"id": entry.id})

    @post_dump
    def process_fields(self, data):
        """
        Handle permissions levels for fields.
        This is post_dump to manipulate JSON instead of the raw db object

        Admins can see all fields.
        Users (self) can see their edittable and public fields
        Public (user) can only see public fields
        """
        # Gather all possible fields
        removed_field_ids = []
        fields = UserFields.query.all()

        # Select fields for removal based on current view and properties of the field
        for field in fields:
            if self.view == "user":
                if field.public is False:
                    removed_field_ids.append(field.id)
            elif self.view == "self":
                if field.editable is False and field.public is False:
                    removed_field_ids.append(field.id)

        # Rebuild fuilds
        fields = data.get("fields")
        if fields:
            data["fields"] = [
                field for field in fields if field["field_id"] not in removed_field_ids
            ]

    views = {
        "user": [
            "website",
            "name",
            "country",
            "affiliation",
            "bracket",
            "id",
            "oauth_id",
            "fields",
            "team_id",
        ],
        "self": [
            "website",
            "name",
            "email",
            "country",
            "affiliation",
            "bracket",
            "id",
            "oauth_id",
            "password",
            "fields",
            "team_id",
        ],
        "admin": [
            "website",
            "name",
            "created",
            "country",
            "banned",
            "email",
            "affiliation",
            "secret",
            "bracket",
            "hidden",
            "id",
            "oauth_id",
            "password",
            "type",
            "verified",
            "fields",
            "team_id",
        ],
    }

    def __init__(self, view=None, *args, **kwargs):
        if view:
            if isinstance(view, string_types):
                kwargs["only"] = self.views[view]
            elif isinstance(view, list):
                kwargs["only"] = view
        self.view = view

        super(UserSchema, self).__init__(*args, **kwargs)
