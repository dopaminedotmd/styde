@echo off
cd /d D:\styde\_alpedal\styde-forge
python -u Core/forge.py loop-parallel "3d-data-terrain-explorer,ab-testing-statistician,accessibility-auditor" --max 5 --w 3 > forge_parallel_output.log 2>&1
