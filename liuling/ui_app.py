import logging
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# 添加src目录到Python路径以便导入模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from liuling.adjust_crop_city_data import setup, load_data, process_data_for_all_crops_and_provinces


class TextHandler(logging.Handler):
    """自定义日志处理器，将日志输出到Tkinter Text控件"""

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.yview(tk.END)

        self.text_widget.after(0, append)


class AdjustCropDataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("“省-市-县”三级数据智慧化调整软件")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # 初始化变量
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.num_workers = tk.IntVar(value=2)  # 默认值为2
        self.max_workers = tk.IntVar(value=5)  # 默认值为5
        self.is_running = False

        # 设置界面
        self.setup_ui()

        # 配置日志处理器
        self.setup_logger()

        # 初始化配置
        self.config = None
        self.output_adjusted_file = None

    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # 标题
        # title_label = ttk.Label(main_frame, text="PDF文件高精度表格数据智能识别与导出软件V1.0", font=("Arial", 16, "bold"))
        # title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # 输入文件选择
        input_label = ttk.Label(main_frame, text="输入文件:")
        input_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        input_entry = ttk.Entry(main_frame, textvariable=self.input_file, width=50)
        input_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=5)

        input_button = ttk.Button(main_frame, text="浏览...", command=self.browse_input_file)
        input_button.grid(row=1, column=2, pady=5)

        # 输出目录选择
        output_label = ttk.Label(main_frame, text="输出目录:")
        output_label.grid(row=2, column=0, sticky=tk.W, pady=5)

        output_entry = ttk.Entry(main_frame, textvariable=self.output_dir, width=50)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=5)

        output_button = ttk.Button(main_frame, text="浏览...", command=self.browse_output_dir)
        output_button.grid(row=2, column=2, pady=5)

        # 配置参数
        config_frame = ttk.LabelFrame(main_frame, text="配置参数", padding="10")
        config_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        config_frame.columnconfigure(1, weight=1)
        config_frame.columnconfigure(3, weight=1)

        # num_workers
        num_workers_label = ttk.Label(config_frame, text="转换文档最大线程数:")
        num_workers_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        num_workers_spinbox = ttk.Spinbox(config_frame, from_=1, to=10, textvariable=self.num_workers, width=10)
        num_workers_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 30), pady=5)

        # max_workers
        max_workers_label = ttk.Label(config_frame, text="解析文档最大线程数:")
        max_workers_label.grid(row=0, column=2, sticky=tk.W, pady=5)

        max_workers_spinbox = ttk.Spinbox(config_frame, from_=1, to=20, textvariable=self.max_workers, width=10)
        max_workers_spinbox.grid(row=0, column=3, sticky=tk.W, padx=(10, 0), pady=5)

        # 日志文本框
        log_label = ttk.Label(main_frame, text="运行日志:")
        log_label.grid(row=4, column=0, sticky=(tk.W, tk.N), pady=(10, 5))

        self.log_text = tk.Text(main_frame, height=20, width=120, state='disabled')
        log_scrollbar_y = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar_x = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.log_text.xview)
        self.log_text.configure(yscrollcommand=log_scrollbar_y.set, xscrollcommand=log_scrollbar_x.set)

        self.log_text.grid(row=4, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10), pady=(10, 10))
        log_scrollbar_y.grid(row=4, column=2, sticky=(tk.N, tk.S), pady=(10, 10))
        log_scrollbar_x.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=(0, 10))

        # 控制按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=10)

        self.run_button = ttk.Button(button_frame, text="开始调整", command=self.start)
        self.run_button.pack(side=tk.LEFT, padx=(0, 10))

        self.exit_button = ttk.Button(button_frame, text="退出", command=self.root.quit)
        self.exit_button.pack(side=tk.LEFT)

    def setup_logger(self):
        # 创建文本日志处理器
        text_handler = TextHandler(self.log_text)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                                      datefmt="%Y/%m/%d %H:%M:%S")
        text_handler.setFormatter(formatter)

        # 为相关记录器添加处理器
        for logger_name in ['pdf_extractor', 'data.data_handler', 'client.aiclient', 'tqdm.tqdm']:
            logger = logging.getLogger(logger_name)
            # 清除现有的处理程序以避免重复
            # logger.handlers.clear()
            # 添加文本处理程序
            logger.addHandler(text_handler)
            # 设置日志级别
            logger.setLevel(logging.INFO)
            # 禁止传播到父记录器以避免重复
            logger.propagate = False

        # 为其他可能的日志记录器添加处理器
        root_logger = logging.getLogger()
        root_logger.addHandler(text_handler)
        root_logger.setLevel(logging.INFO)

    def browse_input_file(self):
        # directory = filedialog.askdirectory(title="选择输入目录")
        # if directory:
        #     self.input_dir.set(directory)

        input_file = filedialog.askopenfilename(title="选择输入文件")
        if input_file:
            self.input_file.set(input_file)

    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir.set(directory)

    def start(self):
        if not self.input_file.get() or not self.output_dir.get():
            messagebox.showerror("错误", "请选择输入和输出目录")
            return

        if self.is_running:
            messagebox.showinfo("提示", "数据校正任务已在运行中")
            return

        self.is_running = True
        self.run_button.config(state=tk.DISABLED)

        # # 在单独的线程中运行
        # extraction_thread = threading.Thread(target=self.run_adjust_async, daemon=True)
        # extraction_thread.start()

        self.run_adjust()

    def setup_config(self):
        # 初始化配置
        self.config, input_file, output_log_file, output_adjusted_file = setup()

        # 更新配置参数
        self.config.checker['num_workers'] = self.num_workers.get()
        self.config.checker['max_workers'] = self.max_workers.get()
        self.config.checker['input_file'] = self.input_file.get()
        self.config.checker['output_adjusted_file'] = self.output_dir.get() + "/产量数据地区数据调整结果.xlsx"

    def run_adjust(self):
        try:
            self.setup_config()

            # 在 asyncio 事件循环中运行异步任务
            # asyncio.run(self.async_extraction())

            logging.info("开始进行数据调整...")

            df_2022, df_2017, df_national_ref, df_province_ref = load_data(self.config)
            output_file = process_data_for_all_crops_and_provinces(self.config, df_2022, df_2017, df_national_ref,
                                                                   df_province_ref)
        except Exception as e:
            logging.error(f"发生错误: {str(e)}")
        finally:
            self.is_running = False
            self.root.after(0, lambda: self.run_button.config(state=tk.NORMAL))
            logging.info("数据调整完成!")

    def async_extraction(self):
        try:
            logging.info("开始进行数据调整...")

            df_2022, df_2017, df_national_ref, df_province_ref = load_data(self.config)
            output_file = process_data_for_all_crops_and_provinces(self.config, df_2022, df_2017, df_national_ref, df_province_ref)
        except Exception as e:
            logging.error(f"数据调整过程中发生错误: {str(e)}")


def main():
    root = tk.Tk()
    app = AdjustCropDataGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
