import cv2
import numpy as np

# マップのサイズ設定
height = 5
width = 15

# オブジェクトの移動履歴
states = "27,3,0;27,2,1;26,2,2;25,2,3;24,2,4;24,3,5;24,0,6;25,0,7;26,0,8;26,3,9;41,3,10;56,3,11;56,2,12;55,2,13;54,2,14;53,2,15;52,2,16;51,2,17;50,2,18;49,2,19;48,2,20;48,1,21;33,1,22;18,1,23;18,0,24;19,0,25;20,0,26;21,0,27;21,1,28;21,2,29;20,2,30;19,2,31;19,3,32;19,0,33;20,0,34;21,0,35;21,1,36;6,1,37;6,2,38;5,2,39;4,2,40;4,3,41;19,3,42;19,2,43;18,2,44;18,3,45;33,3,46;48,3,47;48,0,48;49,0,49;50,0,50;51,0,51;52,0,52;53,0,53;54,0,54;54,1,55;54,2,56;53,2,57;52,2,58;51,2,59;50,2,60;49,2,61;48,2,62;48,1,63;33,1,64;18,1,65;18,0,66;19,0,67;20,0,68;20,1,69;20,2,70;19,2,71;18,2,72;18,3,73;33,3,74;48,3,75;48,0,76;49,0,77;50,0,78;51,0,79;52,0,80;52,3,81;67,3,82;67,2,83;66,2,84;65,2,85;64,2,86;63,2,87;63,1,88;48,1,89;33,1,90;18,1,91;18,0,92;19,0,93;20,0,94;21,0,95;22,0,96;23,0,97;24,0,98;25,0,99;26,0,100"

# 各状態をリストとしてパース
parsed_states = [tuple(map(int, state.split(','))) for state in states.split(';')]

# 画像を保存するためのフォルダを指定
output_folder = "out1/"

for idx, (position, direction, time) in enumerate(parsed_states):
    # 画像を作成 (白背景)
    image = np.ones((height * 100, width * 100, 3), dtype=np.uint8) * 255

    # マップ上の位置をピクセル座標に変換
    y = position // width
    x = position % width

    # オブジェクトの中心点
    center = (x * 100 + 50, y * 100 + 50)

    # オブジェクト (円) を描画
    cv2.circle(image, center, 40, (0, 0, 255), -1)  # 赤色の円

    # 向きに応じた矢印を描画
    if direction == 1:  # 上
        cv2.arrowedLine(image, center, (center[0], center[1] - 50), (255, 255, 0), 5)
    elif direction == 0:  # 右
        cv2.arrowedLine(image, center, (center[0] + 50, center[1]), (255, 255, 0), 5)
    elif direction == 3:  # 下
        cv2.arrowedLine(image, center, (center[0], center[1] + 50), (255, 255, 0), 5)
    elif direction == 2:  # 左
        cv2.arrowedLine(image, center, (center[0] - 50, center[1]), (255, 255, 0), 5)

    # 画像を保存
    output_path = f"{output_folder}step_{idx:03d}.png"
    cv2.imwrite(output_path, image)

# 最初と最後の画像のパスを返す
first_image_path = f"{output_folder}step_000.png"
last_image_path = f"{output_folder}step_{len(parsed_states)-1:03d}.png"

first_image_path, last_image_path

