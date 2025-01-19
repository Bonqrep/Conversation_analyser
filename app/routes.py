import ast
import json
from config import Config
from flask import (Flask, Response, jsonify, redirect, render_template, request,
                   send_from_directory, url_for, send_file, make_response, session, url_for, flash, Blueprint)
import os
from app import app
from flask import redirect, render_template, url_for
import whisper
from openai import OpenAI
import tempfile

app = Blueprint('app', __name__)

import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = whisper.load_model("base", device="cpu")

base_dir = os.path.dirname(os.path.abspath(__file__))

@app.route("/", methods=["GET"])
def default():
    return redirect(url_for('app.home'))

@app.route("/home", methods=["GET"])
def home():
    message = request.args.get('message')
    return render_template("home.html", title="Conversation Analyser", dark_mode=0, message = message)

@app.route("/home", methods=["POST"])
def home_post():
    if 'file' not in request.files:
        return render_template("home.html", title="Conversation Analyser", dark_mode=0, message="No file part")

    file = request.files['file']

    if file.filename == '':
        return render_template("home.html", title="Conversation Analyser", dark_mode=0, message="No selected file")

    if file and file.filename.endswith('.mp3'):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            file_path = temp_file.name
            file.save(file_path)

        try:

            print(f"Temporary file path: {file_path}")
            print(f"File exists: {os.path.exists(file_path)}")

            result = model.transcribe(file_path, verbose=True)
            transcription = result['text']
            segments = result['segments']
            
            diarized_text = "\n".join([
                f"[{segment['start']:.2f}-{segment['end']:.2f}] {segment['text']}"
                for segment in segments
            ])
            print(diarized_text)

            prompt = f"przeanalizuj dokładnie poniższą rozmowę klienta banku z doradcą. Przygotuj raport z rozmowy który bedzie podzielony na 4 sekcje. 1. Streszczenie rozmowy - w kilku zdaniach przedstaw przegieg i najważniejsze treści z rozmowy. 2. Ryzyka - jakie można wywnioskować z rozmowy. Czyli jaki aspekt rozmowy może sugerować że jakieś zachowanie lub sytuacja może przynieść negatywne skutki w przyszłości w relacji klient-bank. 3. Uwagi- czyli jakie sugestie zmiany zachowania lub wprowadzenie dodatkowych zachowań w rozmowie powinny zostać uwzględnione aby rozmowa przegiegała lepiej, aby klient czuł się bardziej komfortowo i zaopiekowany oraz aby wyeliminować niepozytywne apekty. 4. Podsumowanie - czyli zestawienie wszystkich najważniejszych informacji z rozmowy, podsumowanie wcześniejszych aspektów i zestawienie ich w spójnym podsumowaniu. Opowiedz przygotuj w formacie json o kluczach: 'Streszczenie', 'Ryzyka', 'Uwagi', 'Podsumowanie'. Nie dodawaj innych kluczy z będnych opisów formatu. \n\n Rozmowa:{diarized_text}"

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Jesteś przełożonym doradcy w banku. Musisz kontrolować jego prace i to w jaki sposób prowadzi rozmowe. Sprawdzasz czy rozmowa spełnia wysokie standardy kultury oraz czy jest korzystna dla banku."},
                    {"role": "user", "content": prompt}
                ],
                temperature = 0.3,
                max_tokens = 5000
            )
            
            openai_response = response.choices[0].message.content.strip()
            print(openai_response)

            os.remove(file_path)

            if isinstance(openai_response, str):
                opening = openai_response.find("{")
                closing = openai_response.rfind("}")

                response_string = openai_response[opening:closing +1]
                response_dict = ast.literal_eval(response_string)


            analyse = {
                "diarized_text": diarized_text,
                "Streszczenie": response_dict["Streszczenie"],
                "Ryzyka": response_dict["Ryzyka"],
                "Uwagi": response_dict["Uwagi"],
                "Podsumowanie": response_dict["Podsumowanie"]
            }

        except Exception as e:
            os.remove(file_path)
            return  render_template("home.html", title="Conversation Analyser", dark_mode=0, message=f"An error occurred: {str(e)}")

    else:
        return render_template("home.html", title="Conversation Analyser", dark_mode=0, message="Invalid file type. Please upload an MP3 file.")
    
    return render_template("analyse.html", title="Conversation Analyser", dark_mode=0, analyse=analyse)

@app.route("/analyse", methods=["GET"])
def analyse():

    return render_template("analyse.html", title="Conversation Analyser", dark_mode=0)