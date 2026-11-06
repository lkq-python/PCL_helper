import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from tkinter import messagebox
import subprocess
import threading
import os

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
        name_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        Version_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.what_name_text=toga.Label(
            "下载版本名称：",
            margin=(0, 5),
        )
        self.what_name_input= toga.TextInput(flex=1)
        mumber_text = toga.Label(
    "版本号：",
    margin=(0, 5),
)
        add_text = toga.Label(
                    "mod加载器：",
                    margin=(0, 5),
                )
        self.mumber_input= toga.TextInput(flex=1)
        self.forge__ = toga.Switch("forge", on_change=forge)
        self.neoforge__ = toga.Switch("neoforge", on_change=NeoForge)
        self.fabric__ = toga.Switch("fabric", on_change=Fabric)
        self.where_text = toga.Label(
            "下载位置：",
            margin=(0, 5),
        )
        self.where_input= toga.TextInput(flex=1)
        button = toga.Button(
    "下载",
    margin=5,on_press=self.download
)
        self.download_time = toga.Label(
                    "下载进度：",
                    margin=(0, 5),
                )
        self.progress_bar = toga.ProgressBar(max=100, value=0)
        name_box.add(self.what_name_text)
        name_box.add(self.what_name_input)

        Version_box.add(mumber_text)
        Version_box.add(self.mumber_input)
        Version_box.add(add_text)
        Version_box.add(self.forge__)
        Version_box.add(self.neoforge__)
        Version_box.add(self.fabric__)
        Version_box.add(self.where_text)
        Version_box.add(self.where_input)
        Version_box.add(self.download_time)
        Version_box.add(self.progress_bar)
        Version_box.add(button)

        main_box.add(name_box)
        main_box.add(Version_box)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
    def create_and_run_bat(self):
        exe_path = str(self.paths.app / "resources" / "portablemc.exe")
        if not os.path.exists(exe_path):
            exe_path = r"D:\mcuse\portablemc.exe"
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
{exe_path} start --dry --main-dir "{self.where_text_print}" -u lkq forge:{self.mumber_text_print} --output machine
"""
        elif Fabric_download==True:
            bat_content = f"""@echo off
{exe_path} start --dry --main-dir "{self.where_text_print}" -u lkq fabric:{self.mumber_text_print} --output machine
"""
        elif NeoForge_download==True:
            bat_content = f"""@echo off
{exe_path} start --dry --main-dir "{self.where_text_print}" -u lkq neoforge:{self.mumber_text_print} --output machine
"""
        else:
            bat_content = f"""@echo off
{exe_path} start --dry --main-dir "{self.where_text_print}" -u lkq {self.mumber_text_print} --output machine
"""
        def run_bat():
            try:
                with open(bat_path, "w", encoding="utf-8") as f:
                    f.write(bat_content)
                
                # 1. 启动进程
                process = subprocess.Popen(
                    ["cmd", "/c", bat_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    creationflags=0x08000000
                )

                # 2. 一边读输出，一边判断进程是否存活
                while True:
                    line = process.stdout.readline()
                    if not line:
                        if process.poll() is not None:
                            break # 进程结束了，管道也空了，安全退出循环
                        else:
                            continue
                    
                    # 解析进度
                    if line.startswith("download\t"):
                        parts = line.strip().split('\t')
                        if len(parts) >= 3:
                            try:
                                size_info = parts[2].split('/')
                                downloaded = int(size_info[0])
                                total = int(size_info[1])
                                if total > 0:
                                    percent = (downloaded / total) * 100
                                    self.loop.call_soon_threadsafe(self._update_ui, percent)
                            except ValueError:
                                pass
                
                # 3. 进程彻底结束
                stop = process.wait()

                # 4. 改名和提示
                if stop == 0:
                    self.progress_bar.value = 0
                    new_name = self.what_name_input.value.strip()
                    if new_name:
                        versions_dir = os.path.join(self.where_text_print, "versions")
                        if os.path.exists(versions_dir):
                            folders = [f for f in os.listdir(versions_dir) if os.path.isdir(os.path.join(versions_dir, f))]
                            if folders:
                                folders.sort(key=lambda x: os.path.getmtime(os.path.join(versions_dir, x)), reverse=True)
                                old_path = os.path.join(versions_dir, folders[0])
                                new_path = os.path.join(versions_dir, new_name)
                                if not os.path.exists(new_path):
                                    os.rename(old_path, new_path)
                                    self.loop.call_soon_threadsafe(self._update_ui, 100) # 拉满进度条
                                else:
                                    self.loop.call_soon_threadsafe(self._update_ui, 100)
                    else:
                        self.loop.call_soon_threadsafe(self._update_ui, 100)
                else:
                    self.loop.call_soon_threadsafe(self._update_ui, 100)

            except Exception as e:
                print(f"发生错误: {e}")

        threading.Thread(target=run_bat, daemon=True).start()
    def _update_ui(self, percent):
        """在主线程安全地更新界面"""
        if percent > 100: 
            percent = 100
        self.progress_bar.value = percent
        self.download_time.text = f"下载进度: {percent:.1f}%"
        def update_text(self, msg):
            """专门用来在主线程安全地更新界面文字"""
            self.download_time.text = msg
    def download(self, widget):
        self.create_and_run_bat()

def main():
    return HelloWorld()



