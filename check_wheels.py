import os

new_wheels_dir = "./env/Wheels/"
manifest = "wheels.txt"

missing_wheels = []
conflicting_wheels = []
wheels_list = sorted(os.listdir(new_wheels_dir))

for wheel in wheels_list:
    wheel_name = wheel.split('-')[0]
    with open(manifest, "r") as file:
        if wheel_name in file.read():
            conflicting_wheels.append(wheel_name)
        else:
            missing_wheels.append(wheel_name)


if len(conflicting_wheels) > 0:
    print(conflicting_wheels)
    print(missing_wheels)
else:
    print("All new wheels can be safely merged!")