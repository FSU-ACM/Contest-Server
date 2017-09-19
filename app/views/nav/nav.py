# views.nav.nav

from flask import url_for
from flask_nav import Nav
from flask_nav.elements import *

from app import app

nav_logged_in = Navbar('',
    Link('Home', '/'),
    Link('FAQ','/#faq'),
    Link('Sponsors', '/#sponsors'),
    Link('Teams','/allteams'),
    Link('Account', '/account/profile'),
)

nav_logged_out = Navbar('',
    Link('Home', '/'),
    Link('FAQ','/#faq'),
    Link('Sponsors', '/#sponsors'),
    Link('Teams','/allteams'),
    Link('Login','/login'),
)

nav_admin = Navbar('',
    Link('Home', '/'),
)

nav = Nav()
nav.register_element('logged_in', nav_logged_in)
nav.register_element('logged_out', nav_logged_out)
nav.register_element('admin', nav_admin)
nav.init_app(app)
