from odoo import fields, models, api
from odoo.tools.translate import _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_event_track.models.event_event import Event
import logging
_logger = logging.getLogger(__name__)

class EventEventModify(models.Model):
    _inherit = "event.event"

    ############ new field ############
    publication_date = fields.Datetime(string='Publication Date', required=True, tracking=True, default=fields.Datetime.now())
    is_pending_approval = fields.Boolean(default=False)
    is_approved = fields.Boolean(default=False)
    length_visibility = fields.Boolean("visibility", compute="compute_field_visibility", default=False)

    ############ for mark as rejection ############
    reject = fields.Boolean(default=False)

    @api.depends('is_approved', 'is_pending_approval')
    def _compute_show_reject_button(self):
        group_ssi_super_user = self.env.ref('event.group_ssi_super_user')
        for record in self:
            if not record.is_approved and record.is_pending_approval and group_ssi_super_user in self.env.user.groups_id:
                record.show_reject_button = True
            else:
                record.show_reject_button = False

    ############ do normalize stage every time refreshing page ############
    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options)
        self.normalize_stage()
        return res

    ############ get first stage ############
    def get_new_stage(self):
        return self.env['event.stage'].search([('pipe_stage', '=', 'pipe_new')], limit=1, order='sequence')
    
    def get_wait_approved_stage(self):
        return self.env['event.stage'].search([('pipe_stage', '=', 'pipe_pending_approval')], limit=1, order='sequence')
    
    def get_approved_stage(self):
        return self.env['event.stage'].search([('pipe_stage', '=', 'pipe_approved')], limit=1, order='sequence')

    def get_announced_stage(self):
        return self.env['event.stage'].search([('pipe_stage', '=', 'pipe_announced')], limit=1, order='sequence')
    
    def get_booked_stage(self):
        return self.env['event.stage'].search([('pipe_stage', '=', 'pipe_booked')], limit=1, order='sequence')

    def get_on_active_stage(self):
        return self.env['event.stage'].search([('pipe_stage', '=', 'pipe_on_active')], limit=1, order='sequence')

    def get_ended_stage(self):
        return self.env['event.stage'].search([('pipe_stage', '=', 'pipe_end')], limit=1, order='sequence')

    ############ Button Approved Action ############
    def set_is_approved(self):
        self.is_approved = not self.is_approved
        try:
            if(str(self._context['reject']) == str(1)):
                self.is_pending_approval = False
                self.reject = True
            else:
                self.reject = False
        except:
            self.reject = False
        self.normalize_stage()

    def set_is_pending_approval(self):
        self.is_pending_approval = not self.is_pending_approval
        try:
            if(str(self._context['reject']) == str(1)):
                self.reject = True
            else:
                self.reject = False
        except:
            self.reject = False
        self.normalize_stage()

    ############ Button Send Email Action ############
    def action_mass_mailing_attendees(self):
        res = super(EventEventModify, self).action_mass_mailing_attendees()
        _logger.info(f"////////////////////////////{res}//////////////////{self.env.ref('event.model_event_registration').id}//////////")

        return res


    ############ Action Set Section ############
    def action_set_new(self):
        """
        Action which will move the events
        into the first next (by sequence) stage defined as "New"
        """
        first_new_stage = self.get_new_stage()
        if first_new_stage:
            self.write({'stage_id': first_new_stage.id, 'website_published':False})

    def action_set_wait_approved(self):
        """
        Action which will move the events
        into the first next (by sequence) stage defined as "Wait Approve"
        """
        first_wait_approved_stage = self.get_wait_approved_stage()
        if first_wait_approved_stage:
            self.write({'stage_id': first_wait_approved_stage.id, 'website_published':False})

    def action_set_approved(self):
        """
        Action which will move the events
        into the first next (by sequence) stage defined as "Approved"
        """
        first_approved_stage = self.get_approved_stage()
        if first_approved_stage:
            self.write({'stage_id': first_approved_stage.id, 'website_published':False})

    def action_set_announced(self):
        """
        Action which will move the events
        into the first next (by sequence) stage defined as "Announced"
        """
        first_announced_stage = self.get_announced_stage()
        if first_announced_stage:
            self.write({'stage_id': first_announced_stage.id, 'website_published':True})

    def action_set_booked(self):
        """
        Action which will move the events
        into the first next (by sequence) stage defined as "Booked"
        """
        first_booked_stage = self.get_booked_stage()
        if first_booked_stage:
            self.write({'stage_id': first_booked_stage.id, 'website_published':True})

    def action_set_on_active(self):
        """
        Action which will move the events
        into the first next (by sequence) stage defined as "On Active"
        """
        first_on_active_stage = self.get_on_active_stage()
        if first_on_active_stage:
            self.write({'stage_id': first_on_active_stage.id, 'website_published':True})

    def action_set_done(self):
        """
        Action which will move the events
        into the first next (by sequence) stage defined as "Ended"
        """
        first_ended_stage = self.get_ended_stage()
        if first_ended_stage:
            self.write({'stage_id': first_ended_stage.id, 'website_published':True}) 

    ############ Automatic Section ############
    def events_new(self):
        """ move every new events in the next 'new stage' """
        new_events = self.env['event.event'].search([('date_end', '>=' ,fields.Datetime.now()),
                                                    ('is_pending_approval','=',False),
                                                     ('is_approved','=',False)])
        _logger.info(str(new_events)+""" move every new events in the next 'new stage' """)
        if new_events:
            new_events.action_set_new()

    def events_wait_approved(self):
        """ move every wait_approve events in the next 'wait approve stage' """
        wait_approved_events = self.env['event.event'].search([('date_end', '>=' ,fields.Datetime.now()),
                                                            ('is_pending_approval','=',True),
                                                            ('is_approved','=',False)])
        _logger.info(str(wait_approved_events)+""" move every wait_approve events in the next 'wait approve stage' """)
        if wait_approved_events:
            wait_approved_events.action_set_wait_approved()

    def events_approved(self):
        """ move every approved events in the next 'approved stage' """
        approved_events = self.env['event.event'].search([('date_end', '>=', fields.Datetime.now()),
                                                        ('is_pending_approval','=',True),
                                                        ('is_approved','=',True)])
        _logger.info(str(approved_events)+""" move every approved events in the next 'approved stage' """)
        if approved_events:
            approved_events.action_set_approved()

    def events_announced(self):
        """ move every announced events in the next 'announced stage' """
        announced_events = self.env['event.event'].search([('publication_date', '<=' ,fields.Datetime.now()),
                                                        ('date_end', '>=', fields.Datetime.now()),
                                                        ('is_pending_approval','=',True),
                                                        ('is_approved','=',True)])
        _logger.info(str(announced_events)+""" move every announced events in the next 'announced stage' """)
        if announced_events:
            announced_events.action_set_announced()

    def events_booked(self):
        """ move every booked events in the next 'booked stage' """
        booked_events = self.env['event.event'].search([('publication_date', '<=' ,fields.Datetime.now()),
                                                        ('date_end', '>=', fields.Datetime.now()),
                                                        ('is_pending_approval','=',True),
                                                        ('is_approved','=',True)])
        _logger.info(str(booked_events)+""" move every booked events in the next 'booked stage' """)
        for event in booked_events:
            for ticket in event.event_ticket_ids:
                is_available = ticket.sale_available
                if is_available:
                    event.action_set_booked()
                    break

    def events_on_active(self):
        """ move every on_active events in the next 'on active stage' """
        on_active_events = self.env['event.event'].search([('publication_date', '<=' ,fields.Datetime.now()),
                                                        ('date_begin', '<=' ,fields.Datetime.now()), ('date_end', '>=', fields.Datetime.now()),
                                                        ('is_pending_approval','=',True),
                                                        ('is_approved','=',True)])
        _logger.info(str(on_active_events)+""" move every on_active events in the next 'on active stage' """)
        if on_active_events:
            on_active_events.action_set_on_active()

    def events_ended(self):
        """ move every ended events in the next 'ended stage' """
        ended_events = self.env['event.event'].search([
            ('date_end', '<', fields.Datetime.now()),
        ])
        _logger.info(str(ended_events)+""" move every ended events in the next 'ended stage' """)
        if ended_events:
            ended_events.action_set_done()

    def normalize_stage(self):
        self.events_new()
        self.events_wait_approved()
        self.events_approved()
        self.events_announced()
        self.events_booked()
        self.events_on_active()
        self.events_ended()

    ############### Modify Method ###############
    @api.model_create_multi
    def create(self, vals_list):
        """
        Default "stage_id" field are first stage, if they are not set any new stage
        """
        temp = vals_list.copy()
        i = 0
        for item in temp:
            new_stage = self.get_new_stage().id
            if(new_stage):
                item["stage_id"] = new_stage
                vals_list[i] = item
            else:
                pass
            i += 1
        events = super(EventEventModify, self).create(vals_list)
        return events

    ############ hiding button ############
    @api.model
    def compute_field_visibility(self):
        """ compute function for the visibility of the fields """
        for rec in self:
            if self.env.user.has_group("ssi_event.group_ssi_super_user") or self.env.user.has_group("base.group_system"):
                rec.length_visibility = True
            else:
                rec.length_visibility = False

class EventModify(models.Model):
    _inherit = "event.event"
    website_menu = fields.Boolean(default=True)
    register_menu = fields.Boolean(default=True)
    website_track = fields.Boolean(default=True)

    
    def _update_website_menu_entry(self, fname_bool, fname_o2m, fmenu_type):
        res = super(EventModify, self)._update_website_menu_entry(fname_bool, fname_o2m, fmenu_type)
        if(fmenu_type not in ["register", "track"]):
            self[fname_o2m].mapped('menu_id').sudo().unlink()
        return res
    
    def _get_website_menu_entries(self):
        res = super(EventModify, self)._get_website_menu_entries()
        new_res = []
        for menu in res:
            if menu[-1] == "register" or menu[-1] == "track":
                # register = menu
                if menu[0] == _('Register'):
                    new_res.append((_('Register'), '/event/%s/register' % slug(self), False, 0, 'register'))
                if menu[0] == _('Talks'):
                    new_res.append((_('Schedule'), '/event/%s/track' % slug(self), False, 10, 'track'))
                    continue
                if menu[0] == _('Agenda'):
                    continue

        
        return new_res