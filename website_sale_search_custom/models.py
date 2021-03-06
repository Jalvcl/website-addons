from openerp import api, models, fields, SUPERUSER_ID, http
from openerp.http import request

from openerp.addons.website_sale.controllers.main import website_sale as controller

import werkzeug

class website_sale(controller):

    @http.route(['/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', **post):
        request.context['search_tags'] = search
        if category and search:
            category = None
        return super(website_sale, self).shop(page, category, search, **post)


class Product(models.Model):
    _inherit = 'product.template'

    def _extend_domain(self, domain, context):
        if not (context and context.get('search_tags')):
            return domain
        domain = ['|', ('tag_ids', 'ilike', context.get('search_tags'))] + domain
        return domain

    def search_count(self, cr, uid, domain, context=None):
        domain = self._extend_domain(domain, context)
        return super(Product, self).search_count(cr, uid, domain, context=context)

    def search(self, cr, uid, domain, offset=0, limit=None, order=None, context=None, count=False):
        domain = self._extend_domain(domain, context)
        return super(Product, self).search(cr, uid, domain, offset=offset, limit=limit, order=order, context=context, count=count)
