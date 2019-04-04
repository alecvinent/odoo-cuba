# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

YA_EXISTE = 'Ya existe el elemento.'
ERROR = u'No se pudo realizar la acción.'
ERROR_GRUPOS_RECURSIVOS = u'Error ! No puede crear un Grupo de productos sobre sí mismo.'


class Company(models.Model):
    _inherit = "res.company"

    # ------------------------------------
    @api.model_cr
    def init(self):
        self._cr.execute("UPDATE res_currency SET active=true WHERE active = false")

    # ------------------------------------
    @api.model
    def cron(self):
        # actualizar partner
        logging.info('Actualizando registros de Partner.')
        domain = [('id_subordinacion', '=', None)]
        partners = self.env['res.partner'].search(domain)

        if partners:
            por_defecto = self.env.ref('l10n_cu_config.subordinacion_0')
            partners.write({'id_subordinacion': por_defecto.id})

        domain = [('id_tipo', '=', None)]
        partners = self.env['res.partner'].search(domain)

        if partners:
            por_defecto = self.env.ref('l10n_cu_config.entidad_tipo_1')
            partners.write({'id_tipo': por_defecto.id})

        return


# ------------------------------------
class Lang(models.Model):
    _inherit = "res.lang"

    # ------------------------------------
    @api.model_cr
    def init(self):
        # modificar separador decimales y miles
        # cr.execute("UPDATE res_lang SET thousands_sep=',', decimal_point='.' WHERE code = 'es_ES'")
        self._cr.execute("UPDATE res_lang SET thousands_sep=',', decimal_point='.' WHERE active = true")

        # modificar formato de fecha
        self._cr.execute("UPDATE res_lang SET date_format='%d/%m/%Y' WHERE active = true")

        # -----------------------------------


# ------------------------------------
class Users(models.Model):
    _inherit = 'res.users'

    @api.model_cr
    def init(self):
        # establecer zona horaria por defecto
        self._cr.execute("UPDATE res_partner SET tz='America/Havana' WHERE active = true")


# ------------------------------------
class Partner(models.Model):
    _inherit = 'res.partner'

    # -------------------------
    @api.model_cr
    def init(self):
        # establecer zona horaria por defecto
        self._cr.execute("UPDATE res_partner SET tz='America/Havana' WHERE active = true")

    # -------------------------
    id_organismo = fields.Many2one('res.partner.organismo', string=u'Organismo o Ministerio',
                                   domain=[('activo', '=', True)])
    code = fields.Char(u'Código', size=15, required=True,
                       help=u"Código numérico que identifica la compañía, formado por los últimos 4 dígitos del REUUP. Se actualiza del campo REUUP.")
    id_municipio = fields.Many2one('res.country.state.municipio', 'Municipio')
    id_subordinacion = fields.Many2one('res.partner.subordinacion', u'Subordinación')
    id_tipo = fields.Many2one('res.partner.tipo', u'Tipo de entidad')

    # -------------------------
    _sql_constraints = [
        ('res_partner_name_uniq', 'UNIQUE (name)', YA_EXISTE)
    ]

    @api.model
    def create(self, vals):
        if 'id_subordinacion' not in vals:
            vals['id_subordinacion'] = self.env.ref('l10n_cu_config.subordinacion_0').id
        if 'id_tipo' not in vals:
            vals['id_tipo'] = self.env.ref('l10n_cu_config.entidad_tipo_1').id

        row = super(Partner, self).create(vals)

        try:
            if not row.tz:
                # row.tz = api.model(lambda self: self.env.context.get('tz', 'America/Havana'))
                row.tz = api.model(lambda self: self.env.context.get('tz', False))
        except:
            pass

        return row


class CountryState(models.Model):
    _inherit = 'res.country.state'
    municipio_ids = fields.One2many('res.country.state.municipio', 'state_id', 'Municipios')


class CountryStateMunicipio(models.Model):
    _name = 'res.country.state.municipio'
    _description = "Municipios"

    # ------------------
    name = fields.Char('Nombre', size=64, required=True)
    code = fields.Char(u'Código', size=3, help=u'Código del municipio en 3 caracteres', required=True)
    state_id = fields.Many2one('res.country.state', 'Provincia', required=True)
    country_id = fields.Many2one('res.country', string=u'País',
                                 default=lambda self: self.env.user.company_id.country_id,
                                 related='state_id.country_id', store=True)

    # ------------------

    _order = 'code'
    _sql_constraints = [
        # ('code_municipality_uniq', 'unique(code)', YA_EXISTE)
    ]


class PartnerOrganismo(models.Model):
    _name = "res.partner.organismo"
    _description = "Organismos"
    _rec_name = 'siglas'
    _order = 'name'

    # -----------------------------
    name = fields.Char('Nombre', size=100, required=True, translate=True, help='')
    activo = fields.Boolean('Activo', help=u'Marque si está activo', default=True)
    siglas = fields.Char('Siglas', size=100, required=True, help='')

    _constraints = []

    _sql_constraints = [
        ('unique0', 'unique(name, activo)', YA_EXISTE)
    ]


class PartnerTipo(models.Model):
    _name = "res.partner.tipo"
    _description = "Tipos de Entidades"
    _order = ''

    # -----------------------------
    name = fields.Char(string='Nombre', size=100, required=True, translate=True, help='')
    codigo = fields.Char(string=u'Código', size=100, required=True, translate=True, help='')

    _constraints = []

    _sql_constraints = [
        ('unique0', 'unique(name)', 'Ya ha sido registrado')
    ]


class PartnerSubordinacion(models.Model):
    _name = "res.partner.subordinacion"
    _description = u"Subordinaciones"
    _rec_name = 'name'
    _order = 'name'

    # -----------------------------
    name = fields.Char(string='Nombre', size=100, required=True, translate=True, help='')

    _constraints = []

    _sql_constraints = [
        ('unique0', 'unique(name)', YA_EXISTE)
    ]
