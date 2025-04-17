import os
from openai import OpenAI

# Load your API key from env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read the implementation report
with open("docs/implementation_report.md", "r") as f:
    input_text = f.read()

# Define the prompt with your custom header
prompt = f"""
You're a technical release manager. Based on the following implementation report, generate a clean and professional CHANGELOG.md file.

Make sure to include this header at the top:

# 📦 Changelog — ARE-U-QUERY-OUS

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and uses [Semantic Versioning](https://semver.org/).

---

Use meaningful groupings like Features, Database, Docs, Refactor, etc.

Now generate the changelog from the following implementation report:

{input_text}
"""

# Call the Chat API
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that formats project changelogs."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.4,
)

# Extract the response text
output = response.choices[0].message.content

# Save to file
with open("CHANGELOG.md", "w") as f:
    f.write(output)

print("✅ CHANGELOG.md updated successfully.")
