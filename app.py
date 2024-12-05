from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Set your OpenAI API Key here
openai.api_key = # Put your open ai key here
# Route for the front-end UI

system_prompt = """
You are a news summarizer chatbot. Your task is to summarize the article in clear, concise bullet points, and include key details like:

Who: Identify the main people or entities involved.
What: Summarize the key event or action.
When: Specify the date or time period of the event.
Where: State the location or context of the event.
Why: Explain the cause or reasoning behind the event.
Reflection: Provide a brief reflection or analysis of the event (1-2 sentences). This can include any notable implications or takeaways.
Category: Categorize the article into one of these categories - business, sports, tech, entertainment, politics.

Output the headings, and then the information. Do not bold the headings. Add a linebreak before each bullet point. Ensure that the summary is clear, factual, and easy to understand. 

Don't bold, italicize, or underline anything. Don't add anything other than the 7 bullet points. Keep the reflection neutral and objective, without any bias or opinion.
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        article = request.form.get("article", "")
        if not article:
            return render_template("index.html", error="Please enter a news article.")
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": article}
                ]
            )
            # Extract the completion text
            summary = response.choices[0].message['content']
            return render_template("index.html", summary=summary)
        except Exception as e:
            return render_template("index.html", error=str(e))
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
