import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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
v0 = 76000.0         # 初速 [m/s]
angle_deg = 9.0    # 打ち上げ角度 [度]

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
t_span = [0, 200000] # 最大10000秒まで計算
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

# ==========================================
fig, axes = plt.subplots(2, 1, figsize=(10, 14)) # 縦に2つのグラフエリアを作成

# 共通データ（単位をkmに変換）
r_km = r_data / 1000.0
R_EARTH_KM = R_EARTH / 1000.0
ax1 = axes[0]
x_plot1 = (R_EARTH * theta_data) / 1000.0
y_plot1 = r_km - R_EARTH_KM

ax1.plot(x_plot1, y_plot1, 'b-', linewidth=2, label='Trajectory')
# 最高点、発射点、着弾点のプロット
max_idx = np.argmax(y_plot1)
ax1.plot(x_plot1[max_idx], y_plot1[max_idx], 'ro')
ax1.text(x_plot1[max_idx], y_plot1[max_idx]*1.05, f'Max Alt: {y_plot1[max_idx]:.0f}km', ha='center', color='red')
ax1.plot(x_plot1[0], y_plot1[0], 'go', label='Start')
ax1.plot(x_plot1[-1], y_plot1[-1], 'rx', markersize=10, label='End')

ax1.set_title('1. Altitude vs Downrange Distance (Unfolded View)')
ax1.set_xlabel('Downrange Distance [km]')
ax1.set_ylabel('Altitude [km]')
ax1.grid(True)
ax1.legend()
ax1.axhline(y=0, color='green', linestyle='-', linewidth=2, alpha=0.5) # 地表線

# ---------------------------------------
# グラフ2: 地球中心座標系での軌跡 (丸い地球)
# ---------------------------------------
ax2 = axes[1]

# 極座標(r, theta)から直交座標(X, Y)へ変換
# ※見やすくするため、θ=0を発射点とし、Y軸正方向(上)に向かって発射される配置にします
X_traj = r_km * np.sin(theta_data)
Y_traj = r_km * np.cos(theta_data)

# 地球の描画（水色の円）
earth_patch = Circle((0, 0), R_EARTH_KM, color='skyblue', alpha=0.6, label='Earth')
ax2.add_patch(earth_patch)
# 地表面の描画（緑色の線）
theta_circ = np.linspace(0, 2*np.pi, 360)
ax2.plot(R_EARTH_KM*np.sin(theta_circ), R_EARTH_KM*np.cos(theta_circ), 'g-', linewidth=1.5)

# 軌跡のプロット
ax2.plot(X_traj, Y_traj, 'b-', linewidth=2, label='Trajectory')
# 発射点と着弾点のプロット
ax2.plot(X_traj[0], Y_traj[0], 'go', markersize=8, label='Start')
ax2.plot(X_traj[-1], Y_traj[-1], 'rx', markersize=12, label='End')

# 【重要】アスペクト比を等しくする（地球が楕円にならないように）
ax2.set_aspect('equal', adjustable='box')

ax2.set_title('2. Trajectory in Earth-Centered Coordinates (True Scale View)')
ax2.set_xlabel('X Distance [km]')
ax2.set_ylabel('Y Distance [km]')
ax2.grid(True, linestyle=':')
ax2.legend(loc='upper right')

# 表示範囲の調整（軌道が見えるように自動調整した後、少しマージンを足す）
ax2.autoscale()
xlim = ax2.get_xlim()
ylim = ax2.get_ylim()
max_range = max(abs(xlim[0]), abs(xlim[1]), abs(ylim[0]), abs(ylim[1]))
margin = max_range * 0.1
ax2.set_xlim(-max_range - margin, max_range + margin)
ax2.set_ylim(-max_range - margin, max_range + margin)


plt.tight_layout() # レイアウト調整
plt.show()