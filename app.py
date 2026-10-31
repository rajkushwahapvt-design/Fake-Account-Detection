from flask import Flask, request, jsonify, render_template
import joblib, pandas as pd
import re
from train import FEATURES

app = Flask(__name__)
model = joblib.load("model.pkl")

DISPOSABLE = {"mailinator.com", "10minutemail.com", "tempmail.com",
              "guerrillamail.com", "yopmail.com"}


def digit_ratio(text):
    return sum(c.isdigit() for c in text) / len(text) if text else 0


def check_email(email):
    email = email.strip().lower()
    if not email:
        return None
    if not re.fullmatch(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", email):
        return {"valid": False, "msg": "Email format galat hai"}
    local, domain = email.split("@")
    if domain in DISPOSABLE:
        return {"valid": False, "msg": "Temporary/disposable email hai"}
    if domain == "gmail.com":
        ok = (re.fullmatch(r"[a-z0-9.]{6,30}", local)
              and not local.startswith(".") and not local.endswith(".")
              and ".." not in local)
        if not ok:
            return {"valid": False, "msg": "Gmail ke rules ke hisaab se invalid hai"}
        return {"valid": True, "msg": "Valid Gmail address"}
    return {"valid": True, "msg": "Valid email (Gmail nahi hai: " + domain + ")"}


def get_reasons(row):
    r = []
    if not row["profile_pic"]:
        r.append("No Profile Picture")
    if row["username_digit_ratio"] > 0.4:
        r.append("Username Contains a lot of Digits")
    if row["fullname_words"] == 0:
        r.append("Full name is Empty")
    if row["bio_length"] == 0:
        r.append("Bio is Empty")
    if row["posts"] == 0:
        r.append("No Post")
    if row["following"] > 500 and row["followers"] / max(row["following"], 1) < 0.1:
        r.append("Huge Following, Less Followers")
    return r


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    d = request.get_json()
    username = d.get("username", "").strip()
    fullname = d.get("fullname", "").strip()

    row = {
        "profile_pic": int(d.get("profile_pic", 0)),
        "username_digit_ratio": digit_ratio(username),
        "fullname_words": len(fullname.split()),
        "fullname_digit_ratio": digit_ratio(fullname),
        "name_equals_username": int(fullname.lower().replace(" ", "") == username.lower()),
        "bio_length": len(d.get("bio", "")),
        "external_url": int(d.get("external_url", 0)),
        "private": int(d.get("private", 0)),
        "posts": int(d.get("posts", 0) or 0),
        "followers": int(d.get("followers", 0) or 0),
        "following": int(d.get("following", 0) or 0),
    }

    prob_fake = model.predict_proba(pd.DataFrame([row])[FEATURES])[0][1]

    email_info = check_email(d.get("email", ""))
    reasons = get_reasons(row)
    if email_info and not email_info["valid"]:
        reasons.append("Email suspicious: " + email_info["msg"])

    return jsonify({
        "fake_probability": round(prob_fake * 100, 1),
        "label": "Fake" if prob_fake >= 0.5 else "Real",
        "reasons": reasons,
        "email": email_info,
        "ratio": round(row["followers"] / max(row["following"], 1), 2),
    })


if __name__ == "__main__":
    app.run(debug=True)