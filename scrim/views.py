from scrim import scrim_app

@scrim_app.route('/')
@scrim_app.route('/index')
def index():
    return "Hello, World!"
