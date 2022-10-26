LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/'
LOGIN_URL = '/admin/login/'
BREADCRUMBS_HOME_LABEL = 'Trang chủ'

GOOGLE_CLIENT_ID = "226127222416-2c4reo3d755cofltcev8iars4no55nch.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "EgzjoQoUWB4ax4VIaD4WjDPB"
# You need register
GOOGLE_REDIRECT_URI = "http://localhost:8083/user/accounts/login-social"

CKEDITOR_UPLOAD_PATH = 'ckeditor_uploads/'
CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'toolbar': 'Basic',
    },
}
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 150,
        'width': 800,
    },
}

