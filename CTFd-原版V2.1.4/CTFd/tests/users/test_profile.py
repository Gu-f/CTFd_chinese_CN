#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CTFd.models import Users
from CTFd.utils.crypto import verify_password
from tests.helpers import create_ctfd, destroy_ctfd, register_user, login_as_user


def test_email_cannot_be_changed_without_password():
    """Test that a user can't update their email address without current password"""
    app = create_ctfd()
    with app.app_context():
        register_user(app)
        client = login_as_user(app)

        data = {"name": "user", "email": "user2@ctfd.io"}

        r = client.patch("/api/v1/users/me", json=data)
        assert r.status_code == 400
        user = Users.query.filter_by(id=2).first()
        assert user.email == "user@ctfd.io"

        data = {"name": "user", "email": "user2@ctfd.io", "confirm": "asdf"}

        r = client.patch("/api/v1/users/me", json=data)
        assert r.status_code == 400
        user = Users.query.filter_by(id=2).first()
        assert user.email == "user@ctfd.io"

        data = {"name": "user", "email": "user2@ctfd.io", "confirm": "password"}

        r = client.patch("/api/v1/users/me", json=data)
        assert r.status_code == 200
        user = Users.query.filter_by(id=2).first()
        assert user.email == "user2@ctfd.io"
        assert verify_password(plaintext="password", ciphertext=user.password)
    destroy_ctfd(app)
