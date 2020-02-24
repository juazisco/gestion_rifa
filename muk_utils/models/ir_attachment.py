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

import base64
import logging
import mimetypes

from odoo import api, models, _
from odoo.exceptions import AccessError
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):

    _inherit = 'ir.attachment'

    # ----------------------------------------------------------
    # Helper
    # ----------------------------------------------------------

    @api.model
    def _get_datas_inital_vals(self):
        return {
            'store_fname': False,
            'db_datas': False,
        }

    @api.model
    def _update_datas_vals(self, vals, attach, bin_data):
        vals.update({
            'file_size': len(bin_data),
            'checksum': self._compute_checksum(bin_data),
            'index_content': self._index(bin_data, attach.datas_fname, attach.mimetype),
        })
        return vals

    @api.model
    def _get_datas_clean_vals(self, attach):
        vals = {}
        if attach.store_fname:
            vals['store_fname'] = attach.store_fname
        return vals

    @api.model
    def _clean_datas_after_write(self, vals):
        if 'store_fname' in vals:
            self._file_delete(vals['store_fname'])

    # ----------------------------------------------------------
    # Actions
    # ----------------------------------------------------------

    @api.multi
    def action_migrate(self):
        self.migrate()

    # ----------------------------------------------------------
    # Functions
    # ----------------------------------------------------------

    @api.model
    def storage_locations(self):
        return ['db', 'file']

    @api.model
    def force_storage(self):
        if not self.env.user._is_admin():
            raise AccessError(
                _('Only administrators can execute this action.'))
        storage_domain = {
            'db': ('db_datas', '=', False),
            'file': ('store_fname', '=', False),
        }
        record_domain = [
            '&', ('type', '=', 'binary'),
            '&', storage_domain[self._storage()],
            '|', ('res_field', '=', False), ('res_field', '!=', False)
        ]
        self.search(record_domain).migrate()
        return True

    @api.multi
    def migrate(self):
        record_count = len(self)
        storage = self._storage().upper()
        for index, attach in enumerate(self):
            _logger.info(
                _("Migrate Attachment %s of %s to %s") %
                (index + 1, record_count, storage))
            attach.with_context(migration=True).write({'datas': attach.datas})

    # ----------------------------------------------------------
    # Read
    # ----------------------------------------------------------

    @api.multi
    def _compute_mimetype(self, values):
        if self.env.context.get('migration') and len(self) == 1:
            return self.mimetype or 'application/octet-stream'
        else:
            return super(IrAttachment, self)._compute_mimetype(values)

    # ----------------------------------------------------------
    # Create, Write, Delete
    # ----------------------------------------------------------

    @api.multi
    def _inverse_datas(self):
        location = self._storage()
        for attach in self:
            value = attach.datas
            bin_data = base64.b64decode(value) if value else b''
            vals = self._get_datas_inital_vals()
            vals = self._update_datas_vals(vals, attach, bin_data)
            if value and location != 'db':
                vals['store_fname'] = self._file_write(value, vals['checksum'])
            else:
                vals['db_datas'] = value
            clean_vals = self._get_datas_clean_vals(attach)
            models.Model.write(attach.sudo(), vals)
            self._clean_datas_after_write(clean_vals)
