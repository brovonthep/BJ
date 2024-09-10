import logging
_logger = logging.getLogger(__name__)

from odoo import api, models

#from odoo.addons import base
#base.models.res_users.USER_PRIVATE_FIELDS.append('oauth_access_token')

class ResUsers(models.Model):
    _inherit = 'res.users'
    @api.model
    def _generate_signup_values(self, provider, validation, params):
        values = super(ResUsers, self)._generate_signup_values(provider, validation, params)
        _logger.info(values)
        try:
            values["name"] = validation["FirstName"]+ " " + validation["LastName"]
        except:
            pass
        try:
            values["email"] = validation["Email"]
        except:
            pass
        try:
            values["login"] = validation["Username"]
        except:
            pass
        try:
            values["phone"] = validation["Phone"]
        except:
            pass
        _logger.info(values)
        return values