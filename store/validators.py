from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_KB = 50 
    
    if file.size > max_size_KB * 1024:
        raise ValidationError(f'File cannot be larger than {max_size_KB}KB! ')