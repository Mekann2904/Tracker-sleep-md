import json
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from collections import defaultdict

def time_diff_in_hours(time_range):
    """時間範囲 (例: '12:00 - 14:00') を時間単位で計算"""
    start_time, end_time = time_range.split(' - ')
    time_format = "%H:%M"
    start = datetime.strptime(start_time, time_format)
    end = datetime.strptime(end_time, time_format)
    
    # 経過時間を時間単位で計算
    elapsed_time = (end - start).total_seconds() / 3600
    return elapsed_time

def calculate_sleep_times(json_file_path, start_date=None, end_date=None):
    """睡眠時間を日付ごとに集計し、開始日と終了日のフィルタリングを行う"""
    # JSONファイルを読み込む
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    tasks = data['tasks']
    
    # 日付ごとの睡眠と仮眠時間を集計
    sleep_data = defaultdict(float)
    
    for task in tasks:
        if task['task'] in ['睡眠', '仮眠']:
            # file_name から日付を取得（例: '2024-09-29.md' -> '2024-09-29'）
            date_str = task['file_name'].split('.')[0]
            date = datetime.strptime(date_str, '%Y-%m-%d').date()

            # 開始日と終了日でフィルタリング（デフォルトでは制限なし）
            if (start_date is None or date >= start_date) and (end_date is None or date <= end_date):
                elapsed_time = time_diff_in_hours(task['time_range'])
                sleep_data[date] += elapsed_time
    
    return sleep_data

def plot_sleep_data(sleep_data,  save_path=None):
    # 日付ごとにソート
    sorted_dates = sorted(sleep_data.keys())
    sleep_times = [sleep_data[date] for date in sorted_dates]
    
    # 各日付に対応する曜日を取得
    sorted_labels = [f"{date.strftime('%Y-%m-%d')} ({date.strftime('%a')})" for date in sorted_dates]
    
    # 移動平均を計算するためにデータフレームを作成
    df = pd.DataFrame({'date': sorted_dates, 'sleep_time': sleep_times})
    df['date'] = pd.to_datetime(df['date'])  # 日付をdatetime型に変換
    df.set_index('date', inplace=True)

    # 7日移動平均と3日移動平均を計算
    df['3_day_MA'] = df['sleep_time'].rolling(window=3).mean()
    df['7_day_MA'] = df['sleep_time'].rolling(window=7).mean()

    # グラフを描画
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['sleep_time'], marker='o', color='b', linestyle='-', label='Daily Sleep Time')
    plt.plot(df.index, df['3_day_MA'], color='orange', linestyle='--', label='3-Day Moving Average')
    plt.plot(df.index, df['7_day_MA'], color='green', linestyle='--', label='7-Day Moving Average')
    
    # 各点の近くに睡眠時間を表示
    for i, txt in enumerate(sleep_times):
        plt.text(df.index[i], sleep_times[i] + 0.1, f'{txt:.1f}', ha='center', fontsize=10)

    # 軸ラベルとタイトルを追加
    plt.xlabel('Date')
    plt.ylabel('Hours of Sleep/Nap')
    plt.title('Daily Sleep and Nap Times with Moving Averages')

    # 横軸に1時間ごとのグリッド線を追加
    plt.yticks(range(0, int(max(sleep_times)) + 2, 1))  # 1時間ごとに目盛りを表示

    # グリッド線を表示
    plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)


    # x軸のラベルを45度傾け、曜日付きのラベルを適用
    plt.xticks(ticks=df.index, labels=sorted_labels, rotation=45)

    # 凡例を追加
    plt.legend()

    # 画像を保存
    if save_path:
        #plt.savefig(save_path, dpi=300)
        plt.savefig(save_path, bbox_inches='tight', dpi=300)  # bbox_inches='tight'を追加して見切れを防止
        print("画像を保存しました")

    # # グラフを表示
    # plt.tight_layout()
    # plt.show()

# 使用例
json_file_path = ''  # JSONファイルのパス

# 日付フィルタリングを行いたい場合
# start_date_str = input("開始日 (yyyy-mm-dd) を入力してください（制限なしの場合は Enter キー）: ")
# end_date_str = input("終了日 (yyyy-mm-dd) を入力してください（制限なしの場合は Enter キー）: ")

start_date_str=None
end_date_str=None


# 入力された開始日と終了日を日付に変換
start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

# sleep_data を取得（デフォルトでは制限なし、フィルタリングする場合はstart_dateとend_dateを設定）
sleep_data = calculate_sleep_times(json_file_path, start_date=start_date, end_date=end_date)

# 画像を保存するファイルパスを指定
# save_path = ''
save_path = ''

# sleep_data をプロットし、画像を保存
plot_sleep_data(sleep_data, save_path=save_path)
