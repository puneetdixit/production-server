from flask import Flask, request, render_template
import src.manager as manager
import settings

app = Flask(__name__)

@app.route('/')
def index():
    return {"message": "Server is running"}


@app.route('/docs', methods=['GET'])
def get_docs():
    return render_template('swaggerui.html')


@app.route('/get_producation_count', methods=['GET'])
def get_producation_count():
    """
    This is the view funtion to get the production count according to shift and given time interval.
    :return:
    """
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not start_time or not end_time:
        return {"status": "failure", "message": "start_time or end_time not provided"}
    return {"status": "success", "data": manager.get_production_count_by_time(start_time, end_time)}
    

@app.route('/get_machine_utilization', methods=['GET'])
def get_machine_utilization():
    """
    This is the view funtion to get the production count according to shift and given time interval.
    :return:
    """
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not start_time or not end_time:
        return {"status": "failure", "message": "start_time or end_time not provided"}
    return {"status": "success", "data": manager.get_machine_utilization(start_time, end_time)}


@app.route('/get_average_value', methods=['GET'])
def get_average_value():
    """
    This is the view funtion to get the average value of both belt (belt1 and belt2) in given time interval.
    :return:
    """
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not start_time or not end_time:
        return {"status": "failure", "message": "start_time or end_time not provided"}
    return {"status": "success", "data": manager.get_average_value_for_unique_id(start_time, end_time)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=settings.SERVER_PORT, debug=False)
    