from odoo import api, fields, models

from server.odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[
        ('first_approval', 'First Approval'),
        ('second_approval', 'Second Approval'),
        ('third_approval', 'Third Approval')
    ])

    so_type = fields.Selection([('local', 'Local'), ('export', 'Export')], string='SO Type', default='local')

    def send_to_approve(self):
        for rec in self:
            rec.state="first_approval"

    def action_first_approval(self):
        for rec in self:
            rec.state = 'second_approval'
        # else:
        #     self.state[]

    def action_second_approval(self):
        if self.so_type == 'export':
            for rec in self:
                rec.state = 'third_approval'
        else:
            for rec in self:
                rec.action_confirm()

    def action_third_approval(self):
        # self.state = 'third_approval'
        for rec in self:
            # rec.state = 'sale'
            rec.action_confirm()
        print("confirm")

    def _can_be_confirmed(self):
        self.ensure_one()
        return self.state in {'draft', 'sent','third_approval', 'second_approval'}


    # def action_confirm(self):
    #     for order in self:
    #         if order.state != 'third_approval':
    #             raise UserError("You can only confirm a sale order that has passed third approval.")
    #         # Call the original action_confirm method to proceed with the confirmation
    #         super(SaleOrder, order).action_confirm()



