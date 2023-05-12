from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.form['message']
    # ここでAIモデルやNLPライブラリを使ってレスポンスを作ることが可能です。
    # 現在はエコーボットとして、受け取ったメッセージをそのまま返します。
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)