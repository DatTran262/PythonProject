import os
path = os.path.abspath('QLabel/Images/background.jpg')

if os.path.exists(path):
    print(f"✅ Ảnh tồn tại: {path}")
else:
    print(f"❌ Ảnh không tồn tại: {path}")
