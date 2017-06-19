from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from imageRetriever import image_retrieval

# from KeyPhrasesNew import listToFront, d, courses_list

app = Flask(__name__)
CORS(app)

@app.route('/NLQAS/api/answers', methods=['GET'])
def get_answers():
    return jsonify({'answers': image_retrieval("what is a database?")})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/NLQAS/api/question', methods=['POST'])
def post_question():
    if not request.json:
        exit()

    # question = request.json.get('question', "")
    query_sentence = request.json['question']
    print(query_sentence)
    answers_dictionary = image_retrieval(query_sentence)
    answers = list(answers_dictionary.keys())
    images = list(answers_dictionary.values())
    print(answers)
    print(images)
    return jsonify({
        'answers': answers,
        'images': images
    }, 201)

# @app.after_request()

if __name__ == '__main__':
    app.run(debug=True)