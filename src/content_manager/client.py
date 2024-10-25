import google.generativeai as genai
import os



def experiment_feature():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a story about a magic backpack.")
    # print(response.text)

    return response