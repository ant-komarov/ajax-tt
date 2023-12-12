def get_big_messages(file_name: str) -> list[list[str]]:
    with open(file_name, "r", encoding="utf-8") as file:
        content = file.readlines()

    info_lines = [line.split(">")[1].split(";") for line in content if "BIG" in line]
    return info_lines


def get_device_error_message(log_message: list) -> str:
    errors_codes = {
        1: "Battery device error",
        2: "Temperature device error",
        3: "Threshold central error",
    }

    s_p_1 = log_message[0]
    s_p_2 = log_message[1]

    status_string = s_p_1[:-1] + s_p_2

    splitted_status_string = [
        status_string[i : i + 2] for i in range(0, len(status_string), 2)
    ]
    binary_status_string = [
        bin(int(num)).lstrip("0b").zfill(8) for num in splitted_status_string
    ]

    err_code = 0
    for code_flag in binary_status_string:
        err_code += int(code_flag[4])

    device_error = errors_codes.get(err_code, "Unknown device error")

    return device_error


def print_big_messages_info(file_name: str) -> None:
    info_lines = get_big_messages(file_name)
    broken_sensors = {}
    good_sensors = {}

    for line in info_lines:
        if line[-2] == "DD" and line[2] not in broken_sensors:
            broken_sensors[line[2]] = [line[6], line[13]]
            if line[2] in good_sensors:
                del good_sensors[line[2]]
        if line[2] not in good_sensors and line[2] not in broken_sensors:
            good_sensors[line[2]] = 1
        elif line[2] in good_sensors and line[2] not in broken_sensors:
            good_sensors[line[2]] += 1

    all_sensors_count = len(good_sensors) + len(broken_sensors)

    print(
        f"All big massages: {all_sensors_count}\n"
        f"Successful big massages: {len(good_sensors)}\n"
        f"Failed big messages: {len(broken_sensors)}\n"
    )

    for sensor_id, statuses in broken_sensors.items():
        err_message = get_device_error_message(statuses)
        print(f"{sensor_id}: {err_message}")

    print("\nSuccess messages count:")
    for sensor_id, messages_count in good_sensors.items():
        print(f"{sensor_id}: {messages_count}")


if __name__ == "__main__":
    LOG_FILE = "app_2.log"
    print_big_messages_info(LOG_FILE)
