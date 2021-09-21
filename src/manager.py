import requests
import settings
import json
from datetime import datetime


def get_production_count_by_time(start_time, end_time):
    """
    This function is used to get the production count for a given time according to the shifts.
    :param start_time:
    :param end_time:
    :return dict:
    """
    r = requests.get(url=settings.SAMPLE_JSON_1_URL)
    data = json.loads(r.text)
    start_time = datetime.fromisoformat(start_time[:-1])
    end_time = datetime.fromisoformat(end_time[:-1])
    shift_a_start = datetime.strptime(settings.SHIFT_TIMINGS["shiftA_start"], '%H::%M::%S').time()
    shift_a_end = datetime.strptime(settings.SHIFT_TIMINGS["shiftA_end"], '%H::%M::%S').time()
    shift_b_start = datetime.strptime(settings.SHIFT_TIMINGS["shiftB_start"], '%H::%M::%S').time()
    shift_b_end = datetime.strptime(settings.SHIFT_TIMINGS["shiftB_end"], '%H::%M::%S').time()
    output = {
                "shiftA":{
                    "production_A":0,
                    "production_B":0
                },
                "shiftB":{
                    "production_A":0,
                    "production_B":0
                },
                "shiftC":{
                    "production_A":0,
                    "production_B":0
                }
            }
    for record in data:
        record_datetime = datetime.fromisoformat(record["time"])
        if start_time <= record_datetime < end_time:
            actual_time = datetime.fromisoformat(record["time"]).time()
            if shift_a_start <= actual_time < shift_a_end:
                if record["production_A"]:
                    output["shiftA"]["production_A"] += 1
                if record["production_B"]:
                    output["shiftA"]["production_B"] += 1
            elif shift_b_start <= actual_time < shift_b_end:
                if record["production_A"]:
                    output["shiftB"]["production_A"] += 1
                if record["production_B"]:
                    output["shiftB"]["production_B"] += 1
            else:
                if record["production_A"]:
                    output["shiftC"]["production_A"] += 1
                if record["production_B"]:
                    output["shiftC"]["production_B"] += 1 

    # print(json.dumps(output, indent=4))
    return output

def get_machine_utilization(start_time, end_time):
    """
    This function is used to get machine utilization from given time period.
    :prarm start_time:
    :param end_time:
    :return dict:
    """
    max_runtime = 1021
    r = requests.get(url=settings.SAMPLE_JSON_2_URL)
    data = json.loads(r.text)
    total_runtime = 0
    total_downtime = 0
    start_time = datetime.fromisoformat(start_time[:-1])
    end_time = datetime.fromisoformat(end_time[:-1])
    for record in data:
        record_datetime = datetime.fromisoformat(record["time"])
        if start_time <= record_datetime < end_time:
            if record["runtime"] > max_runtime:
                total_runtime += max_runtime
                total_downtime += record["runtime"] - max_runtime
            else:
                total_runtime += record["runtime"]
            total_downtime += record["downtime"]
    utilization = total_runtime / (total_runtime + total_downtime) * 100
    # print(get_time_from_seconds(total_runtime))
    # print(get_time_from_seconds(total_downtime))
    # print(utilization)
    return {"runtime": total_runtime, "downtime": total_downtime, "utilization": utilization}


def get_average_value_for_unique_id(start_time, end_time):
    """
    This function is used to calculate the average of belts of every id in the given time interval.
    :param start_time:
    :param end_time:
    :return list:
    """
    r = requests.get(url=settings.SAMPLE_JSON_3_URL)
    data = json.loads(r.text)
    start_time = datetime.fromisoformat(start_time[:-1])
    end_time = datetime.fromisoformat(end_time[:-1])
    id_wise_data = {}
    # id_wise_data = defaultdict({"belt1": 0, "belt2": 0,"counter": 0})
    for record in data:
        record_datetime = datetime.fromisoformat(record["time"])
        if start_time <= record_datetime < end_time:
            if record["id"] not in id_wise_data:
                id_wise_data[record["id"]] = {
                    "belt1": 0,
                    "belt2": 0,
                    "counter": 0
                }
            if record["state"]:
                id_wise_data[record["id"]]["belt2"] += record["belt2"]
            else:
                id_wise_data[record["id"]]["belt1"] += record["belt1"]
            id_wise_data[record["id"]]["counter"] += 1
    output = []
    for id, data in id_wise_data.items():
        temp = {}
        temp["id"] = int(id[-1])
        temp["avg_belt1"] = data["belt1"] // data["counter"]
        temp["avg_belt2"] = data["belt2"] // data["counter"]
        output.append(temp)
    
    output = sorted(output, key = lambda i: i['id'])
    # print(json.dumps(output, indent=4))
    return output


def get_time_from_seconds(seconds):
    """
    This function is used to convert seconds into (hour, min, sec) time format
    :param seconds:
    :return time:
    """
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%dh:%02dm:%02ds" % (hour, min, sec)


# get_average_value_for_unique_id("2021-01-28T18:30:00z", "2021-01-28T20:10:00z")
# get_machine_utilization("2021-01-28T08:30:00z", "2021-01-28T10:30:00z")
# get_production_count_by_time("2021-01-28T07:30:00z", "2021-01-28T13:30:00z")