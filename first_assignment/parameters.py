class ParameterManager:
    def __init__(self):
        self.parameters = {}

    def set_parameter(self, key, value):
        self.parameters[key] = value

    def get_parameter(self, key):
        return self.parameters.get(key)

    def collect_parameters(self):
        # Here, we can add more inputs as we extend the functionality
        self.set_parameter('first_name', input("Enter your first name: "))
        self.set_parameter('last_name', input("Enter your last name: "))
        self.set_parameter('email', input("Enter your email: "))
