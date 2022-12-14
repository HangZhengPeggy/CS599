import airsim
import time

client = airsim.MultirotorClient()
client.confirmConnection()
for i in range(1, 4):
    name = "Drone" + str(i)
    client.enableApiControl(True, vehicle_name=name)
    client.armDisarm(True, vehicle_name=name)

for i in range(1, 4):
    name = "Drone" + str(i)
    if(i != 3):
        client.takeoffAsync(vehicle_name=name)
    else:
        client.takeoffAsync(vehicle_name=name).join()
time.sleep(2)

for i in range(3, 0, -1):
    name = "Drone" + str(i)
    client.moveToPositionAsync(-1.8, -3.2, -6, 4, vehicle_name=name).join()
time.sleep(10)

# for i in range(3, 0, -1):
#     name = "Drone" + str(i)
#     client.moveToPositionAsync(-1.8, -1.7 + (i - 1)  * -1.5, -4 + (i - 1)  * -2, 4, vehicle_name=name).join()
# time.sleep(10)

# for i in range(1, 4):
#     name = "Drone" + str(i)
#     client.moveToPositionAsync(0, 1.5 + (i - 1) * 1.5, 0, 4, vehicle_name=name).join()
# time.sleep(10)

# # take images
# responses = client.simGetImages([
#     airsim.ImageRequest("0", airsim.ImageType.DepthVis),
#     airsim.ImageRequest("1", airsim.ImageType.DepthPlanar, True)])
# print('Retrieved images: %d', len(responses))
#
# # do something with the images
# for response in responses:
#     if response.pixels_as_float:
#         print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
#         airsim.write_pfm(os.path.normpath('/temp/py1.pfm'), airsim.get_pfm_array(response))
#     else:
#         print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
#         airsim.write_file(os.path.normpath('/temp/py1.png'), response.image_data_uint8)
