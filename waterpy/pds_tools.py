# -*- coding: UTF-8 -*-
from __future__ import division
from __future__ import unicode_literals

def pds(q, Cdop):

    """
    Предельно допустимый сброс, г/ч, т/г
    q - наибольший расход сточной воды, м3/ч;
    Сdop - допустимая концентрация загрязняющего вещества
    в сточной воде, которая обеспечивает в контрольном створе
    концентрацию вещества, не превышающую ПДК, г/м3;
        """

    result = q * Cdop
    text = "ПДС = q · C[sub]доп[/sub] = {} · {:.5g} = {:.5g} г/с".format(q, Cdop, result)
    return (result, text)


def Cdopus(n, PDK, Cf):

    """
    n - кратность разбавления;
    PDK - ПДК мг/л, г/м3;
    Сf - концентрация вещества в воде водоток, г/м3;
    """

    result = n * (PDK - Cf) + Cf
    text = "C[sub]доп[/sub] = n · (ПДК - C[sub]ф[/sub]) + C[sub]ф[/sub]) = {0:.5g} · ({1} - {2}) + {2} = {3:.5g} г/м[sup]3[/sup]".format(
    n, PDK, Cf, result)
    return (result, text)

def fact_M(q, Cst):

    """ Фактический сброс вредного вещества """

    result = q * Cst
    text = "M = q · C[sub]ст[/sub] = {} · {:.5g} = {:.5g}  г/ч".format(q, Cst, result)
    return (result, text)

def pur_eff(Cst, Cdop):

    """ Необходимая степень очистки сточных вод перед сбросом в водный объект """

    result = (Cst- Cdop) / Cst * 100
    text = "Z = (C[sub]ст[/sub] - C[sub]доп[/sub]) / C[sub]ст[/sub] · 100%  = ({0} - {1:.5g}) / {1:.5g} · 100% \
 = {2:.5g}%".format(Cst, Cdop, result)
    return (result, text)
