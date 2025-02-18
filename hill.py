# -*- coding: utf-8 -*-
"""Hill.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1c9taqriFdZDOufxGJhZcmVDS_f2AsIaw
"""

from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

def encrypt(text, key):
    text = text.upper().replace(" ", "")
    while len(text) % 2 != 0:
        text += 'X'  # Padding if text length is not even

    key_matrix = np.array(key)
    if key_matrix.shape != (2, 2):
        return "Invalid Key Matrix! Must be 2x2."

    text_vector = [[ord(text[i]) - 65, ord(text[i + 1]) - 65] for i in range(0, len(text), 2)]
    encrypted_text = ""

    for pair in text_vector:
        result = np.dot(key_matrix, pair) % 26
        encrypted_text += chr(result[0] + 65) + chr(result[1] + 65)

    return encrypted_text

@app.route("/", methods=["GET", "POST"])
def home():
    encrypted_message = ""
    if request.method == "POST":
        text = request.form["text"]
        try:
            key = [[int(request.form["k11"]), int(request.form["k12"])],
                   [int(request.form["k21"]), int(request.form["k22"])]]
            encrypted_message = encrypt(text, key)
        except ValueError:
            encrypted_message = "Invalid input! Enter numeric values for the key."

    return render_template("index.html", encrypted_message=encrypted_message)

if __name__ == "__main__":
    app.run(debug=True)