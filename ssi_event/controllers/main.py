from odoo import http
from odoo.addons.website.controllers.main import Website
# from odoo.addons.website_sale.controllers.main import WebsiteSale
# from odoo.addons.website_event.controllers.main import WebsiteEventController
# from odoo.addons.event.controllers.main import EventController
# from odoo.addons.web.controllers.home import Home as WebHome
from odoo.http import request, Controller
#from odoo.tools.translate import _
import werkzeug.urls
import werkzeug.utils
import datetime
import re
import json
from werkzeug.utils import redirect

import logging
_logger = logging.getLogger(__name__)

# class WebsiteEventControllerModify(WebsiteEventController):
#     @http.route(['''/event/<model("event.event"):event>'''], type='http', auth="public", website=True, sitemap=True)
#     def event(self, event, **post):
#         res = super().event(event, **post)
#         _logger.info(f"------------{res}--------------")
#         if event.menu_id and event.menu_id.child_id:
#             target_url = event.menu_id.child_id[0].url
#         else:
#             target_url = '/event/%s/register' % str(event.id)
#         if post.get('enable_editor') == '1':
#             target_url += '?enable_editor=1'
#         return request.redirect(target_url+str("?notification="))

# class WebsiteSaleModify(WebsiteSale):

#     def checkout_values(self, order, **kw):
#         res = super().checkout_values(order, **kw)
#         order = order or request.website.sale_get_order(force_create=True)
#         Partner = order.partner_id.with_context(show_address=1).sudo()

#         partner_invoice = order.partner_invoice_id
#         # commercial_partner = order.partner_id.commercial_partner_id
#         # _logger.info(Partner)
#         # _logger.info(commercial_partner)
#         res["customer_partner"] = Partner
#         res["no_show_address"] = self._check_billing_partner_mandatory_fields(partner_invoice)
#         first_redirect = '/shop/address?partner_id=%d&mode=billing' % partner_invoice.id
#         res["first_redirect"] = first_redirect
#         return res
    
#     @http.route(['/shop/checkout'], type='http', auth="public", website=True, sitemap=False)
#     def checkout(self, **post):

#         #res = super().checkout(**post)
#         #_logger.info("======================")
#         #_logger.info(res)
#         order_sudo = request.website.sale_get_order()
#         #_logger.info(order_sudo)
#         #_logger.info(order_sudo._is_public_order())
#         #redirection = self.checkout_check_address(order_sudo)
#         #_logger.info(redirection)
 
#         values = self.checkout_values(order_sudo, **post)
#         return request.render("website_sale.checkout", values)

class WebsiteModify(Website):
    @http.route(['/website/publish'], type='json', auth="user", website=True)
    def publish(self, id, object):
        Model = request.env[object]
        record = Model.browse(int(id))

        if 'website_published' in Model._fields and 'event.event' == Model._name:
            values = {}
            values['website_published'] = record.website_published
            record.write(values)
            return bool(record.website_published)
        res = super().publish(id, object)
        return res

class EventRegistrationConfirm(Controller):
    @http.route(['/event/registration_confirm'], type='http', auth="public", website=True)
    def action_set_done(self, **args):
        _logger.info(f"////////1/////{args}/////////////")
        registration_id = request.env['event.registration'].search([
            ("barcode","=",args["barcode"])
        ])
        _logger.info(f"///////2//////{registration_id.event_id.id}/////////////")
        registration_id.action_set_done()
        return request.redirect(f'/event/{registration_id.event_id.id}?notification=success')

    #@http.route(['/is_public'], auth='public')
    @http.route(['/is_public'], type='json', auth="public", website=True)
    def route_is_public(self):
        # response = redirect(self.list_providers()[0]["auth_link"])
        # return response
        return not request.env.user._is_public()

    # @http.route(['/is_public2'], auth='public')
    # #@http.route(['/is_public'], type='json', auth="public", website=True)
    # def route_is_public2(self):
    #     response = redirect(self.list_providers()[0]["auth_link"])
    #     return response
    #     #return request.env.user

    @http.route(['/base_url_to_js'], type='json', auth="public", website=True)
    def base_url_to_js(self):
        try:
            result = request.env['ir.config_parameter'].sudo().search([
                ("key","=","web.wordpress.base.url")
            ]).value
            _logger.info(result)
            return result
        except Exception as e:
            _logger.error("Failed to retrieve base URLs: %s", e)
            return "/"
        

    @http.route(['/list_providers'], type='json', auth="public", website=True)
    def route_list_providers(self):
        return self.list_providers()
    
    def list_providers(self):
        try:
            providers = request.env['auth.oauth.provider'].sudo().search_read([('enabled', '=', True)])
        except Exception:
            providers = []
        for provider in providers:
            return_url = request.httprequest.url_root + 'auth_oauth/signin'
            state = self.get_state(provider)
            params = dict(
                response_type='token',
                client_id=provider['client_id'],
                redirect_uri=return_url,
                scope=provider['scope'],
                state=json.dumps(state),
                # nonce=base64.urlsafe_b64encode(os.urandom(16)),
            )
            provider['auth_link'] = "%s?%s" % (provider['auth_endpoint'], werkzeug.urls.url_encode(params))
        return providers

    def get_state(self, provider):
        redirect = request.params.get('redirect') or 'web'
        if not redirect.startswith(('//', 'http://', 'https://')):
            redirect = '%s%s' % (request.httprequest.url_root, redirect[1:] if redirect[0] == '/' else redirect)
        state = dict(
            d=request.session.db,
            p=provider['id'],
            r=werkzeug.urls.url_quote_plus(redirect),
        )
        token = request.params.get('token')
        if token:
            state['t'] = token
        return state