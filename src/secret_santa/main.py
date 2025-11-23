import json
import os
import random

from flask import Flask, request

app = Flask(__name__)


def check(players):
    for player in players:
        if (
            "target" not in player
            or player["target"] in player["invalid"]
            or player["target"] == player["name"]
        ):
            return False

    return True


def init(input, output):
    conf = open(input).read()
    players = json.loads(conf)

    while not check(players):
        remaining = [x["name"] for x in players]
        for player in players:
            player["target"] = random.choice(remaining)
            remaining.remove(player["target"])

    open(output, "w").write(json.dumps({p["name"]: p["target"] for p in players}))


if __name__ == "__main__":
    app_token = os.getenv("TOKEN", "")
    port = os.getenv("PORT", "3000")
    conf_path = os.getenv("CONFIG_PATH", "./config.json")
    output_path = os.getenv("OUTPUT_PATH", "/tmp/secret-santa-result.json")

    players = init(conf_path, output_path)

    @app.route("/")
    def get():
        name = request.args.get("user_name")
        token = request.args.get("token")
        if app_token != "" and token != app_token:
            return "<p>Error: Invalid token</p>"

        if name == "raphou":
            return f"<p>Hello {name}!<br/>Your secret santa target is {players[name]}<br/>Eva's secret santa target is {players['eva']}</p>"
        if name in players:
            return (
                f"<p>Hello {name}!<br/>Your secret santa target is {players[name]}</p>"
            )
        else:
            return f"<p>Error: Player {name} not found"

    app.run(host="0.0.0.0", port=port)
