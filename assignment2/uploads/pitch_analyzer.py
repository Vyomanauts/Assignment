import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import BertTokenizer, BertModel
import torch
import torch.nn.functional as F

# Make sure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

def preprocess_text(text):
    """
    Preprocess the text extracted from pitch decks
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    
    # Tokenize text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    # Join the tokens back into text
    preprocessed_text = ' '.join(filtered_tokens)
    
    return preprocessed_text

def identify_sections(pitch_text):
    """
    Identify key sections from a pitch deck text
    """
    sections = {
        'problem': None,
        'solution': None,
        'market': None,
        'business_model': None,
        'financials': None,
        'team': None
    }
    
    # Keywords to identify each section
    section_keywords = {
        'problem': ['problem', 'challenge', 'pain point', 'issue', 'need'],
        'solution': ['solution', 'product', 'service', 'offering', 'value proposition'],
        'market': ['market', 'industry', 'opportunity', 'tam', 'sam', 'som', 'customers'],
        'business_model': ['business model', 'revenue', 'pricing', 'monetization', 'go-to-market'],
        'financials': ['financials', 'projections', 'forecast', 'revenue', 'profits', 'burn rate'],
        'team': ['team', 'founders', 'leadership', 'management', 'experience', 'background']
    }
    
    # Assign weights to sections
    section_weights = {
        'problem': 0.15,
        'solution': 0.20,
        'market': 0.15,
        'business_model': 0.20,
        'financials': 0.15,
        'team': 0.15
    }
    
    # Split text into paragraphs
    paragraphs = pitch_text.split('\n\n')
    
    # First pass: Look for section headings
    for i, paragraph in enumerate(paragraphs):
        paragraph_lower = paragraph.lower().strip()
        
        for section_name, keywords in section_keywords.items():
            # Check if paragraph starts with any of the keywords
            if any(paragraph_lower.startswith(keyword + ":") for keyword in keywords):
                sections[section_name] = paragraph
                
                # If there's a next paragraph, append it (likely part of the same section)
                if i + 1 < len(paragraphs):
                    sections[section_name] += " " + paragraphs[i + 1]
    
    # Second pass: If sections are still empty, look for keywords anywhere in paragraphs
    for section_name, section_content in sections.items():
        if section_content is None:
            for paragraph in paragraphs:
                paragraph_lower = paragraph.lower()
                if any(keyword in paragraph_lower for keyword in section_keywords[section_name]):
                    if sections[section_name] is None:
                        sections[section_name] = paragraph
                    else:
                        sections[section_name] += " " + paragraph
    
    return sections, section_weights

class PitchScoringModel:
    def __init__(self):
        try:
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            self.model = BertModel.from_pretrained('bert-base-uncased')
        except:
            # Fallback if BERT model loading fails
            self.tokenizer = None
            self.model = None
        
        # Define quality patterns for each section
        self.quality_patterns = {
            'problem': [
                "clearly defined problem", "market validation", "statistics", "urgency",
                "impact", "pain point", "customer need", "market gap"
            ],
            'solution': [
                "unique value proposition", "innovative approach", "technical details",
                "competitive advantage", "feasibility", "scalability", "intellectual property"
            ],
            'market': [
                "market size", "tam", "sam", "som", "growth rate", "trends", "competition",
                "target audience", "market validation", "market research"
            ],
            'business_model': [
                "revenue streams", "pricing strategy", "unit economics", "go to market",
                "sales channels", "customer acquisition", "path to profitability"
            ],
            'financials': [
                "revenue projections", "profit margins", "cash flow", "break even",
                "burn rate", "funding needs", "key metrics", "financial assumptions"
            ],
            'team': [
                "founder experience", "industry expertise", "technical skills",
                "track record", "complementary skills", "advisors", "board members"
            ]
        }
    
    def score_section(self, section_text, section_name):
        """
        Score a section based on content quality and completeness
        """
        if section_text is None or len(section_text.strip()) == 0:
            return 0
        
        # Get quality patterns for this section
        patterns = self.quality_patterns.get(section_name, [])
        if not patterns:
            return 50  # Default score if no patterns defined
        
        # Convert text to lowercase for pattern matching
        section_text = section_text.lower()
        
        # Count how many quality patterns are mentioned
        matches = 0
        for pattern in patterns:
            if pattern.lower() in section_text:
                matches += 1
        
        # Calculate score based on pattern matches
        # If all patterns are present, score is 100
        # If no patterns are present, minimum score is 40
        base_score = 40
        if patterns:
            match_score = (matches / len(patterns)) * 60
            score = base_score + match_score
        else:
            score = 50
        
        # Add bonus points for section length (up to 10 points)
        words = len(section_text.split())
        length_bonus = min(10, words / 20)
        
        return min(100, score + length_bonus)
    
    def calculate_overall_score(self, sections, section_weights):
        """
        Calculate overall pitch score
        """
        overall_score = 0
        section_scores = {}
        
        for section_name, section_text in sections.items():
            section_score = self.score_section(section_text, section_name)
            section_scores[section_name] = section_score
            overall_score += section_score * section_weights[section_name]
        
        return overall_score, section_scores

def analyze_strengths_weaknesses(section_scores):
    """
    Analyze strengths and weaknesses based on section scores
    """
    strengths = []
    weaknesses = []
    improvement_suggestions = {}
    
    # Threshold for determining strengths and weaknesses
    strength_threshold = 70
    weakness_threshold = 60
    
    for section, score in section_scores.items():
        if score >= strength_threshold:
            strengths.append(section)
        elif score <= weakness_threshold:
            weaknesses.append(section)
            
            # Generate improvement suggestions
            if section == 'problem':
                improvement_suggestions[section] = "Clearly define the problem and validate it with market research. Show the urgency and impact of the problem."
            elif section == 'solution':
                improvement_suggestions[section] = "Highlight your unique value proposition and how your solution addresses the problem. Emphasize innovation and feasibility."
            elif section == 'market':
                improvement_suggestions[section] = "Include market size (TAM, SAM, SOM), growth rate, and competitive analysis. Define your target audience more precisely."
            elif section == 'business_model':
                improvement_suggestions[section] = "Detail your revenue streams, pricing strategy, and path to profitability. Explain your go-to-market approach."
            elif section == 'financials':
                improvement_suggestions[section] = "Provide realistic projections with clear assumptions. Include key metrics and funding requirements."
            elif section == 'team':
                improvement_suggestions[section] = "Highlight relevant experience, skills, and achievements of key team members. Consider adding advisors if needed."
    
    return strengths, weaknesses, improvement_suggestions

def create_sample_pitches():
    """
    Create a dataset of 5 sample pitch decks
    """
    pitch_decks = [
        {
            "name": "EcoDelivery",
            "content": """
            Problem: Last-mile delivery is responsible for 40% of emissions in urban logistics. Traditional delivery methods are inefficient and environmentally harmful.
            
            Solution: EcoDelivery is an electric cargo bike delivery service with proprietary route optimization software that reduces emissions by 75% compared to van deliveries.
            
            Market: The global last-mile delivery market is valued at $108B and growing at 21% CAGR. Our initial target is urban centers in North America, estimated at $30B.
            
            Business Model: We charge merchants a flat fee plus distance-based pricing. Our margins are 40% per delivery, with additional revenue from premium services.
            
            Financials: Projecting $2M revenue in Year 1, growing to $20M by Year 3. Initial capital expenditure of $500K for fleet, with break-even expected in Month 18.
            
            Team: Founded by former Uber Eats operations director and Tesla battery engineer. Advisory board includes former FedEx executive.
            """
        },
        {
            "name": "MediTrack",
            "content": """
            Problem: 30% of prescribed medications are never taken as directed, leading to 125,000 deaths annually and $300B in avoidable healthcare costs.
            
            Solution: MediTrack is an IoT-enabled smart pill dispenser with companion app that tracks medication adherence and provides timely reminders.
            
            Market: The medication adherence market is $3.9B currently, expected to reach $11.5B by 2027.
            
            Business Model: Hardware sales ($199 per unit) plus subscription service ($15/month) for premium features. B2B sales to healthcare providers and insurance companies.
            
            Financials: Year 1: $1.2M revenue with 40% margins. Year 3 projection: $10M with 60% margins as software revenue grows. Seeking $2M seed funding.
            
            Team: CEO is former pharmaceutical executive. CTO previously led development at a successful health tech startup.
            """
        },
        {
            "name": "FarmAI",
            "content": """
            Problem: Small-scale farmers lose 20-40% of crops due to inefficient pest management. Traditional methods are costly and often ineffective.
            
            Solution: FarmAI uses drone imagery and machine learning to identify pests and plant diseases early, enabling targeted treatment.
            
            Market: The agricultural AI market is $1B today, growing at 25% annually. We target 2.1M small farmers across North America.
            
            Business Model: SaaS model with tiered pricing ($50-200/month). Additional revenue from data licensing to agricultural companies.
            
            Team: Founders include agricultural scientists and machine learning engineers with 15+ years combined experience.
            """
        },
        {
            "name": "CyberGuard",
            "content": """
            Problem: Small businesses experience 43% of cyber attacks but have limited security resources. Existing solutions are too complex and expensive.
            
            Solution: CyberGuard offers AI-powered cybersecurity monitoring tailored for small businesses, with automatic threat detection and remediation.
            
            Market: The SMB cybersecurity market is $40B globally, growing at 15% annually.
            
            Business Model: Monthly subscription ($99-499) based on business size and industry risk profile.
            
            Financials: Projecting $1.5M ARR in Year 1, growing to $15M by Year 3. Customer acquisition cost estimated at $800 with 18-month payback period.
            
            Team: Founded by former security analysts from Microsoft and Cisco with combined 20 years of experience in threat detection.
            """
        },
        {
            "name": "LearnLoop",
            "content": """
            Problem: Corporate training has poor retention rates with only 12% of employees applying skills learned. Traditional training is expensive and time-consuming.
            
            Solution: LearnLoop uses AI to create personalized microlearning experiences delivered via Slack/Teams, with spaced repetition to improve retention.
            
            Market: The corporate e-learning market is $21B in North America, growing at 13% annually.
            
            Business Model: SaaS with per-seat pricing ($15-25/user/month) and enterprise plans. Content creation services as additional revenue stream.
            
            Financials: $800K revenue in Year 1, projecting $8M by Year 3. Gross margins of 85% after content development costs.
            
            Team: CEO previously built and sold an EdTech company. CTO was senior engineer at Coursera.
            """
        }
    ]
    
    return pitch_decks

def analyze_pitch(pitch_deck):
    """
    Analyze a pitch deck and provide a score with feedback
    """
    # Identify sections and their weights
    sections, section_weights = identify_sections(pitch_deck["content"])
    
    # Initialize the scoring model
    scoring_model = PitchScoringModel()
    
    # Calculate overall score and section scores
    overall_score, section_scores = scoring_model.calculate_overall_score(sections, section_weights)
    
    # Analyze strengths and weaknesses
    strengths, weaknesses, improvement_suggestions = analyze_strengths_weaknesses(section_scores)
    
    # Check if any sections are missing
    missing_sections = []
    for section, content in sections.items():
        if content is None or len(content.strip()) == 0:
            missing_sections.append(section)
            section_scores[section] = 0
    
    # Prepare output
    output = {
        "pitch_name": pitch_deck["name"],
        "overall_score": round(overall_score, 1),
        "section_scores": {k: round(v, 1) for k, v in section_scores.items()},
        "strengths": strengths,
        "weaknesses": weaknesses,
        "missing_sections": missing_sections,
        "improvement_suggestions": improvement_suggestions
    }
    
    return output

def main():
    print("AI Pitch Analysis Model")
    print("=" * 50)
    
    # Create sample pitch decks
    pitch_decks = create_sample_pitches()
    
    # Analyze each pitch deck
    results = []
    for pitch_deck in pitch_decks:
        result = analyze_pitch(pitch_deck)
        results.append(result)
        
        # Display results
        print(f"\n=== Analysis for {result['pitch_name']} ===")
        print(f"Overall Score: {result['overall_score']}/100")
        print("\nSection Scores:")
        for section, score in result['section_scores'].items():
            print(f"- {section.replace('_', ' ').title()}: {score}/100")
        
        print("\nStrengths:")
        if result['strengths']:
            for strength in result['strengths']:
                print(f"- {strength.replace('_', ' ').title()}")
        else:
            print("- No significant strengths identified")
        
        print("\nWeaknesses:")
        if result['weaknesses']:
            for weakness in result['weaknesses']:
                print(f"- {weakness.replace('_', ' ').title()}")
        else:
            print("- No significant weaknesses identified")
        
        if result['missing_sections']:
            print("\nMissing Sections:")
            for section in result['missing_sections']:
                print(f"- {section.replace('_', ' ').title()}")
        
        print("\nImprovement Suggestions:")
        if result['improvement_suggestions']:
            for section, suggestion in result['improvement_suggestions'].items():
                print(f"- {section.replace('_', ' ').title()}: {suggestion}")
        else:
            print("- No specific improvement suggestions")
        
        print("="*50)
    
    return results

if __name__ == "__main__":
    main()