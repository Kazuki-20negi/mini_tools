import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib as mpl

# --- 定数設定 ---
G = 6.67430e-11     # 万有引力定数 [m^3 kg^-1 s^-2]
M = 5.972e24        # 地球の質量 [kg]
R_EARTH = 6371000   # 地球の半径 [m]
RHO_0 = 1.225       # 地表の空気密度 [kg/m^3]
H_S = 8500          # スケールハイト (空気密度の減少率) [m]

# --- 弾道・環境パラメータ（ユーザー設定） ---
Cd = 0.25            # 抗力係数
Area = 0.00034    # 前面投影面積 [m^2]
mass = 1.4       # 質量 [kg]
v0 = 2700.0         # 初速 [m/s]
angle_deg = 45.0    # 打ち上げ角度 [度]

# --- 運動方程式 (微分方程式) ---
def equations(t, state):
    # state = [r, theta, v_r, omega]
    r, theta, v_r, omega = state
    
    # 現在の高度
    h = r - R_EARTH
    
    # 1. 空気密度の計算 (指数関数モデル)
    # 高度が負（地下）または極端に高い場合は密度0とする簡易処理
    if h < 0:
        rho = RHO_0
    else:
        rho = RHO_0 * np.exp(-h / H_S)
    
    # 2. 速度ベクトルの計算
    # v_theta (水平速度) = r * omega
    v_theta = r * omega
    v = np.sqrt(v_r**2 + v_theta**2)
    
    # 3. 空気抵抗力 (Drag Force)
    # F_drag = 0.5 * rho * Cd * A * v^2
    if v == 0:
        drag_force = 0
    else:
        drag_force = 0.5 * rho * Cd * Area * v**2

    # 成分分解
    d_r = drag_force * (v_r / v)       # 半径方向の抵抗
    d_theta = drag_force * (v_theta / v) # 接線方向の抵抗

    # 4. 運動方程式の記述
    # 半径方向の加速度 (dv_r/dt)
    # gravity = G * M / r^2
    dr_dt = v_r
    dv_r_dt = r * omega**2 - (G * M / r**2) - (d_r / mass)
    
    # 角度の変化 (dtheta/dt)
    dtheta_dt = omega
    
    # 角速度の変化 (domega/dt)
    # コリオリ項: -2 * v_r * omega / r
    # 抵抗項: -d_theta / (m * r)
    domega_dt = -2 * v_r * omega / r - d_theta / (mass * r)
    
    return [dr_dt, dtheta_dt, dv_r_dt, domega_dt]

# --- 着弾判定イベント（高度が0になったら計算停止） ---
def hit_ground(t, state):
    r = state[0]
    return r - R_EARTH
hit_ground.terminal = True  # これがTrueだと計算をそこで打ち切る
hit_ground.direction = -1   # プラスからマイナスへ通過するときのみ検知

# --- 初期条件の設定 ---
theta_rad = np.radians(angle_deg)
initial_r = R_EARTH           # 地表から発射
initial_theta = 0.0           # 経度0地点
initial_v_r = v0 * np.sin(theta_rad)             # 垂直成分
initial_v_theta = v0 * np.cos(theta_rad)         # 水平成分
initial_omega = initial_v_theta / initial_r      # 角速度に変換

# 状態ベクトル: [r, theta, v_r, omega]
y0 = [initial_r, initial_theta, initial_v_r, initial_omega]

# --- 計算実行 ---
print("計算中……")
t_span = [0, 100000] # 最大10000秒まで計算
sol = solve_ivp(equations, t_span, y0, events=hit_ground, rtol=1e-6, atol=1e-12, max_step=0.5)

# --- 結果の表示 ---
final_r = sol.y[0][-1]
final_theta = sol.y[1][-1]
flight_time = sol.t[-1]

# 地表面に沿った飛距離 (弧の長さ) = R * theta
ground_distance = R_EARTH * final_theta

print(f"計算終了")
print(f"飛行時間: {flight_time:.2f} 秒")
print(f"最高高度: {(np.max(sol.y[0]) - R_EARTH)/1000:.2f} km")
print(f"着弾距離(地表距離): {ground_distance/1000:.2f} km")

# 必要であればここでグラフ描画を行います
r_data = sol.y[0]
theta_data = sol.y[1]
mpl.rcParams['font.family'] = 'Meiryo'

# 横軸：地表に沿った距離 [km]
x_plot = (R_EARTH * theta_data) / 1000.0
# 縦軸：高度 [km]
y_plot = (r_data - R_EARTH) / 1000.0

# グラフの作成
fig, ax = plt.subplots(figsize=(10, 5)) # 横長のグラフエリアを作成

# 軌跡をプロット
ax.plot(x_plot, y_plot, 'b-', linewidth=2, label='弾道軌跡')

# 最高点を見つけてプロット
max_height_idx = np.argmax(y_plot)
ax.plot(x_plot[max_height_idx], y_plot[max_height_idx], 'ro', label='最高点')
# 最高点の高度を表示
ax.text(x_plot[max_height_idx], y_plot[max_height_idx] + 5, 
        f'{y_plot[max_height_idx]:.1f} km', ha='center', color='red')

# 発射点と着弾点をプロット
ax.plot(x_plot[0], y_plot[0], 'go', label='発射点')
ax.plot(x_plot[-1], y_plot[-1], 'rx', markersize=10, label='着弾点')

# グラフの装飾
ax.set_title('弾道飛行シミュレーション (高度 vs 地表距離)')
ax.set_xlabel('地表距離 (Downrange) [km]')
ax.set_ylabel('高度 (Altitude) [km]')
ax.grid(True, linestyle='--', alpha=0.7) # グリッドを表示
ax.legend() # 凡例を表示

# 地表のライン（高度0）を強調
ax.axhline(y=0, color='green', linestyle='-', linewidth=1.5)
ax.set_ylim(bottom=-10) # 地表より少し下まで表示範囲を広げる

plt.tight_layout() # レイアウトの自動調整
plt.show() # グラフ表示