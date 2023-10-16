# fel_digifact

Para referencia interna:

```python
from odoo import fields

attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
nsdef = {'dtecomm':'https://www.digifact.com.gt/dtecomm'}
ns = "{https://www.digifact.com.gt/dtecomm}"

fecha = factura.invoice_date.strftime('%Y-%m-%d') if factura.invoice_date else fields.Date.context_today(factura).strftime('%Y-%m-%d')
hora = "07:00:00"
fecha_hora = fecha+'T'+hora

Informacion_COMERCIAL = etree.SubElement(Adenda, ns+"Informacion_COMERCIAL", {attr_qname: 'https://www.digifact.com.gt/dtecomm'}, nsmap=nsdef)
InformacionAdicional = etree.SubElement(Informacion_COMERCIAL, ns+"InformacionAdicional", Version="7.1234654163")
REFERENCIA_INTERNA = etree.SubElement(InformacionAdicional, ns+"REFERENCIA_INTERNA")
REFERENCIA_INTERNA.text = factura.journal_id.code+str(factura.id)
FECHA_REFERENCIA = etree.SubElement(InformacionAdicional, ns+"FECHA_REFERENCIA")
FECHA_REFERENCIA.text = fecha_hora
VALIDAR_REFERENCIA_INTERNA = etree.SubElement(InformacionAdicional, ns+"VALIDAR_REFERENCIA_INTERNA")
VALIDAR_REFERENCIA_INTERNA.text = "VALIDAR"
```
