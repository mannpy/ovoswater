# -*- coding: UTF-8 -*-
from __future__ import division
from __future__ import unicode_literals
import sys
from .suspended_solids import Cvdopus, vzv_pur_eff
from .bpk_tools import bpk_dop, bpk_pur_eff, t_func
from .pds_tools import pds, Cdopus, fact_M, pur_eff
from .dilution_tools import (alfa_func,
    betta_func, mixing_ratio, concentraion_before_target_fold,
    fi_func, D_func, fold_dilution    )


class Task(object):

    """ Основной класс решения задачи """

    def __init__(self, Q, q, Lpr, Lf, Hsr, Vsr, gamma, fi, dzeta=1.5, M=0, C=0, n=0):
        self.text = ''
        self.Q, self.q, self.dzeta = Q, q, dzeta
        self.Lpr, self.Lf = Lpr, Lf
        self.Hsr, self.Vsr = Hsr, Vsr
        self.fi, self.gamma = fi, gamma
        self.M, self.Cm, self.n = M, C, n
        if not gamma:
            if self.n:
                self.gamma, text = mixing_ratio(Q, q, formula=1, n=self.n)
                self.update(text, 2)
            else:
                if not fi:
                    self.update("[b]• [color=004D40]Определяем коэффициент извилистости реки[/color][/b]")
                    self.fi, text = fi_func(Lf, Lpr)
                    self.update(text, 2)
                self.update("[b]• [color=004D40]Определяем коэффициент турбулентной диффузии по формуле[/color][/b]")
                self.D, text = D_func(Vsr, Hsr)
                self.update(text, 2)
                self.update("[b]• [color=004D40]Определяем коэффициент α по формуле[/color][/b]")
                self.alfa, text = alfa_func(dzeta, self.fi, self.D, q)
                self.update(text, 2)
                self.update("[b]• [color=004D40]Определяем коэффициент β по формуле[/color][/b]")
                self.betta, text = betta_func(self.alfa, Lf)
                self.update(text, 2)
                self.update("[b]• [color=004D40]Определяем коэффициент смешения[/color][/b]")
                self.gamma, text = mixing_ratio(Q, q, self.betta)
                self.update(text, 2)

    def update(self, text, count=1):
        self.text += text
        for _ in range(count):
            self.text += "\n"

    def find_pds(self):
        self.update("[b]• [color=004D40]Предельно допустимый сброс[/color][/b]")
        self.pds, text = pds(self.q, self.Cdop)
        self.update(text, 2)

    def find_pur_eff(self):
        if self.Cst:
            self.update("[b]• [color=004D40]Необходимая степень очистки сточных вод перед сбросом[/color][/b]")
            self.Z, text = pur_eff(self.Cst, self.Cdop)
            self.update(text, 2)

    @property
    def result(self):
        return self.text



class DilutionTask(Task):

    """ Класс для решения задач по расчету разбавления для проточных водоемов """

    def __init__(self, Q, q, Lpr, Lf, Hsr, Vsr, gamma, fi, Cst, Cf, PDK, dzeta=1.5,
                 M=0, C=0, find_n=False, n=0):
        super(DilutionTask, self).__init__(Q, q, Lpr, Lf, Hsr, Vsr, gamma, fi, dzeta=dzeta, M=M, C=C, n=n)
        self.text = "[i]Расчет разбавления для проточных водоемов[/i]\n\n" + self.text
        self.Cst, self.Cf = Cst, Cf
        if find_n:
            self.update("[b]• [color=004D40]Кратность разбавления[/color][/b]")
            self.n, text = fold_dilution(Q, q, self.gamma)
            self.update(text, 2)
        self.update("[b]• [color=004D40]Рассчитываем ожидаемую концентрацию вещества в контрольном створе[/color][/b]")
        if self.n:
            self.Ckst, text = concentraion_before_target_fold(Cst, Cf, n=self.n, formula=True)
        else:
            self.Ckst, text = concentraion_before_target_fold(Cst, Cf, Q=Q, q=q, gamma=self.gamma)
        self.update(text, 3)
        if self.Ckst < PDK:
            self.update("[b][color=4CAF50]C[sub]к.ст[/sub] ({:.5g} мг/дм[sup]3[/sup]) \
< ПДК ({} мг/дм[sup]3[/sup]). Сброс сточных вод допустим[/color][/b]".format(self.Ckst, PDK))
        elif self.Ckst == PDK:
            self.update("[b][color=4CAF50]C[sub]к.ст[/sub] ({:.5g} мг/дм[sup]3[/sup]) \
= ПДК ({} мг/дм[sup]3[/sup]). Сброс сточных вод допустим[/color][/b]".format(self.Ckst, PDK))
        else:
            self.update("[b][color=E91E63]C[sub]к.ст[/sub] ({:.5g} мг/дм[sup]3[/sup]) \
> ПДК ({} мг/дм[sup]3[/sup]). Сброс сточных вод недопустим. Необходимо применить \
мероприятия по очистке сточных вод.[/color][/b]".format(self.Ckst, PDK), 2)
            if not self.n:
                self.update("[b]• [color=004D40]Кратность разбавления[/color][/b]")
                self.n, text = fold_dilution(Q, q, self.gamma)
                self.update(text, 2)
            self.update("[b]• [color=004D40]Допустимая концентрация загрязняющего вещества \
в сточной воде перед сбросом в водный объект[/color][/b]")
            self.Cdop, text = Cdopus(self.n, PDK, self.Cf)
            self.update(text, 2)
            self.find_pds()
            self.find_pur_eff()



class PdsTask(Task):

    """ Класс для решения задачи ПДС """

    def __init__(self, Q, q, Lpr, Lf, Hsr, Vsr, gamma, fi, Cst, Cf, PDK, n=0, Cdop=0, dzeta=1.5, M=0, C=0, find_M=False):
        super(PdsTask, self).__init__(Q, q, Lpr, Lf, Hsr, Vsr, gamma, fi, dzeta=dzeta, M=M, C=C, n=n)
        self.text = "[i]Расчет ПДС для проточных водоемов[/i]\n\n" + self.text
        self.Cst, self.Cf, self.PDK = Cst, Cf, PDK
        self.Cdop = Cdop
        if not self.Cdop:
            if not self.n:
                self.update("[b]• [color=004D40]Кратность разбавления[/color][/b]")
                self.n, text = fold_dilution(Q, q, self.gamma)
                self.update(text, 2)
            self.update("[b]• [color=004D40]Допустимая концентрация загрязняющего вещества \
в сточной воде перед сбросом в водный объект[/color][/b]")
            self.Cdop, text = Cdopus(self.n, PDK, self.Cf)
            self.update(text, 2)
        self.find_pds()
        if self.Cst < self.Cdop:
            self.update("[b][color=4CAF50]C[sub]доп[/sub] ({:.5g} мг/дм[sup]3[/sup]) \
> C[sub]ст[/sub] ({} мг/дм[sup]3[/sup]), следовательно, перед сбросом в водный объект сточную воду \
не следует подвергать очистке. [/color][/b]".format(self.Cdop, self.Cst), 2)
        elif self.Cst == self.Cdop:
            self.update("[b][color=4CAF50]C[sub]доп[/sub] ({:.5g} мг/дм[sup]3[/sup]) \
= C[sub]ст[/sub] ({} мг/дм[sup]3[/sup]), следовательно, перед сбросом в водный объект сточную воду \
не следует подвергать очистке. [/color][/b]".format(self.Cdop, self.Cst), 2)
        else:
            self.update("[b][color=E91E63]C[sub]доп[/sub] ({:.5g} мг/дм[sup]3[/sup]) \
< C[sub]ст[/sub] ({} мг/дм[sup]3[/sup]). Необходимо применить очистку. [/color][/b]".format(self.Cdop, self.Cst), 2)
            self.find_pur_eff()
        if self.Cst and find_M:
            self.update("[b]• [color=004D40]Фактический сброс М вредного вещества в сточной воде[/color][/b]")
            self.pds, text = fact_M(self.q, self.Cst)
            self.update(text, 2)



class DopusVzvTask(Task):

    """ Расчет допустимой концентрации взвешенных веществ в сточной воде перед сбросом в водоем """

    def __init__(self, Q, q, Lpr, Lf, Hsr, Vsr, gamma, fi, Cvst, Cf, P=0.25, dzeta=1.5, M=0, C=0):
        super(DopusVzvTask, self).__init__(Q, q, Lpr, Lf, Hsr, Vsr, gamma, fi, dzeta=dzeta, M=M, C=C)
        self.text = "[i]Расчет допустимой концентрации взвешенных веществ в сточной воде перед сбросом в водоем[/i]\n\n" + self.text
        self.Cvst, self.Cf, self.P = Cvst, Cf, P
        self.update("[b]• [color=004D40]Концентрация взвешенных веществ в очищенной сточной воде, разрешенной к сбросу в водный объект[/color][/b]")
        self.Cvdop, text = Cvdopus(self.Q, self.q, self.gamma, self.Cf, P=self.P)
        self.update(text, 2)
        if self.Cvst:
            if self.Cvdop < self.Cvst:
                self.update("[b][color=E91E63]C[sub]в.доп[/sub] ({:.5g} мг/дм[sup]3[/sup]) \
< C[sub]в.ст[/sub] ({} мг/дм[sup]3[/sup]). Необходимо применить очистку.[/color][/b]".format(self.Cvdop, self.Cvst), 2)
                self.update("[b]• [color=004D40]Необходимая эффективность очистки сточных вод от взвешенных веществ[/color][/b]")
                self.Z, text = vzv_pur_eff(self.Cvst, self.Cvdop)
                self.update(text, 2)
            elif self.Cvdop == self.Cvst:
                self.update("[b][color=4CAF50]C[sub]в.доп[/sub] ({:.5g} мг/дм[sup]3[/sup]) \
= C[sub]в.ст[/sub] ({} мг/дм[sup]3[/sup]), следовательно, перед сбросом в водный объект сточную воду \
не следует подвергать очистке. [/color][/b]".format(self.Cvdop, self.Cvst), 2)
            else:
                self.update("[b][color=4CAF50]C[sub]в.доп[/sub] ({:.5g} мг/дм[sup]3[/sup]) \
> C[sub]в.ст[/sub] ({} мг/дм[sup]3[/sup]), следовательно, перед сбросом в водный объект сточную воду \
не следует подвергать очистке. [/color][/b]".format(self.Cvdop, self.Cvst), 2)


class DopusBpkTask(Task):

    """ Расчет допустимого значения БПКполн в сточной воде перед сбросом в водоем """

    def __init__(self, Q, q, Lpr, Lf, Hsr, Vsr, gamma, fi, kst, kv, bpk_pdk, bpk_fon, bpk_st=0, t=0, dzeta=1.5, M=0, C=0):
        super(DopusBpkTask, self).__init__(Q, q, Lpr, Lf, Hsr, Vsr, gamma, fi, dzeta=dzeta, M=M, C=C)
        self.text = "[i]Расчет допустимого значения БПК[sub]полн[/sub] в сточной воде перед сбросом в водоем [/i]\n\n" + self.text
        self.kst, self.kv, self.bpk_pdk, self.bpk_fon, self.t = kst, kv, bpk_pdk, bpk_fon, t
        if not self.t:
            self.update("[b]• [color=004D40]Продолжительность перемещения воды от места сброса сточных вод до контрольного створа[/color][/b]")
            self.t, text = t_func(self.Lf, self.Vsr)
            self.update(text, 2)
        self.update("[b]• [color=004D40]Допустимое значение БПК[sub]полн[/sub] сточной воды (БПК[sub]доп[/sub]),\
 разрешенной к сбросу, с учетом того, что БПК[sub]ПДК[/sub]={} мг/л[/color][/b]".format(bpk_pdk))
        self.bpk_dop, text = bpk_dop(Q, q, self.gamma, self.t, kst, kv, bpk_fon, bpk_pdk)
        self.update(text, 2)
        if bpk_st:
            if bpk_st > self.bpk_dop:
                self.update("[b][color=E91E63]БПК[sub]доп[/sub] ({:.5g} мг/л) \
< БПК[sub]ст[/sub] ({} мг/л). Необходимо применить очистку.[/color][/b]".format(self.bpk_dop, bpk_st), 2)
                self.update("[b]• [color=004D40]Необходимая степень очистки сточных вод по БПК[sub]полн[/sub][/color][/b]")
                self.Z, text = bpk_pur_eff(bpk_st, self.bpk_dop)
                self.update(text, 2)
            elif bpk_st == self.bpk_dop:
                self.update("[b][color=4CAF50]БПК[sub]доп[/sub] ({:.5g} мг/л) \
= БПК[sub]ст[/sub] ({} мг/л). Очищать данную сточную воду не следует.[/color][/b]".format(self.bpk_dop, bpk_st), 2)
            else:
                self.update("[b][color=4CAF50]БПК[sub]доп[/sub] ({:.5g} мг/л) \
> БПК[sub]ст[/sub] ({} мг/л). Очищать данную сточную воду не следует.[/color][/b]".format(self.bpk_dop, bpk_st), 2)



if __name__ == '__main__':
    task = Task(45, 0.274, 1750, 2125, 3.1, 0.22, 2259, 152.8, 1.5)
    print(task.result)
