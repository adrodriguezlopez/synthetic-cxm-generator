import random
from datetime import datetime, timedelta

class BaseFieldGenerator:
    '''
    Abstract field generator for an interaction event.
    Can be extended by channel-specific field generators
    '''
    def __init__(self, profile=None):
        self.profile = profile or {}

    def generate(self, field_name: str, field_type: str = None):
        """
        Resolution priority:
        1. generate_<fieldname>_<type>()
        2. generate_<fieldname>()
        3. generate_type_<type>()
        """
        #Try exact field_name method
        method = None	
        
        if field_name and field_type:
            method = getattr(self, f"generate_{field_name}_{field_type}", None)
            if method: 
                return method()
            
        if field_name:
            method = getattr(self, f"generate_{field_name}", None)
            if method:
                return method()
        
        if field_type:
            method = getattr(self, f"generate_{field_type}", None)
            if method:
                return method()
            
        return self._default()
    
    def _default(self):
        return None
    
    def generate_type_str(self):
        return f"str_{random.randint(1000, 9999)}"
    
    def generate_type_int(self):
        return random.randint(0,100)
    
    def generate_type_float(self):
        return round(random.uniform(0.0, 1.0), 3)

    def generate_type_bool(self):
        return random.choice([True, False])
    
    def generate_type_datetime(self):
        return datetime.now() - timedelta(seconds=random.randint(0,3600))