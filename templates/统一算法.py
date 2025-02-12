import sys
import os
from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

from argon2 import PasswordHasher
import time

class PasswordHasherApp(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化窗口
        self.setWindowTitle("Argon2 密码哈希生成器")
        self.setGeometry(100, 100, 400, 250)

        # 创建布局和控件
        self.layout = QVBoxLayout()

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("请输入密码")
        self.layout.addWidget(self.password_input)

        self.generate_button = QPushButton("生成哈希", self)
        self.layout.addWidget(self.generate_button)

        self.hash_label = QLabel("", self)
        self.layout.addWidget(self.hash_label)

        self.save_button = QPushButton("保存哈希到文件", self)
        self.layout.addWidget(self.save_button)

        self.copy_button = QPushButton("复制哈希到剪贴板", self)
        self.layout.addWidget(self.copy_button)

        # 设置按钮事件
        self.generate_button.clicked.connect(self.generate_hash)
        self.save_button.clicked.connect(self.save_hash)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        # 设置布局
        self.setLayout(self.layout)

    def generate_hash(self):
        # 获取输入的密码
        password = self.password_input.text()

        if password:
            # 使用 Argon2 算法生成哈希，设置相同的参数
            ph = PasswordHasher(
                time_cost=3,    # t = 3
                memory_cost=65536,  # m = 65536
                parallelism=4,  # p = 4
                hash_len=32,    # 默认哈希长度
                salt_len=16     # 默认盐长度
            )

            try:
                # 使用设置的参数生成哈希
                hash_value = ph.hash(password)
                # 显示生成的哈希值
                self.hash_label.setText(f"生成的哈希值：\n{hash_value}")
                self.generated_hash = hash_value  # 保存生成的哈希值
            except Exception as e:
                self.hash_label.setText(f"错误: {str(e)}")
        else:
            self.hash_label.setText("请输入密码！")

    def save_hash(self):
        # 确保已经生成了哈希值
        if hasattr(self, 'generated_hash') and self.generated_hash:
            # 获取当前时间，确保文件名唯一
            timestamp = int(time.time())
            filename = f"argon2_hash_{timestamp}.txt"

            # 保存哈希值到当前目录
            with open(filename, 'w') as f:
                f.write(self.generated_hash)
            
            self.hash_label.setText(f"哈希已保存为：{filename}")
        else:
            self.hash_label.setText("没有生成哈希，无法保存！")

    def copy_to_clipboard(self):
        # 确保已经生成了哈希值
        if hasattr(self, 'generated_hash') and self.generated_hash:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.generated_hash)
            self.hash_label.setText("哈希已复制到剪贴板！")
        else:
            self.hash_label.setText("没有生成哈希，无法复制！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordHasherApp()
    window.show()
    sys.exit(app.exec_())
