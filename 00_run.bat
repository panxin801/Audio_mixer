@echo off&setlocal enabledelayedexpansion
::wav_output is output dir
if not exist wav_output mkdir wav_output
::wav is input dir
for /f "delims=" %%a in ('DIR "wav" /B') do set "txt=%%~a"&call :s !txt!
pause
:s
:: wav and wav_output in the following two lines need change either.
set readPath=%cd%\wav\%1
ffmpeg -i %readPath% -acodec pcm_s16le -ac 1 -ar 16000 wav_output\%1 -y
goto :eof