import os
import shutil

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class ImageResizeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resize")
        self.root.geometry("1280x650")  # 设置窗口初始大小

        # 初始化图像大小调整参数
        self.width_var = tk.IntVar()
        self.height_var = tk.IntVar()

        # 初始化图像保存参数
        self.quality_var = tk.IntVar()
        self.quality_var.set(50)
        self.format_var = tk.StringVar()
        self.format_var.set("jpg")

        # 临时文件路径
        self.temp_output_path = None

        # 图像路径
        self.image_path = None

        # 创建界面元素
        self.create_widgets()

        self.display_size = 400

    def create_widgets(self):
        # 创建文件选择按钮
        self.select_button = tk.Button(self.root, text="选择图片", command=self.load_image)
        self.select_button.pack(pady=10)

        # # 创建预览区域
        # self.preview_frame = tk.Frame(self.root)
        # self.preview_frame.pack(pady=10, expand=True, fill="both")
        # 创建预览区域
        self.preview_frame = tk.Frame(self.root)
        self.preview_frame.pack(pady=10, expand=True)

        # 创建图像大小调整输入框
        self.width_label = tk.Label(self.root, text="宽度:")
        self.width_label.pack(side="left", padx=10)
        self.width_entry = tk.Entry(self.root, textvariable=self.width_var)
        self.width_entry.pack(side="left")

        self.height_label = tk.Label(self.root, text="高度:")
        self.height_label.pack(side="left", padx=10)
        self.height_entry = tk.Entry(self.root, textvariable=self.height_var)
        self.height_entry.pack(side="left")

        # 创建图像保存参数输入框
        self.quality_label = tk.Label(self.root, text="保存质量(1-100):")
        self.quality_label.pack(side="left", padx=10)
        self.quality_entry = tk.Entry(self.root, textvariable=self.quality_var)
        self.quality_entry.pack(side="left")

        # 创建图像保存格式下拉菜单
        self.format_label = tk.Label(self.root, text="保存格式:")
        self.format_label.pack(side="left", padx=10)
        self.format_combobox = ttk.Combobox(self.root, textvariable=self.format_var, values=["png", "jpg"])
        self.format_combobox.pack(side="left")
        self.format_combobox.set("jpg")

        # 创建应用按钮
        self.apply_button = tk.Button(self.root, text="预览", command=self.apply_changes)
        self.apply_button.pack(side="left", pady=10)

        # 创建保存按钮
        self.save_button = tk.Button(self.root, text="保存图片", command=self.save_image)
        self.save_button.pack(side="left", pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.display_input_image()

    def display_input_image(self):
        image = Image.open(self.image_path)
        width, height = image.size
        self.width_var.set(width)
        self.height_var.set(height)
        # self.display_resolution(image)
        width, height = image.size
        resolution_text = f"分辨率: {width} x {height}"

        file_size_text = f"文件大小: {self.get_formatted_file_size(self.image_path)}"

        info_label2 = tk.Label(self.preview_frame, text=f"{resolution_text}\n{file_size_text}")
        info_label2.grid(row=1, column=0, pady=5)

        temp = min(width, height)
        if temp > self.display_size:
            temp = self.display_size

        resized_image = self.resize_image_object(image, (temp, temp))
        photo = ImageTk.PhotoImage(resized_image)

        if hasattr(self, "input_image_label"):
            self.input_image_label.configure(image=photo)
            self.input_image_label.image = photo
        else:
            self.input_image_label = tk.Label(self.preview_frame, text="原始图像", image=photo)
            self.input_image_label.grid(row=0, column=0, padx=10)
            self.input_image_label.image = photo

    def get_formatted_file_size(self, file_path):
        file_size = os.path.getsize(file_path)
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        while file_size >= 1024 and unit_index < len(units) - 1:
            file_size /= 1024
            unit_index += 1
        return f"{file_size:.2f} {units[unit_index]}"

    def get_file_size(self, file_path):
        return os.path.getsize(file_path) // 1024  # 文件大小以KB为单位

    # 在 ImageResizeApp 类中的 display_resized_image 方法中添加新的 Label 来显示分辨率和文件大小
    # 在 display_resized_image 方法中，确保 temp_output_path 不为 None
    def display_resized_image(self, resized_image):
        # self.display_resolution(resized_image)
        width, height = resized_image.size
        temp = min(width, height)

        if temp > self.display_size:
            temp = self.display_size
        resized_image = self.resize_image_object(resized_image, (temp, temp))
        photo = ImageTk.PhotoImage(resized_image)

        if hasattr(self, "resized_image_label"):
            self.resized_image_label.configure(image=photo)
            self.resized_image_label.image = photo
        else:
            self.resized_image_label = tk.Label(self.preview_frame, text="调整大小后的图像", image=photo)
            self.resized_image_label.grid(row=0, column=1, padx=10)
            self.resized_image_label.image = photo





    def resize_image_object(self, image, size):
        return image.resize(size, Image.ANTIALIAS)

    # 在 ImageResizeApp 类中的 apply_changes 方法中获取调整后的图像的分辨率和文件大小
    def apply_changes(self):
        if hasattr(self, "image_path") and self.image_path is not None:
            original_image = Image.open(self.image_path)
            new_width = self.width_var.get()
            new_height = self.height_var.get()
            resized_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)

            # # 显示调整后的图像
            # self.display_resized_image(resized_image)

            # 保存调整后的图像到临时文件
            temp_output_dir = "temp_output"
            os.makedirs(temp_output_dir, exist_ok=True)
            file_extension = self.format_var.get()  # 获取选择的文件格式
            self.temp_output_path = os.path.join(temp_output_dir, f"temp_output_image.{file_extension}")
            # 保存调整后的图像到临时文件
            resized_image = resized_image.convert('RGB')  # 转换为RGB模式`
            resized_image.save(self.temp_output_path, quality=self.quality_var.get())
            # 显示调整后的图像
            resized_image = Image.open(self.temp_output_path)
            self.display_resized_image(resized_image)

            # 获取调整后的图像的分辨率和文件大小
            resized_resolution = f"分辨率: {resized_image.width} x {resized_image.height}"
            resized_file_size = f"文件大小: {self.get_formatted_file_size(self.temp_output_path)}"
            # 更新显示分辨率和文件大小的 Label 打开这里
            info_label = tk.Label(self.preview_frame, text=f"{resized_resolution}\n{resized_file_size}")
            info_label.grid(row=1, column=1, pady=5)

    def save_image(self):
        if self.temp_output_path:
            output_image_path = filedialog.asksaveasfilename(
                defaultextension=f".{self.format_var.get()}",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")],
                initialfile=self.generate_output_filename()
            )
            if output_image_path:
                # os.rename(self.temp_output_path, output_image_path)
                shutil.copy(self.temp_output_path, output_image_path)
                messagebox.showinfo("保存成功", "调整大小后的图像已保存成功！")

    def generate_output_filename(self):
        base_name = os.path.basename(self.image_path)
        filename, extension = os.path.splitext(base_name)
        resolution_suffix = f"_{self.width_var.get()}x{self.height_var.get()}"
        quality_suffix = f"_q{self.quality_var.get()}"
        format_suffix = f".{self.format_var.get()}"
        output_filename = f"{filename}{resolution_suffix}{quality_suffix}{format_suffix}"
        return output_filename


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizeApp(root)
    root.mainloop()
