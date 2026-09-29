from flask import Flask, render_template, request
from textblob import TextBlob
import nltk

app = Flask(__name__)

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text', '')
        
        if not text.strip():
            return render_template('index.html', error="Please enter some text")
        
        try:
            blob = TextBlob(text)
            sentiment = "neutral"
            
            # Determine sentiment based on polarity
            polarity = blob.sentiment.polarity
            if polarity > 0.1:
                sentiment = "positive"
            elif polarity < -0.1:
                sentiment = "negative"
            
            # Get language (correct method)
            language = "en"  # Default to English
            try:
                # This is the correct way to detect language in TextBlob
                if hasattr(blob, 'detect_language'):
                    language = blob.detect_language()
                else:
                    # Fallback method for newer versions
                    language = blob.translate(to='en').detect_language()
            except:
                language = "Unknown"
            
            # Prepare results
            results = {
                'text': text,
                'sentiment': sentiment,
                'polarity': f"{polarity:.2f}",
                'subjectivity': f"{blob.sentiment.subjectivity:.2f}",
                'language': language
            }
            return render_template('index.html', results=results)
        
        except Exception as e:
            return render_template('index.html', error=f"Analysis error: {str(e)}")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)