# Founder-Investor Matching AI Model 🚀

## Overview
This project is an AI-powered **Founder-Investor Matching System** that helps startup founders find the most compatible investors based on industry, funding stage, and business model. Using **Google's Gemini API**, the model calculates a **match score** between founders and investors to rank the best investment opportunities.

## Features ✨
- **Gemini API Integration**: Uses LLM-based analysis for investor-founder compatibility.
- **Structured Matching Process**: Compares startup traits with investor preferences.
- **Match Score Calculation**: Returns a ranked list of investors based on compatibility.
- **Custom Dataset Creation**: Synthetic data generated for founders and investors.
- **CSV-Based Data Handling**: Loads and processes structured startup and investor data.

## How It Works ⚙️
1. **Load Startup & Investor Data** 📊  
   - Founders provide details like **industry, stage, funding required, traction, and business model**.  
   - Investors specify their **preferred industries, investment range, and key focus areas**.

2. **Match Score Calculation** 🎯  
   - A structured **prompt** is sent to Gemini API, analyzing alignment between founder & investor profiles.
   - The API returns a **compatibility score (0-100)** based on key factors.

3. **Ranked Output** 📈  
   - A sorted list of investors is generated, ranked by compatibility.
   - Displayed in a structured format.

## Dataset Creation 🏗️
Since no predefined dataset was available, I **generated synthetic data** for testing. The dataset consists of:

- **`founders.csv`** 🏢  
  - 5 startup founders with attributes like **industry, stage, funding required, traction, and business model**.
  
- **`investors.csv`** 💰  
  - 5 investors with preferences such as **preferred industries, investment range, key focus areas, and previous investments**.

**Example Data Snippet:**
```
Founder 1 | Industry: FinTech | Stage: Seed | Funding: $500K | Model: B2B SaaS
Investor 1 | Prefers: FinTech | Range: $100K-$500K | Stage: Seed
```

## Installation & Usage 🛠️
### 1️⃣ Install Dependencies
```bash
pip install pandas google-generativeai
```
### 2️⃣ Set Up API Key (Gemini API)
Replace `API_KEY` with your actual Gemini API key:
```python
API_KEY = "your_gemini_api_key_here"
```

### 3️⃣ Run the Matching Model
```python
matcher = FounderInvestorMatcher(API_KEY)
matcher.load_data('founders.csv', 'investors.csv')
matches = matcher.calculate_match_score(founder_id=1)
matcher.display_matches(matches)
```

## Output Format 📋
```
# Founder-Investor Matching AI Model 🚀

## Overview
This project is an AI-powered **Founder-Investor Matching System** that helps startup founders find the most compatible investors based on industry, funding stage, and business model. Using **Google's Gemini API**, the model calculates a **match score** between founders and investors to rank the best investment opportunities.

## Features ✨
- **Gemini API Integration**: Uses LLM-based analysis for investor-founder compatibility.
- **Structured Matching Process**: Compares startup traits with investor preferences.
- **Match Score Calculation**: Returns a ranked list of investors based on compatibility.
- **Custom Dataset Creation**: Synthetic data generated for founders and investors.
- **CSV-Based Data Handling**: Loads and processes structured startup and investor data.

## How It Works ⚙️
1. **Load Startup & Investor Data** 📊  
   - Founders provide details like **industry, stage, funding required, traction, and business model**.  
   - Investors specify their **preferred industries, investment range, and key focus areas**.

2. **Match Score Calculation** 🎯  
   - A structured **prompt** is sent to Gemini API, analyzing alignment between founder & investor profiles.
   - The API returns a **compatibility score (0-100)** based on key factors.

3. **Ranked Output** 📈  
   - A sorted list of investors is generated, ranked by compatibility.
   - Displayed in a structured format.

## Dataset Creation 🏗️
Since no predefined dataset was available, I **generated synthetic data** for testing. The dataset consists of:

- **`founders.csv`** 🏢  
  - 5 startup founders with attributes like **industry, stage, funding required, traction, and business model**.
  
- **`investors.csv`** 💰  
  - 5 investors with preferences such as **preferred industries, investment range, key focus areas, and previous investments**.

**Example Data Snippet:**
```
Founder 1 | Industry: FinTech | Stage: Seed | Funding: $500K | Model: B2B SaaS
Investor 1 | Prefers: FinTech | Range: $100K-$500K | Stage: Seed
```

## Installation & Usage 🛠️
### 1️⃣ Install Dependencies
```bash
pip install pandas google-generativeai
```
### 2️⃣ Set Up API Key (Gemini API)
Replace `API_KEY` with your actual Gemini API key:
```python
API_KEY = "your_gemini_api_key_here"
```

### 3️⃣ Run the Matching Model
```python
matcher = FounderInvestorMatcher(API_KEY)
matcher.load_data('founders.csv', 'investors.csv')
matches = matcher.calculate_match_score(founder_id=1)
matcher.display_matches(matches)
```

## Output Format 📋
```
=== FOUNDER-INVESTOR MATCHES ===

Rank  Investor             Industry             Stage           Match Score
----------------------------------------------------------------------
1     Investor 2           FinTech              Seed            65        
2     Investor 3           FinTech              Series B        35        
3     Investor 1           EdTech               Series B        30  

```







# Pitch Deck Analysis Tool

## Overview 🚀
This tool analyzes startup pitch decks by identifying key sections, scoring them based on quality metrics, and providing feedback on strengths and weaknesses. It leverages **BERT-based NLP** techniques along with traditional text preprocessing to ensure accurate evaluations.

## Features ✨
- **Preprocesses Pitch Deck Text**: Cleans and tokenizes text for analysis.
- **Identifies Key Sections**: Extracts `Problem`, `Solution`, `Market`, `Business Model`, `Financials`, and `Team` sections.
- **Scores Sections**: Evaluates sections based on predefined quality criteria.
- **Generates Overall Score**: Weighted scoring for a holistic pitch evaluation.
- **Provides Improvement Suggestions**: Highlights strengths and weaknesses with actionable feedback.
- **Includes Sample Pitches**: Five example pitch decks for testing.

## Installation 📦
```bash
pip install nltk torch transformers
```

## Setup 🛠️
Ensure required NLTK data is available:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Usage 🚀
### 1️⃣ Preprocess Text
```python
preprocessed_text = preprocess_text(raw_text)
```
### 2️⃣ Identify Sections
```python
sections, section_weights = identify_sections(preprocessed_text)
```
### 3️⃣ Score Sections
```python
scoring_model = PitchScoringModel()
overall_score, section_scores = scoring_model.calculate_overall_score(sections, section_weights)
```
### 4️⃣ Analyze Strengths & Weaknesses
```python
strengths, weaknesses, suggestions = analyze_strengths_weaknesses(section_scores)
```
### 5️⃣ Generate Sample Pitches
```python
sample_pitches = create_sample_pitches()
```

## Example Output 📊
```json
{
    "overall_score": 78.5,
    "section_scores": {
        "problem": 85,
        "solution": 90,
        "market": 72,
        "business_model": 60,
        "financials": 50,
        "team": 80
    },
    "strengths": ["problem", "solution", "team"],
    "weaknesses": ["financials", "business_model"],
    "suggestions": {
        "business_model": "Detail your revenue streams and pricing strategy.",
        "financials": "Provide clear revenue projections and funding requirements."
    }
}
```

## Output Format 📋
```
AI Pitch Analysis Model
==================================================

=== Analysis for EcoDelivery ===
Overall Score: 46.9/100

Section Scores:
- Problem: 46.9/100
- Solution: 46.9/100
- Market: 46.9/100
- Business Model: 46.9/100
- Financials: 46.9/100
- Team: 46.9/100

Strengths:
- No significant strengths identified

Weaknesses:
- Problem
- Solution
- Market
- Business Model
- Financials
- Team

Improvement Suggestions:
- Problem: Clearly define the problem and validate it with market research. Show the urgency and impact of the problem.
- Solution: Highlight your unique value proposition and how your solution addresses the problem. Emphasize innovation and feasibility.
- Market: Include market size (TAM, SAM, SOM), growth rate, and competitive analysis. Define your target audience more precisely.
- Business Model: Detail your revenue streams, pricing strategy, and path to profitability. Explain your go-to-market approach.
- Financials: Provide realistic projections with clear assumptions. Include key metrics and funding requirements.
- Team: Highlight relevant experience, skills, and achievements of key team members. Consider adding advisors if needed.
==================================================

=== Analysis for MediTrack ===
Overall Score: 45.7/100

Section Scores:
- Problem: 45.8/100
- Solution: 45.8/100
- Market: 45.8/100
- Business Model: 45.8/100
- Financials: 45.8/100
- Team: 45.8/100

Strengths:
- No significant strengths identified

Weaknesses:
- Problem
- Solution
- Market
- Business Model
- Financials
- Team

Improvement Suggestions:
- Problem: Clearly define the problem and validate it with market research. Show the urgency and impact of the problem.
- Solution: Highlight your unique value proposition and how your solution addresses the problem. Emphasize innovation and feasibility.
- Market: Include market size (TAM, SAM, SOM), growth rate, and competitive analysis. Define your target audience more precisely.
- Business Model: Detail your revenue streams, pricing strategy, and path to profitability. Explain your go-to-market approach.
- Financials: Provide realistic projections with clear assumptions. Include key metrics and funding requirements.
- Team: Highlight relevant experience, skills, and achievements of key team members. Consider adding advisors if needed.
==================================================

=== Analysis for FarmAI ===
Overall Score: 44.4/100

Section Scores:
- Problem: 44.4/100
- Solution: 44.4/100
- Market: 44.4/100
- Business Model: 44.4/100
- Financials: 44.4/100
- Team: 44.4/100

Strengths:
- No significant strengths identified

Weaknesses:
- Problem
- Solution
- Market
- Business Model
- Financials
- Team

Improvement Suggestions:
- Problem: Clearly define the problem and validate it with market research. Show the urgency and impact of the problem.
- Solution: Highlight your unique value proposition and how your solution addresses the problem. Emphasize innovation and feasibility.
- Market: Include market size (TAM, SAM, SOM), growth rate, and competitive analysis. Define your target audience more precisely.
- Business Model: Detail your revenue streams, pricing strategy, and path to profitability. Explain your go-to-market approach.
- Financials: Provide realistic projections with clear assumptions. Include key metrics and funding requirements.
- Team: Highlight relevant experience, skills, and achievements of key team members. Consider adding advisors if needed.
==================================================

=== Analysis for CyberGuard ===
Overall Score: 46.9/100

Section Scores:
- Problem: 45.1/100
- Solution: 45.1/100
- Market: 45.1/100
- Business Model: 53.7/100
- Financials: 45.1/100
- Team: 45.1/100

Strengths:
- No significant strengths identified

Weaknesses:
- Problem
- Solution
- Market
- Business Model
- Financials
- Team

Improvement Suggestions:
- Problem: Clearly define the problem and validate it with market research. Show the urgency and impact of the problem.
- Solution: Highlight your unique value proposition and how your solution addresses the problem. Emphasize innovation and feasibility.
- Market: Include market size (TAM, SAM, SOM), growth rate, and competitive analysis. Define your target audience more precisely.
- Business Model: Detail your revenue streams, pricing strategy, and path to profitability. Explain your go-to-market approach.
- Financials: Provide realistic projections with clear assumptions. Include key metrics and funding requirements.
- Team: Highlight relevant experience, skills, and achievements of key team members. Consider adding advisors if needed.
==================================================

=== Analysis for LearnLoop ===
Overall Score: 45.2/100

Section Scores:
- Problem: 45.2/100
- Solution: 45.2/100
- Market: 45.2/100
- Business Model: 45.2/100
- Financials: 45.2/100
- Team: 45.2/100

Strengths:
- No significant strengths identified

Weaknesses:
- Problem
- Solution
- Market
- Business Model
- Financials
- Team

Improvement Suggestions:
- Problem: Clearly define the problem and validate it with market research. Show the urgency and impact of the problem.
- Solution: Highlight your unique value proposition and how your solution addresses the problem. Emphasize innovation and feasibility.
- Market: Include market size (TAM, SAM, SOM), growth rate, and competitive analysis. Define your target audience more precisely.
- Business Model: Detail your revenue streams, pricing strategy, and path to profitability. Explain your go-to-market approach.
- Financials: Provide realistic projections with clear assumptions. Include key metrics and funding requirements.
- Team: Highlight relevant experience, skills, and achievements of key team members. Consider adding advisors if needed.
==================================================

```

