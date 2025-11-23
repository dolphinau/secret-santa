import json
import random
import sys

from flask import Flask

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
    if len(sys.argv) == 4:
        conf_path = sys.argv[1]
        out_path = sys.argv[2]
        port = sys.argv[3]
    else:
        print("Error: need two args <input conf> <output file>")
        exit(1)

    try:
        players = json.loads(open(out_path).read())
    except FileNotFoundError:
        players = init(conf_path, out_path)

    @app.route("/<name>")
    def get(name):
        if name == "raphael":
            return f"<p>Hello {name}!<br/>Your secret santa target is {players[name]}<br/>Eva's secret santa target is {players['eva']}</p>"
        if name in players:
            return (
                f"<p>Hello {name}!<br/>Your secret santa target is {players[name]}</p>"
            )
        else:
            return f"<p>Error: Player {name} not found"

    app.run(host="0.0.0.0", port=port)
