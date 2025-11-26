import os
import json
import logging
from datetime import datetime

from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.exceptions import ResourceNotFoundError

# ---------- CONFIG ----------
CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
TODO_CONTAINER = os.getenv("TODO_CONTAINER", "todo-data")
TODO_BLOB_NAME = "todos.json"

if not CONN_STR:
    raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING is not set. See .env.example.")

bsc = BlobServiceClient.from_connection_string(CONN_STR)
cc = bsc.get_container_client(TODO_CONTAINER)

# Ensure container exists
try:
    cc.create_container()
except Exception:
    # already exists or policy prevents recreation; ignore
    pass

app = Flask(__name__, template_folder="templates")


# ---------- HELPERS ----------
def _now_id() -> str:
    # simple unique-ish ID
    return datetime.utcnow().strftime("%Y%m%dT%H%M%S%f")


def load_todos():
    try:
        bc = cc.get_blob_client(TODO_BLOB_NAME)
        data = bc.download_blob().readall().decode("utf-8")
        todos = json.loads(data)
        if not isinstance(todos, list):
            return []
        return todos
    except ResourceNotFoundError:
        return []
    except Exception as e:
        logging.exception("Error loading todos: %s", e)
        return []


def save_todos(todos):
    bc = cc.get_blob_client(TODO_BLOB_NAME)
    data = json.dumps(todos, indent=2)
    bc.upload_blob(
        data.encode("utf-8"),
        overwrite=True,
        content_settings=ContentSettings(content_type="application/json"),
    )


# ---------- API ----------
@app.get("/api/todos")
def api_get_todos():
    todos = load_todos()
    return jsonify(ok=True, todos=todos)


@app.post("/api/todos")
def api_add_todo():
    body = request.get_json(silent=True) or {}
    text = (body.get("text") or "").strip()
    if not text:
        return jsonify(ok=False, error="text is required"), 400

    todos = load_todos()
    todo = {"id": _now_id(), "text": text, "done": False}
    todos.append(todo)
    save_todos(todos)
    return jsonify(ok=True, todo=todo), 201


@app.post("/api/todos/<todo_id>/toggle")
def api_toggle_todo(todo_id):
    todos = load_todos()
    changed = None
    for t in todos:
        if t.get("id") == todo_id:
            t["done"] = not bool(t.get("done"))
            changed = t
            break
    if not changed:
        return jsonify(ok=False, error="not found"), 404
    save_todos(todos)
    return jsonify(ok=True, todo=changed)


@app.delete("/api/todos/<todo_id>")
def api_delete_todo(todo_id):
    todos = load_todos()
    new_todos = [t for t in todos if t.get("id") != todo_id]
    if len(new_todos) == len(todos):
        return jsonify(ok=False, error="not found"), 404
    save_todos(new_todos)
    return jsonify(ok=True)


@app.get("/api/health")
def api_health():
    return jsonify(ok=True, status="healthy"), 200


# ---------- FRONTEND ----------
@app.get("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # For Docker / local: respect PORT env, default 8000
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
