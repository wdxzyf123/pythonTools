import fitz, os  # PyMuPDF
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox


class PDFConverterApp:
    def __init__(self, root, main_window):
        self.root = root
        self.root.geometry("1300x600")  # 调整窗口大小
        self.root.title("PDF转图片工具")
        self.main_window = main_window

        self.pdf_path = ""
        self.image_folder = ""
        self.merge_images_var = tk.BooleanVar()
        self.merge_images_var.set(True)  # 默认合并图片
        self.resolution_var = tk.StringVar()
        self.quality_var = tk.StringVar()
        self.format_var = tk.StringVar()
        self.format_var.set("PNG")  # 默认保存为PNG

        # 创建界面元素
        self.label1 = tk.Label(root, text="PDF文件:")
        self.label1.pack(pady=5)

        # self.pdf_entry = tk.Entry(root, width=40)
        # self.pdf_entry.pack(pady=5)

        # self.browse_button = tk.Button(root, text="浏览", command=self.browse_pdf)
        # self.browse_button.pack(pady=5)

        browse_pdf_entry_frame = tk.Frame(root)
        browse_pdf_entry_frame.pack(pady=5)

        # 将浏览按钮移到输入路径文本框的左侧
        self.browse_button = tk.Button(browse_pdf_entry_frame, text="浏览", command=self.browse_pdf)
        self.browse_button.pack(side=tk.LEFT, padx=5, anchor="n")
        self.pdf_entry = tk.Entry(browse_pdf_entry_frame, width=100)
        self.pdf_entry.pack(side=tk.LEFT,  pady=5, anchor="n")

        output_pdf_entry_frame = tk.Frame(root)
        output_pdf_entry_frame.pack(pady=5)

        # 将选择输出路径按钮移到输出路径文本框左侧
        self.browse_output_button = tk.Button(output_pdf_entry_frame, text="输出", command=self.browse_output_folder)
        self.browse_output_button.pack(side=tk.LEFT, padx=5, anchor="n")

        self.output_folder_entry = tk.Entry(output_pdf_entry_frame, width=100)
        self.output_folder_entry.pack(side=tk.LEFT, pady=5, anchor="n")



        resolution_quality_frame = tk.Frame(root)
        resolution_quality_frame.pack(padx=170, pady=5, anchor="nw")

        self.label2 = tk.Label(resolution_quality_frame, text="分辨率 (DPI):")
        self.label2.pack(side=tk.LEFT, padx=5)

        self.resolution_entry = tk.Entry(resolution_quality_frame, textvariable=self.resolution_var)
        self.resolution_entry.insert(0, "300")  # 默认分辨率
        self.resolution_entry.pack(side=tk.LEFT, padx=5)

        self.label3 = tk.Label(resolution_quality_frame, text="保存质量 (0-100):")
        self.label3.pack(side=tk.LEFT, padx=5)

        self.quality_entry = tk.Entry(resolution_quality_frame, textvariable=self.quality_var)
        self.quality_entry.insert(0, "95")  # 默认质量
        self.quality_entry.pack(side=tk.LEFT, padx=5)

        format_frame = tk.Frame(root)
        format_frame.pack(padx=170,pady=5, anchor="nw")

        self.label4 = tk.Label(format_frame, text="保存格式:")
        self.label4.pack(side=tk.LEFT, padx=5)

        self.png_radiobutton = tk.Radiobutton(format_frame, text="PNG", variable=self.format_var, value="PNG")
        self.png_radiobutton.pack(side=tk.LEFT, padx=5)

        self.jpeg_radiobutton = tk.Radiobutton(format_frame, text="JPEG", variable=self.format_var, value="JPEG")
        self.jpeg_radiobutton.pack(side=tk.LEFT, padx=5)

        self.merge_checkbutton = tk.Checkbutton(root, text="合并所有图片到一个文件", variable=self.merge_images_var)
        self.merge_checkbutton.pack(pady=5,padx=170, anchor="nw")

        # self.browse_output_button = tk.Button(root, text="选择输出路径", command=self.browse_output_folder)
        # self.browse_output_button.pack(pady=5)
        #
        # self.output_folder_entry = tk.Entry(root, width=40)
        # self.output_folder_entry.pack(pady=5)



        self.convert_button = tk.Button(root, text="转换", command=self.convert_pdf)
        self.convert_button.pack(pady=20)

    def on_closing(self):
        # 在关闭事件中调用主窗口的方法
        self.main_window.show_main_window()
        self.root.destroy()
    def show(self):
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()
    def browse_output_folder(self):
        self.image_folder = filedialog.askdirectory()
        self.output_folder_entry.delete(0, tk.END)
        self.output_folder_entry.insert(0, self.image_folder)
    def browse_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF文件", "*.pdf")])
        if not self.pdf_path.lower().endswith('.pdf'):
            messagebox.showerror("错误", "请选择一个PDF文件！")
            return
        self.pdf_entry.delete(0, tk.END)
        self.pdf_entry.insert(0, self.pdf_path)

    def convert_pdf(self):
        if not self.pdf_path:
            messagebox.showerror("错误", "请选择一个PDF文件！")
            return

        if not (0 <= int(self.quality_var.get()) <= 100):
            messagebox.showerror("错误", "保存质量必须在0到100之间！")
            return

        self.image_folder = self.output_folder_entry.get()
        resolution = int(self.resolution_var.get())
        quality = int(self.quality_var.get())
        merge_images = self.merge_images_var.get()
        output_format = self.format_var.get()

        # 获取源文件名（不包含路径和扩展名）
        source_filename = os.path.splitext(os.path.basename(self.pdf_path))[0]

        pdf_to_images(self.pdf_path, self.image_folder, resolution=resolution, quality=quality,
                      merge_images=merge_images, format=output_format, source_filename=source_filename)

        if merge_images:
            messagebox.showinfo("转换完成",
                                f"PDF转图片成功！\n保存位置：{self.image_folder}/合并图片_{source_filename}.{output_format.lower()}")
        else:
            messagebox.showinfo("转换完成", f"PDF转图片成功！\n图片保存在：{self.image_folder}")


def pdf_to_images(pdf_path, image_folder, resolution=300, quality=95, merge_images=True, format="PNG", source_filename=""):
    pdf_document = fitz.open(pdf_path)

    # 如果用户选择合并图片，则创建一个空白图片用于存放所有页面
    if merge_images:
        combined_image = Image.new("RGB", (1, 1), (255, 255, 255))

    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        pixmap = page.get_pixmap(matrix=fitz.Matrix(resolution / 72.0, resolution / 72.0), alpha=False)

        # 修改图像文件名，加上源文件名作为前缀
        image_filename = f"{source_filename}_第{page_number + 1}页.{format.lower()}" if source_filename else f"第{page_number + 1}页.{format.lower()}"
        image_path = os.path.join(image_folder, image_filename)

        pil_image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

        if merge_images:
            combined_image = concatenate_images(combined_image, pil_image)
        else:
            pil_image.save(image_path, format, dpi=(resolution, resolution), quality=quality)

    pdf_document.close()

    if merge_images:
        # 修改合并图片的文件名，加上源文件名作为前缀
        merge_filename = f"{source_filename}_合并图片.{format.lower()}" if source_filename else "合并图片.{format.lower()}"
        combined_image.save(os.path.join(image_folder, merge_filename), format, dpi=(resolution, resolution),
                            quality=quality)


def concatenate_images(img1, img2):
    width = max(img1.width, img2.width)
    height = img1.height + img2.height
    new_image = Image.new("RGB", (width, height), (255, 255, 255))
    new_image.paste(img1, (0, 0))
    new_image.paste(img2, (0, img1.height))
    return new_image


if __name__ == "__main__":
    root = tk.Tk()
    main_window = tk.Toplevel(root)
    app = PDFConverterApp(main_window, None)  # 暂时传递 None
    main_window.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()