from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
import threading
from kivy.clock import mainthread,Clock
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import time

import requests
from hoverable import HoverBehavior
import portalAccess
from kivy.properties import StringProperty,ObjectProperty
login = "https://www.unilus.ac.zm/Students/Login.aspx"
studentPortal = "https://www.unilus.ac.zm/Students/StudentPortal.aspx"
link = "http://192.168.137.1:3000/vote"
Window.fullscreen = 'auto'


candidate_names = {"ur":{"01":"Pumulo Mutemwa","02":"Taonga Mutambo","03":"Samuel Nsalange","04":"Yolanda Dias","05":"Jonah Kafunda","06":"Felistus Lwipa","07":"Lupasha Chellah","08":"Leonard Subulwa","09":"Sepo Liyungu","10":"Chilufya Mukuka"}
,"ud":{"01":"Nsama Mpundu","02":"Victor Chizawu","03":"Mwiza Bwali","04":"Sharon Tembo","05":"Mwanakasele Muchindu","06":"Chola Chintu","07":"Fassie Mubanga","08":"Abdullah Kamunga","09":"Christopher Kanoyangwa","10":"Mwenzi Lungu"}}

position_names=["President","Vice President","Secretary General","Publicity Secretary","Treasurer","Sports Secretary","Entertainment Secretary","Transport and Accommodation Secretary","Vice Treasurer","Academic Secretary"]
class Loading_gif(FloatLayout,ButtonBehavior):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(self.parent)
    pass
class Home (ScreenManager):
    pass
class LoginScreen(Screen,FloatLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    def login(self):

        pass
    def access(self,username,password):
        ""

    pass

class Submitting(FloatLayout):

    pass

class Submit(Image,ButtonBehavior):
    submitting=Submitting()
    pressed=False
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
    #         load async task
            self.submitting.add_widget(Loading_gif())
            self.parent.parent.parent.parent.parent.add_widget(self.submitting)
            threading.Thread(target=self.submit_to_db).start()
    def submit_to_db(self):
        if not self.pressed:
            self.pressed=True
            data = self.parent.parent.parent.parent.parent.selection_schema
            data["timestamp"]=time.time()
            data["campus"]="main"
            self.widget = Loading_gif(id="loading")
            try:
                with open("./id.oo", "r")as w:
                    data["voter_id"]=w.read()
            #     post

                data = requests.post(link,data).json()
                if not data["success"]:
                    if data["code"]==102:
                        self.submitting.clear_widgets()
                        self.submitting.add_widget(Label(text="ALREADY VOTED!!!", color=(1,0,0,1),font_size="60px"))
                        Clock.schedule_once(self.login, 3)
                    else:
                        self.submitting.clear_widgets()
                        self.submitting.add_widget(Label(text="SOMETHING WENT WRONG!!!\n PLEASE CALL SUPERVISOR", color=(1, 0, 0, 1), font_size="60px"))
                        Clock.schedule_once(self.login, 3)
                else:
                    self.submitting.clear_widgets()
                    self.submitting.add_widget(Label(text="SUCCESS!!!", color=(0, 1, 0, 1), font_size="60px"))
                    Clock.schedule_once(self.login,3)



            except FileNotFoundError:
                app = App.get_running_app()

                self.parent.parent.parent.parent.parent.parent.current="login"
            except:
                self.submitting.clear_widgets()
                self.submitting.add_widget(Label(text="NETWORK ERROR!!!", color=(0, 1, 0, 1), font_size="60px"))
                Clock.schedule_once(self.login, 3)
        #         add banner failer
    def login(self,dt):
        self.parent.parent.parent.parent.parent.parent.current = "login"
    pass
class LoginButton(Image,ButtonBehavior):
    widget=""
    pressed=False
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    def on_touch_down(self, touch):
#         attempt login
        if self.collide_point(*touch.pos):
            self.widget = Loading_gif(id="loading")
            if not self.pressed:
                self.show_animation()
                self.pressed=True
                threading.Thread(target=self.login_attempt).start()



    def login_attempt(self):
        # TODO://

        password = self.parent.parent.parent.ids.password.text
        student_id = self.parent.parent.parent.ids.student_id.text
        # fix auth


        if student_id !="" or password !="":

            try:
                validation = portalAccess.auth(base_url=login,target_url=studentPortal,username=student_id,password=password)

                if validation[0] == "success":
            #         go to next page
                    with open("./id.oo","w")as w:
                        w.write(student_id)

                    self.remove_anim()
                    self.pressed=False
                    self.parent.parent.parent.ids.err.clear_widgets()
                    self.parent.parent.parent.parent.current="main"
                    self.parent.parent.parent.ids.student_id.text
                    self.parent.parent.parent.ids.password.text=""
                else:
                    self.parent.parent.parent.ids.err.clear_widgets()
                    self.parent.parent.parent.ids.err.add_widget(Label(text="Error with credentials", color=(1, 0, 0, 1)))

                    self.remove_anim()
                    self.pressed=False
            except:
                # show eror
                self.remove_anim()
                self.pressed=False

                self.parent.parent.parent.ids.err.clear_widgets()
                self.parent.parent.parent.ids.err.add_widget(Label(text="Network Error",color=(1,0,0,1)))

    def remove_anim(self):
        try:

            self.widget.parent.remove_widget(self.widget.parent.children[0])
        except:

            pass
    @mainthread
    def show_animation(self):
        print("showing")

        self.parent.parent.parent.add_widget(self.widget)

#         handle animations

class CandidateImage(Image,HoverBehavior):

    path = ObjectProperty(None)
    party = ObjectProperty(None)
    cand_id = ObjectProperty(None)


    print(path.name)
    def __init__(self,**kwargs):

        super().__init__(**kwargs)
        Clock.schedule_once(self.set_name,0)


    def set_name(self,dt):
        self.parent.parent.parent.parent.children[2].children[0].text=position_names[self.parent.parent.parent.parent.parent.page-1]


        name = candidate_names[self.party]["{:02d}".format(self.parent.parent.parent.parent.parent.page)]
        path = "./dependencies/images/"+self.party+"_"+"{:02d}".format(self.parent.parent.parent.parent.parent.page)+".jpg"
        labels = self.parent.parent.parent.parent.parent.names
        images= self.parent.parent.parent.parent.parent.images
        print(self.parent.parent.parent.parent.parent.children[0].children[0].children)

        labels[self.party]=self.parent.children[0]
        images[self.party]=self.parent.children[1]

        images[self.party].path = path
        labels[self.party].text = name



    def change_name(self,dt):
        labels = self.parent.parent.parent.parent.parent.names
        labels['ur'].text=candidate_names['ur']["{:02d}".format(self.parent.parent.parent.parent.parent.page)]
        labels['ud'].text = candidate_names['ud']["{:02d}".format(self.parent.parent.parent.parent.parent.page)]
        images = self.parent.parent.parent.parent.parent.images
        images['ur'].path="./dependencies/images/ur_"+"{:02d}".format(self.parent.parent.parent.parent.parent.page)+".jpg"
        images['ud'].path = "./dependencies/images/ud_" + "{:02d}".format(self.parent.parent.parent.parent.parent.page) + ".jpg"
        self.parent.parent.parent.parent.children[2].children[0].text = position_names[
            self.parent.parent.parent.parent.parent.page - 1]


    def call(self,dt):
        print(self.parent.children[0],self.cand_id)
    def on_enter(self):
        anim = Animation(size=(290,420),duration=.5)
        anim.start(self)

        pass

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
    #         change source
            if self.parent.parent.parent.parent.parent.page<self.parent.parent.parent.parent.parent.pages:

                # app = App.get_running_app()
                root = self.parent.parent.parent.parent.parent
                selection_schema=root.selection_schema
                keys = root.keys
                selection_schema[keys[root.page-1]]=str(self.cand_id).split("_",-1)[0]+"_"+"{:02d}".format(root.page)
                root.page = root.page + 1
                Clock.schedule_once(self.change_name,0)
                print(selection_schema)
                self.parent.parent.parent.parent.parent.update_selections()

            elif self.parent.parent.parent.parent.parent.page==self.parent.parent.parent.parent.parent.pages:
                root = self.parent.parent.parent.parent.parent
                selection_schema = root.selection_schema
                keys = root.keys
                selection_schema[keys[root.page - 1]] = str(self.cand_id).split("_", -1)[0] + "_" + "{:02d}".format(root.page)
                print(selection_schema)

                self.parent.parent.parent.parent.parent.update_selections()

                self.parent.parent.parent.parent.parent.add_button()

                root.page = root.page + 1
    # if on last page



    def on_leave(self):
        anim = Animation(size=(300,430),duration=.1)
        anim.start(self)
    pass

class ErrBady(BoxLayout):
    pass
class MainScreen(Screen,FloatLayout):
    pages = 10
    page = 1
    selection_schema = {'voter_id':"",'candidate_president':"",'candidate_v_president':"",'candidate_pub_sec':"",'candidate_treasurer':"",'candidate_sports':"",'candidate_ent':"",'candidate_trans_acc':"",'candidate_sec_gen':"",'candidate_v_treasurer':"",'candidate_academic_sec':""}
    keys=['candidate_president','candidate_v_president','candidate_pub_sec','candidate_treasurer','candidate_sports','candidate_ent','candidate_trans_acc','candidate_sec_gen','candidate_v_treasurer','candidate_academic_sec']
    names={"ur":"","ud":""}
    images = {"ur":"","ud":""}

    def on_enter(self, *args):
        self.add_widget(ErrBady())
    def on_leave(self, *args):
        self.pages = 10
        self.page = 1
        self.selection_schema = {'voter_id': "", 'candidate_president': "", 'candidate_v_president': "",
                            'candidate_pub_sec': "", 'candidate_treasurer': "", 'candidate_sports': "",
                            'candidate_ent': "", 'candidate_trans_acc': "", 'candidate_sec_gen': "",
                            'candidate_v_treasurer': "", 'candidate_academic_sec': ""}
        self.keys = ['candidate_president', 'candidate_v_president', 'candidate_pub_sec', 'candidate_treasurer',
                'candidate_sports', 'candidate_ent', 'candidate_trans_acc', 'candidate_sec_gen',
                'candidate_v_treasurer', 'candidate_academic_sec']
        self.names = {"ur": "", "ud": ""}
        self.images = {"ur": "", "ud": ""}
        self.clear_widgets()
    def update_selections(self):
        widget=self.children[0].children[0]
        widget = widget.parent.children[1].children[0].children[0]
        widget.clear_widgets()
        for key in range(self.keys.__len__()):
            try:
                cand_id = self.selection_schema[self.keys[key]].split("_",-1)
                party =cand_id[0]
                number = cand_id[1]

                widget.add_widget(Label(text=position_names[key]+": \n"+candidate_names[party][number],halign="center",size_hint_x=None,width=widget.width))
            except:
                pass

    def add_button(self):
        widget = self.children[0].children[0]
        widget = widget.parent.children[1].children[0].children[0]

        widget.add_widget(Submit(source="./dependencies/button.png"))



    pass

class EVS(App):
    def build(self):
        return Home();

if __name__=="__main__":
    EVS().run()