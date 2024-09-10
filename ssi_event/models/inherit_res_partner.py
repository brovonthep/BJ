from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

_get_company_type_ssi_event_user = [('specker', 'Specker'), ('location', 'Location'),
                                ('online_meeting', 'Online Meeting'), ('company', 'Company')]
_get_company_type_ssi_admin = [('specker', 'Specker'), ('person', 'User'), ('location', 'Location'),
                                ('online_meeting', 'Online Meeting'), ('company', 'Company')]

class PartnerModify(models.Model):
    _inherit = 'res.partner'

    _interface_company_type = fields.Selection(string='Contact Type',
                                selection='_get_company_type',
                                default='specker')
    company_type = fields.Selection(compute='_compute_company_type')
    _compute_readonly_field = fields.Boolean(default=False, compute="_compute_readonly")

    @api.model
    def _get_company_type(self):
        if self.user_has_groups("ssi_event.group_ssi_user"):
            return _get_company_type_ssi_event_user
        else:
            return _get_company_type_ssi_admin

    @api.onchange('_interface_company_type')
    def _on_change_compute_company(self):
        if( self.user_has_groups('ssi_event.group_ssi_user') and (self._interface_company_type == "person" 
                                                            or self.env['res.partner'].search([
                                                                ('id','=',self._origin.id)
                                                                ])._interface_company_type == "person") ):             
            self._interface_company_type = self.env['res.partner'].search([('id','=',self._origin.id)])._interface_company_type 
            return {'value': {'_interface_company_type':self.env['res.partner'].search([('id','=',self._origin.id)])._interface_company_type},
                    'warning': {'title': ('Warning'),
                                'message': 'The requested operation cannot be completed due to your access rights. You are not allowed to change the "Contact type" to User. Please contact your system administrator.',
                    },
            }
        _logger.info(f"=-------={self.env['res.partner'].search([('id','=',self._origin.id)])._interface_company_type}=-------=")
        _logger.info(f"=-------={self._interface_company_type}=-------=")

    @api.depends('_interface_company_type')
    def _compute_company_type(self):
        res = super(PartnerModify, self)._compute_company_type()
        _logger.info(f"{self.company_type} *************** {self._interface_company_type}")
        _mapping_1 = {"specker":"person", "person":"person", "location":"company", "online_meeting":"company", "company":"company"}
        _mapping_2 = {"person":"specker", "company":"company"}
        try:
            if(self._interface_company_type):
                self.company_type = _mapping_1[self._interface_company_type]
            else:
                self._interface_company_type = _mapping_2[self.company_type]
        except:
            pass
        _logger.info(f"{self.company_type} /////////////// {self._interface_company_type}")
        return res

    @api.depends('_interface_company_type')
    def _compute_readonly(self):
        # Define the logic to determine if the field should be read-only
        field_value = self._interface_company_type
        
        # Check if the user is in the target group and if the field_value meets the condition
        if self.user_has_groups('ssi_event.group_ssi_user') and field_value == 'person':
            self._compute_readonly_field = True
        else:
            self._compute_readonly_field = False