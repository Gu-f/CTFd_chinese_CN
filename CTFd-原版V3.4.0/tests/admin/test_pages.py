from tests.helpers import create_ctfd, destroy_ctfd, login_as_user


def test_previewing_pages_works():
    """Test that pages can be previewed properly"""
    app = create_ctfd()
    with app.app_context():
        client = login_as_user(app, name="admin", password="password")

        with client.session_transaction() as sess:
            data = {
                "title": "title",
                "route": "route",
                "content": "content_testing",
                "nonce": sess.get("nonce"),
                "draft": "y",
                "hidden": "y",
                "auth_required": "y",
            }

        r = client.post("/admin/pages/preview", data=data)
        assert r.status_code == 200
        resp = r.get_data(as_text=True)
        assert "content_testing" in resp

    destroy_ctfd(app)
