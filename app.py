# 重要 終端機請先執行
# py -m venv env              # 建立 env 虛擬環境
# env\Scripts\activate        # 啟動 env 虛擬環境
# (env) pip install requests  # 安裝 requests 套件


# 字典-可能會有的需求key
# {'os': '', 'cpu': '', 'ram': '', 'gpu': '', 'directx': '', 'rom': ''}
# os=系統, cpu=處理器, ram=記憶體, gpu=顯示卡, directx=directX版本, rom=可用儲存空間
# .db-可能會有的需求key
# name, min_os, min_cpu, min_ram, min_gpu, min_directx, min_rom,
# rec_os, rec_cpu, rec_ram, rec_gpu, rec_directx, rec_rom,
# name=遊戲名稱, 前綴min_=最低配備, 前綴rec_=建議配備
# os=系統, cpu=處理器, ram=記憶體, gpu=顯示卡, directx=directX版本, rom=可用儲存空間


# 抓取參考範例網址
# https://store.steampowered.com/app/1774580/STAR_WARS/
# https://store.steampowered.com/app/227300/Euro_Truck_Simulator_2/
# https://store.steampowered.com/app/2358720/_/
# https://store.steampowered.com/app/1091500/Cyberpunk_2077/
# https://store.steampowered.com/app/2878980/NBA_2K25/
# https://store.steampowered.com/app/1623730/Palworld/
# https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/


# 合併說明
# <= <= <= 是程式合併要修改的地方
# 請調用資料庫顯示而不是字典
# 以windows系統需求為主，有些需求像是:備註、音訊卡等 重要程度偏低不用做
# 資料庫用完請close()，有用到在打開，以保安全

# 畫面說明
# 視窗標題->題目名稱
# URL元件、網址輸入框、按鈕 在上面；URL元件、網址輸入框、按鈕相對位置隨你便
# 顯示系統需求會有一個顯示框來顯示
# 請用try以便使用者不須重開程式
# 另外當按鈕再次按下後要刷新顯示框

# 其他問題直接問群組

import re
import requests
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def on_button1_click(url):
    try:
        game_name = None
        min_requirement = {'os': '', 'cpu': '', 'ram': '', 'gpu': '', 'directx': '', 'rom': ''}
        rec_requirement = {'os': '', 'cpu': '', 'ram': '', 'gpu': '', 'directx': '', 'rom': ''}
        # url = "https://store.steampowered.com/app/227300/Euro_Truck_Simulator_2/" # <= <= <=這邊要改成點擊按鈕，將網址輸入框資料給url
        response = requests.get(url)

        # 爬蟲
        pattern = re.compile(r'<div id="appHubAppName" class="apphub_AppName">([^<]+)')
        match = pattern.findall(response.text)
        game_name = "".join(match)
        # print(game_name)

        pattern = re.compile(r'<strong>OS:</strong>\s?([^<]+)')
        match = pattern.findall(response.text)
        if match:
            min_requirement["os"]=match[0]
            rec_requirement["os"]=match[1]

        pattern = re.compile(r'<strong>Processor:</strong>\s?([^<]+)')
        match = pattern.findall(response.text)
        if match:
            min_requirement["cpu"]=match[0]
            rec_requirement["cpu"]=match[1]

        pattern = re.compile(r'<strong>Memory:</strong>\s?([^(RAM)]+)')
        match = pattern.findall(response.text)
        if match:
            min_requirement["ram"]=match[0]
            rec_requirement["ram"]=match[1]

        pattern = re.compile(r'<strong>Graphics:</strong>\s?([^<]+)')
        match = pattern.findall(response.text)
        if match:
            min_requirement["gpu"]=match[0]
            rec_requirement["gpu"]=match[1]

        pattern = re.compile(r'<strong>DirectX:</strong>\s?Version ([^<]+)')
        match = pattern.findall(response.text)
        if match:
            min_requirement["directx"]=match[0]
            rec_requirement["directx"]=match[1]

        pattern = re.compile(r'<strong>Storage:</strong>\s?([^(available)]+)')
        match = pattern.findall(response.text)
        if match:
            min_requirement["rom"]=match[0]
            rec_requirement["rom"]=match[1]
        pattern = re.compile(r'<strong>Hard Drive:</strong>\s?([^(available)]+)')
        match = pattern.findall(response.text)
        if match:
            min_requirement["rom"]=match[0]
            rec_requirement["rom"]=match[1]


        # 資料庫儲存資料
        conn = sqlite3.connect('game_info.db')
        cursor = conn.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS contacts(
                name TEXT, min_os TEXT, min_cpu TEXT, min_ram TEXT, min_gpu TEXT, min_directx TEXT, min_rom TEXT, rec_os TEXT, rec_cpu TEXT, rec_ram TEXT, rec_gpu TEXT, rec_directx TEXT, rec_rom TEXT)''')
        cursor.execute("INSERT OR IGNORE INTO contacts(name, min_os, min_cpu, min_ram, min_gpu, min_directx, min_rom, rec_os, rec_cpu, rec_ram, rec_gpu, rec_directx, rec_rom) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (game_name, min_requirement['os'], min_requirement['cpu'], min_requirement['ram'], min_requirement['gpu'], min_requirement['directx'], min_requirement['rom'],
        rec_requirement['os'], rec_requirement['cpu'], rec_requirement['ram'], rec_requirement['gpu'], rec_requirement['directx'], rec_requirement['rom']))
        # cursor.execute("SELECT * FROM contacts")
        cursor.execute('SELECT name FROM contacts')
        result_all = cursor.fetchall()
        box['values'] = result_all
        box.set('{'+game_name+'}')
        # contacts = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
    except:
        messagebox.showinfo('', '錯誤')




def on_button2_click():
    # 清空
    try:
        conn = sqlite3.connect('game_info.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts")
        conn.commit()
        cursor.close()
        conn.close()
        box['values']=''
        box.set('')
        listbox.delete(0, last=100)
    except:
        messagebox.showinfo('', '錯誤')

def on_button3_click(nm):
    try:
        listbox.delete(0, last=100)
        conn = sqlite3.connect('game_info.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE name LIKE ?",(nm,))
        contacts = cursor.fetchall()
        for row in contacts:
            listbox.insert(tk.END, "最低配備: ")
            listbox.insert(tk.END, "作業系統: " + row[1])
            listbox.insert(tk.END, "處理器: " + row[2])
            listbox.insert(tk.END, "記憶體: " + row[3])
            listbox.insert(tk.END, "顯示卡: " + row[4])
            listbox.insert(tk.END, "DirectX: " + row[5])
            listbox.insert(tk.END, "儲存空間: " + row[6])
            listbox.insert(tk.END, "")
            listbox.insert(tk.END, "建議配備: ")
            listbox.insert(tk.END, "作業系統: " + row[7])
            listbox.insert(tk.END, "處理器: " + row[8])
            listbox.insert(tk.END, "記憶體: " + row[9])
            listbox.insert(tk.END, "顯示卡: " + row[10])
            listbox.insert(tk.END, "DirectX: " + row[11])
            listbox.insert(tk.END, "儲存空間: " + row[12])
        conn.commit()
        cursor.close()
        conn.close()
    except:
        messagebox.showinfo('', '錯誤')
form = tk.Tk()
form.title("抓取steam遊戲系統要求")

form.geometry("800x600")
form.resizable(0, 0)
label1 = tk.Label(text="URL輸入欄")
label1.pack(padx=10, pady=0)
entry1 = tk.Entry(width=100)
entry1.pack(padx=10, pady=0)
label2 = tk.Label(text="",height=1)
label2.pack(padx=10, pady=0)
label3 = tk.Label(text="資料庫內遊戲選擇")
label3.pack(padx=10, pady=0)
conn = sqlite3.connect('game_info.db')
cursor = conn.cursor()
try:
    cursor.execute('SELECT name FROM contacts')
    result_all = cursor.fetchall()
    box = ttk.Combobox(values=result_all,width=97,state="readonly")
except:
    box = ttk.Combobox(values="",width=97,state="readonly")

conn.commit()
cursor.close()
conn.close()
box.pack(padx=10, pady=0)

listbox = tk.Listbox()
listbox.pack(fill= "both",expand = True,padx=10, pady=10)


button1 = tk.Button(form, text="爬蟲", command=lambda: on_button1_click(entry1.get()),width=10,height=1)
button1.pack(side="left", anchor="s",padx=10, pady=10)

button4 = tk.Button(form, text="資料庫搜索", command=lambda: on_button3_click(box.get().strip( '{').strip( '}' )),width=10,height=1)
button4.pack(side="left", anchor="s",padx=10, pady=10)

button2 = tk.Button(form, text="清空資料庫", command=lambda: on_button2_click(),width=10,height=1)
button2.pack(side="left", anchor="s",padx=10, pady=10)

button3 = tk.Button(form, text="離開", command=form.quit,width=10,height=1)
button3.pack(side="left", anchor="s",padx=10, pady=10)


form.mainloop()

