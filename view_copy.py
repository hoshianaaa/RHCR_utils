import cv2
import numpy as np

# マップのサイズ設定
height = 5
width = 15

# 各エージェントの移動履歴（ここではエージェント1の履歴のみ実際のデータを使用し、残りはダミーデータ）
states_agent1 = "27,3,0;27,2,1;26,2,2;25,2,3;24,2,4;24,3,5;"
states_agent2 = "43,2,0;42,2,1;41,2,2;41,1,3;26,1,4;11,1,5;"
states_agent3 = "57,1,0;57,1,1;42,1,2;27,1,3;12,1,4;12,2,5;"

# 各エージェントの状態をリストとしてパース
parsed_states_agent1 = [tuple(map(int, state.split(','))) for state in states_agent1.split(';') if state]
parsed_states_agent2 = [tuple(map(int, state.split(','))) for state in states_agent2.split(';') if state]
parsed_states_agent3 = [tuple(map(int, state.split(','))) for state in states_agent3.split(';') if state]

# 画像を保存するためのフォルダを指定
output_folder = "out1/"

# 最大のステップ数を決定（全エージェントの中で最も長い移動履歴を持つもの）
max_steps = max(len(parsed_states_agent1), len(parsed_states_agent2), len(parsed_states_agent3))

for idx in range(max_steps):
    # 画像を作成 (白背景)
    image = np.ones((height * 100, width * 100, 3), dtype=np.uint8) * 255

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

