from datetime import datetime

def analyze_datetime(input_datetime_str):
    """
    分析輸入的日期時間字串，完成以下任務：
    1. 回傳該日期為星期幾。
    2. 回傳該日期是當年的第幾天。
    3. 計算從輸入的時刻至現在時間，共經過幾個太陽日（以浮點表示）。

    :param input_datetime_str: 日期時間字串，格式為 'YYYY-MM-DD HH:MM'
    :return: 包含分析結果的字典
    """
    try:
        # 將輸入的字串轉換為 datetime 物件
        input_datetime = datetime.strptime(input_datetime_str, "%Y-%m-%d %H:%M")
        
        # 1. 回傳該日期為星期幾
        weekday = input_datetime.strftime("%A")  # 例如: Monday, Tuesday
        
        # 2. 回傳該日期是當年的第幾天
        day_of_year = input_datetime.timetuple().tm_yday  # 例如: 1 表示 1 月 1 日
        
        # 3. 計算從輸入的時刻至現在時間，共經過幾個太陽日
        now = datetime.now()
        delta = now - input_datetime
        days_elapsed = delta.total_seconds() / (24 * 3600)  # 將秒數轉換為天數
        
        # 回傳結果
        return {
            "weekday": weekday,
            "day_of_year": day_of_year,
            "days_elapsed": days_elapsed
        }
    except ValueError:
        return "輸入的日期時間格式無效，請使用 'YYYY-MM-DD HH:MM' 格式。"

if __name__ == "__main__":
    # 讓使用者輸入日期時間字串
    input_datetime_str = input("請輸入日期時間 (格式為 YYYY-MM-DD HH:MM): ").strip()
    result = analyze_datetime(input_datetime_str)
    
    if isinstance(result, dict):
        print(f"該日期為星期: {result['weekday']}")
        print(f"該日期是當年的第 {result['day_of_year']} 天")
        print(f"從輸入的時刻至現在時間，共經過 {result['days_elapsed']:.2f} 個太陽日")
    else:
        print(result)