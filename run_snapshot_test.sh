echo "Running CDK Synth"

if ! [[ -v AWS_ACCOUNT_ID ]]
then
    echo 'AWS_ACCOUNT_ID not set. Setting it to 948045320516'
    export AWS_ACCOUNT_ID=948045320516
fi

if ! [[ -v AWS_REGION]]
then
    echo 'AWS region not set. Setting it to us-east-1'
    export AWS_REGION = 'us-east-1'
fi

if ! [[ -v AWS_ENVIRONMENT]]
then
    echo 'AWS_ENVIRONMENT not set. Setting it to dev'
    export AWS_ENVIRONMENT = 'dev'
fi

export AWS_ENVIRONMENT
export AWS_REGION

pushd infra/cdk
cdk synth --output cdk.out/$AWS_ENVIRONMENT/$AWS_REGION
popd

echo 'Running cfn template snashot test'
pushd infra/cdk
python -m pytest tests/snapshot/
popd