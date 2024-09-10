from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class EventStageModify(models.Model):
    _inherit = "event.stage"
    pipe_new = fields.Boolean(
        string='New Stage', default=False,
        help='Events will automatically be moved into this stage when they are New or return to edit event because rejection.')
    pipe_pending_approval = fields.Boolean(
        string='Wait for Approval', default=False,
        help='Events will automatically be moved into this stage when they are ready to be approved.')
    pipe_approved = fields.Boolean(
        string='Approved Stage', default=False,
        help='Events will automatically be moved into this stage when they are approved but not yet announced.')
    pipe_announced = fields.Boolean(
        string='Announced Stage', default=False,
        help='Events will automatically be moved into this stage when they are announced.')
    pipe_booked = fields.Boolean(
        string='Booked Stage', default=False,
        help='Events will automatically be moved into this stage when they are booked.')
    pipe_on_active = fields.Boolean(
        string='On Active Stage', default=False,
        help='Events will automatically be moved into this stage when they are active.')
    pipe_stage = fields.Selection([('pipe_new', 'New Stage'), ('pipe_pending_approval', 'Wait for Approval Stage'),
                                   ('pipe_approved', 'Approved Stage'), ('pipe_announced', 'Announced Stage'),
                                   ('pipe_booked', 'Booked Stage'), ('pipe_on_active', 'On Active Stage'),
                                   ('pipe_end', 'End Stage')], string='Action Stage', default='pipe_new')