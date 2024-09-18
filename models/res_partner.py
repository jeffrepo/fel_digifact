    # -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
from lxml import etree
import requests
import re

class Partner(models.Model):
    _inherit = 'res.partner'

    def _datos_sat(self, company, vat):
        if vat:
            request_token = "https://felgtaws.digifact.com.gt/gt.com.fel.api.v3/api/login/get_token"
            request_tax_info = "https://felgtaws.digifact.com.gt/gt.com.fel.api.v3/api/SHAREDINFO"
            if company.pruebas_fel:
                request_token = "https://felgttestaws.digifact.com.gt/gt.com.fel.api.v3/api/login/get_token"
                request_tax_info = "https://felgttestaws.digifact.com.gt/gt.com.fel.api.v3/api/SHAREDINFO"

            headers = { "Content-Type": "application/json" }

            data = {
                "Username": company.usuario_fel,
                "Password": company.clave_fel,
            }
            r = requests.post(request_token, json=data, headers=headers, verify=False)
            token_json = r.json()
            if "Token" in token_json:
                token = token_json["Token"]
                headers_nuevos = {
                    "Content-Type": "applcation/json",
                    "Authorization": token,
                }
                r = requests.get(request_tax_info+'?NIT={}&DATA1=SHARED_GETINFONITcom&DATA2=NIT|{}&COUNTRY=GT&USERNAME={}'.format(company.vat.replace('-','').zfill(12), vat, company.usuario_fel), headers= headers_nuevos)
                certificacion_json = r.json()
                if "RESPONSE" in certificacion_json and len(certificacion_json["RESPONSE"]) > 0:
                    if "NOMBRE" in certificacion_json["RESPONSE"][0]:
                        nombre = certificacion_json["RESPONSE"][0]["NOMBRE"]
                        nit = certificacion_json["RESPONSE"][0]["NIT"]
                        return {'nombre': nombre, 'nit': nit}
                    else:
                        return {'nombre': '', 'nit': ''}
                else:
                    raise UserError(certificacion_json)
