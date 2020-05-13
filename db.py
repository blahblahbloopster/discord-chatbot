import json


def add_user(user: str):
    current = load()
    current[user] = {"points": 0, "rank": 0}
    save(current)


def upgrade_user(user: str, field: str, value):
    current = load()
    current[user][field] = value


def get_rank(user: str) -> int:
    current = load()
    return current[user]["rank"]


def set_rank(user: str, rank: int):
    current = load()
    current[user]["rank"] = rank
    save(current)


def add_points(user: str, points: int) -> int:
    current = load()
    current[user]["points"] += points
    save(current)
    return current[user]["points"]


def get_points(user: str) -> int:
    return load()[user]["points"]


def load() -> dict:
    with open("users.json") as f:
        output = json.loads(f.read())
    return output


def save(new_data: dict):
    with open("users.json", "wt") as f:
        f.write(json.dumps(new_data))
