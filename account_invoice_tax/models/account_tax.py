##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api
from odoo.tools.misc import formatLang

import logging

_logger = logging.getLogger(__name__)


class AccountTaxRepartitionLine(models.Model):
    _inherit = "account.tax.repartition.line"

    fixed_amount_in_currency = fields.Float()

class AccountTax(models.Model):

    _inherit = "account.tax"

    @api.model
    def _add_accounting_data_to_base_line_tax_details(self, base_line, company, include_caba_tags=False):
    #base_line['tax_details']['taxes_data']
        # import pdb; pdb.set_trace()
        return super()._add_accounting_data_to_base_line_tax_details(base_line, company, include_caba_tags=include_caba_tags)

    # @api.model
    # def _prepare_base_line_tax_repartition_grouping_key(self, base_line, base_line_grouping_key, tax_data, tax_rep_data):
    #     res = super()._prepare_base_line_tax_repartition_grouping_key(base_line, base_line_grouping_key, tax_data, tax_rep_data)
    #     return res

    # @api.model
    # def _add_tax_details_in_base_line(self, base_line, quitcompany, rounding_method=None):
    #     import pdb; pdb.set_trace()
    #     res = super()._add_tax_details_in_base_line(base_line, company, rounding_method=rounding_method)
    #     return res

    def _prepare_tax_line_for_taxes_computation(self, record, **kwargs):
        res = super()._prepare_tax_line_for_taxes_computation(record, **kwargs)
        res['manual_amount_in_currency'] = record.manual_amount_in_currency

        if res['tax_repartition_line_id'].fixed_amount_in_currency:
            res['amount_currency'] = 22
            res['balance'] = 22 * res['sign']
            # res['amount_currency'] = res['tax_repartition_line_id'].fixed_amount_in_currency
            # res['balance'] = res['tax_repartition_line_id'].fixed_amount_in_currency * res['sign']
        return res

#   def _compute_tax_totals(self):
#         """ super() computes these using account.tax.compute_all(). For price-included taxes this will show the wrong totals
#         because it uses the percentage amount on the tax which will always be 1%. This sets the correct totals using
#         account.move.line fields set by `_set_external_taxes()`. """
#         super()._compute_tax_totals()
#         for move in self.filtered(lambda move: move.is_tax_computed_externally and move.tax_totals):
#             lines = move.invoice_line_ids.filtered(lambda l: l.display_type == 'product')
#             tax_totals = move.tax_totals
#             subtotal = tax_totals['subtotals'][0]
#             tax_totals['same_tax_base'] = True
#             tax_totals['total_amount_currency'] = move.currency_id.round(sum(lines.mapped('price_total')))
#             tax_totals['base_amount_currency'] = move.currency_id.round(sum(lines.mapped('price_subtotal')))
#             tax_totals['tax_amount_currency'] = tax_totals['total_amount_currency'] - tax_totals['base_amount_currency']
#             tax_totals['subtotals'] = [
#                 {
#                     **subtotal,
#                     'base_amount_currency': tax_totals['base_amount_currency'],
#                     'tax_amount_currency': tax_totals['tax_amount_currency'],
#                     'tax_groups': [],
#                 }
#             ]
#             if subtotal['tax_groups']:
#                 tax_group = subtotal['tax_groups'][0]
#                 tax_totals['subtotals'][0]['tax_groups'].append({
#                     **tax_group,
#                     'base_amount_currency': tax_totals['base_amount_currency'],
#                     'tax_amount_currency': tax_totals['tax_amount_currency'],
#                 })
#             move.tax_totals = tax_total

    # @api.model
    # def _add_tax_details_in_base_line(self, base_line, company, rounding_method=None):
    #     import pdb; pdb.set_trace()
    #     res = super()._add_tax_details_in_base_line(base_line, company, rounding_method=rounding_method)
    #     return res

    # @api.model
    # def _get_tax_totals_summary(self, base_lines, currency, company, cash_rounding=None):
    #     for base_line in base_lines:
    #         if base_line.record.manual_amount_in_currency:

    #     totals = super()._get_tax_totals_summary(base_lines, currency, company, cash_rounding)
    #     return totals

        # altered = False
        # for base_line in base_lines:
        #     if base_line.record.manual_amount_in_currency:
        #         altered = True

        # # recorrer totals y si comple on la condicion y esta en self.env._context.get('tax_total_origin')
        # tax_total_origin = self.env.context.get('tax_total_origin')
        # if tax_total_origin:
        #     tax_list_origin = self.env.context.get('tax_list_origin')
        #     i = 0
        #     for subtotals in totals['subtotals']:
        #         for tax_group in subtotals['tax_groups']:
        #             id_fixed = tax_list_origin.filtered(lambda x:
        #                 x.amount_type == 'fixed' and x.type_tax_use == 'purchase'
        #                 and x.tax_group_id.id == tax_group['id'])
        #             origin_tax_group = get_origin_group(tax_group['id'], tax_total_origin['subtotals'][i]['tax_groups'])
        #             if id_fixed and origin_tax_group:
        #                 tax_group = origin_tax_group
        #                 altered = True
        #         i += 1
        # if altered:
        #     pass
            # subtotals = []
            # amount_tax = 0
            # for subtotal_title in totals['subtotals_order']:
            #     amount_total = totals['amount_untaxed'] + amount_tax
            #     subtotals.append({
            #         'name': subtotal_title,
            #         'amount': amount_total,
            #         'formatted_amount': formatLang(self.env, amount_total, currency_obj=currency),
            #     })
            #     amount_tax += sum(x['tax_group_amount'] for x in totals['groups_by_subtotal'][subtotal_title])

            # amount_total = totals['amount_untaxed'] + amount_tax

            # totals['amount_tax'] = amount_tax
        # return totals
