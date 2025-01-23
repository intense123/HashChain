from flask import Flask, render_template, request, jsonify
from hashchain import ServerController

app = Flask(__name__)

# Initialize the ServerController as a global variable
controller = ServerController(mod=145321, numberOfServer=3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/network-state')
def get_network_state():
    state = {
        'servers': list(controller.servers),
        'data': controller.dataStorage
    }
    return jsonify(state)

@app.route('/api/add-data', methods=['POST'])
def add_data():
    data = request.json.get('data')
    try:
        data = int(data)  # Convert to integer
        controller.insert_data(data)
        return jsonify({'success': True, 'message': f'Successfully added data: {data}'})
    except ValueError:
        return jsonify({'success': False, 'message': 'Data must be a valid integer'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/remove-data', methods=['POST'])
def remove_data():
    data = request.json.get('data')
    try:
        data = int(data)
        success = controller.delete_data(data)
        return jsonify({'success': success, 'message': 'Data deleted successfully' if success else 'Data not found'})
    except ValueError:
        return jsonify({'success': False, 'message': 'Data must be a valid integer'})

@app.route('/api/find-data', methods=['POST'])
def find_data():
    data = request.json.get('data')
    try:
        data = int(data)
        server = controller.get_server_by_data(data)
        return jsonify({
            'success': True,
            'found': server is not None,
            'server': server
        })
    except ValueError:
        return jsonify({'success': False, 'message': 'Data must be a valid integer'})

@app.route('/api/add-server', methods=['POST'])
def add_server():
    try:
        controller.insert_a_new_server()
        return jsonify({'success': True, 'message': 'New server added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/remove-server', methods=['POST'])
def remove_server():
    server_index = request.json.get('serverIndex')
    try:
        result = controller.delete_a_server(server_index)
        if isinstance(result, dict) and result['success']:
            return jsonify({
                'success': True,
                'message': 'Server removed successfully',
                'deleted_server': result['deleted_server'],
                'data_movement': result['data_movement']
            })
        return jsonify({
            'success': False,
            'message': 'Invalid server index'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 