import numpy as np 
from scipy.stats import norm
import tkinter as tk

# Close form by martingale pricing method

def Close_form(S0, r, q, sigma, T, k1, k2, k3, k4):
  """
  """
  d11 = ((np.log(S0/k1) + (r-q-(sigma**2)/2)*T))/(sigma*(T**0.5))
  d12 = ((np.log(S0/k2) + (r-q-(sigma**2)/2)*T))/(sigma*(T**0.5))
  d13 = ((np.log(S0/k3) + (r-q-(sigma**2)/2)*T))/(sigma*(T**0.5))
  d14 = ((np.log(S0/k4) + (r-q-(sigma**2)/2)*T))/(sigma*(T**0.5))

  d21 = ((np.log(S0/k1) + (r-q+(sigma**2)/2)*T))/(sigma*(T**0.5))
  d22 = ((np.log(S0/k2) + (r-q+(sigma**2)/2)*T))/(sigma*(T**0.5))
  d23 = ((np.log(S0/k3) + (r-q+(sigma**2)/2)*T))/(sigma*(T**0.5))
  d24 = ((np.log(S0/k4) + (r-q+(sigma**2)/2)*T))/(sigma*(T**0.5))

  fn_1 = S0*np.exp((r-q)*T)*(norm.cdf(d21)-norm.cdf(d22))
  fn_2 = k1*(norm.cdf(d11)-norm.cdf(d12))
  fn_3 = (k2-k1)*(norm.cdf(d12)-norm.cdf(d13))
  fn_4 = (k2-k1)/(k4-k3)*S0*np.exp((r-q)*T)*(norm.cdf(d23)-norm.cdf(d24))
  fn_5 = (k2-k1)/(k4-k3)*k4*(norm.cdf(d13)-norm.cdf(d14))
  
  option_price = np.exp(-r*T)*(fn_1 - fn_2 + fn_3 - fn_4 + fn_5)
  option_price = round(option_price, 4)
  return option_price
  # print('The close form solution is:', round(option_price, 4))
  
  
  # Monte Carlo Simulation

def sampling(S0, r, q, sigma, T, k1, k2, k3, k4):
    '''
    '''
    mu = np.log(S0) + (r-q-sigma**2*0.5)*T
    std = sigma * (T**0.5)
    log_ST = np.random.normal(loc=mu, scale=std, size=10000)
    sample = np.exp(log_ST)
    
    sample[(sample<=k1) | (sample>=k4)] = 0
    sample[(sample>k1) & (sample<=k2)] = sample[(sample>k1) & (sample<=k2)]-k1
    sample[(sample>k2) & (sample<=k3)] = k2-k1
    sample[(sample>k3) & (sample<k4)] = (k2-k1)/(k4-k3) * (k4-sample[(sample>k3)&(sample<k4)])

    return np.mean(sample)

def MonteCarlo(S0, r, q, sigma, T, k1, k2, k3, k4):
    '''
    '''
    sample_mean = []
    for _ in range(20):
      sample_mean.append(sampling(S0, r, q, sigma, T, k1, k2, k3, k4))
    print('Sample mean:', round(np.mean(sample_mean)*np.exp(-r*T), 4))
    print('Upper Bound:', round(np.mean(sample_mean)*np.exp(-r*T) + 2*np.std(sample_mean)*np.exp(-r*T), 4))
    print('Lower Bound:', round(np.mean(sample_mean)*np.exp(-r*T) - 2*np.std(sample_mean)*np.exp(-r*T), 4))


def GUI(model):
  # Tkinter視窗
  window = tk.Tk()
  window.title("輸入數字並相加")
  """_summary_
    # 輸入框
  input_frame = tk.Frame(window)
  input_frame.pack(side=tk.TOP)
  input_label = tk.Label(input_frame, text="請輸入數字，以逗號分隔:")
  input_label.pack(side=tk.LEFT)
  input_entry = tk.Entry(input_frame)
  input_entry.pack(side=tk.LEFT)
  """

  # 輸入框
  string_frame = tk.Frame(window)
  string_frame.pack(side=tk.TOP)
  string_label = tk.Label(string_frame, text="請輸入字串:")
  string_label.pack(side=tk.LEFT)
  string_entry = tk.Entry(string_frame)
  string_entry.pack(side=tk.LEFT)

  numbers_frame = tk.Frame(window)
  numbers_frame.pack(side=tk.TOP)
  numbers_label = tk.Label(numbers_frame, text="請輸入數字清單，以逗號分隔:")
  numbers_label.pack(side=tk.LEFT)
  numbers_text = tk.Text(numbers_frame, height=1)
  numbers_text.pack(side=tk.LEFT)
  
  # 按鈕
  button_frame = tk.Frame(window)
  button_frame.pack(side=tk.TOP)
  def calculate():
      # 從輸入框中取得使用者輸入的字串
      string = string_entry.get().strip()
      string = eval(string)
      # 從輸入框中取得使用者輸入的數字清單，並轉換為數字型態的列表
      numbers = [float(x.strip()) for x in numbers_text.get("1.0", "end-1c").split(",")]
      # 呼叫使用者定義的函數
      result = string(numbers)
      # 將結果顯示在視窗中
      output_label.config(text="結果: {}".format(result))
  button = tk.Button(button_frame, text="計算", command=calculate)
  button.pack()

  """_summary_
  # 按鈕
  button_frame = tk.Frame(window)
  button_frame.pack(side=tk.TOP)
  def calculate():
      # 從輸入框中取得使用者輸入的數字，並轉換為數字型態
      numbers = input_entry.get().split(",")
      numbers = [float(x.strip()) for x in numbers]
      # 呼叫使用者定義的函數
      result = model(*numbers)
      # 將結果顯示在視窗中
      output_label.config(text="BS pricing: {}".format(result))
  button = tk.Button(button_frame, text="計算", command=calculate)
  button.pack()
  """

  # 輸出框
  output_frame = tk.Frame(window)
  output_frame.pack(side=tk.TOP)
  output_label = tk.Label(output_frame, text="BS pricing:")
  output_label.pack()

  # 執行視窗
  window.mainloop()

GUI(Close_form)

# S0, r, q, sigma, T, k1, k2, k3, k4 = 100, 0.05, 0.02, 0.5, 0.4, 90, 98, 102, 110
# Close_form(input)
# MonteCarlo(input)
"""
S0, r, q, sigma, T, k1, k2, k3, k4 = 100, 0.05, 0.02, 0.5, 0.4, 90, 98, 102, 104
Close_form(S0, r, q, sigma, T, k1, k2, k3, k4)
MonteCarlo(S0, r, q, sigma, T, k1, k2, k3, k4)
"""

