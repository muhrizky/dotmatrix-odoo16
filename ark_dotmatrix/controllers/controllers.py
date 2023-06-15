# -*- coding: utf-8 -*-
# from odoo import http


# class ArkDotmatrix(http.Controller):
#     @http.route('/ark_dotmatrix/ark_dotmatrix', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ark_dotmatrix/ark_dotmatrix/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ark_dotmatrix.listing', {
#             'root': '/ark_dotmatrix/ark_dotmatrix',
#             'objects': http.request.env['ark_dotmatrix.ark_dotmatrix'].search([]),
#         })

#     @http.route('/ark_dotmatrix/ark_dotmatrix/objects/<model("ark_dotmatrix.ark_dotmatrix"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ark_dotmatrix.object', {
#             'object': obj
#         })
