import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def plot_normal_pdf(mu, sigma, output_file="normal_pdf.jpg"):
    """
    繪製常態分佈的機率密度函數 (PDF) 並儲存為 JPG 圖檔。

    :param mu: 常態分佈的平均值
    :param sigma: 常態分佈的標準差
    :param output_file: 儲存的 JPG 檔案名稱
    """
    # 定義 x 軸範圍
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)
    # 計算 PDF 值
    pdf = norm.pdf(x, mu, sigma)

    # 繪製圖形
    plt.figure(figsize=(8, 6))
    plt.plot(x, pdf, label=f"μ={mu}, σ={sigma}", color="blue")
    plt.title("Normal Distribution PDF")
    plt.xlabel("x")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.grid()

    # 儲存圖形為 JPG 檔案
    plt.savefig(output_file, format="jpg")
    plt.close()
    print(f"圖形已儲存為 {output_file}")

if __name__ == "__main__":
    # 讓使用者輸入 mu 和 sigma
    try:
        mu = float(input("請輸入常態分佈的平均值 (mu): "))
        sigma = float(input("請輸入常態分佈的標準差 (sigma): "))
        output_file = input("請輸入輸出的 JPG 檔案名稱 (預設為 normal_pdf.jpg): ").strip()
        if not output_file:
            output_file = "normal_pdf.jpg"
        
        # 呼叫函數繪製圖形
        plot_normal_pdf(mu, sigma, output_file)
    except ValueError:
        print("輸入的值無效，請輸入數字格式的 mu 和 sigma。")