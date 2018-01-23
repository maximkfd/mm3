import math
import matplotlib.pyplot as plt
import numpy
from mpl_toolkits.mplot3d import Axes3D

# параметры
engine_forces = [1, 1, 1, 10]  # подъёмные силы, производимые каждым двигателем в Ньютонах
STOP = 1000  # время моделирования в мс
m = 1  # kg
g = 10
mg = m * g  # вес квадрокоптера в Ньютонах
length = 0.1  # длина лап квадрокоптера в метрах

pitch_radial_velocity = 0
pitch_radial_position = 0
pitch_accel = 0
roll_radial_velocity = 0
roll_radial_position = 0
roll_accel = 0

yaw_accel = 0
pi_4 = math.pi / 4
engine_angles = [pi_4, 2 * pi_4, 3 * pi_4, 4 * pi_4]
ef = engine_forces
proection_coeff = math.sqrt(2)
# t = 0
dt = 0.001
x = [0.0]
y = [0.0]
z = [0.0]
yaw = [0.0]
roll = [0.0]
pitch = [0.0]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for t in range(STOP):
    # position
    # x
    angle = roll_radial_position
    summ = ef[0] + ef[1] + ef[2] + ef[3]
    summ = math.sin(angle) * summ * math.cos(pitch_radial_position)
    accel = summ / m
    vel = accel * dt
    x.append(x[t] + vel * dt)
    # y
    angle = pitch_radial_position
    summ = ef[0] + ef[1] + ef[2] + ef[3]
    summ = math.sin(angle) * summ * math.cos(roll_radial_position)
    accel = summ / m
    vel = accel * dt
    y.append(y[t] + vel * dt)
    # z
    summ = ef[0] + ef[1] + ef[2] + ef[3]
    summ = math.cos(roll_radial_position) * summ * math.cos(pitch_radial_position)
    accel = (summ - mg) / m
    vel = accel * dt
    z.append(z[t] + vel * dt)
    # рысканье
    if engine_forces[0] + engine_forces[2] != engine_forces[1] + engine_forces[3]:
        yaw_accel = engine_forces[0] + engine_forces[2] - engine_forces[1] + engine_forces[3]
        yaw_accel /= length
        yaw_velocity = yaw_accel * dt
        yaw.append(yaw[t] + yaw_velocity * dt)
    # тангаж + крен
    roll_accel = sum([math.sin(engine_angles[i])*ef[i] for i in range(4)])/length
    roll_accel /= length
    pitch_accel = sum([math.cos(engine_angles[i])*ef[i] for i in range(4)])/length
    pitch_accel *= 2 / length
    roll_radial_velocity += roll_accel * dt
    pitch_radial_velocity += pitch_accel * dt
    roll.append(roll[t] + roll_radial_velocity * dt)
    pitch.append(pitch[t] + pitch_radial_velocity * dt)
    roll_radial_position += roll_radial_velocity * dt
    pitch_radial_position += pitch_radial_velocity * dt
    print("pitch", pitch_radial_position)
    print("roll", roll_radial_position)
    print("yaw", yaw[t])
    for i in engine_angles:
        i += yaw[t+1]
xt = []
for i in range(STOP + 1):
    xt.append(i)
ax.plot(x, y, z)
plt.figure()
plt.title("yaw (angle/time)")
plt.plot(xt, yaw)
plt.figure()
plt.title("roll (angle/time)")
plt.plot(xt, roll)
plt.figure()
plt.title("pitch (angle/time)")
plt.plot(xt, pitch)
plt.show()
