import tkinter as tk
from tkinter import filedialog, messagebox
import os
import fitz
from PIL import Image


class PDFCompressorApp:
    def __init__(self, root, main_window):
        self.root = root
        self.main_window = main_window  # 引用主窗口实例
        self.root.title("PDF压缩工具")
        self.root.geometry("1300x600")  # 调整窗口大小

        self.file_path = ""
        self.output_path = ""
        self.quality_var = tk.StringVar(value="85")
        tk.Label(self.root, text="原PDF文件：").pack(pady=10)
        self.frame1 = tk.Frame(root)
        self.frame1.pack(padx=170, pady=5, anchor="nw")
        self.file_path_entry = tk.Entry(self.frame1, width=120, state="readonly")  # 调整文本框宽度
        self.frame2 = tk.Frame(root)
        self.frame2.pack(padx=170, pady=5, anchor="nw")

        self.frame3 = tk.Frame(root)
        self.frame3.pack(padx=170, pady=5, anchor="nw")
        self.output_path_entry = tk.Entry(self.frame3, width=120, state="readonly")  # 调整文本框宽度

        self.create_widgets()


    def on_closing(self):
        # 在关闭事件中调用主窗口的方法
        self.main_window.show_main_window()
        self.root.destroy()

    def show(self):
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()



    def create_widgets(self):


        tk.Button(self.frame1, text="浏览", command=self.browse_pdf).pack(side=tk.LEFT, padx=5,pady=5)
        self.file_path_entry.pack(side=tk.LEFT, padx=5,pady=5)

        tk.Label(self.frame2, text="压缩质量（1-100）：").pack(side=tk.LEFT, padx=5,pady=5)
        quality_entry = tk.Entry(self.frame2, textvariable=self.quality_var)
        quality_entry.pack(side=tk.LEFT, padx=5,pady=5)
        quality_entry.bind("<KeyRelease>", self.update_output_filename)  # 使用KeyRelease事件

        tk.Button(self.frame3, text="保存路径", command=self.choose_output_path).pack(side=tk.LEFT, padx=5,pady=5)
        self.output_path_entry.pack(side=tk.LEFT, padx=5,pady=5)

        tk.Button(self.root, text="压缩PDF", command=self.compress_pdf).pack(pady=10)

    def browse_pdf(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF文件", "*.pdf")])
        if self.file_path:
            self.file_path_entry.configure(state="normal")
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, self.file_path)
            self.file_path_entry.configure(state="readonly")

        # Set default output path to source file path + _compressed_quality.pdf
        base_name = os.path.basename(self.file_path)
        file_name, file_ext = os.path.splitext(base_name)
        quality_str = self.quality_var.get()
        self.output_path = os.path.join(
            os.path.dirname(self.file_path),
            f"{file_name}_compressed_{quality_str}.pdf"
        )

        self.output_path_entry.configure(state="normal")
        self.output_path_entry.delete(0, tk.END)
        self.output_path_entry.insert(0, self.output_path)
        self.output_path_entry.configure(state="readonly")

    def choose_output_path(self):
        output_dir = filedialog.askdirectory(title="选择保存目录")
        if output_dir:
            # Update the output path with the selected directory
            base_name = os.path.basename(self.file_path)
            file_name, file_ext = os.path.splitext(base_name)
            quality_str = self.quality_var.get()
            self.output_path = os.path.join(
                output_dir,
                f"{file_name}_compressed_{quality_str}.pdf"
            )
            self.output_path_entry.configure(state="normal")
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, self.output_path)
            self.output_path_entry.configure(state="readonly")

    def update_output_filename(self, event):
        # Update the output filename when quality changes
        base_name = os.path.basename(self.file_path)
        file_name, file_ext = os.path.splitext(base_name)
        quality_str = self.quality_var.get()
        self.output_path = os.path.join(
            os.path.dirname(self.file_path),
            f"{file_name}_compressed_{quality_str}.pdf"
        )
        self.output_path_entry.configure(state="normal")
        self.output_path_entry.delete(0, tk.END)
        self.output_path_entry.insert(0, self.output_path)
        self.output_path_entry.configure(state="readonly")

    def compress_pdf(self):
        if not self.file_path:
            messagebox.showerror("错误", "请选择一个PDF文件。")
            return

        quality_input = self.quality_var.get()
        if not quality_input.isdigit() or not 1 <= int(quality_input) <= 100:
            messagebox.showerror("错误", "请输入有效的压缩质量（1-100之间的整数）。")
            return

        compression_quality = int(quality_input)

        if not self.output_path:
            messagebox.showerror("错误", "请选择保存路径。")
            return

        try:
            self.convert_and_compress_pdf(compression_quality)
            messagebox.showinfo("成功", f"PDF压缩完成。保存路径：{self.output_path}")
        except Exception as e:
            messagebox.showerror("错误", f"压缩PDF时出错：{str(e)}")

    def convert_and_compress_pdf(self, compression_quality):
        pdf_document = fitz.open(self.file_path)

        img_list = []
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            img = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 提高分辨率以获得更好的图像质量
            img_list.append(Image.frombytes("RGB", [img.width, img.height], img.samples))

        img_list = [img.convert("RGB") for img in img_list]

        img_list[0].save(
            self.output_path,
            save_all=True,
            append_images=img_list[1:],
            quality=compression_quality,
        )

    def get_output_filename(self):
        base_name = os.path.basename(self.file_path)
        file_name, file_ext = os.path.splitext(base_name)
        quality_str = self.quality_var.get()
        return f"{file_name}_compressed_{quality_str}.pdf"


if __name__ == "__main__":
    root = tk.Tk()
    main_window = tk.Toplevel(root)
    app = PDFCompressorApp(main_window, None)  # 暂时传递 None
    main_window.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()