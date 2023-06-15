# -*- coding: utf-8 -*-

from odoo import models, fields, api
import html2text

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    print_data = fields.Text('Print Data') 
    
    def generate_print_data(self):
        tpl = self.env['mail.template'].search([('name','=','Dotmatrix SO')])
        # fields = list(self._fields.keys())
        # data = tpl._render_template(tpl.body_html,'sale.order',self.ids, post_process=False)
        data = tpl.generate_email(
            self.ids,
            ['body_html']
        )
        raw = list(data.values())[0]['body']
        self.print_data = html2text.html2text(raw).replace('?', ' ').replace('\n\\','\n')

    def action_confirm(self):
        res=super(SaleOrder,self).action_confirm()
        self.generate_print_data()
        return res

    def action_cancel(self):
        self.print_data = ''
        return super(SaleOrder,self).action_cancel()

    def print_button(self):
        return

    def get_data(self):
        print(self.print_data)
        return {
            'data' : {
                'text' : self.print_data
            }
        }
    
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    print_data = fields.Text('Print Data')
    button_times = fields.Integer('Button Times',default="0")
    
    def generate_print_data(self):
        tpl = self.env['mail.template'].search([('name','=','Dotmatrix DO')])
        # fields = list(self._fields.keys())
        # data = tpl._render_template(tpl.body_html,'sale.order',self.ids, post_process=False)
        data = tpl.generate_email(
            self.ids,
            ['body_html']
        )
        raw = list(data.values())[0]['body']
        self.print_data = html2text.html2text(raw).replace('?', ' ').replace('\n\\','\n').replace('\\','')

    def button_validate(self):
        res=super(StockPicking,self).button_validate()
        self.generate_print_data()
        return res

    def action_cancel(self):
        self.print_data = ''
        return super(StockPicking,self).action_cancel()

    def print_button(self):
        return

    def get_data(self):
        print(self.print_data)
        self.button_times += 1
        return {
            'data' : {
                'text' : self.print_data
            }
        }

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    print_data = fields.Text('Print Data')    

    def generate_print_data(self):
       tpl = self.env['mail.template'].search([('name','=','Dotmatrix Kwitansi')])
       # fields = list(self._fields.keys())
       # data = tpl._render_template(tpl.body_html,'sale.order',self.ids, post_process=False)
       data = tpl.generate_email(
           self.ids,
           ['body_html']
       )
       raw = list(data.values())[0]['body']
       self.print_data = html2text.html2text(raw).replace('?', ' ')

    def action_post(self):
        res = super(AccountPayment,self).action_post()
        self.generate_print_data()
        return res

    def action_cancel(self):
        self.print_data = ''
        return super(AccountPayment,self).action_cancel()

    def print_button(self):
        return

    def get_data(self):
        print(self.print_data)
        return {
            'data' : {
                'text' : self.print_data
            }
        }