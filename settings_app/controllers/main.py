# -*- encoding: utf-8 -*-
##############################################################################
#
#    Samples module for Odoo Web Login Screen
#    Copyright (C) 2017- XUBI.ME (http://www.xubi.me)
#    @author binhnguyenxuan (https://www.linkedin.com/in/binhnguyenxuan)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
##############################################################################

import base64
import io
import logging
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
from werkzeug.utils import redirect

_logger = logging.getLogger(__name__)

DEFAULT_ICON = '/settings_app/static/src/img/icon.png'
DEFAULT_BG_LOGIN = '/settings_app/static/src/img/background.jpg'
DEFAULT_LOGO = '/settings_app/static/src/img/logo.png'


class LoginHome(Home):
    @http.route(['/web/login', '/web/reset_password'], type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        app_config_settings = http.request.env['res.company'].sudo().search(
            [], order='id desc', limit=1)
        request.params['default_system_name'] = app_config_settings.default_system_name
        request.params['default_system_version'] = app_config_settings.default_system_version
        request.params['login_text_title1'] = app_config_settings.login_text_title1
        request.params['login_text_title2'] = app_config_settings.login_text_title2
        request.params['url_text_footer'] = app_config_settings.login_text_footer
        request.params['title'] = app_config_settings.default_system_name
        return super(LoginHome, self).web_login(redirect, **kw)

    @http.route('/web/background_login', auth='public')
    def web_background_login(self):
        app_config_settings = http.request.env['res.company'].sudo().search(
            [], order='id desc', limit=1)
        background_login = app_config_settings.login_background_image
        if background_login:
            image = base64.b64decode(background_login)
        else:
            return redirect(DEFAULT_BG_LOGIN)
        return http.request.make_response(
            image, [('Content-Type', 'image')])

    @http.route(['/web/binary/company_logo', '/logo', '/logo.png'], type='http', auth="none", website=False)
    def web_company_logo(self, dbname=None, company_id=None, **kw):
        app_config_settings = http.request.env['res.company'].sudo().search(
            [], order='id desc', limit=1)
        company_logo = app_config_settings.logo_image
        if not company_logo:
            return redirect(DEFAULT_LOGO)
        else:
            company_logo = base64.b64decode(company_logo)
        return http.request.make_response(
            company_logo, [('Content-Type', 'image')])


class WebFavicon(http.Controller):

    @http.route('/web_favicon/favicon', type='http', auth="none")
    def icon(self, redirect=None, **kw):
        app_config_settings = http.request.env['res.company'].sudo().search(
            [], order='id desc', limit=1)
        favicon = app_config_settings.default_system_favicon
        favicon_mimetype = app_config_settings.default_system_favicon_mimetype
        if not favicon:
            favicon = open(DEFAULT_ICON, 'r')
            favicon_mimetype = 'image/png'
        else:
            favicon = io.BytesIO(base64.b64decode(favicon))
        return http.request.make_response(
            favicon.read(), [('Content-Type', favicon_mimetype)])
