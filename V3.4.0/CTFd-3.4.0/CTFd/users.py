from flask import Blueprint, render_template, request, url_for

from CTFd.models import Users
from CTFd.utils import config
from CTFd.utils.decorators import authed_only
from CTFd.utils.decorators.visibility import (
    check_account_visibility,
    check_score_visibility,
)
from CTFd.utils.helpers import get_errors, get_infos
from CTFd.utils.user import get_current_user

users = Blueprint("users", __name__)


@users.route("/users")
@check_account_visibility
def listing():
    q = request.args.get("q")
    field = request.args.get("field", "name")
    field_CN_kv = {
        "name": "用户名",
        "affiliation": "单位/组织",
        "website": "Blog/网站"
    }
    if field not in ("name", "affiliation", "website"):
        field = "name"
        field_CN = "用户名"
    else:
        field_CN = field_CN_kv.get(field)

    filters = []
    if q:
        filters.append(getattr(Users, field).like("%{}%".format(q)))

    users = (
        Users.query.filter_by(banned=False, hidden=False)
        .filter(*filters)
        .order_by(Users.id.asc())
        .paginate(per_page=50)
    )

    args = dict(request.args)
    args.pop("page", 1)

    return render_template(
        "users/users.html",
        users=users,
        prev_page=url_for(request.endpoint, page=users.prev_num, **args),
        next_page=url_for(request.endpoint, page=users.next_num, **args),
        q=q,
        field=field,
        field_CN=field_CN
    )


@users.route("/profile")
@users.route("/user")
@authed_only
def private():
    infos = get_infos()
    errors = get_errors()

    user = get_current_user()

    if config.is_scoreboard_frozen():
        infos.append("Scoreboard has been frozen")

    return render_template(
        "users/private.html",
        user=user,
        account=user.account,
        infos=infos,
        errors=errors,
    )


@users.route("/users/<int:user_id>")
@check_account_visibility
@check_score_visibility
def public(user_id):
    infos = get_infos()
    errors = get_errors()
    user = Users.query.filter_by(id=user_id, banned=False, hidden=False).first_or_404()

    if config.is_scoreboard_frozen():
        infos.append("Scoreboard has been frozen")

    return render_template(
        "users/public.html", user=user, account=user.account, infos=infos, errors=errors
    )
