import yaml

class Settings:
    def __init__(self):
        self.CountFailures = 0
        self.CountRepairTeams = 0
        self.RecoveryIntensity = 0.00
        self.Policy = 'FAST'

    def read_settings(self, name_file):
        with open(name_file, 'r', encoding='utf-8') as file:
            read_data = yaml.load(file, Loader=yaml.FullLoader)
        self.CountFailures = read_data['CountFailures']
        self.CountRepairTeams = read_data['CountRepairTeams']
        self.RecoveryIntensity = read_data['RecoveryIntensity']
        self.Policy = read_data['Policy']

    @staticmethod
    def create_settings(name_file):
        data = {'CountFailures': 0, 'CountRepairTeams': 0, 'RecoveryIntensity': 0.00,
                'Policy': 'FAST'}
        with open(name_file, 'w', encoding='utf-8') as file:
            yaml.dump(data, file)

    def get_settings(self):
        return [self.CountFailures, self.CountRepairTeams, self.RecoveryIntensity, self.Policy]

    def set_settings(self, name_file, settings):
        self.CountFailures = settings[0]
        self.CountRepairTeams = settings[1]
        self.RecoveryIntensity = settings[2]
        self.Policy = settings[3]
        data = {'CountFailures': settings[0], 'CountRepairTeams': settings[1],
                'RecoveryIntensity': settings[2], 'Policy': settings[3]}
        with open(name_file, 'w', encoding='utf-8') as file:
            yaml.dump(data, file)