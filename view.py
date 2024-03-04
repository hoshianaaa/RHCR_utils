import cv2
import numpy as np
import os

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

# マップを画像に変換し、枠線とインデックスを描画する関数
def draw_map_with_grid(image):
    tile_size = 100  # タイルのサイズ
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            color = colors.get(cell, (255, 255, 255))  # デフォルトは白色
            top_left = (x * tile_size, y * tile_size)
            bottom_right = ((x + 1) * tile_size, (y + 1) * tile_size)
            cv2.rectangle(image, top_left, bottom_right, color, -1)  # セルを塗りつぶし
            cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), 1)  # 枠線を描画

            # セルの中央に一次元インデックスを描画
            index = y * width + x
            center = (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2))
            cv2.putText(image, str(index), center, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1)

# ファイルからエージェントの経路を読み込む関数
def load_agent_states_from_file(file_path):
    with open(file_path, 'r') as file:
        num_agents = int(file.readline().strip())  # エージェントの数を読み込む
        agent_states = [file.readline().strip() for _ in range(num_agents)]
    parsed_states = [[tuple(map(int, state.split(','))) for state in agent.split(';') if state] for agent in agent_states]
    return parsed_states

# 入力ファイルのパス（適切なパスに置き換えてください）
input_file_path = '/home/dev/exp/test\paths.txt'

# エージェントの経路を読み込む
parsed_states = load_agent_states_from_file(input_file_path)

# 画像を保存するためのフォルダを指定
output_folder = "output_images/"

# 出力フォルダが存在しない場合は作成
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 最大のステップ数を決定
max_steps = max(len(states) for states in parsed_states)

for idx in range(max_steps):
    # 画像を作成 (マップのグリッドを含む)
    image = np.ones((height * 100, width * 100, 3), dtype=np.uint8) * 255
    draw_map_with_grid(image)  # マップのグリッドと枠線を描画

    # 各エージェントの状態を更新して描画
    for agent_id, states in enumerate(parsed_states):
        if idx < len(states):
            position, direction, _ = states[idx]
            y = position // width
            x = position % width
            center = (x * 100 + 50, y * 100 + 50)
            color = [(0, 0, 255), (0, 255, 0), (255, 0, 0)][agent_id % 3]
            cv2.circle(image, center, 40, color, -1)  # エージェントを描画

            arrow_end = {
                1: (center[0], center[1] - 50),
                0: (center[0] + 50, center[1]),
                3: (center[0], center[1] + 50),
                2: (center[0] - 50, center[1])
            }[direction]
            cv2.arrowedLine(image, center, arrow_end, (255, 255, 0), 5)

    # 画像を表示
    cv2.imshow("MAPD Simulation", image)
    cv2.waitKey(500)  # 500ミリ秒待つ

    # 画像をファイルに保存
    output_path = f"{output_folder}step_{idx:03d}.png"
    cv2.imwrite(output_path, image)

# 画像ウィンドウを閉じる
cv2.destroyAllWindows()

