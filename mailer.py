from model_utils import get_neon_client 

def get_mailing_list(): 
    engine = get_neon_client()
    query = "SELECT email"