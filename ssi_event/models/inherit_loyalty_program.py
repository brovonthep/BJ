from odoo import fields, models, api

class LoyaltyProgramModify(models.Model):
    _inherit = 'loyalty.program'

    sale_ok = fields.Boolean(default=False)
    can_view_available_on = fields.Boolean(compute='_compute_can_view_available_on')

    def _compute_can_view_available_on(self):
        for record in self:
            user = self.env.user
            record.can_view_available_on = user.has_group('ssi_event.group_ssi_user') or user.has_group('ssi_event.group_ssi_super_user')