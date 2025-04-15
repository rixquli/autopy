REM filepath: ./assets/make.bat
@echo off
echo Creating program icon...
python -c "from PIL import Image; img = Image.new('RGBA', (256,256), (0,0,0,0)); img.save('icon.ico')"