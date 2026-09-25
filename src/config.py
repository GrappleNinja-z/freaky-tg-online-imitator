import os
from dataclasses import dataclass

@dataclass
class Config:
    api_key: str
    database_url: str
    secret_token: str

    @classmethod
    def load(cls):
        return cls(
            api_key=os.getenv('API_KEY', ''),
            database_url=os.getenv('DATABASE_URL', ''),
            secret_token=os.getenv('SECRET_TOKEN', '')
        )

    def validate(self):
        if not all([self.api_key, self.database_url, self.secret_token]):
            raise ValueError("Missing required environment variables")
