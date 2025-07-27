from flask import Flask, render_template, request
import json
import random

with open("sample_recipes.json", "r", encoding="utf-8") as f:
    foods = json.load(f)

app = Flask(__name__)

NUM_RANDOM_OPTIONS = 5

def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

def get_tags(food_name, foods):
    for f in foods:
        if f["food"] == food_name:
            print(f"[get_tags] 찾음: {food_name} → 태그: {f['tags']}")
            return set(f["tags"])
    return set()

def recommend_foods(favorite_foods, foods, top_n=5):
    user_tags = set()
    for food in favorite_foods:
        user_tags |= get_tags(food, foods)

    scores = []
    for f in foods:
        if f["food"] in favorite_foods:
            continue

        print(f"[비교 대상] {f['food']} 태그: {f['tags']}")
        print("교집합:", user_tags & set(f["tags"]))
        print("유사도:", jaccard_similarity(user_tags, set(f["tags"])))
        print("선택한 항목: ", user_tags )
        score = jaccard_similarity(user_tags, set(f["tags"]))
       
        scores.append((f["food"], score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations=[]
    selected_foods=[]

    if request.method =="POST":
        selected_foods = request.form.getlist("foods")
        recommendations = recommend_foods(selected_foods, foods)
        displayed_foods =  [f for f in foods if f["food"] in selected_foods]   
    else:
        #GET
        displayed_foods = random.sample(foods, NUM_RANDOM_OPTIONS)
    
    return render_template("index.html", foods=displayed_foods, recommendations=recommendations, selected_foods=selected_foods)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)