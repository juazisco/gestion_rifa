##########################################################################
#
#    Copyright (C) 2018 MuK IT GmbH
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

from odoo import api, models, fields


class ResCompany(models.Model):

    _inherit = 'res.company'

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------
    logo_image = fields.Binary(
        string="App Logo Image",
        attachment=True)

    background_image = fields.Binary(
        string="Apps Menu Background Image",
        attachment=True)

    background_blend_mode = fields.Selection(
        selection=[
            ('normal', 'Normal'),
            ('multiply', 'Multiply'),
            ('screen', 'Screen'),
            ('overlay', 'Overlay'),
            ('hard-light', 'Hard-light'),
            ('darken', 'Darken'),
            ('lighten', 'Lighten'),
            ('color-dodge', 'Color-dodge'),
            ('color-burn', 'Color-burn'),
            ('hard-light', 'Hard-light'),
            ('difference', 'Difference'),
            ('exclusion', 'Exclusion'),
            ('hue', 'Hue'),
            ('saturation', 'Saturation'),
            ('color', 'Color'),
            ('luminosity', 'Luminosity'),
        ],
        string="Apps Menu Background Blend Mode",
        default='normal')

    default_sidebar_preference = fields.Selection(
        selection=[
            ('invisible', 'Invisible'),
            ('small', 'Small'),
            ('large', 'Large')
        ],
        string="Sidebar Type",
        default='small')

    default_chatter_preference = fields.Selection(
        selection=[
            ('normal', 'Normal'),
            ('sided', 'Sided'),
        ],
        string="Chatter Position",
        default='sided')

    default_system_name = fields.Char(
        'App Name', help='Configure el nombre de la aplicacion')
    default_system_version = fields.Char(
        'Version', help='Configure la version de la aplicacion')
    default_system_favicon = fields.Binary(
        attachment=True, string='Icono Favicon')
    default_system_favicon_mimetype = fields.Selection(
        selection=[('image/x-icon', 'image/x-icon'),
                   ('image/gif', 'image/gif'),
                   ('image/png', 'image/png')],
        string='Favicon mimetype',
        help='Set the mimetype of your file.')
    login_text_title1 = fields.Char('Text 1', help='Text 2')
    login_text_title2 = fields.Char('Text 2', help='Text 2')
    login_text_footer = fields.Char('Footer', help='Footer')
    login_background_image = fields.Binary(
        string="Apps Menu Background Image",
        attachment=True)

    app_show_documentation = fields.Boolean('Mostrar Url de la Documentation', help='Mostrar Documentation')
    app_documentation_url = fields.Char('Url de la Documentacion')
    app_show_support = fields.Boolean('Mostrar Url de Soporte', help='Mostrar enlace de Soporte')
    app_support_url = fields.Char('Url de Soporte')
    app_show_website = fields.Boolean('Mostrar Url adicional', help='Mostrar Url adicional')
    app_website_url = fields.Char('Url del enlace')

    @api.model
    def get_default_all(self):
        app_res_company = self.env['res.company'].search([], order='id desc', limit=1)
        app_show_documentation = app_res_company.app_show_documentation
        app_show_support = app_res_company.app_show_support
        app_show_website = app_res_company.app_show_website
        app_documentation_url = app_res_company.app_documentation_url
        app_support_url = app_res_company.app_support_url
        app_website_url = app_res_company.app_website_url
        return dict(
            app_show_documentation=app_show_documentation,
            app_show_support=app_show_support,
            app_show_website=app_show_website,
            app_documentation_url=app_documentation_url,
            app_support_url=app_support_url,
            app_website_url=app_website_url,
        )
