import airsim
import time
import pandas as pd
import math

def printStatus(df):
    list = []
    # rotor_thrust:
    list.append(client.getRotorStates().rotors[0]['thrust'])
    list.append(client.getRotorStates().rotors[1]['thrust'])
    list.append(client.getRotorStates().rotors[2]['thrust'])
    list.append(client.getRotorStates().rotors[3]['thrust'])

    # rotor_speed
    list.append(client.getRotorStates().rotors[0]['speed'])
    list.append(client.getRotorStates().rotors[1]['speed'])
    list.append(client.getRotorStates().rotors[2]['speed'])
    list.append(client.getRotorStates().rotors[3]['speed'])

    # angular_acceleration:
    angular_acceleration_x = client.simGetGroundTruthKinematics().angular_acceleration.x_val
    angular_acceleration_y = client.simGetGroundTruthKinematics().angular_acceleration.y_val
    angular_acceleration_z = client.simGetGroundTruthKinematics().angular_acceleration.z_val
    angular_acceleration = math.sqrt(angular_acceleration_x * angular_acceleration_x + angular_acceleration_y * angular_acceleration_y + angular_acceleration_z * angular_acceleration_z)
    list.append(angular_acceleration)

    # angular_velocity:
    angular_velocity_x = client.simGetGroundTruthKinematics().angular_velocity.x_val
    angular_velocity_y = client.simGetGroundTruthKinematics().angular_velocity.y_val
    angular_velocity_z = client.simGetGroundTruthKinematics().angular_velocity.z_val
    angular_velocity = math.sqrt(angular_velocity_x * angular_velocity_x + angular_velocity_y * angular_velocity_y + angular_velocity_z * angular_velocity_z)
    list.append(angular_velocity)

    # linear_acceleration:
    linear_acceleration_x = client.simGetGroundTruthKinematics().linear_acceleration.x_val
    linear_acceleration_y = client.simGetGroundTruthKinematics().linear_acceleration.y_val
    linear_acceleration_z = client.simGetGroundTruthKinematics().linear_acceleration.z_val
    linear_acceleration = math.sqrt(
        linear_acceleration_x * linear_acceleration_x + linear_acceleration_y * linear_acceleration_y + linear_acceleration_z * linear_acceleration_z)
    list.append(linear_acceleration)

    # linear_velocity:
    linear_velocity_x = client.simGetGroundTruthKinematics().linear_velocity.x_val
    linear_velocity_y = client.simGetGroundTruthKinematics().linear_velocity.y_val
    linear_velocity_z = client.simGetGroundTruthKinematics().linear_velocity.z_val
    linear_velocity = math.sqrt(
        linear_velocity_x * linear_velocity_x + linear_velocity_y * linear_velocity_y + linear_velocity_z * linear_velocity_z)
    list.append(linear_velocity)

    # position
    list.append(client.simGetGroundTruthKinematics().position.x_val)
    list.append(client.simGetGroundTruthKinematics().position.y_val)
    list.append(client.simGetGroundTruthKinematics().position.z_val)

    # Orientation: pitch, roll, yaw
    orientation = airsim.to_eularian_angles(client.simGetGroundTruthKinematics().orientation)
    list.append(orientation[0])
    list.append(orientation[1])
    list.append(orientation[2])
    df.loc[len(df)] = list


df = pd.DataFrame(columns=['rotor_thrust_1', 'rotor_thrust_2', 'rotor_thrust_3', 'rotor_thrust_4',
                           'rotor_speed_1', 'rotor_speed_2', 'rotor_speed_3', 'rotor_speed_4',
                           'angular_acceleration', 'angular_velocity', 'linear_acceleration', 'linear_velocity',
                           'position_x', 'position_y', 'position_z',
                           'orientation_pitch', 'orientation_roll', 'orientation_yaw'])


# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Async methods returns Future. Call join() to wait for task to complete.
client.takeoffAsync().join()

client.moveToPositionAsync(0, -2, -8, 1).join()
client.moveToPositionAsync(0, -2, -1, 1).join()
client.hoverAsync().join()
time.sleep(2)

for i in range(12):
    j = -1 + (-0.1) * (i + 1)
    client.moveToPositionAsync(0, -2, j, 8).join()
    printStatus(df)


df.to_csv("result_v8.csv")