from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from water import DilutionTask, PdsTask, DopusVzvTask, DopusBpkTask


class MainClass(Widget):

    """ Основной виджет-класс """

    pass


class ImageButton(ButtonBehavior, Image):

    """ Класс кнопка-картинка """

    def change_color(self, clear=0, color=(0, 0, 0, 0.1)):
        with self.canvas.after:
            Color(*color)
            Rectangle(pos=self.pos, size=self.size)
            if clear:
                self.canvas.after.clear()





class OvosWaterSet(Screen):

    """ класс для экрана-настроек """

    def add_widget_to_screen(self, screen, label_text, input_id, input_text="", markup=False, color=(0, 0, 0, 1)):
        """ добавляет виджеты на экран """
        screen.layout.add_widget(Label(text=label_text, color=color, size_hint_y=None, markup=markup))
        screen.layout.add_widget(TextInput(id=input_id, text=input_text, multiline=False,
                                             size_hint_y=None, input_type="number", input_filter="float"))

    def if_gamma(self, gamma, fi, n, mc):

        """ Добавляет элементы в зависимости от гамма и фи """

        if gamma.active:
            self.add_widget_to_screen(self.ovosinput, "Q (м[sup]3[/sup]/c)", "Q", markup=True)
            self.add_widget_to_screen(self.ovosinput, "γ (Гамма)", "gamma")
        else:
            self.add_widget_to_screen(self.ovosinput, "Q (м[sup]3[/sup]/c)", "Q", markup=True)
            if n.active:
                self.add_widget_to_screen(self.ovosinput, "n", "n")
            else:
                if fi.active:
                    self.add_widget_to_screen(self.ovosinput, "φ", "fi")
                else:
                    self.add_widget_to_screen(self.ovosinput, "L [sub]пр[/sub] (м)", "Lpr", markup=True)
                self.add_widget_to_screen(self.ovosinput, "L [sub]ф[/sub] (м)", "Lf", markup=True)
                self.add_widget_to_screen(self.ovosinput, "H [sub]ср[/sub] (м)", "Hsr", markup=True)
                self.add_widget_to_screen(self.ovosinput, "V [sub]ср[/sub] (м/c)", "Vsr", markup=True)
                self.add_widget_to_screen(self.ovosinput, "ζ (дзета)", "dzeta", input_text="1.5", markup=True)
                if mc.active:
                    self.add_widget_to_screen(self.ovosinput, "M (м/с[sup]2[/sup])", "M", markup=True)
                    self.add_widget_to_screen(self.ovosinput, "C (м[sup]1/2[/sup]/c)", "C", markup=True)

    def add_cf_pdk(self):
        self.add_widget_to_screen(self.ovosinput, "С[sub] ф[/sub] (г/м[sup]3[/sup])", "Cf", markup=True)
        self.add_widget_to_screen(self.ovosinput, "ПДК (г/м[sup]3[/sup])", "PDK", markup=True)

    def apply(self):

        """ применить настройки """

        # очистить экран
        self.ovosinput.layout.clear_widgets()

        self.add_widget_to_screen(self.ovosinput, "q (м[sup]3[/sup]/c)", "q", markup=True)
        self.if_gamma(self.gamma, self.fi, self.n, self.mc)
        # БЛОК 1
        if self.task1.active:
            self.add_cf_pdk()
            self.add_widget_to_screen(self.ovosinput, "С[sub] ст[/sub] (г/м[sup]3[/sup])", "Cst", markup=True)

        elif self.task2.active:
            if not self.task2_Cdop.active:
                self.add_cf_pdk()
                if not self.cdop.active:
                    self.add_widget_to_screen(self.ovosinput, "С[sub] доп.[/sub] (г/м[sup]3[/sup])", "Cdop", markup=True)
            else:
                self.add_widget_to_screen(self.ovosinput, "С[sub] доп.[/sub] (г/м[sup]3[/sup])", "Cdop", markup=True)
            if self.task2_M.active or self.task2_Z.active:
                self.add_widget_to_screen(self.ovosinput, "С[sub] ст[/sub] (г/м[sup]3[/sup])", "Cst", markup=True)

        elif self.task3.active:
            self.add_widget_to_screen(self.ovosinput, "P (мг/дм[sup]3[/sup])", "P", input_text="0.25", markup=True)
            self.add_widget_to_screen(self.ovosinput, "С[sub] ф[/sub] (г/м[sup]3[/sup])", "Cf", markup=True)
            if self.task3_Z.active:
                self.add_widget_to_screen(self.ovosinput, "С[sub] в.ст[/sub] (г/м[sup]3[/sup])", "Cvst", markup=True)

        elif self.task4.active:
            self.add_widget_to_screen(self.ovosinput, "БПК[sub] ПДК[/sub] (мг/дм[sup]3[/sup])", "bpk_pdk", markup=True)
            self.add_widget_to_screen(self.ovosinput, "БПК[sub] ф[/sub] (мг/дм[sup]3[/sup])", "bpk_fon", markup=True)
            self.add_widget_to_screen(self.ovosinput, "k[sub] ст[/sub]", "kst", markup=True)
            self.add_widget_to_screen(self.ovosinput, "k[sub] v[/sub]", "kv", markup=True)
            if self.t.active:
                self.add_widget_to_screen(self.ovosinput, "t (сут.)", "t")
            else:
                self.add_widget_to_screen(self.ovosinput, "L [sub]ф[/sub] (м)", "Lf", markup=True)
                self.add_widget_to_screen(self.ovosinput, "V [sub]ср[/sub] (м/c)", "Vsr", markup=True)
            if self.task4_Z.active:
                self.add_widget_to_screen(self.ovosinput, "БПК[sub] ст[/sub] (мг/дм[sup]3[/sup])", "bpk_st", markup=True)



class OvosWaterInput(Screen):

    """ класс для экрана-ввода данных """

    def calculate(self):
        dataset = {}
        data = ("Q", "q", "Vsr", "Hsr", "Lpr", "Lf", "fi", "gamma", "Cst", "Cf", "dzeta", "PDK",
        	"n", "M", "C", "Cvst", "bpk_st", "bpk_fon", "bpk_pdk", "t", "kst", "kv", "Cdop", "P")
        not_zero = ("q",)

        for w in self.walk():
            if w.id is not None:
                try:
                    dataset[w.id] = float(w.text)
                except ValueError:
                    w.text = "!"
                    dataset[w.id] = w.text

        for d in data:
            if d not in dataset:
                dataset[d] = 0

        # !!! учесть нули !!!
        if dataset["q"] == 0:
            dataset["q"] = "!"

        if "!" not in dataset.values():
            # если первая задача
            if self.ovosset.task1.active:
                task = DilutionTask(Q=dataset['Q'], q=dataset['q'], Lpr=dataset['Lpr'],
                             Lf=dataset['Lf'], Hsr=dataset['Hsr'], Vsr=dataset['Vsr'],
                             gamma=dataset['gamma'], fi=dataset['fi'],
                             Cst=dataset['Cst'], Cf=dataset['Cf'],
                             PDK=dataset['PDK'], dzeta=dataset['dzeta'],
                             M=dataset['M'], C=dataset['C'],
                             n=dataset['n'], find_n=self.ovosset.find_n.active)
            elif self.ovosset.task2.active:
                task = PdsTask(Q=dataset['Q'], q=dataset['q'], Lpr=dataset['Lpr'],
                             Lf=dataset['Lf'], Hsr=dataset['Hsr'], Vsr=dataset['Vsr'],
                             gamma=dataset['gamma'], fi=dataset['fi'],
                             Cst=dataset['Cst'], Cf=dataset['Cf'],
                             PDK=dataset['PDK'], dzeta=dataset['dzeta'],
                             M=dataset['M'], C=dataset['C'],
                             n=dataset['n'], Cdop=dataset["Cdop"], find_M=self.ovosset.task2_M.active)
            elif self.ovosset.task3.active:
                task = DopusVzvTask(Q=dataset['Q'], q=dataset['q'], Lpr=dataset['Lpr'],
                             Lf=dataset['Lf'], Hsr=dataset['Hsr'], Vsr=dataset['Vsr'],
                             gamma=dataset['gamma'], fi=dataset['fi'],
                             Cvst=dataset['Cvst'], Cf=dataset['Cf'],
                             P=dataset['P'], dzeta=dataset['dzeta'],
                             M=dataset['M'], C=dataset['C'])
            elif self.ovosset.task4.active:
                task = DopusBpkTask(Q=dataset['Q'], q=dataset['q'], Lpr=dataset['Lpr'],
                             Lf=dataset['Lf'], Hsr=dataset['Hsr'], Vsr=dataset['Vsr'],
                             gamma=dataset['gamma'], fi=dataset['fi'],
                             dzeta=dataset['dzeta'], kst=dataset['kst'],
                             kv = dataset['kv'], bpk_pdk = dataset['bpk_pdk'],
                             bpk_fon = dataset['bpk_fon'], bpk_st = dataset['bpk_st'],
                             t = dataset['t'],
                             M=dataset['M'], C=dataset['C'])
            self.manager.result.text=task.result
            self.manager.current = '_result'


class OvosWaterApp(App):

    """ Основной класс-приложение """

    def build(self):
        return MainClass()

    def on_pause(self):
        return True

    def on_resume(self):
        passs


if __name__ == '__main__':
    OvosWaterApp().run()
