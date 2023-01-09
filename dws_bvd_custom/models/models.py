# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductAttribute(models.Model):
    _inherit = "product.attribute"
    
    # display_type = fields.Selection(selection_add=[
    #     ('calculated','Calculated')], ondelete={'calculated': 'cascade'})
    value_type = fields.Selection([('integer', 'Integer'), ('float', 'Float'),('text','Text'),('calculation','Calculation')])    
    formula = fields.Char('Formula')