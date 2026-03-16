import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# 获取当前 Mac 用户名
username = os.getlogin()
options = webdriver.ChromeOptions()

# 这里的路径指向你的 Chrome 资料库
# 注意：末尾不要带 "Default"，Selenium 会自动在 user-data-dir 下寻找 Default
user_path = f"/Users/{username}/Library/Application Support/Google/Chrome"
options.add_argument(f"--user-data-dir={user_path}")
# 1. 配置浏览器（保持登录状态是关键）
# 建议先手动启动一个 Chrome 窗口并登录百度云，然后通过用户配置文件路径启动
# 这样脚本打开的浏览器就是已登录状态，不需要每次都扫码

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# 2. 读取表格（假设 A 列是链接，B 列是提取码）
df = pd.read_excel("links.xlsx")


def save_to_pan(url, pwd):
    driver.get(url)
    time.sleep(2)  # 等待加载

    try:
        # 输入提取码
        input_box = driver.find_element(
            By.CLASS_NAME, "wp-s-save-to-pan__input"
        )  # 这里的 Class 名可能随网盘更新变化
        input_box.send_keys(pwd)

        # 点击确认/提取文件
        confirm_btn = driver.find_element(
            By.XPATH, "//span[contains(text(), '提取文件')]"
        )
        confirm_btn.click()
        time.sleep(2)

        # 点击全选并“保存到网盘”
        # 注意：此处需要根据网盘页面的具体按钮 ID 定位
        save_btn = driver.find_element(
            By.XPATH, "//span[contains(text(), '保存到网盘')]"
        )
        save_btn.click()
        print(f"成功保存: {url}")
    except Exception as e:
        print(f"保存失败: {url}, 错误: {e}")


# 3. 循环执行
for index, row in df.iterrows():
    save_to_pan(row["链接"], row["提取码"])

driver.quit()
