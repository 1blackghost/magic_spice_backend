from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from administrator.models import Admin
import hashlib

def generate_md5_hash(input_string):
    md5_hash = hashlib.md5()
    
    md5_hash.update(input_string.encode('utf-8'))
    
    hex_digest = md5_hash.hexdigest()
    
    return hex_digest


def add(request,server_password,username, password):
    passw="842f911b44e1d411643bcf7d9c8e533e"#prince@123
    if str(generate_md5_hash(server_password))==passw:
        try:
            admin, created = Admin.objects.get_or_create(email=username)
            admin.password = make_password(password)
            admin.save()
            return JsonResponse({"status": "ok", "message": "Password updated successfully."})
        except Exception as e:
            return JsonResponse({"status": "bad", "error": str(e)})
