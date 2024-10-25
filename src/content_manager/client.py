import google.generativeai as genai
import os



def experiment_feature():
    API_KEY = os.environ["GOOGLE_API_KEY"]
    
    genai.configure(api_key=API_KEY)



    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a story about a magic backpack.")
    # print(response.text)

    return response