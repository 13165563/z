import tkinter as tk
import pyautogui
import pyperclip
from tkinter import messagebox


class MouseCoordinateCapture:
    def __init__(self, root):
        self.root = root
        self.root.title("鼠标坐标捕获器")

        # 创建界面组件
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack()

        self.btn_start = tk.Button(self.frame, text="开始捕获", command=self.start_capture)
        self.btn_start.grid(row=0, column=0, padx=5, pady=5)

        self.btn_copy = tk.Button(self.frame, text="复制坐标", command=self.copy_coordinates)
        self.btn_copy.grid(row=0, column=1, padx=5, pady=5)

        self.live_label = tk.Label(self.frame, text="实时坐标：未启动")
        self.live_label.grid(row=1, column=0, columnspan=2, pady=5)

        self.locked_label = tk.Label(self.frame, text="锁定坐标：未锁定")
        self.locked_label.grid(row=2, column=0, columnspan=2, pady=5)

        # 初始化变量
        self.capturing = False
        self.locked_coords = None
        self.update_job = None

    def start_capture(self):
        if not self.capturing:
            self.capturing = True
            self.btn_start.config(text="捕获中...")
            self.root.bind('<Return>', self.lock_coordinates)
            self.update_coordinates()

    def update_coordinates(self):
        if self.capturing:
            x, y = pyautogui.position()
            self.live_label.config(text=f"实时坐标：X={x}, Y={y}")
            self.update_job = self.root.after(100, self.update_coordinates)

    def lock_coordinates(self, event=None):
        if self.capturing:
            self.capturing = False
            self.btn_start.config(text="开始捕获")
            x, y = pyautogui.position()
            self.locked_coords = (x, y)
            self.locked_label.config(text=f"锁定坐标：X={x}, Y={y}")
            self.root.unbind('<Return>')
            if self.update_job:
                self.root.after_cancel(self.update_job)

    def copy_coordinates(self):
        if self.locked_coords:
            x, y = self.locked_coords
            pyperclip.copy(f"X={x}, Y={y}")
            messagebox.showinfo("复制成功", "坐标已复制到剪贴板")
        else:
            messagebox.showwarning("无坐标", "请先锁定坐标")

    def on_close(self):
        if messagebox.askokcancel("退出", "确定要退出程序吗？"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MouseCoordinateCapture(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()