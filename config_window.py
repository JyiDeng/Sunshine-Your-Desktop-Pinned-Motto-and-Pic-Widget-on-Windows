import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
import json

class ConfigWindow:
    """
    本文件用于配置窗口，只能在运行 Sunshine.py 时调用
    """
    def __init__(self, parent=None, callback=None):
        # 添加翻译字典
        self.translations = {
            'zh_CN': {
                'window_title': '小太阳 Sunshine 配置',
                'theme_section': '主题选择 (实时预览)',
                'image_section': '图片设置',
                'browse_btn': '浏览',
                'window_size_section': '窗口大小',
                'width_label': '宽度 (建议>=250):',
                'height_label': '高度 (建议>=310):',
                'refresh_section': '文字刷新间隔 (最小支持1秒，否则无法保存)',
                'interval_label': '间隔(秒):',
                'font_section': '字体大小 (最小为5)',
                'size_label': '大小:',
                'language_section': '语言设置 Language Settings',
                'language_label': '语言 Language:',
                'save_btn': '保存 Save',
                'cancel_btn': '取消 Cancel',
                'image_file_type': '图片文件类型',
                'all_files': '所有文件',
                
            },
            'en_US': {
                'window_title': '小太阳 Sunshine Settings',
                'theme_section': 'Theme Selection (Live Preview)',
                'image_section': 'Image Settings',
                'browse_btn': 'Browse',
                'window_size_section': 'Window Size',
                'width_label': 'Width (Suggested: w>=310):',
                'height_label': 'Height (Suggested: h>=310):',
                'refresh_section': 'Text Refresh Interval (Minimum 1 second)',
                'interval_label': 'Interval(s):',
                'font_section': 'Font Size (Minimum 5)',
                'size_label': 'Size:',
                'language_section': '语言设置 Language Settings',
                'language_label': '语言 Language:',
                'save_btn': 'Save',
                'cancel_btn': 'Cancel',
                'image_file_type': 'Image File Type',
                'all_files': 'All Files',
            }
        }

        self.load_config()
        self.current_lang = self.config.get('language', 'zh_CN')
        
        # 使用Toplevel而不是Window
        self.root = ttk.Toplevel(parent)
        self.root.title(self.get_text('window_title'))  # 使用翻译的窗口标题
        self.root.resizable(False, False)
        
        # 设置模态窗口
        self.root.transient(parent)
        self.root.grab_set()
        
        self.callback = callback
        # 保存原始配置用于取消时恢复
        self.original_config = self.config.copy()
        
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # 主题选择
        theme_frame = ttk.LabelFrame(main_frame, text=self.get_text('theme_section'), padding="10")
        theme_frame.pack(fill='x', pady=(0, 10))
        
        self.themes = [
            "cosmo", "flatly", "litera", "minty", "lumen", 
            "sandstone", "yeti", "pulse", "united", "morph", 
            "journal", "darkly", "superhero", "solar", "cyborg", "vapor"
        ]
        
        self.theme_var = tk.StringVar(value=self.config.get('theme', 'minty'))
        self.theme_combo = ttk.Combobox(
            theme_frame, 
            textvariable=self.theme_var,
            values=self.themes,
            state='readonly',
            width=30
        )
        self.theme_combo.pack()
        # 绑定主题切换事件
        self.theme_combo.bind('<<ComboboxSelected>>', self.on_theme_change)
        
        # 图片选择
        image_frame = ttk.LabelFrame(main_frame, text=self.get_text('image_section'), padding="10")
        image_frame.pack(fill='x', pady=(0, 10))
        
        self.image_path_var = tk.StringVar(value=self.config.get('image_path', 'sun.png'))
        image_entry = ttk.Entry(image_frame, textvariable=self.image_path_var, width=30)
        image_entry.pack(side='left', padx=(0, 5))
        
        browse_btn = ttk.Button(
            image_frame,
            text=self.get_text('browse_btn'),
            command=self.browse_image,
            bootstyle="info-outline"
        )
        browse_btn.pack(side='right')
        
        # 窗口大小设置
        size_frame = ttk.LabelFrame(main_frame, text=self.get_text('window_size_section'), padding="10")
        size_frame.pack(fill='x', pady=(0, 10))
        
        # 宽度
        width_frame = ttk.Frame(size_frame)
        width_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(width_frame, text=self.get_text('width_label')).pack(side='left')
        self.width_var = tk.StringVar(value=str(self.config.get('window_width', 250)))
        self.width_spinbox = ttk.Spinbox(
            width_frame,
            from_=200,
            to=400,
            increment=10,
            textvariable=self.width_var,
            width=10,
            command=self.on_size_change
        )
        self.width_spinbox.bind('<Return>', self.on_size_change)
        self.width_spinbox.pack(side='right')
        
        # 高度
        height_frame = ttk.Frame(size_frame)
        height_frame.pack(fill='x')
        ttk.Label(height_frame, text=self.get_text('height_label')).pack(side='left')
        self.height_var = tk.StringVar(value=str(self.config.get('window_height', 250)))
        self.height_spinbox = ttk.Spinbox(
            height_frame,
            from_=200,
            to=400,
            increment=10,
            textvariable=self.height_var,
            width=10,
            command=self.on_size_change
        )
        self.height_spinbox.bind('<Return>', self.on_size_change)
        self.height_spinbox.pack(side='right')
        
        # 刷新时间设置
        refresh_frame = ttk.LabelFrame(main_frame, text=self.get_text('refresh_section'), padding="10")
        refresh_frame.pack(fill='x', pady=(0, 10))
        
        self.refresh_var = tk.StringVar(value=str(self.config.get('refresh_interval', 120)))
        # 添加验证函数
        def validate_refresh(value):
            try:
                val = int(value)
                return val >= 1
            except ValueError:
                return False
        
        refresh_frame_inner = ttk.Frame(refresh_frame)
        refresh_frame_inner.pack(fill='x')
        ttk.Label(refresh_frame_inner,text=self.get_text('interval_label')).pack(side='left')

        # vcmd = (self.root.register(validate_refresh), '%P')
        self.refresh_spinbox = ttk.Spinbox(
            refresh_frame_inner,
            from_=1,
            to=3600,
            increment=1,
            textvariable=self.refresh_var,
            width=10,
            validate='all',
            # validatecommand=vcmd,
            command=lambda: self.on_spinbox_change(self.refresh_spinbox)
        )
        self.refresh_spinbox.bind('<Return>', lambda e: self.on_spinbox_change(self.refresh_spinbox))
        self.refresh_spinbox.pack(side='right')
        
        # 字体大小设置
        font_frame = ttk.LabelFrame(main_frame, text=self.get_text('font_section'), padding="10")
        font_frame.pack(fill='x', pady=(0, 10))

        font_frame_inner = ttk.Frame(font_frame)
        font_frame_inner.pack(fill='x')
        ttk.Label(font_frame_inner, text=self.get_text('size_label')).pack(side='left')
        
        self.font_size_var = tk.StringVar(value=str(self.config.get('font_size', 10)))
        # 添加验证函数
        def validate_font(value):
            try:
                val = int(value)
                return val >= 5
            except ValueError:
                return False
                
        # vcmd_font = (self.root.register(validate_font), '%P')
        self.font_spinbox = ttk.Spinbox(
            font_frame_inner,
            from_=5,
            to=16,
            textvariable=self.font_size_var,
            width=10,
            # validate='all',
            # validatecommand=vcmd_font,
            command=lambda: self.on_spinbox_change(self.font_spinbox)
        )
        self.font_spinbox.bind('<Return>', lambda e: self.on_spinbox_change(self.font_spinbox))
        self.font_spinbox.pack(side='right')

        # 添加语言选择部分
        lang_frame = ttk.LabelFrame(main_frame, text=self.get_text('language_section'), padding="10")
        lang_frame.pack(fill='x', pady=(0, 10))
        
        self.lang_var = tk.StringVar(value=self.config.get('language', 'zh_CN'))
        lang_frame_inner = ttk.Frame(lang_frame)
        lang_frame_inner.pack(fill='x')
        ttk.Label(lang_frame_inner, text=self.get_text('language_label')).pack(side='left')
        
        self.lang_var = tk.StringVar(value=self.current_lang)
        self.lang_combo = ttk.Combobox(
            lang_frame_inner,
            textvariable=self.lang_var,
            values=['zh_CN', 'en_US'],
            state='readonly',
            width=10
        )
        self.lang_combo.pack(side='right')
        self.lang_combo.bind('<<ComboboxSelected>>', lambda e: self.save_config(preview=True))
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        save_btn = ttk.Button(
            button_frame,
            text=self.get_text('save_btn'),
            command=self.save_config,
            bootstyle="success",
            width=8
        )
        save_btn.pack(side='right', padx=(5, 0))
        
        cancel_btn = ttk.Button(
            button_frame,
            text=self.get_text('cancel_btn'),
            command=self.on_cancel,
            bootstyle="danger-outline",
            width=10
        )
        cancel_btn.pack(side='right')
        
        # 设置窗口位置为屏幕中央
        self.center_window()

    def get_text(self, key):
        """获取当前语言的翻译文本"""
        return self.translations[self.current_lang][key]

    def on_theme_change(self, event=None):
        # 实时预览主题
        ttk.Style().theme_use(self.theme_var.get())
        # 立即应用到主窗口
        self.save_config(preview=True)
        
    def on_size_change(self, event=None):
        try:
            # 验证输入值是否在有效范围内
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            if 200 <= width <= 400 and 200 <= height <= 400:
                self.save_config(preview=True)
        except ValueError:
            pass
        
    def load_config(self):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.config = {
                'theme': 'minty',
                'image_path': 'sun.png',
                'window_width': 250,
                'window_height': 250,
                'refresh_interval': 120,
                'font_size': 10
            }
    
    def browse_image(self):
        filename = filedialog.askopenfilename(
            title=self.get_text('image_section'),
            filetypes=[
                (self.get_text('image_file_type'), "*.png *.jpg *.jpeg *.gif *.bmp"),
                (self.get_text('all_files'), "*.*")
            ]
        )
        if filename:
            self.image_path_var.set(filename)
            self.save_config(preview=True)
    
    def save_config(self, preview=False):
        try:
            new_config = {
                'theme': self.theme_var.get(),
                'image_path': self.image_path_var.get(),
                'window_width': int(self.width_var.get()),
                'window_height': int(self.height_var.get()),
                'refresh_interval': int(self.refresh_var.get()),
                'font_size': int(self.font_size_var.get()),
                'language': self.lang_var.get()  # 添加语言设置
            }
            
            if preview:
                # 预览模式只调用回调函数，不保存到文件
                if self.callback:
                    self.callback(new_config)
            else:
                # 保存模式既保存到文件也调用回调函数
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(new_config, f, indent=4, ensure_ascii=False)
                
                if self.callback:
                    self.callback(new_config)
                self.root.destroy()
                
                self.root.destroy()
        except ValueError as e:
            print(f"配置值无效: {e}")
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def on_cancel(self):
        # 恢复原始配置
        if self.callback:
            self.callback(self.original_config)
        self.root.destroy()

    def on_spinbox_change(self, spinbox):
        """处理spinbox值变化"""
        try:
            value = int(spinbox.get())
            min_val = int(spinbox.cget('from'))
            if value < min_val:
                spinbox.set(str(min_val))
            self.save_config(preview=True)
        except ValueError:
            pass

    def update_window_texts(self):
        """更新窗口中的所有文本"""
        self.root.title(self.get_text('window_title'))
        
        # 遍历所有控件更新文本
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame):
                        if 'theme' in str(child):
                            child.configure(text=self.get_text('theme_section'))
                        elif 'image' in str(child):
                            child.configure(text=self.get_text('image_section'))
                        elif 'size' in str(child):
                            child.configure(text=self.get_text('window_size_section'))
                        elif 'refresh' in str(child):
                            child.configure(text=self.get_text('refresh_section'))
                        elif 'font' in str(child):
                            child.configure(text=self.get_text('font_section'))
                        elif 'lang' in str(child):
                            child.configure(text=self.get_text('language_section'))
                            
                    elif isinstance(child, ttk.Button):
                        if 'browse' in str(child):
                            child.configure(text=self.get_text('browse_btn'))
                        elif 'save' in str(child):
                            child.configure(text=self.get_text('save_btn'))
                        elif 'cancel' in str(child):
                            child.configure(text=self.get_text('cancel_btn'))
                    # 更新标签文本
                    elif isinstance(child, ttk.Label):
                        if '宽度' in str(child) or 'Width' in str(child):
                            child.configure(text=self.get_text('width_label'))
                        elif '高度' in str(child) or 'Height' in str(child):
                            child.configure(text=self.get_text('height_label'))
                        elif '间隔' in str(child) or 'Interval' in str(child):
                            child.configure(text=self.get_text('interval_label'))
                        elif '大小' in str(child) or 'Size' in str(child):
                            child.configure(text=self.get_text('size_label'))
                        elif '语言' in str(child) or 'Language' in str(child):
                            child.configure(text=self.get_text('language_label'))

    def on_language_change(self, event=None):
        """语言改变时的处理"""
        self.current_lang = self.lang_var.get()
        self.update_window_texts()
        # 立即预览更改
        self.save_config(preview=True)

if __name__ == "__main__":
    app = ConfigWindow()
    try:
        app.run()
    except Exception as e:
        print(f"本文件不支持直接运行，请通过 Sunshine.py 进行设置。")