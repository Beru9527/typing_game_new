import tkinter as tk
import random
import time

# ========= 建立視窗（必須最先） =========
root = tk.Tk()
root.title("Typing Practice Game")
root.geometry("650x400")

# ========= 題庫 & 全域變數 =========
difficulty_settings = {
    "NORMAL": {"time": 10, "words": ["apple", "banana", "cherry", "keyboard", "window"]},
    "HARD": {"time": 10, "words": ["binary search", "linked list", "cloud storage", "working hard", "pay attention"]},
    "NIGHTMARE": {"time": 15, "words": ["Practice makes perfect.", "Accuracy is more important than speed."]}
}

difficulty = tk.StringVar(value="NORMAL")
TIME_LIMIT = 10
round_now = 0
round_total = 0
correct_count = 0
wrong_count = 0
time_left = TIME_LIMIT
current_sentence = ""
scores = []
start_time = 0

# ========= 遊戲邏輯 =========
def start_game():
    global round_now, scores, round_total, time_left
    global correct_count, wrong_count, TIME_LIMIT, current_sentence, start_time
    
    try:
        round_total_val = int(round_entry.get())
        if round_total_val <= 0:
            raise ValueError
    except ValueError:
        result_label.config(text="⚠ 請輸入正確回合數", fg="red")
        return
    
    round_now = 0
    scores.clear()
    correct_count = 0
    wrong_count = 0
    result_label.config(text="")
    
    setting = difficulty_settings[difficulty.get()]
    TIME_LIMIT = setting["time"]
    
    start_time = time.time()
    next_round()

def next_round():
    global round_now, time_left, current_sentence, start_time
    
    round_now += 1
    if round_now > int(round_entry.get()):
        end_game()
        return
    
    setting = difficulty_settings[difficulty.get()]
    current_sentence = random.choice(setting["words"])
    time_left = setting["time"]
    
    round_label.config(text=f"回合：{round_now} / {round_entry.get()}")
    sentence_label.config(text=current_sentence, fg="black")
    entry.delete(0, tk.END)
    timer_label.config(text=f"剩餘時間：{time_left} 秒")
    wpm_label.config(text="WPM: 0")
    result_label.config(text="")
    
    start_time = time.time()
    countdown()
    
def countdown():
    global time_left
    if time_left > 0:
        timer_label.config(text=f"剩餘時間：{time_left} 秒")
        time_left -= 1
        root.after(1000, countdown)
    else:
        check_answer()

def check_answer(event=None):
    global correct_count, wrong_count, scores, start_time
    
    user_input = entry.get()
    correct_chars = 0
    for i in range(min(len(user_input), len(current_sentence))):
        if user_input[i] == current_sentence[i]:
            correct_chars += 1
    
    accuracy = correct_chars / len(current_sentence) * 100
    scores.append(accuracy)
    
    # WPM 計算
    elapsed_time = max(time.time() - start_time, 1)
    words_typed = len(user_input.split())
    wpm = words_typed / elapsed_time * 60
    wpm_label.config(text=f"WPM: {wpm:.1f}")
    
    # 正確/錯誤提示
    if user_input == current_sentence:
        correct_count += 1
        result_label.config(text=f"✅ 完全正確！({accuracy:.1f}%)", fg="green")
    else:
        wrong_count += 1
        result_label.config(text=f"❌ 有錯誤 ({accuracy:.1f}%)", fg="red")
    
    root.after(1000, next_round)

def end_game():
    avg = sum(scores) / len(scores)
    sentence_label.config(text="🎉 遊戲結束！")
    timer_label.config(text="")
    round_label.config(text="")
    entry.delete(0, tk.END)
    result_label.config(
        text=f"📊 總成績\n難度：{difficulty.get()}\n答對：{correct_count} 題\n答錯：{wrong_count} 題\n平均正確率：{avg:.2f}%",
        fg="blue"
    )

# ========= GUI =========
title = tk.Label(root, text="Typing Practice Game", font=("Arial", 20))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="輸入回合數：").grid(row=0, column=0)
round_entry = tk.Entry(frame, width=10)
round_entry.grid(row=0, column=1)

tk.Label(frame, text="選擇難度：").grid(row=1, column=0)
tk.Radiobutton(frame, text="NORMAL", variable=difficulty, value="NORMAL").grid(row=1, column=1)
tk.Radiobutton(frame, text="HARD", variable=difficulty, value="HARD").grid(row=1, column=2)
tk.Radiobutton(frame, text="NIGHTMARE", variable=difficulty, value="NIGHTMARE").grid(row=1, column=3)

start_btn = tk.Button(frame, text="開始遊戲", command=start_game)
start_btn.grid(row=2, column=1, pady=5)

round_label = tk.Label(root, text="回合：")
round_label.pack()

sentence_label = tk.Label(root, text="請選擇難度並輸入回合數", font=("Arial", 14), wraplength=600)
sentence_label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), width=50)
entry.pack()
entry.bind("<Return>", check_answer)

timer_label = tk.Label(root, text="")
timer_label.pack()

wpm_label = tk.Label(root, text="WPM: 0")
wpm_label.pack()

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()