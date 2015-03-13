# -*- coding: utf-8 -*-
from openerp import http

# class L10Cu(http.Controller):
#     @http.route('/l10_cu/l10_cu/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10_cu/l10_cu/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10_cu.listing', {
#             'root': '/l10_cu/l10_cu',
#             'objects': http.request.env['l10_cu.l10_cu'].search([]),
#         })

#     @http.route('/l10_cu/l10_cu/objects/<model("l10_cu.l10_cu"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10_cu.object', {
#             'object': obj
#         })