$ZIPFILE="layer.zip"

If (!(Test-Path $ZIPFILE)) {
    Write-Error -Category ObjectNotFound -TargetObject $ZIPFILE "$ZIPFILE not found. Run build-layer first."
    exit
} 

aws lambda publish-layer-version `
    --layer-name LambdaLogger `
    --description 'An opinionated structured logging decorator for Python Lambda functions' `
    --compatible-runtimes python3.6 python3.7 `
    --zip-file fileb://layer.zip `
    --query LayerVersionArn `
    --output text
