##########################################################################
#
#    Copyright (C) 2017 MuK IT GmbH
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
##########################################################################

from odoo import api, fields, models

XML_ID = "settings_app._assets_primary_variables"
SCSS_URL = "/settings_app/static/src/scss/colors.scss"


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------
    theme_logo_image = fields.Binary(
        related="company_id.logo_image",
        readonly=False)

    theme_background_image = fields.Binary(
        related="company_id.background_image",
        readonly=False)

    theme_background_blend_mode = fields.Selection(
        related="company_id.background_blend_mode",
        readonly=False)

    theme_default_sidebar_preference = fields.Selection(
        related="company_id.default_sidebar_preference",
        readonly=False)

    theme_default_chatter_preference = fields.Selection(
        related="company_id.default_chatter_preference",
        readonly=False)

    theme_color_brand = fields.Char(
        string="Theme Brand Color")

    theme_color_primary = fields.Char(
        string="Theme Primary Color")

    theme_color_menu = fields.Char(
        string="Theme Menu Color")

    theme_color_appbar_color = fields.Char(
        string="Theme AppBar Color")

    theme_color_appbar_background = fields.Char(
        string="Theme AppBar Background")

    app_system_name = fields.Char(
        related="company_id.default_system_name",
        readonly=False,
        required=True)

    app_system_version = fields.Char(
        related="company_id.default_system_version",
        readonly=False,
        required=True)

    app_system_favicon = fields.Binary(
        related="company_id.default_system_favicon",
        readonly=False)

    app_system_favicon_mimetype = fields.Selection(
        related="company_id.default_system_favicon_mimetype",
        readonly=False)

    login_text_title1 = fields.Char(
        related="company_id.login_text_title1",
        readonly=False)

    login_text_title2 = fields.Char(
        related="company_id.login_text_title2",
        readonly=False)
    login_text_footer = fields.Char(
        related="company_id.login_text_footer",
        readonly=False)

    login_background_image = fields.Binary(
        related="company_id.login_background_image",
        readonly=False)

    app_show_documentation = fields.Boolean(
        related="company_id.app_show_documentation",
        readonly=False)
    app_documentation_url = fields.Char(
        related="company_id.app_documentation_url",
        readonly=False)

    app_show_support = fields.Boolean(
        related="company_id.app_show_support",
        readonly=False)
    app_support_url = fields.Char(
        related="company_id.app_support_url",
        readonly=False)

    app_show_website = fields.Boolean(
        related="company_id.app_show_website",
        readonly=False)
    app_website_url = fields.Char(
        related="company_id.app_website_url",
        readonly=False)

    # ----------------------------------------------------------
    # Functions
    # ----------------------------------------------------------

    @api.multi
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        variables = [
            'o-brand-odoo',
            'o-brand-primary',
            'mk-apps-color',
            'mk-appbar-color',
            'mk-appbar-background',
        ]
        colors = self.env['muk_utils.scss_editor'].get_values(
            SCSS_URL, XML_ID, variables
        )
        colors_changed = []
        colors_changed.append(self.theme_color_brand != colors['o-brand-odoo'])
        colors_changed.append(self.theme_color_primary != colors['o-brand-primary'])
        colors_changed.append(self.theme_color_menu != colors['mk-apps-color'])
        colors_changed.append(
            self.theme_color_appbar_color != colors['mk-appbar-color'])
        colors_changed.append(
            self.theme_color_appbar_background != colors['mk-appbar-background'])
        if(any(colors_changed)):
            variables = [
                {'name': 'o-brand-odoo',
                 'value': self.theme_color_brand or "#243742"},
                {'name': 'o-brand-primary',
                 'value': self.theme_color_primary or "#5D8DA8"},
                {'name': 'mk-apps-color',
                 'value': self.theme_color_menu or "#f8f9fa"},
                {'name': 'mk-appbar-color',
                 'value': self.theme_color_appbar_color or "#dee2e6"},
                {'name': 'mk-appbar-background',
                 'value': self.theme_color_appbar_background or "#000000"},
            ]
            self.env['muk_utils.scss_editor'].replace_values(
                SCSS_URL, XML_ID, variables
            )
        param.set_param(
            'settings_app.background_blend_mode',
            self.theme_background_blend_mode)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        variables = [
            'o-brand-odoo',
            'o-brand-primary',
            'mk-apps-color',
            'mk-appbar-color',
            'mk-appbar-background',
        ]
        colors = self.env['muk_utils.scss_editor'].get_values(
            SCSS_URL, XML_ID, variables
        )
        res.update({
            'theme_color_brand': colors['o-brand-odoo'],
            'theme_color_primary': colors['o-brand-primary'],
            'theme_color_menu': colors['mk-apps-color'],
            'theme_color_appbar_color': colors['mk-appbar-color'],
            'theme_color_appbar_background': colors['mk-appbar-background'],
            'theme_background_blend_mode': params.get_param('settings_app.background_blend_mode', 'normal'),
        })
        return res
