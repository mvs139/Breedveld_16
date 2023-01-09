# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

from odoo.addons.sale_product_configurator.controllers.main import ProductConfiguratorController


class CalcFieldController(http.Controller):
    @http.route(['/sale/calculate_fields'], type='json', auth="user", methods=['POST'])
    def calculate_fields(self,product_tmpl_id,values, **kw):
        calculations = {}
        product_template = request.env['product.template'].browse(int(product_tmpl_id))
        for attribute_line in product_template.attribute_line_ids:
            if attribute_line.attribute_id.value_type == 'calculation':
                formula = attribute_line.attribute_id.formula
                for attr,value in values.items():
                    formula = formula.replace("[" + attr + "]", str(value))
                calculations.update({attribute_line.attribute_id.name: eval(formula)})
            
        
        return calculations

class ProductConfiguratorController(ProductConfiguratorController):
    @http.route(['/sale_product_configurator/configure'], type='json', auth="user", methods=['POST'])
    def configure(self, product_template_id, pricelist_id, **kw):
        add_qty = float(kw.get('add_qty', 1))
        product_template = request.env['product.template'].browse(int(product_template_id))
        pricelist = self._get_pricelist(pricelist_id)

        product_combination = False
        attribute_value_ids = set(kw.get('product_template_attribute_value_ids', []))
        attribute_value_ids |= set(kw.get('product_no_variant_attribute_value_ids', []))
        if attribute_value_ids:
            product_combination = request.env['product.template.attribute.value'].browse(attribute_value_ids)

        if pricelist:
            product_template = product_template.with_context(pricelist=pricelist.id, partner=request.env.user.partner_id)
        
        print("test")
        print(product_combination)
        return request.env['ir.ui.view']._render_template(
            "sale_product_configurator.configure",
            {
                'product': product_template,
                'pricelist': pricelist,
                'add_qty': add_qty,
                'product_combination': product_combination
            },
        )

