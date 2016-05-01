# -*- coding: UTF-8 -*-
from __future__ import division
from __future__ import unicode_literals

E_const = 2.718281828459045


def mixing_ratio(Q, q, betta, **kwargs):

    """
    Коэффициент смешения, учитывающий особенности водотока
    определяется по формуле Фролова-Родзиллера
    Q, q - расход воды соответственно в реке и сточных водах, м3/с;
    formula - если 0, то 1 формула, иначе - 2 формула
    n - кратность разбавления
    Q, q, betta - 1 формула;
    Q, q, formula=1, n - 2 формула;
    """
    # по первой формуле
    if not kwargs.get('formula', None):
        result = (1 - betta) / (1 + Q / q * betta)
        text = "γ = (1 - β) / (1 + Q / q · β) =  (1 - {2:.5g}) / (1 + {0} / {1} · {2:.5g}) = {3:.5g}".format(Q, q, betta, result)
    # по второй формуле
    else:
        n = kwargs.get('n', 0)
        if not n:
            assert n != 0, "Для n нужно дать значение"
        result = ((n - 1) * q) / Q
        text = "γ = ((n - 1) · q) / Q =  (({2} - 1) · {1}) / {0} = {3:.5g}".format(Q, q, n, result)
    return (result, text)


def betta_func(alfa, Lf):

    """
    Коэффициент бетта
    alfa - коэффициент, учитывающий гидравлические условия смешения.
    Lf - расстояние по форватеру от места выпуска сточных вод до ближайшего створа
    водопользования, м;
    """

    result = E_const ** (-alfa * Lf ** (1 / 3))
    text = "β = e[sup]-α · 3√Lф[/sup] = e[sup]-{:.5g} · 3√{}[/sup] = {:.5g}".format(alfa, Lf, result)
    return (result, text)


def alfa_func(dzeta, fi, D, q):

    """
    Коэффициент альфа, учитывающий гидравлические условия смешения;
    dzeta - коэффициент зависящий от расположения выпуска сточных вод в водосток;
    fi - коэффициент извилистости водотока, равен отношению расстояний
    между местом сброса сточных вод и местом водопользования по форватеру и по прямой линии;
    D - коэффициент турбулентной диффузии, м2/с;
    q - расход воды в сточных водах, м3/с;
    """

    result = dzeta * fi * (D / q) ** (1 / 3)
    text = "α = ζ · φ · 3√(D / q) = {} · {:.5g} · 3√({:.5g} / {}) = {:.5g}".format(dzeta, fi, D, q, result)
    return (result, text)


def fi_func(Lf, Lpr):

    """
    коэффициент извилистости водотока, равен отношению расстояний между местом сброса
    сточных вод и местом водопользования по форватеру и по прямой линии;
    Lf - расстояние по форватеру от места выпуска сточных вод до
    ближайшего створа водопользования, м;
    Lpr - расстояние по прямой линии от места выпуска сточных вод
    до ближайшего створа водопользования, м;
    """

    result = Lf / Lpr
    text = "φ = Lф / Lпр = {} / {} = {:.5g}".format(Lf, Lpr, result)
    return (result, text)


def D_func(Vsr, Hsr, M=None, C=None):

    """
    коэффициент турбулентной диффузии, м2/с;
    g - ускорение свободного падения, 9.81 м/с2;
    V - средняя скорость течения реки, м/с;
    H - средняя глубина реки, м;
    M - функция от коэффициента Шези, размерность [MC], м/с2
    зависит от С: при С >= 60: M =48, при 10 < C < 60: M = 0.7C + 6;
    C - коэффициент Шези, м(1/2)/с, который принимает значения 15-35
    для горных рек, 20-40 для предгорных рек, 30-70 для равнинных рек.
    """

    result = Vsr * Hsr / 200
    text = "D = V[sub]ср[/sub] · H[sub]ср[/sub] / 200 = {} · {} / 200 = {:.5g}".format(
    Vsr, Hsr, result)
    if M and C:
        result = 9.81 * Vsr * Hsr / (M * C)
        text = "D = g · V[sub]ср[/sub] · H[sub]ср[/sub] / MC = 9.81 · {} · {} / ({} · {}) = {:.5g}".format(
        Vsr, Hsr, M, C)
    return (result, text)


def  fold_dilution(Q, q, gamma):

    """
    кратность разбавления
    Q, q - расход воды соответственно в реке и сточных водах, м3/с;
    gamma - коэффициент смешения;
    """

    result = (gamma * Q + q) / q
    text = "n = (γ · Q + q) / q = ({2:.5g} · {0} + {1}) / {1} = {3:.5g}".format(Q, q, gamma, result)
    return (result, text)


def concentraion_before_target_fold(*args, **kwargs):

    """
    Концентрация вещества перед контрольным
    (расчетным) створом, г/м3
    Сf - концентрация вещества в воде водотока, г/м3;
    Сst - концентрация вещества в сточной воде, г/м3;
    Q, q - расход воды соответственно в реке и сточных водах, м3/с;
    gamma - коэффициент смешения;
    formula - если 0, то 1 формула, иначе - 2 формула
    n - кратность разбавления
    Cst, Cf, Q, q, gamma - 1 формула
    cst, Cf, n - 2 формула
    """

    try:
        Cst, Cf = args[0], args[1]
    except IndexError:
        Cst, Cf = kwargs.get('Cst', 0), kwargs.get('Cf', 0)
    Q, q = kwargs.get('Q', 0), kwargs.get('q', 0)
    gamma = kwargs.get('gamma', 0)
    formula, n = kwargs.get('formula', 0), kwargs.get('n', 0)

    # по первой формуле
    if not formula:
        result = (q * Cst + gamma * Q * Cf) / (q + gamma * Q)
        text = "C[sub]к ст[/sub] = (q · C[sub]ст[/sub] + γ · Q · C[sub]ф[/sub]) / (q + γ · Q) \
= ({1} · {3} + {2:.5g} · {0} · {4}) / ({1} + {2:.5g} · {0}) = {5:.5g} г/м[sup]3[/sup]".format(Q, q, gamma, Cst, Cf, result)
    # по второй формуле
    else:
        if not n:
            assert n != 0, "Для n нужно дать значение"
        result = (Cst - Cf) / n + Cf
        text = "C[sub]к ст[/sub] = (C[sub]ст[/sub] - C[sub]ф[/sub]) / n + C[sub]ф[/sub] \
= ({0} - {1}) / {2:.5g} + {1} = {3:.5g} г/м[sup]3[/sup]".format(Cst, Cf, n, result)
    return (result, text)


if __name__ == "__main__":
    import sys

    def wincode(text):
        if sys.platform == 'win32':
            text = text.encode('utf-8').decode('cp866')
        return text
