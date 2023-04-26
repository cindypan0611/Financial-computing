import tkinter as tk

# 使用者定義的函數，將多個數字相加
def add_numbers(*numbers):
    result = sum(numbers)
    return result

# Tkinter視窗
window = tk.Tk()
window.title("輸入數字並相加")

# 輸入框
input_frame = tk.Frame(window)
input_frame.pack(side=tk.TOP)
input_label = tk.Label(input_frame, text="請輸入數字，以逗號分隔:")
input_label.pack(side=tk.LEFT)
input_entry = tk.Entry(input_frame)
input_entry.pack(side=tk.LEFT)

# 按鈕
button_frame = tk.Frame(window)
button_frame.pack(side=tk.TOP)
def calculate():
    # 從輸入框中取得使用者輸入的數字，並轉換為數字型態
    numbers = input_entry.get().split(",")
    numbers = [float(x.strip()) for x in numbers]
    # 呼叫使用者定義的函數
    result = add_numbers(*numbers)
    # 將結果顯示在視窗中
    output_label.config(text="計算結果: {}".format(result))
button = tk.Button(button_frame, text="計算", command=calculate)
button.pack()

# 輸出框
output_frame = tk.Frame(window)
output_frame.pack(side=tk.TOP)
output_label = tk.Label(output_frame, text="計算結果:")
output_label.pack()

# 執行視窗
window.mainloop()