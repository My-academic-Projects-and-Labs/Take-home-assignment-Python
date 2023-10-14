class TranscriptManager:
    # Singleton Design Pattern
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TranscriptManager, cls).__new__(cls)
            cls._instance.transcripts = {
                'English': {
                    'welcome': "Welcome, {client_name}. This is coach {coach_name}, from Coachello.",
                    'goodbye': "Goodbye, {client_name}. It was a pleasure coaching you. - Coach {coach_name}",
                    'progress': "Great progress, {client_name}. Keep it up! - Coach {coach_name}"
                },
                'Spanish': {
                    'welcome': "Bienvenido, {client_name}. Este es entrenador {coach_name}, de Coachello.",
                    'goodbye': "Adiós, {client_name}. Fue un placer entrenarte. - Entrenador {coach_name}",
                    'progress': "Gran progreso, {client_name}. ¡Sigue así! - Entrenador {coach_name}"
                }
            }
        return cls._instance

    # Public methods to manage transcripts (abstraction)
    def add_transcript(self, language, transcript_type, transcript):
        if language not in self.transcripts:
            self.transcripts[language] = {}
        self.transcripts[language][transcript_type] = transcript

    def get_transcript(self, language, transcript_type):
        return self.transcripts.get(language, {}).get(transcript_type, "")

class PromptHandler:
    def __init__(self, transcript_manager):
        self.transcript_manager = transcript_manager
        self.coach_name = ""
        self.client_name = ""
        self.language = "English"
        self.format = "Text"
        self.transcript_type = "welcome"

    # Public setter methods
    def set_coach_name(self, coach_name):
        self.coach_name = coach_name

    def set_client_name(self, client_name):
        self.client_name = client_name

    def set_language(self, language):
        self.language = language

    def set_format(self, format):
        self.format = format

    def set_transcript_type(self, transcript_type):
        self.transcript_type = transcript_type

    # Public method to get the formatted prompt
    def get_formatted_prompt(self):
        transcript = self.transcript_manager.get_transcript(self.language, self.transcript_type)
        transcript = transcript.format(coach_name=self.coach_name, client_name=self.client_name)
        if self.format == 'HTML':
            transcript = f"<p>{transcript}</p>"
        return transcript


class PromptHandlerFactory:
    # Factory Method: Class to create and return instances of different types of PromptHandler objects
    # We can add other types of PromptHandler objects at the end as needed
    @staticmethod
    def create_prompt_handler(type_of_handler):
        transcript_manager = TranscriptManager()
        if type_of_handler == 'base':
            return PromptHandler(transcript_manager)

def main():
    try:
        # Create PromptHandler instance using Factory Method
        # * Polymorphism - PromptHandler class, the code is set up to handle 
        # multiple types of prompt handlers through a common interface
        # * Inheritance - The use of a base PromptHandler class allows 
        # for easy extension to other types of prompt handlers
        prompt_handler = PromptHandlerFactory.create_prompt_handler('base')
        if prompt_handler is None:
            raise ValueError("Invalid handler type.")

        # TranscriptManager and PromptHandler instances (encapsulation)
        transcript_manager = TranscriptManager()
        prompt_handler = PromptHandler(transcript_manager)

        # User Input Handling
        coach_name = input("Enter the coach name: ")
        prompt_handler.set_coach_name(coach_name)

        client_name = input("Enter the client name: ")
        prompt_handler.set_client_name(client_name)

        print("Available languages: English, Spanish")
        language = input("Select the language: ")
        if language not in ['English', 'Spanish']:
            raise ValueError("Invalid language selected.")
        prompt_handler.set_language(language)

        print("Available formats: Text, HTML")
        format = input("Select the format: ")
        if format not in ['Text', 'HTML']:
            raise ValueError("Invalid format selected.")
        prompt_handler.set_format(format)

        print("Available transcript types: welcome, goodbye, progress")
        transcript_type = input("Select the transcript type: ")
        if transcript_type not in ['welcome', 'goodbye', 'progress']:
            raise ValueError("Invalid transcript type selected.")
        prompt_handler.set_transcript_type(transcript_type)

        formatted_prompt = prompt_handler.get_formatted_prompt()
        print("\nFormatted Prompt:")
        print(formatted_prompt)

    except ValueError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
