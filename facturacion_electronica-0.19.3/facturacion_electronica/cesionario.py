# -*- coding: utf-8 -*-
from facturacion_electronica import clase_util as util
from facturacion_electronica.clase_util import UserError


class Cesionario():

    def __init__(self, vals):
        util.set_from_keys(self, vals)

    @property
    def RUT(self):
        if not hasattr(self, '_rut'):
            return False
        return self._rut

    @RUT.setter
    def RUT(self, val):
        self._rut = val

    @property
    def RazonSocial(self):
        if not hasattr(self, '_razon_social'):
            return False
        return self._razon_social[:100]

    @RazonSocial.setter
    def RazonSocial(self, val):
        self._razon_social = val

    @property
    def Direccion(self):
        if not hasattr(self, '_direccion'):
            return False
        return self._direccion[:70]

    @Direccion.setter
    def Direccion(self, val):
        self._direccion = val

    @property
    def eMail(self):
        if not hasattr(self, '_email'):
            return False
        return self._email

    @eMail.setter
    def eMail(self, val):
        self._email = val
