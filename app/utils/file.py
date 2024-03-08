import base64


def get_file_info(file_base64_str: str):
    """
        get file_name, data_type, file_data, mime_type
        return  file_name, data_type, file_data, mime_type
    """
    data_type: str = file_base64_str.split(';base64,')[0]
    file_size: int = (len(file_base64_str) * 3) / 4 - file_base64_str.count('=', -2)
    file_size /= 1024.0
    file_encode_str: str = file_base64_str.split(';base64,')[1]
    file_data: bytes = base64.b64decode(file_encode_str)
    mime_type: str = data_type.split('data:')[1]
    img_type: str = data_type.split('image/')[1]
    return img_type, data_type, file_data, mime_type, int(file_size)