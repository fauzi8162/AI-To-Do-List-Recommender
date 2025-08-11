from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

GROQ_API_KEY = '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' #input valid apikey, this just sample
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    user_input = ""
    error_msg = None

    if request.method == 'POST':
        user_input = request.form.get('description', '').strip()
        if user_input:
            prompt = (
                "Berikan daftar rekomendasi kegiatan singkat dalam format JSON array, "
                "untuk seseorang dengan deskripsi berikut:\n\n"
                f"{user_input}\n\n"
                "Berikan Format JSON Array saja, tanpa ada text pembuka maupun penutup, contoh hasil yang diharapkan:\n"
                "[\"Kegiatan 1\", \"Kegiatan 2\", ...]"
            )

            headers = {
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            }
            payload = {
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            try:
                resp = requests.post(GROQ_API_URL, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data['choices'][0]['message']['content']
                    try:
                        # Parsing JSON dari respons AI
                        recommendations = json.loads(content)
                        if not isinstance(recommendations, list):
                            raise ValueError("Response bukan list")
                    except Exception as e:
                        error_msg = content
                        #error_msg = "Gagal parsing respon AI: " + str(e) + content
                        recommendations = []
                else:
                    error_msg = f"Error API: {resp.status_code} - {resp.text}"
            except Exception as e:
                error_msg = "Request gagal: " + str(e)

    return render_template('index.html', 
                           recommendations=recommendations, 
                           user_input=user_input,
                           error_msg=error_msg)

if __name__ == '__main__':
    app.run(debug=True)
