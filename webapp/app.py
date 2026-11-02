"""A very small web application built with Flask.

Endpoints:
  /          -> HTML page with region, availability zone and instance id
  /api/info  -> the same information as JSON
  /health    -> "OK", used by the load balancer to check that the app is alive
"""

from flask import Flask, jsonify

from common.ec2_metadata import get_instance_info

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Where am I running?</title>
  <style>
    body {{ font-family: "Segoe UI", Arial, sans-serif; background: #f4f6f8;
           color: #1f2937; margin: 0; padding: 40px 16px; }}
    .card {{ max-width: 520px; margin: 0 auto; background: #fff; border-radius: 10px;
             padding: 24px 28px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }}
    h1 {{ margin-top: 0; color: #232f3e; font-size: 1.5rem; }}
    .label {{ color: #6b7280; font-size: 0.9rem; margin-top: 16px; }}
    .value {{ font-size: 1.3rem; font-weight: 600; color: #ff9900; }}
    p.hint {{ color: #6b7280; font-size: 0.85rem; margin-top: 24px; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Where am I running?</h1>
    <div class="label">Region</div>
    <div class="value">{region}</div>
    <div class="label">Availability Zone</div>
    <div class="value">{availability_zone}</div>
    <div class="label">Instance ID</div>
    <div class="value">{instance_id}</div>
    <p class="hint">Refresh the page: behind a load balancer the zone may change.</p>
  </div>
</body>
</html>
"""


@app.route("/")
def index():
    return PAGE.format(**get_instance_info())


@app.route("/api/info")
def api_info():
    return jsonify(get_instance_info())


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    # Only for testing on your own computer: python -m webapp.app
    app.run(host="0.0.0.0", port=8080)
