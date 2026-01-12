from flask import Flask, request, render_template_string
import os
from google import genai

app = Flask(__name__)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

HTML = """
<!doctype html>
<html>
<head>
  <title>Gemini Chat</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f5f5f5;
      padding: 20px;
      font-size: 18px;
    }
    h2 {
      font-size: 26px;
    }
    input {
      width: 100%;
      padding: 12px;
      font-size: 18px;
      margin-top: 10px;
    }
    button {
      margin-top: 10px;
      padding: 12px;
      font-size: 18px;
      width: 100%;
      cursor: pointer;
    }
    .response {
      margin-top: 20px;
      padding: 15px;
      background: white;
      border-radius: 5px;
      font-size: 18px;
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <h2>dev's ai model</h2>

  <form method="post">
    <input name="prompt" placeholder="Type your message here" required>
    <button type="submit">Send</button>
  </form>

  {% if reply %}
    <div class="response">
      <b>Response:</b><br><br>
      {{ reply }}
    </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chat():
    reply = ""
    if request.method == "POST":
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.form["prompt"]
        )
        reply = response.text
    return render_template_string(HTML, reply=reply)

app.run(host="0.0.0.0", port=3000)