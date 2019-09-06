from CTFd import create_app
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--profile", help="Enable flask_profiler profiling", action="store_true")
args = parser.parse_args()

app = create_app()

if args.profile:
    from flask_debugtoolbar import DebugToolbarExtension
    import flask_profiler
    app.config["flask_profiler"] = {
        "enabled": app.config["DEBUG"],
        "storage": {
            "engine": "sqlite"
        },
        "basicAuth": {
            "enabled": False,
        },
    }
    flask_profiler.init_app(app)
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)
    print(" * Flask profiling running at http://127.0.0.1:4000/flask-profiler/")

app.run(debug=True, threaded=True, host="127.0.0.1", port=4000)
