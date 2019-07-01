$TARGET_DIR="layerdist"
$ZIPFILE="layer.zip"

Remove-Item -Recurse -ErrorAction Ignore $TARGET_DIR
python setup.py bdist_wheel
pipenv --python 3.7
pipenv run python setup.py install
pipenv run pip freeze > requirements.txt
pipenv run pip install --find-links=dist -r requirements.txt -t $TARGET_DIR

Remove-Item -ErrorAction Ignore $ZIPFILE
Compress-Archive -Path $TARGET_DIR\* -DestinationPath $ZIPFILE
