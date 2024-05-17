from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

points = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_point', methods=['POST'])
def add_point():
    global points
    data = request.get_json()
    points.append(data)
    print("Added point:", data)  # Debug log
    return jsonify(points)

@app.route('/delete_point', methods=['POST'])
def delete_point():
    global points
    data = request.get_json()
    if data in points:
        points.remove(data)
    print("Deleted point:", data)  # Debug log
    return jsonify(points)

@app.route('/get_points', methods=['GET'])
def get_points():
    return jsonify(points)

@app.route('/execute', methods=['POST'])
def execute():
    global points
    # 处理逻辑
    result = {"status": "success", "message": "Execution started."}
    print("Execution started with points:", points)  # Debug log
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)