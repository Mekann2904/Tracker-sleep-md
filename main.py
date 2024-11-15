import re
import os
import json
from datetime import datetime
import subprocess


def extract_tasks(directory):
    tasks = []
    
    # ディレクトリ内のすべての.mdファイルを取得
    for file_name in os.listdir(directory):
        if file_name.endswith('.md'):
            file_path = os.path.join(directory, file_name)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                for line in lines:
                    # タスクのステータス、時間、内容を抽出する正規表現
                    match = re.search(r'\[( |x)\]\s+(\d{2}:\d{2}\s*-\s*\d{2}:\d{2})\s*(.*)', line)
                    if match:
                        completed = True if match.group(1) == 'x' else False
                        time_range = match.group(2)
                        task_content = match.group(3)
                        tasks.append({
                            'file_name': file_name,
                            'completed': completed,
                            'time_range': time_range,
                            'task': task_content
                        })
    
    return tasks

def save_json_summary(output_path, tasks):
    # 現在の日時を取得
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # JSON形式のデータを作成
    data = {
        'generated_on': current_time,
        'tasks': tasks
    }
    
    # JSONファイルに保存
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    print(f"Summary saved to {output_path}")

# 使用例
input_directory = ''  # ディレクトリを指定
output_file_path = ''  # 保存先のJSONファイルのパス

tasks = extract_tasks(input_directory)
save_json_summary(output_file_path, tasks)

# 2.pyを実行
subprocess.run(['python3', ''])

