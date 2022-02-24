# kube-config
### Utility to auto-generate the KUBECONFIG file (~/.kube/config)

---

## How to run:
#### - Prerequisites
1) Ensure you have the AWS DevOpsRole
2) Ensure you have aws profile `[profile prod-admin]` setup in `~/.aws/credentials` (required for the boto3 session)

#### - Setup
1) Edit `kube-config/config/config.ini` properties accordingly
2) Via a terminal, navigate to `kube-config/`
3) Make a virtual environment directory: `mkdir ./venv`
4) Start your virtual environment: `python -m venv ./venv`
5) Install required modules: `pip install -r requirements.txt`

#### - Run
1) To run the  script: `python3 app.py`
2) You will be prompted to confirm the config.
3) After a few seconds the config file will generate and save to your set OUTPUT_PATH in config.ini. You will need to move this to `~/.kube/config`

