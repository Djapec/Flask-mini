import os
from flask_app import createApp
from flask_app import db

os.environ['FLASK_ENV_TYPE'] = 'Development'

if os.environ['FLASK_ENV_TYPE'] == 'Development':
    from config.development import Development as Config
elif os.environ['FLASK_ENV_TYPE'] == 'Production':
    from config.production import Production as Config
else:
    raise Exception('Not proper FLASK_ENV_TYPE set.')


app = createApp(Config)


@app.route('/')
def hello():
    # db.create_all()
    return 'Heeey'