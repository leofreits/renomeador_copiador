@echo off
echo Iniciando a compilação do executável...
echo.

:: Ativa o ambiente virtual (ajuste se o nome da sua pasta for diferente de venv)
call .\venv\Scripts\activate

:: Executa o PyInstaller com todas as configurações que definimos
pyinstaller --noconsole --onefile --collect-all customtkinter app.py

echo.
echo ##########################################
echo #   PROCESSO CONCLUÍDO COM SUCESSO!      #
echo #   O novo .exe está na pasta 'dist'     #
echo ##########################################
echo.
pause