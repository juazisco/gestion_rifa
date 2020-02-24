# -*- coding: utf-8 -*-

from odoo import api, models


class View(models.Model):
    _inherit = 'ir.ui.view'

    @api.model
    def render_template(self, template, values=None, engine='ir.qweb'):
        if template in ('web.login', 'web.webclient_bootstrap'):
            if not values:
                values = {}
            app_config_settings = self.env['res.company'].sudo().search([], order='id desc', limit=1)
            values['title'] = app_config_settings.default_system_name
        return super(View, self).render_template(
            template, values=values, engine=engine)
