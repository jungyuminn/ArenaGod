import os
import json

class DataService:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.champions_data = {"champions": {}}
            # Windows AppData 폴더에 데이터 저장
            self.data_dir = os.path.join(os.getenv('APPDATA'), 'ArenaGod')
            self.data_file = os.path.join(self.data_dir, "champion_records.json")
            os.makedirs(self.data_dir, exist_ok=True)
            self.load_data()
            DataService._initialized = True
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.champions_data = json.load(f)
            except json.JSONDecodeError:
                self.champions_data = {"champions": {}}
    
    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.champions_data, f, ensure_ascii=False, indent=2)
    
    def set_champion_status(self, en_name, is_checked):
        self.champions_data["champions"][en_name] = is_checked
        self.save_data()
    
    def get_champion_status(self, en_name):
        return self.champions_data["champions"].get(en_name, False)