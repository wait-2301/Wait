from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import services.queue_service as queue_service

app = Flask(__name__)

queue = []
admission_count = 5  # Example: 5 admissions available

@app.route('/')
def index():
    return render_template('index.html', queue=queue)

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    purpose = request.form.get('purpose')
    if name and purpose:
        queue.append({
            'id': len(queue) + 1,
            'name': name,
            'purpose': purpose,
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'admission': None
        })
        for admission in range(1, admission_count + 1):
            if not any(q['admission'] == admission for q in queue):
                queue[-1]['admission'] = admission
                break
    return redirect(url_for('index'))

@app.route('/queue', methods=['GET'])
def get_all_queue():
    queue_data = queue_service.get_all_queue_service()
    serialized_queues = [queue.to_dict() for queue in queue_data]
    return jsonify(serialized_queues)


if __name__ == "__main__":
    app.run(debug=True)
