from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import google.generativeai as genai
import os
import time

app = Flask(__name__)
API_KEY = ""  # Replace with your actual Gemini API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

founders_df = None
investors_df = None

def load_csv(file, type_):
    global founders_df, investors_df
    if type_ == 'founders':
        founders_df = pd.read_csv(file)
    elif type_ == 'investors':
        investors_df = pd.read_csv(file)

def calculate_match_score(founder_id):
    founder_info = founders_df[founders_df['id'] == founder_id].iloc[0].to_dict()
    investors_info = [row.to_dict() for _, row in investors_df.iterrows()]
    matches = []
    
    for investor in investors_info:
        prompt = f"""
        Task: Analyze compatibility between a startup founder and an investor.
        Founder Industry: {founder_info.get('industry', 'N/A')}, Stage: {founder_info.get('startup_stage', 'N/A')}
        Investor Preferred Industry: {investor.get('preferred_industry', 'N/A')}, Stage: {investor.get('preferred_stage', 'N/A')}
        Match Score: """
        
        try:
            response = model.generate_content(prompt)
            score = int(response.text.split("Match Score:")[1].strip()) if "Match Score:" in response.text else 50
        except:
            score = 0
        
        investor['match_score'] = score
        matches.append(investor)
        time.sleep(0.5)
    
    return sorted(matches, key=lambda x: x['match_score'], reverse=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    global founders_df, investors_df
    matches = []
    founder_id = request.form.get("founder_id")
    
    if request.method == 'POST':
        if 'founders' in request.files:
            load_csv(request.files['founders'], 'founders')
        if 'investors' in request.files:
            load_csv(request.files['investors'], 'investors')
        if founder_id:
            matches = calculate_match_score(int(founder_id))
    
    return render_template('index.html', 
                           founders=founders_df.to_dict('records') if founders_df is not None else [],
                           matches=matches)

if __name__ == '__main__':
    app.run(debug=True)
