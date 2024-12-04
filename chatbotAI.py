import pandas as pd
import openai

#TODO: REMOVE API KEY BEFORE UPLOADING

class ChatbotAI:

    def __init__(self):
        self.client = OpenAI(
            api_key = "")

    def get_chatgpt_response(self, csv_filepath, user_query):
        pd.set_option('display.max_columns', None)
        csv = pd.read_csv(csv_filepath, encoding='utf-8')

        prompt = f"""
        You are an assistant that helps search through a car database.
        Here is a portion of the database:
        {csv}
        
        User Query: {user_query}
        Based on the above data, provide the most relevant rows or answers.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are an assistant that searches a CSV of cars."},
                      {"role": "user", "content": prompt}]
        )

        message_content = response.choices[0].message.content

        return message_content

#tester
if __name__ == "__main__":
    test_csv = "Organized_Car_Data/Chevrolet/Coupe.csv"
    chatbot =  ChatbotAI()
    query = "Under 30000"
    test_response = chatbot.get_chatgpt_response(csv_filepath="Organized_Car_Data/Chevrolet/Coupe.csv", user_query=query)
    print(test_response)
else
    query = "Acura"
    df = pd.read_csv("Organized_Car_Data/Chevrolet/Coupe.csv")
    response = getchatgpt_response(df, query)
    print(response)
    


