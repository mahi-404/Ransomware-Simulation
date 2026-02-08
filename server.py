from flask import Flask, render_template, jsonify
import subprocess
import os
import sys

app = Flask(__name__)

# Global variable to keep track of the simulation process
simulation_process = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run-simulation', methods=['POST'])
def run_simulation():
    global simulation_process
    
    try:
        # Check if a process is already running
        if simulation_process is not None:
            # Check if it's still active
            if simulation_process.poll() is None:
                return jsonify({'status': 'error', 'message': 'Simulation is already running'}), 409

        # Get the path to the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, 'rans.py')
        
        # Run the script in a new process using the same python interpreter
        simulation_process = subprocess.Popen([sys.executable, script_path], cwd=current_dir)
        
        return jsonify({'status': 'success', 'message': 'Simulation started'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
