import flet as ft
import os
import fnmatch
from ncmdump import dump
from tkinter import Tk
from tkinter.filedialog import askdirectory

class NCMConverterApp:
    def __init__(self):
        # 动态获取当前用户的桌面路径
        self.download_folder = os.path.join(os.environ["USERPROFILE"], "Desktop")
        self.waiting = True
        self.folder_text = None

    def all_files(self, root, patterns='*', single_level=False, yield_folder=False):
        patterns = patterns.split(';')
        for path, subdirs, files in os.walk(root):
            if yield_folder:
                files.extend(subdirs)
            files.sort()
            for fname in files:
                for pt in patterns:
                    if fnmatch.fnmatch(fname, pt):
                        yield os.path.join(path, fname)
                        break
            if single_level:
                break

    def start_conversion(self, page, folder_text):
        page.add(ft.Text("正在转换..."))
        thefile = list(self.all_files(folder_text, '*.ncm'))
        if not thefile:
            page.add(ft.Text("没有找到.ncm文件！"))
            return
        
        for item in thefile:
            dump(item)  # 转换操作
            os.remove(item)  # 删除原始.ncm文件
            page.add(ft.Text(f"{item} 转换成功！"))

        page.add(ft.Text("所有文件已转换完成！"))

    def build(self):
        self.folder_text = ft.TextField(value=self.download_folder, width=400)
        
        # 创建按钮用于调用 tkinter 来选择文件夹
        return ft.Column(
            controls=[
                ft.Text("请输入网易云音乐下载路径(默认桌面):"),
                self.folder_text,
                ft.ElevatedButton("浏览", on_click=self.select_folder),
                ft.ElevatedButton("开始转换", on_click=lambda e: self.start_conversion(e.page, self.folder_text.value)),
            ]
        )

    def select_folder(self, e):
        # 使用 tkinter 打开文件夹选择框
        root = Tk()
        root.withdraw()  # 隐藏主窗口
        folder_selected = askdirectory(title="选择文件夹")
        if folder_selected:
            self.download_folder = folder_selected
            self.folder_text.value = self.download_folder
            e.page.update()


def main(page):
    app = NCMConverterApp()
    page.add(app.build())
    
    # 设置固定窗口大小
    page.window_width = 400
    page.window_height = 225
    
    page.update()


ft.app(target=main)
