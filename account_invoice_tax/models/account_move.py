from odoo import models, fields
import logging
import copy

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    manual_amount_in_currency = fields.Float()

    # def onchange(self, values, field_names, fields_spec):
    #     import pdb; pdb.set_trace()
    #     return super().onchange(values, field_names, fields_spec)

class AccountMove(models.Model):

    _inherit = "account.move"

    # def _get_rounded_base_and_tax_lines(self, round_from_tax_lines=True):
    #     base_lines, tax_lines = super()._get_rounded_base_and_tax_lines(round_from_tax_lines=round_from_tax_lines)
    #     #import pdb; pdb.set_trace()
    #     for tax_line in tax_lines:
    #         tax_aml = self.line_ids.filtered(lambda x: x.tax_repartition_line_id == tax_line['tax_repartition_line_id'] and x.manual_amount_in_currency)
    #         tax_line['amount_currency'] = tax_aml.manual_amount_in_currency
    #         tax_line['balance'] = tax_aml.manual_amount_in_currency * tax_line['sign']
    #     return base_lines, tax_lines

    def onchange(self, values, field_names, fields_spec):
        old_tax_totals = copy.copy(self.tax_totals)
        # if 'invoice_line_ids' in field_names:
        #     import pdb; pdb.set_trace()

        if 'tax_totals' in field_names:
            invoice_totals = values['tax_totals']
            for subtotal in invoice_totals['subtotals']:
                for tax_group in subtotal['tax_groups']:
                    tax_lines = self.line_ids.filtered(lambda line: line.tax_line_id.tax_group_id.id == tax_group['id'])
                    for tax_line in tax_lines.filtered(lambda x: x.tax_line_id.amount_type == 'fixed' and x.tax_line_id.type_tax_use == 'purchase'):
                        tax_line.tax_repartition_line_id.fixed_amount_in_currency = tax_line.amount_currency


            import pdb; pdb.set_trace()
        return super().onchange(values, field_names, fields_spec)

    def _inverse_tax_totals(self):
        super()._inverse_tax_totals()
        if self.env.context.get('skip_invoice_sync'):
            return
        with self._sync_dynamic_line(
            existing_key_fname='term_key',
            needed_vals_fname='needed_terms',
            needed_dirty_fname='needed_terms_dirty',
            line_type='payment_term',
            container={'records': self},
        ):
            for move in self:
                if not move.is_invoice(include_receipts=True):
                    continue
                invoice_totals = move.tax_totals
                import pdb; pdb.set_trace()
                for subtotal in invoice_totals['subtotals']:
                    for tax_group in subtotal['tax_groups']:
                        tax_lines = move.line_ids.filtered(lambda line: line.tax_line_id.tax_group_id.id == tax_group['id'])
                        for tax_line in tax_lines.filtered(lambda x: x.tax_line_id.amount_type == 'fixed' and x.tax_line_id.type_tax_use == 'purchase'):
                            tax_line.manual_amount_in_currency = tax_line.amount_currency
                            tax_line.tax_repartition_line_id.fixed_amount_in_currency = tax_line.amount_currency


    # def _compute_tax_totals(self):
    #     """ Computed field used for custom widget's rendering.
    #         Only set on invoices.
    #     """
    #     for move in self:
    #         super(AccountMove, move.with_context(
    #             tax_list_origin=move._origin.mapped('invoice_line_ids.tax_ids'),
    #             tax_total_origin=move._origin.tax_totals)
    #         )._compute_tax_totals()

    # @api.returns('self', lambda value: value.id)
    # def copy(self, default=None):
    #     res = super().copy(default)

    #     if res.move_type in ['in_refund', 'in_invoice']:
    #         res.tax_totals = self.tax_totals

    #     return res
