from flask import Flask, render_template, request
import json

with open("sample_recipes.json", "r", encoding="utf-8") as f:
    foods = json.load(f)

app = Flask(__name__)


#foods = {
#    "치킨": {"고기", "튀김", "매운맛", "한국식"},
#    "양념치킨": {"고기", "튀김", "매운맛", "한국식", "달콤"},
 #   "된장찌개": {"찌개", "국물", "한국식", "구수한맛", "채소"},
 #   "순두부찌개": {"찌개", "국물", "매운맛", "한국식", "부드러운"},
  #  "김치찌개": {"찌개", "국물", "매운맛", "한국식", "부드러운"},
   # "피자": {"고기", "빵", "양식", "치즈", "기름진"},
    #"파스타": {"면", "양식", "기름진", "치즈"},
    #"비빔밥": {"밥", "한국식", "채소", "매운맛", "고기"},
    #"초밥": {"밥", "생선", "일식", "신선한"},
    #"떡볶이": {"떡", "매운맛", "간식", "한국식"},
#}

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
    for food in favorite_foods:
        user_tags |= get_tags(food, foods)

    scores = []
    for f in foods:
        if f["food"] in favorite_foods:
            continue
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
    return render_template("index.html", foods=[f["food"] for f in foods], recommendations=recommendations, selected_foods=selected_foods)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)