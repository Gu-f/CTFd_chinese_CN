#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CTFd.models import Users
from CTFd.utils.crypto import verify_password
from tests.helpers import create_ctfd, register_user, login_as_user, destroy_ctfd


def test_user_set_profile():
    """Test that a user can set and remove their information in their profile"""
    app = create_ctfd()
    with app.app_context():
        register_user(app)
        client = login_as_user(app)

        data = {
            "name": "user",
            "email": "user@ctfd.io",
            "confirm": "",
            "password": "",
            "affiliation": "affiliation_test",
            "website": "https://ctfd.io",
            "country": "US",
        }

        r = client.patch("/api/v1/users/me", json=data)
        assert r.status_code == 200

        user = Users.query.filter_by(id=2).first()
        assert user.affiliation == data["affiliation"]
        assert user.website == data["website"]
        assert user.country == data["country"]

        r = client.get("/settings")
        resp = r.get_data(as_text=True)
        for k, v in data.items():
            assert v in resp

        data = {
            "name": "user",
            "email": "user@ctfd.io",
            "confirm": "",
            "password": "",
            "affiliation": "",
            "website": "",
            "country": "",
        }

        r = client.patch("/api/v1/users/me", json=data)
        assert r.status_code == 200

        user = Users.query.filter_by(id=2).first()
        assert user.affiliation == data["affiliation"]
        assert user.website == data["website"]
        assert user.country == data["country"]
    destroy_ctfd(app)


def test_user_can_change_password():
    """Test that a user can change their password and is prompted properly"""
    app = create_ctfd()
    with app.app_context():
        register_user(app)
        client = login_as_user(app)

        data = {
            "name": "user",
            "email": "user@ctfd.io",
            "confirm": "",
            "password": "new_password",
            "affiliation": "",
            "website": "",
            "country": "",
        }

        r = client.patch("/api/v1/users/me", json=data)
        user = Users.query.filter_by(id=2).first()
        assert verify_password(data["password"], user.password) is False
        assert r.status_code == 400
        assert r.get_json() == {
            "errors": {"confirm": ["Please confirm your current password"]},
            "success": False,
        }

        data["confirm"] = "wrong_password"

        r = client.patch("/api/v1/users/me", json=data)
        user = Users.query.filter_by(id=2).first()
        assert verify_password(data["password"], user.password) is False
        assert r.status_code == 400
        assert r.get_json() == {
            "errors": {"confirm": ["Your previous password is incorrect"]},
            "success": False,
        }

        data["confirm"] = "password"
        r = client.patch("/api/v1/users/me", json=data)
        assert r.status_code == 200
        user = Users.query.filter_by(id=2).first()
        assert verify_password(data["password"], user.password) is True
    destroy_ctfd(app)
