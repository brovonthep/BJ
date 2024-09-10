from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class EventTrackModify(models.Model):
    _inherit = "event.track"
    date = fields.Datetime(string='Schedule Date')