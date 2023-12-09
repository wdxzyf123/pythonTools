import tkinter as tk
from pdfCompress import PDFCompressorApp
from pdf2image import PDFConverterApp
# main_window.py


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("主窗口")

        # 设置主窗口的初始大小
        self.root.geometry("300x150")

        # 按钮上下排列在左侧
        btn_compressor = tk.Button(self.root, text="PDF压缩", command=self.open_pdf_compressor)
        btn_compressor.pack(pady=10, anchor="center")

        btn_converter = tk.Button(self.root, text="PDF转图片", command=self.open_pdf_converter)
        btn_converter.pack(pady=10, anchor="center")

    def open_pdf_compressor(self):
        self.hide_main_window()
        compressor_root = tk.Toplevel(self.root)
        compressor_app = PDFCompressorApp(compressor_root, self)
        compressor_root.protocol("WM_DELETE_WINDOW", compressor_app.on_closing)
        compressor_app.show()

    def open_pdf_converter(self):
        self.hide_main_window()
        converter_root = tk.Toplevel(self.root)
        converter_app = PDFConverterApp(converter_root, self)
        converter_root.protocol("WM_DELETE_WINDOW", converter_app.on_closing)
        converter_app.show()

    def hide_main_window(self):
        self.root.withdraw()

    def show_main_window(self):
        self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    main_window = MainWindow(root)
    root.mainloop()
