from flask import Flask, render_template, request
from scraper import get_recommendations

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form.get('query')
        recommendations = get_recommendations(query)
        return render_template("result.html", recommendations=recommendations)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)

