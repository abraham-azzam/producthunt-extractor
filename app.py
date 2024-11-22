from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Extract user data from Product Hunt profile
def extract_user_data(profile_url):
    try:
        response = requests.get(profile_url)
        if response.status_code != 200:
            return {"error": f"Couldn't access the page. Status code: {response.status_code}"}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract name
        name_tag = soup.find('h1')
        name = name_tag.text.strip() if name_tag else "Name not found"

        # Extract followers count
        followers_tag = soup.find('a', {'href': lambda x: x and '/followers' in x})
        followers = followers_tag.text.strip() if followers_tag else "Followers count not found"

        # Extract LinkedIn URL
        linkedin_tag = soup.find('a', {'href': lambda x: x and 'linkedin.com' in x})
        linkedin_url = linkedin_tag['href'] if linkedin_tag else "LinkedIn URL not found"

        return {
            "name": name,
            "followers": followers,
            "linkedin_url": linkedin_url,
            "producthunt_url": profile_url  # Return the input URL
        }
    except Exception as e:
        return {"error": str(e)}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    profile_url = data.get("profile_url")
    if not profile_url:
        return jsonify({"error": "Profile URL is required"}), 400

    # Call extract_user_data to get user info
    user_data = extract_user_data(profile_url)

    # Get first name only
    full_name = user_data['name']
    first_name = full_name.split()[0] if full_name != "Name not found" else "there"

    # Generate a message
    message = f"""
Hi {first_name},

Shopless helps startups scale smarter and faster. 🚀 Join us on Product Hunt to support innovation—click "Notify Me" here: https://www.producthunt.com/products/shopless-business-solutions. 🎉
    """

    return jsonify({"user_data": user_data, "message": message})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
