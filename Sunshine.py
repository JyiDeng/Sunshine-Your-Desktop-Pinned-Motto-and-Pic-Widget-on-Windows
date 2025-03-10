import ttkbootstrap as ttk
from PIL import Image, ImageTk
import json
import random
from config_window import ConfigWindow

class Sunshine:
    """
    悬浮在屏幕上的小太阳，给阴雨天在电脑前工作的你带来温暖！
    """
    def __init__(self):
        self.load_config()
        
        # 创建主窗口
        self.root = ttk.Window(themename=self.config['theme'])
        self.root.title("Sunshine小太阳")
        
        # 设置窗口无边框
        self.root.overrideredirect(True)
        
        # 创建主框架并设置固定大小
        self.frame = ttk.Frame(
            self.root,
            bootstyle="light",
            width=self.config['window_width'],
            height=self.config['window_height']
        )
        self.frame.pack(padx=5, pady=5)
        # 强制框架保持设定的大小
        self.frame.pack_propagate(False)
        
        self.load_translations()
        
        self.create_widgets()
        
    def load_config(self):
        try:
            with open(r'config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.config = {
                'theme': 'minty',
                'image_path': 'pic/sun.png',
                'window_width': 250,
                'window_height': 350,
                'refresh_interval': 120,
                'font_size': 10
            }
    def load_translations(self):
        """加载语言翻译"""
        self.translations = {
            'zh_CN': {
                'title': 'Sunshine小太阳',
                'toggle_top': '取消置顶',
                'toggle_normal': '置顶',
                'close': '关闭',
                'settings': '设置'
            },
            'en_US': {
                'title': 'Sunshine',
                'toggle_top': 'Unpin',
                'toggle_normal': 'Pin',
                'close': 'Close',
                'settings': 'Settings'
            }
        }  
    def create_widgets(self):
        """
        核心 - 创建窗口部件：图片、箴言、按钮
        """

        # 1. 图片部分
        try:
            # 加载图片并保持原始比例
            image = Image.open(self.config['image_path'])
            # 计算缩放比例，保持宽高比
            aspect_ratio = image.width / image.height
            # 预留固定空间：50px给按钮区域，10px上边距，
            # 取消10px按钮区域上边距
            target_height = min(self.config['window_height'] - 60, 150)  # 70 = 50(按钮) + 10(上) + 10(按钮上)
            target_width = int(target_height * aspect_ratio)
            
            # 如果宽度超出窗口，则以宽度为基准重新计算
            if target_width > self.config['window_width'] - 20:  # 预留边距
                target_width = self.config['window_width'] - 20
                target_height = int(target_width / aspect_ratio)
                
            image = image.resize((target_width, target_height))
            self.photo = ImageTk.PhotoImage(image)
            
            # 创建一个固定高度的Frame来显示图片
            self.image_frame = ttk.Frame(self.frame, width=230, height=target_height + 20)  # 加上上下边距
            self.image_frame.pack(anchor="center", pady=(10, 10))
            self.image_frame.pack_propagate(False)  # 保持固定高度
            
            # 创建标签显示图片
            self.label = ttk.Label(
                self.image_frame,
                image=self.photo,
                bootstyle="light"
            )
            self.label.pack(anchor="center")
            # 使用place布局让图片在高度上居中
            self.label.place(relx=0.5, rely=0.5, anchor="center")
            
        except Exception as e:
            print(f"无法加载图片: {e}")
            self.image_frame = ttk.Frame(self.frame, width=230, height=75)  # 固定高度
            self.image_frame.pack(anchor="center", pady=(10, 10))
            self.image_frame.pack_propagate(False)  # 保持固定高度
            
            self.label = ttk.Label(
                self.image_frame,
                text="小太阳图片无法加载! \nUnable to load the \nimage of Sunshine!",
                bootstyle="warning"
            )
            self.label.pack(anchor="center")
            # 使用place布局让图片在高度上居中
            self.label.place(relx=0.5, rely=0.5, anchor="center")

        # 2.箴言部分
        # 加载箴言
        try:
            with open('mottos.json', 'r', encoding='utf-8') as f:
                self.quotes = json.load(f)['quotes']
        except Exception as e:
            print(f"无法加载箴言文件: {e}")
            self.quotes = ["可爱的小太阳今天也要为你驱散阴霾！"]

        # 创建一个Frame来容纳箴言标签，以实现真正的居中
        remaining_height = self.config['window_height'] - 70  # 减去按钮区域和边距
        self.mottos_frame = ttk.Frame(self.frame, width=230,height=75)
        # self.mottos_frame.pack(fill='both', expand=True)
        self.mottos_frame.pack(fill='x', expand=False)  # 改为False，防止自动扩展
        self.mottos_frame.pack_propagate(False)  # 保持固定高度
        
        # 创建箴言标签
        self.mottos_label = ttk.Label(
            self.mottos_frame,
            text="",
            wraplength=200,
            justify="center",
            anchor="center",
            bootstyle="info",
            font=("微软雅黑", self.config['font_size'])
        )
        # 使用place让文字真正居中
        self.mottos_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # 3.按钮部分
        # 创建控制按钮框架，固定高度
        self.button_frame = ttk.Frame(self.frame, height=50)
        self.button_frame.pack(fill='x', pady=(0, 10))
        self.button_frame.pack_propagate(False)  # 保持固定高度
        lang = self.config.get('language', 'zh_CN')

        # 创建按钮，使用bootstrap风格
        self.toggle_button = ttk.Button(
            self.button_frame,
            text=self.translations[lang]['toggle_top'],
            command=self.toggle_topmost,
            bootstyle="warning-outline",
            width=7
        )
        self.toggle_button.pack(side='left', padx=3)
        
        self.close_button = ttk.Button(
            self.button_frame,
            text=self.translations[lang]['close'],
            command=self.root.quit,
            bootstyle="danger-outline",
            width=5
        )
        self.close_button.pack(side='left', padx=3)
        
        self.config_button = ttk.Button(
            self.button_frame,
            text=self.translations[lang]['settings'],
            command=self.open_config,
            bootstyle="secondary-outline",
            width=7
        )
        self.config_button.pack(side='right', padx=2)
        
        # 绑定鼠标事件用于拖动窗口
        self.label.bind('<Button-1>', self.start_move)
        self.label.bind('<B1-Motion>', self.on_move)
        
        # 初始状态设置为置顶
        self.is_topmost = True
        self.root.attributes('-topmost', self.is_topmost)

        # 更新第一条箴言
        self.update_mottos()
        
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        
    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    def toggle_topmost(self):
        self.is_topmost = not self.is_topmost
        self.root.attributes('-topmost', self.is_topmost)
        lang = self.config.get('language', 'zh_CN')
        self.toggle_button.configure(
            text=self.translations[lang]['toggle_top'] if self.is_topmost else self.translations[lang]['toggle_normal'],
            bootstyle="warning-outline" if self.is_topmost else "info-outline"
        )
        
    def open_config(self):
        def on_config_save(new_config):
            # 保存当前窗口位置
            current_x = self.root.winfo_x()
            current_y = self.root.winfo_y()
            
            self.config = new_config
            # 更新主题
            ttk.Style().theme_use(new_config['theme'])
            
            # 更新窗口大小
            self.frame.configure(width=new_config['window_width'], height=new_config['window_height'])
             # 更新语言
            lang = new_config.get('language', 'zh_CN')
            self.root.title(self.translations[lang]['title'])
            self.toggle_button.configure(text=self.translations[lang]['toggle_top'])
            self.close_button.configure(text=self.translations[lang]['close'])
            self.config_button.configure(text=self.translations[lang]['settings'])
        
            # 更新图片
            try:
                image = Image.open(new_config['image_path'])
                # 计算缩放比例，保持宽高比
                aspect_ratio = image.width / image.height
                target_height = min(new_config['window_height'] - 70, 150)  # 70 = 50(按钮) + 10(上) + 10(按钮上)
                target_width = int(target_height * aspect_ratio)
                
                # 如果宽度超出窗口，则以宽度为基准重新计算
                if target_width > new_config['window_width'] - 20:  # 预留边距
                    target_width = new_config['window_width'] - 20
                    target_height = int(target_width / aspect_ratio)
                    
                image = image.resize((target_width, target_height))
                self.photo = ImageTk.PhotoImage(image)
                self.label.configure(image=self.photo)
            except Exception as e:
                print(f"无法加载图片: {e}")
            
            # 更新字体大小
            self.mottos_label.configure(font=("微软雅黑", new_config['font_size']))
            
            # 使用保存的位置重新设置窗口位置
            self.root.geometry(f'+{current_x}+{current_y}')
            
        config_window = ConfigWindow(parent=self.root, callback=on_config_save)

    def update_mottos(self):
        """更新箴言显示"""
        random_quote = random.choice(self.quotes)
        self.mottos_label.configure(text=random_quote)
        # 使用配置中的刷新间隔
        self.root.after(self.config['refresh_interval'] * 1000, self.update_mottos)
        
    def run(self):
        # 将窗口放置在屏幕中央
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.config['window_width'] // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.config['window_height'] // 2)
        self.root.geometry(f'+{x}+{y}')
        
        self.root.mainloop()

if __name__ == "__main__":
    app = Sunshine()
    app.run()
