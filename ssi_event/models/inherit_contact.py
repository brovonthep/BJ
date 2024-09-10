from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class EventStageModify(models.Model):
    _inherit = "res.partner.title"
    active = fields.Boolean("Active", default=True)