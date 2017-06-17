from flask import Flask, request, make_response, jsonify
from patternRecognizer import filtered_answers

app = Flask(__name__)

@app.route('/NLQAS/api/answers', methods=['GET'])
def get_answers():
    return jsonify({'answers': filtered_answers})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/NLQAS/api/question', methods=['POST'])
def post_question():
    if not request.json:
        exit()
    question = {
        'question': request.json.get('question', "")
    }
    # questions.append(question)
    return jsonify({'question': question}), 201

if __name__ == '__main__':
    app.run(debug=True)