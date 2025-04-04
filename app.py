from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    folder = data.get("folder_name", "downloads")
    filename = data.get("file_name", "video")
    url = data.get("video_url")

    if not url:
        return jsonify({"error": "Missing video_url"}), 400

    cmd = f"yt-dlp -o '{folder}/{filename}.mp4' -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' '{url}'"
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        return jsonify({"success": True, "message": "Download started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)  # Railway uses port 3000
