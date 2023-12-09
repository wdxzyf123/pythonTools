# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

class ImageBrightnessAdjustmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Brightness Adjustment")
        self.root.geometry("880x600")  # 设置窗口初始大小

        # 初始化亮度调整参数
        self.brightness_factor = tk.DoubleVar()
        self.brightness_factor.set(1.0)

        # 创建界面元素
        self.create_widgets()

    def create_widgets(self):
        # 创建文件选择按钮
        self.select_button = tk.Button(self.root, text="选择图片", command=self.load_image)
        self.select_button.pack(pady=10)

        # 创建预览区域
        self.preview_frame = tk.Frame(self.root)
        self.preview_frame.pack(pady=10, expand=True, fill="both")

        # 创建亮度调整滑块
        self.brightness_label = tk.Label(self.root, text="亮度调整:")
        self.brightness_label.pack(side="left", padx=10)
        self.brightness_slider = tk.Scale(
            self.root, from_=0.1, to=2.0, resolution=0.1, orient="vertical", variable=self.brightness_factor
        )
        self.brightness_slider.pack(side="left")

        # 创建应用按钮
        self.apply_button = tk.Button(self.root, text="预览", command=self.adjust_brightness)
        self.apply_button.pack(side="left", padx=10)

        # 创建保存按钮
        self.save_button = tk.Button(self.root, text="保存输出图片", command=self.save_image)
        self.save_button.pack(side="left", pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.display_input_image()

    def display_input_image(self):
        image = Image.open(self.image_path)
        resized_image = self.resize_image(image, (400, 400))
        photo = ImageTk.PhotoImage(resized_image)

        if hasattr(self, "input_image_label"):
            self.input_image_label.configure(image=photo)
            self.input_image_label.image = photo
        else:
            self.input_image_label = tk.Label(self.preview_frame, text="输入图像", image=photo)
            self.input_image_label.grid(row=0, column=0, padx=10)
            self.input_image_label.image = photo

    def display_output_image(self, output_image):
        resized_image = self.resize_image(output_image, (400, 400))
        photo = ImageTk.PhotoImage(resized_image)

        if hasattr(self, "output_image_label"):
            self.output_image_label.configure(image=photo)
            self.output_image_label.image = photo
        else:
            self.output_image_label = tk.Label(self.preview_frame, text="输出图像", image=photo)
            self.output_image_label.grid(row=0, column=1, padx=10)
            self.output_image_label.image = photo

    def resize_image(self, image, size):
        return image.resize(size, Image.ANTIALIAS)

    def adjust_brightness(self):
        if hasattr(self, "image_path"):
            original_image = Image.open(self.image_path)
            adjusted_image = original_image.point(lambda p: p * self.brightness_factor.get())
            self.display_output_image(adjusted_image)

    def save_image(self):
        if hasattr(self, "output_image_label"):
            output_image_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                               filetypes=[("PNG files", "*.png"),
                                                                          ("JPEG files", "*.jpg;*.jpeg")])
            if output_image_path:
                output_image = Image.open(self.image_path).point(lambda p: p * self.brightness_factor.get())
                output_image.save(output_image_path)
                messagebox.showinfo("保存成功", "输出图像已保存成功！")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageBrightnessAdjustmentApp(root)
    root.mainloop()
