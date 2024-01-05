from flask import Flask
from model import trianing_first, get_search_result
app = Flask(__name__)
news_directory = r'C:\Users\hp\Downloads\archive\Viswa\Viswa/'

trianing_first(news_directory)

@app.route("/members")
def members():
    return{"members": ["Member1", "Member2"]}

@app.route("/search")
def search_result():
    query ="एमाओवादी रूपान्तरणमा भारतीय चासो एमाओवादीले महाधिवेशनबाट औपचारिक रूपमै आफ्नो नीतिमा परिवर्तन ल्याएपछि त्यो रूपान्तरणलाई भारतभित्र निकै चाखपूर्वक हेरिएको छ  "
    return get_search_result(query)
if __name__=="__main__":
    app.run(debug=True)