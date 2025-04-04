from flask import Flask, request, jsonify
import subprocess
import os
from pathlib import Path

app = Flask(__name__)

# Configuration
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)  # Create downloads directory if it doesn't exist

@app.route('/download', methods=['POST'])
def download():
    # Get JSON data from request
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    url = data.get('video_url')
    if not url:
        return jsonify({"error": "Missing video_url parameter"}), 400

    try:
        # Sanitize filename and create output path
        filename = "downloaded_video.mp4"
        output_path = DOWNLOAD_DIR / filename
        
        # Build yt-dlp command
        cmd = [
            "yt-dlp",
            "-o", str(output_path),
            "-f", "best[ext=mp4]",
            "--no-check-certificate",  # Bypass SSL verification if needed
            url
        ]
        
        # Execute command
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Verify file was created
        if not output_path.exists():
            return jsonify({"error": "Download failed - no file created"}), 500
            
        return jsonify({
            "success": True,
            "file_path": str(output_path),
            "output": result.stdout
        })
        
    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Download failed",
            "details": e.stderr,
            "return_code": e.returncode
        }), 500
    except Exception as e:
        return jsonify({
            "error": "Server error",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)