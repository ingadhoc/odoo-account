##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    commission_amount = fields.Monetary(
        compute="_compute_commission_amount",
        currency_field="company_currency_id",
    )
    commission_invoice_ids = fields.Many2many(
        "account.move",
        "account_invoice_commission_inv_rel",
        "commissioned_id",
        "commission_id",
        string="Commission Invoices",
        domain=[("move_type", "in", ("in_invoice", "in_refund"))],
        readonly=True,
        help="Commision invoices where this invoice is commissioned",
        copy=False,
    )
    commissioned_invoice_ids = fields.Many2many(
        "account.move",
        "account_invoice_commission_inv_rel",
        "commission_id",
        "commissioned_id",
        # 'commission_invoice_id',
        domain=[("move_type", "in", ("out_invoice", "out_refund"))],
        string="Commissioned invoices",
        readonly=True,
        help="The invoices that this commission invoice is commissioning",
        copy=False,
    )
    # este campo lo agregamos aca y no en account_usability para no perjudicar
    # a quien no usa comisiones en temas de performance
    date_last_payment = fields.Date(
        compute="_compute_date_last_payment",
        string="Last Payment Date",
        store=True,
    )
    partner_user_id = fields.Many2one(
        "res.users",
        compute="_compute_partner_user",
    )

    @api.depends("partner_id.user_ids")
    def _compute_partner_user(self):
        for rec in self:
            users = rec.partner_id.user_ids
            rec.partner_user_id = users and users[0] or False

    # dependemos de amount_residual que depende de line_ids.amount_residual porque no hay ningun campo almacenado que
    # vaya derecho contra las lineas de pago, toda esa logica ya la tiene implementada el campo
    @api.depends("amount_residual")
    def _compute_date_last_payment(self):
        for rec in self.filtered(lambda x: x.move_type != "entry" and x.state == "posted"):
            payments = rec._get_reconciled_payments()
            rec.date_last_payment = payments and payments[-1].date

    @api.depends("invoice_line_ids.commission_amount")
    @api.depends_context("commissioned_partner_id")
    def _compute_commission_amount(self):
        commissioned_partner_id = self._context.get("commissioned_partner_id")
        if commissioned_partner_id:
            _logger.info("Computing commission amount")
            for rec in self:
                rec.commission_amount = sum(rec.mapped("invoice_line_ids.commission_amount"))
        else:
            self.commission_amount = 0.0

    def web_read(self, specification):
        """Esto lo agregamos para propagar el contexto del commissioned_partner_id
        La idea es que si esta presente el campo commissioned_invoice_ids agregamos en el contexto
        el commissioned_partner_id y llamamos a super de web_read pisando estos valores."""
        res = super().web_read(specification)
        for vals, rec in zip(res, self):
            partner_id = vals.get("partner_id")
            if (
                partner_id
                and isinstance(partner_id, dict)
                and partner_id.get("id")
                and "commissioned_invoice_ids" in specification
            ):
                vals["commissioned_invoice_ids"] = (
                    super(AccountMove, rec)
                    .with_context(commissioned_partner_id=vals["partner_id"]["id"])
                    .web_read({"commissioned_invoice_ids": specification["commissioned_invoice_ids"]})[0][
                        "commissioned_invoice_ids"
                    ]
                )
        return res
