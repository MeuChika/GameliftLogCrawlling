@echo off
pyinstaller -w -F --icon=tag_generator.ico gameliftlogcrawling.py 
copy .\dist\tag_generator.exe .\