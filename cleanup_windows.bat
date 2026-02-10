@echo off
echo Cleaning up repository...
echo.

REM Debug/diagnostic scripts
if exist debug_api.py del debug_api.py
if exist diagnostic_full_trace.py del diagnostic_full_trace.py
if exist restart_backend.py del restart_backend.py
if exist verify_fixes.py del verify_fixes.py

REM Test files in root
if exist test_api_timing.py del test_api_timing.py
if exist test_pathological_direct.py del test_pathological_direct.py
if exist test_samples.py del test_samples.py
if exist test_samples.bat del test_samples.bat

REM Phase-specific files
if exist run_phase5.py del run_phase5.py
if exist run_phase5.sh del run_phase5.sh
if exist start_phase5.sh del start_phase5.sh
if exist stop_phase5.sh del stop_phase5.sh

REM Redundant requirements files
if exist requirements-phase5.txt del requirements-phase5.txt
if exist requirements_phase5.txt del requirements_phase5.txt

REM Redundant documentation
if exist QUICKSTART_PHASE1.md del QUICKSTART_PHASE1.md
if exist QUICK_FIX_GUIDE.md del QUICK_FIX_GUIDE.md
if exist TESTING.md del TESTING.md
if exist TESTING_GUIDE.md del TESTING_GUIDE.md
if exist TODO.md del TODO.md

REM Cleanup markers
if exist .cleanup_marker del .cleanup_marker

REM Remove overly polished architecture doc
if exist docs\ARCHITECTURE.md del docs\ARCHITECTURE.md

REM Remove this cleanup guide
if exist CLEANUP_NEEDED.md del CLEANUP_NEEDED.md

echo.
echo Cleanup complete!
echo.
echo Now run:
echo   git add -A
echo   git commit -m "Clean up repository structure"
echo   git push
echo.
echo After pushing, you can delete this cleanup script:
echo   del cleanup_windows.bat
echo.
pause
