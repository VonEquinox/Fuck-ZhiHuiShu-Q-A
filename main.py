import random
import time
import re
import os
import json
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from reloading import reloading

from Question import Questions

print("正在启动浏览器")
driver = webdriver.Edge(
    service=Service(EdgeChromiumDriverManager().install(), log_path="nul"),
    options=Options().add_argument("--disable-logging"),
)

print("请自己登陆并且打开提问页面")
driver.get("https://www.zhihuishu.com/")


WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "notLogin")))
driver.find_element(By.ID, "notLogin").click()
WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.NAME, "username")))
driver.find_element(By.NAME, "username").send_keys("")
WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.NAME, "password")))
driver.find_element(By.NAME, "password").send_keys("")

Handles_Before = driver.window_handles

def Cheack():
    try:
        driver.find_element(By.CLASS_NAME, "yidun_modal")
        input("验证码已加载，请手动输入验证码并按回车键继续")
    except Exception:
        pass

@reloading
def SendQuestion(Question):
    try:
        driver.get(driver.current_url)
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "qa-list-container")))
        Temp = driver.find_element(By.CLASS_NAME, "qa-list-container")
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "ask-btn")))
        Cheack()
        Temp.find_element(By.CLASS_NAME, "ask-btn").click()
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "el-textarea__inner")))
        AnswerBox = driver.find_element(By.CLASS_NAME, "el-textarea__inner")
        Cheack()
        AnswerBox.send_keys(Question)
        time.sleep(3)
        Cheack()
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".up-btn.ZHIHUISHU_QZMD.set-btn")))
        Cheack()
        driver.find_element(By.CSS_SELECTOR, ".up-btn.ZHIHUISHU_QZMD.set-btn").click()
    except Exception as e:
        print(e)

input("按回车键继续...")
Handles_After = driver.window_handles
new_window = None
for handle in Handles_After:
    if handle not in Handles_Before:
        new_window = handle
        break
driver.switch_to.window(new_window)

if __name__ == "__main__":
    while True:
        for Question in Questions:
            SendQuestion(Question)
            print("发送问题")