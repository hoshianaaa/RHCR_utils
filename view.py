# 各エージェントの移動履歴（ここではエージェント1の履歴のみ実際のデータを使用し、残りはダミーデータ）
states_agent1 = "27,3,0;27,2,1;26,2,2;25,2,3;24,2,4;24,3,5;24,0,6;25,0,7;26,0,8;26,3,9;41,3,10;56,3,11;56,2,12;55,2,13;54,2,14;53,2,15;52,2,16;51,2,17;50,2,18;49,2,19;48,2,20;"
states_agent2 = "43,2,0;42,2,1;41,2,2;41,1,3;26,1,4;11,1,5;11,2,6;10,2,7;9,2,8;8,2,9;7,2,10;6,2,11;5,2,12;5,3,13;20,3,14;20,0,15;21,0,16;22,0,17;23,0,18;24,0,19;25,0,20;"
states_agent3 = "57,1,0;57,1,1;42,1,2;27,1,3;12,1,4;12,2,5;12,2,6;11,2,7;10,2,8;9,2,9;8,2,10;7,2,11;7,3,12;22,3,13;22,0,14;22,1,15;7,1,16;7,2,17;6,2,18;6,3,19;21,3,20;"


import cv2
import numpy as np

# マップのデータ
map_data = [
    "...............",
    ".rr.eeeeeee.rr.",
    ".rr.@@@@@@@.rr.",
    ".rr.eeeeeee.rr.",
    "..............."
]

# マップのサイズ設定
height = 5  # マップの高さ
width = 15  # マップの幅

# マップの色の設定
colors = {
    'r': (128, 128, 128),  # 灰色
    'e': (0, 255, 255),    # 黄色
    '@': (0, 0, 0),        # 黒
    '.': (255, 255, 255)   # 白
}

# マップを画像に変換し、枠線を描画する関数
def draw_map_with_grid(image):
    tile_size = 100  # タイルのサイズ
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            color = colors.get(cell, (255, 255, 255))  # デフォルトは白色
            top_left = (x * tile_size, y * tile_size)
            bottom_right = ((x + 1) * tile_size, (y + 1) * tile_size)
            cv2.rectangle(image, top_left, bottom_right, color, -1)  # セルを塗りつぶし
            cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), 1)  # 枠線を描画

# 各エージェントの移動履歴
#states_agent1 = "27,3,0;27,2,1;26,2,2;25,2,3;24,2,4;24,3,5;"
#states_agent2 = "43,2,0;42,2,1;41,2,2;41,1,3;26,1,4;11,1,5;"
#states_agent3 = "57,1,0;57,1,1;42,1,2;27,1,3;12,1,4;12,2,5;"

# 各エージェントの状態をリストとしてパース
parsed_states_agent1 = [tuple(map(int, state.split(','))) for state in states_agent1.split(';') if state]
parsed_states_agent2 = [tuple(map(int, state.split(','))) for state in states_agent2.split(';') if state]
parsed_states_agent3 = [tuple(map(int, state.split(','))) for state in states_agent3.split(';') if state]

# 画像を保存するためのフォルダを指定
output_folder = "out1/"

# 最大のステップ数を決定
max_steps = max(len(parsed_states_agent1), len(parsed_states_agent2), len(parsed_states_agent3))

for idx in range(max_steps):
    # 画像を作成 (マップのグリッドを含む)
    image = np.ones((height * 100, width * 100, 3), dtype=np.uint8) * 255
    draw_map_with_grid(image)  # マップのグリッドと枠線を描画

    # 各エージェントの状態を更新して描画
    for agent_id, (parsed_states, color) in enumerate(zip([parsed_states_agent1, parsed_states_agent2, parsed_states_agent3], [(0, 0, 255), (0, 255, 0), (255, 0, 0)])):
        if idx < len(parsed_states):
            position, direction, _ = parsed_states[idx]
            y = position // width
            x = position % width
            center = (x * 100 + 50, y * 100 + 50)
            cv2.circle(image, center, 40, color, -1)  # エージェントごとに異なる色

            # 向きに応じた矢印を描画
            arrow_end = {
                1: (center[0], center[1] - 50),
                0: (center[0] + 50, center[1]),
                3: (center[0], center[1] + 50),
                2: (center[0] - 50, center[1])
            }[direction]
            cv2.arrowedLine(image, center, arrow_end, (255, 255, 0), 5)

    # 画像を保存
    output_path = f"{output_folder}step_{idx:03d}.png"
    cv2.imwrite(output_path, image)

