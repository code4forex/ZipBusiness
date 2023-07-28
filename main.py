from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os


app = Flask(__name__)


load_dotenv()


api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
reg_headers = {
    "Authorization": f"sso-key {api_key}:{api_secret}",
    "accept": "application/json"
}


def get_reg_url(check_domain):
    return f"https://api.godaddy.com/v1/domains/available?domain={check_domain}&checkType=FULL&forTransfer=false"


def check_domain_available(check_domain):
    reg_url = get_reg_url(check_domain)
    req = requests.get(reg_url, headers=reg_headers)

    if req.status_code != 200:
        return {"message": "Could not complete the request"}, 500

    response = req.json()
    if response["available"]:
        return {"message": f"Domain {check_domain} is available!"}, 200
    else:
        return {"message": f"Domain {check_domain} is not available"}, 200


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/checkdomain", methods=["POST"])
def check_domain_route():
    domain_name = request.form.get("domain_name")
    if not domain_name:
        return {"message": "Domain name is required"}, 400

    result, status_code = check_domain_available(domain_name)
    return jsonify(result), status_code



if __name__ == '__main__':
    app.run()
