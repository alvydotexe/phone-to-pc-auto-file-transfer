from flask import Flask, render_template, request
import os


f = "/run/media/alvy/storage/phone"
os.makedirs(f, exist_ok=True)



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename:
            path = os.path.join(f, file.filename)
            file.save(path)
            return "File Uploaded"

        return "No file selected", 400

    return render_template("form.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
