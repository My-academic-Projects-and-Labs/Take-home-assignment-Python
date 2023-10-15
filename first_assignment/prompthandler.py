import subprocess
import sys
import os
import json
from parameters import ParameterManager
from transcripts import TranscriptManager

class PromptHandler:
    def __init__(self):
        self.parameter_manager = ParameterManager()
        self.transcript_manager = TranscriptManager()
        self.language = "English"
        self.format = "Text"

    def collect_user_input(self):
        self.parameter_manager.collect_parameters()
        print("Available languages: English, Spanish")
        self.language = input("Preferred Language: ")
        self.parameter_manager.set_parameter('language', self.language)
        print("Available formats: Text, HTML")
        self.format = input("Output Format: ")


    def translate_prompt(self, prompt):
        # Issue getting the permission of the system to install the requirements
        
        # if self.language == "Spanish":
        #     install_requirements()
        #     target_language='ES'
        #     api_url = "https://api.mymemory.translated.net/get"
        #     params = {
        #         "q": prompt,
        #         "langpair": f"en|{target_language}"
        #     }
        #     response = requests.get(api_url, params=params)
        #     if response.status_code == 200:
        #         json_data = json.loads(response.text)
        #         prompt = json_data['responseData']['translatedText']
        #     else:
        #         print(f"Translation failed: {response.status_code}")
        return prompt

    def get_formatted_prompt(self):
        transcript = self.transcript_manager.get_transcript()
        formatted_prompt = transcript.format(**self.parameter_manager.parameters)
        translated_prompt = self.translate_prompt(formatted_prompt)
        return translated_prompt

    def save_output(self, output):
        path = '../out/1st_out/'
        if not os.path.exists(path):
            os.makedirs(path)

        if self.format == "HTML":
            filename = "prompt.html"
            html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Coaching Prompt</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1 class="mt-4 mb-4">Coaching Prompt</h1>
        <div class="card">
            <div class="card-body">
                {formatted_prompt}
            </div>
        </div>
    </div>
</body>
</html>
            """
            output = html_template.format(formatted_prompt=output.replace("\n", "<br/>"))
        else:
            filename = "prompt.txt"

        with open(os.path.join(path, filename), 'w') as f:
            f.write(output)

def install_requirements():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

if __name__ == "__main__":
    try:
        prompt_handler = PromptHandler()
        prompt_handler.collect_user_input()
        formatted_prompt = prompt_handler.get_formatted_prompt()
        prompt_handler.save_output(formatted_prompt)
        print("Output generated successfully. Please check the 'out/1st_out' folder.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
