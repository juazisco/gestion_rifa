# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning
import random

SELECTION_STATE_LOT = [
    ('generado', 'En Venta'),
    ('reservado', 'Reservado'),
    ('pagado', 'Pagado'),
    ('ganador', 'Ganador'),
]

DESCRIPCION_RIFA = """
    <div>
        <b>Únete a la Rifa Pro-Salud Eliot</b> <br />
⭐ Por la Recuperación de nuestro hermano y amigo Eliot egresado de la UNI FIC⭐
Cada rifa está 10 soles y los premios son:
<ul>
<li>1er Premio: 01 Telescopio Mod. F700776, ampliación con lentes barlow</li>
<li>2do Premio: 01 Whisky Black Label Johnnie Walker 750 ml. </li>
<li>3er Premio: 01 Licuadora</li>
<li>4to Premio: 01 Micrófono para karaoke Ealsem, ES 1100</li>
<li>5to premio: 01 olla arrocera</li>
</ul>
<b>Sorteo:</b> 12 de marzo a través de Facebook live <br />
    </div>"""

class rifa(models.Model):
    _name = 'rifa.rifa'
    _description = 'rifa.rifa'
    _rec_name = 'ticket_number'

    ticket_number = fields.Char(string='Numero', readonly=True)
    description = fields.Text(default=DESCRIPCION_RIFA)
    state = fields.Selection(SELECTION_STATE_LOT,required=True, default='generado')
    name = fields.Char()
    email = fields.Char()
    telephone = fields.Char()
    address = fields.Char()
    winner = fields.Boolean()
    cost = fields.Integer(default=10)

    @api.model
    def create(self, vals):
        # Get next ticket number from the sequence
        vals['ticket_number'] = self.env['ir.sequence'].next_by_code('rifa.rifa')
        new_id = super(rifa, self).create(vals)       

        return new_id

    @api.multi
    def button_reservado(self):
        for rec in self:
            if rec.name:
                rec.write({'state': 'reservado'})
            else:
                raise Warning('Debe registrar al menos los Nombres')
    
    @api.multi
    def button_pagado(self):
        for rec in self:
            rec.write({'state': 'pagado'})

    @api.multi
    def send_email(self):
        #Send an email out to everyone in the category
        notification_template_reservado = self.env['ir.model.data'].sudo().get_object('rifa', 'message_reservado')
        notification_template_pagado = self.env['ir.model.data'].sudo().get_object('rifa', 'message_pagado')
        values = {}
        for rec in self:
            if rec.state == 'reservado':
                values = notification_template_reservado.generate_email([self.id])[self.id]
            
            if rec.state == 'pagado':
                values = notification_template_pagado.generate_email([self.id])[self.id]
            if len(values)>0:
                values['body_html'] = values['body_html']
                values['email_to'] = self.email
                print(values)
                send_mail = self.env['mail.mail'].create(values)
                send_mail.send()

                raise Warning('El mensaje fué enviado')

                #Remove the message from the chatter since this would bloat the communication history by a lot
                #send_mail.mail_message_id.res_id = 0

class sorteo(models.Model):
    _name = 'rifa.sorteo'
    _description = 'rifa.sorteo'
    _rec_name = 'nro_premio'

    nro_premio = fields.Char(string='Nº Premio')
    description = fields.Text()
    state = fields.Selection([('no_sorteado', 'No Sorteado'),('sorteado', 'Sorteado')],required=True, default='no_sorteado')
    nro_participantes  = fields.Integer()
    ticket_winner = fields.Many2one('rifa.rifa', string="Ganador")
    ticket_winner_name = fields.Char(related='ticket_winner.name')
    ticket_winner_number = fields.Char(related='ticket_winner.ticket_number',default='')
    ticket_winner_email = fields.Char(related='ticket_winner.email')
    ticket_winner_telephone = fields.Char(related='ticket_winner.telephone')

    @api.multi
    def button_liberar_sorteo(self):
        for rec in self:
            if rec.ticket_winner:
                #rifa_sorteada = self.env['rifa.rifa'].search([('id','=',rec.ticket_winner)])
                rec.ticket_winner.write({
                    'winner': False
                })
                rec.write({'state': 'no_sorteado','ticket_winner':None})

            else:
                raise Warning('No se pudo liberar el Premio')
    
    @api.multi
    def rifa_sortear(self):
        list_pagados = self.env['rifa.rifa'].search([('state','=','pagado'),('winner','!=',True)])
        try:        
            nro_participantes = len(list_pagados)
            winner_ticket = random.choice(list_pagados)
            self.update({'ticket_winner':winner_ticket})
            self.write({'state': 'sorteado','nro_participantes':nro_participantes})
            winner_ticket.write({
                'winner': True
            })
        except:
            raise Warning('No se pudo realizar el Sorteo')
  
  