from datetime import datetime
import os
from uuid import uuid4
from django.core.files.images import get_image_dimensions
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

def validate_avatar(avatar):
    """
    Kiểm tra tính hợp lệ của file avatar:
      - Kiểm tra loại file upload.
      - Kiểm tra định dạng ảnh thông qua get_image_dimensions.
      - Kiểm tra phần mở rộng.
    """
    if not isinstance(avatar, InMemoryUploadedFile):
        raise serializers.ValidationError("File upload is not valid.")

    try:
        # Kiểm tra xem file có phải là hình ảnh hợp lệ không
        width, height = get_image_dimensions(avatar)
    except Exception:
        raise serializers.ValidationError("Invalid image file.")

    allowed_extensions = [".jpg", ".jpeg", ".png"]
    file_ext = os.path.splitext(avatar.name)[-1].lower()
    if file_ext not in allowed_extensions:
        raise serializers.ValidationError("Only .jpg, .jpeg, .png files are allowed.")

    return avatar

def user_avatar_upload_path(instance, filename):
    """ Path using User ID """
    ext = os.path.splitext(filename)[-1].lower()  # .jpg, .png, ...
    if not ext or ext not in [".jpg", ".jpeg", ".png"]:
        ext = ".jpg"
    new_filename = f"avatar_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}{ext}"
    return os.path.join("avatars", f"user_{instance.id}", new_filename)