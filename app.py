from flask import Flask, render_template, request, session, redirect, url_for
import json
import random
import os

with open("sample_recipes.json", "r", encoding="utf-8") as f:
    foods = json.load(f)

app = Flask(__name__)
app.secret_key = os.urandom(24)

NUM_RANDOM_OPTIONS = 5

def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

def get_tags(food_name, foods):
    for f in foods:
        
        if f["food"] == food_name:
            return set(f["tags"])
    return set()


def recommend_foods(favorite_foods, foods, top_n=5):
    user_tags = set()
    for food_name in favorite_foods:
        user_tags |= get_tags(food_name, foods)

    favorite_food_names = set(favorite_foods)

    scores = []
    for f in foods:
        if f["food"] in favorite_food_names:
            continue

        score = jaccard_similarity(user_tags, set(f["tags"]))
        scores.append((f["food"], score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]


@app.route("/", methods=["GET", "POST"])
def index():
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        selected = request.form.getlist("foods")
        session["history"] += selected  # 선택한 음식 누적
        # 중복 제거
        session["history"] = list(set(session["history"]))

        recommendations = recommend_foods(session["history"], foods)
        displayed_foods = random.sample(foods, NUM_RANDOM_OPTIONS)

    else:
        displayed_foods = random.sample(foods, NUM_RANDOM_OPTIONS)
        recommendations = []
        selected = []

    return render_template("index.html",
                           foods=displayed_foods,
                           recommendations=recommendations,
                           selected_foods=session.get("history", []))

@app.route("/reset", methods=["GET"])
def reset_session():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)