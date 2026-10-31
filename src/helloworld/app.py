import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

mumber_text_print=""
where_text_print=""
forge_download=False
NeoForge_download=False
Fabric_download=False
def forge(widget):
    global forge_download
    if widget.value:
        forge_download=True
    else:
        forge_download=False
def NeoForge(widget):
    global NeoForge_download
    if widget.value:
        NeoForge_download=True
    else:
        NeoForge_download=False
def Fabric(widget):
    global Fabric_download
    if widget.value:
        Fabric_download=True
    else:
        Fabric_download=False
class HelloWorld(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        mumber_text = toga.Label(
    "版本号：",
    margin=(0, 5),
)
        self.mumber_input= toga.TextInput(flex=1)
        self.forge__ = toga.Switch("forge", on_change=forge)
        self.neoforge__ = toga.Switch("neoforge", on_change=NeoForge)
        self.fabric__ = toga.Switch("fabric", on_change=Fabric)
        where_text = toga.Label(
            "下载位置：",
            margin=(0, 5),
        )
        self.where_input= toga.TextInput(flex=1)
        button = toga.Button(
    "下载",
    margin=5,on_press=self.download
)
        main_box.add(mumber_text)
        main_box.add(self.mumber_input)
        main_box.add(self.forge__)
        main_box.add(self.neoforge__)
        main_box.add(self.fabric__)
        main_box.add(where_text)
        main_box.add(self.where_input)
        main_box.add(button)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
    def create_and_run_bat(self):
        exe_path = str(self.paths.app / "resources" / "portablemc.exe")
        self.mumber_text_print= self.mumber_input.value
        self.where_text_print= self.where_input.value
        doc_dir = self.paths.documents 
        bat_path = str(doc_dir / "run_portablemc.bat")
        if ((Fabric_download==True and forge_download==True and NeoForge_download==True)
            or(forge_download==True and NeoForge_download==True)
            or (Fabric_download==True and NeoForge_download==True)
            or (Fabric_download==True and forge_download==True)):
            messagebox.showinfo(title="错误！", message="你不能同时添加两个加载器！")
            return
        elif forge_download==True:
            bat_content = f"""@echo off
{exe_path} start --dry --main-dir "{self.where_text_print}" -u lkq forge:{self.mumber_text_print}
"""
        elif Fabric_download==True:
            bat_content = f"""@echo off
{exe_path} start --dry --main-dir "{self.where_text_print}" -u lkq fabric:{self.mumber_text_print}
"""
        elif NeoForge_download==True:
            bat_content = f"""@echo off
{exe_path} start --dry --main-dir "{self.where_text_print}" -u lkq neoforge:{self.mumber_text_print}
"""
        else:
            bat_content = f"""@echo off
{exe_path} start --dry --main-dir "{self.where_text_print}" -u lkq {self.mumber_text_print}
"""
        def run_bat():
            try:
                with open(bat_path, "w", encoding="utf-8") as f:
                    f.write(bat_content)
                stop=subprocess.call(
                   ["cmd", "/c", bat_path],
                   creationflags=0x08000000
               )
                if stop == 0:
                    messagebox.showinfo("提示", "下载成功！")
                else:
                    messagebox.showerror("错误", "下载失败！")

            except Exception as e:
                messagebox.showinfo(title="错误！", message="无法加载bat文件！")
        threading.Thread(target=run_bat, daemon=True).start()
    def download(self, widget):
        self.create_and_run_bat()

def main():
    return HelloWorld()



