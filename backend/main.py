from fastapi import FastAPI, HTTPException
from datetime import datetime
from models import Donor, Blood, Request
from utils import read_data, write_data

app = FastAPI()

DONOR_FILE = "../data/donors.json"
REQUEST_FILE = "../data/requests.json"
BLOOD_FILE = "../data/blood.json"


# =========================
# 🩸 ADD DONOR (WITH 90 DAYS VALIDATION)
# =========================
@app.post("/donor/add")
def add_donor(donor: Donor):
    donors = read_data(DONOR_FILE)

    # ✅ Convert to JSON-safe dict (fixes date issue)
    data = donor.model_dump(mode="json")

    # 🔥 90 DAYS VALIDATION
    for d in donors:
        if d["name"].lower() == data["name"].lower() and d["blood_group"] == data["blood_group"]:
            
            last = datetime.strptime(d["last_donation"], "%Y-%m-%d")
            new = datetime.strptime(data["last_donation"], "%Y-%m-%d")

            days = (new - last).days

            if days < 90:
                raise HTTPException(
                    status_code=400,
                    detail=f"Donor not eligible. Only {days} days passed (need 90 days)."
                )

    # ✅ Add donor
    data["id"] = len(donors) + 1
    donors.append(data)

    write_data(DONOR_FILE, donors)

    return {"msg": "Donor added successfully"}


# =========================
# 📋 GET ALL DONORS
# =========================
@app.get("/donor/all")
def get_donors():
    return read_data(DONOR_FILE)


# =========================
# ✅ ELIGIBLE DONORS (>=90 DAYS)
# =========================
@app.get("/donor/eligible")
def eligible():
    donors = read_data(DONOR_FILE)
    res = []

    for d in donors:
        last = datetime.strptime(d["last_donation"], "%Y-%m-%d")

        if (datetime.now() - last).days >= 90:
            res.append(d)

    return res


# =========================
# 🔍 SEARCH DONORS
# =========================
@app.get("/donor/search")
def search(blood_group: str):
    donors = read_data(DONOR_FILE)
    return [d for d in donors if d["blood_group"] == blood_group]


# =========================
# 🩸 ADD BLOOD
# =========================
@app.post("/blood/add")
def add_blood(blood: Blood):
    data = read_data(BLOOD_FILE)

    data.append(blood.model_dump())  # ✅ better than .dict()

    write_data(BLOOD_FILE, data)

    return {"msg": "Blood added"}


# =========================
# 📊 BLOOD AVAILABILITY
# =========================
@app.get("/blood/availability")
def availability():
    blood = read_data(BLOOD_FILE)
    summary = {}

    for b in blood:
        grp = b["blood_group"]
        summary[grp] = summary.get(grp, 0) + b["units"]

    return summary


# =========================
# 📩 CREATE REQUEST
# =========================
@app.post("/request/add")
def create_request(req: Request):
    data = read_data(REQUEST_FILE)

    r = req.model_dump()
    r["id"] = len(data) + 1

    data.append(r)

    write_data(REQUEST_FILE, data)

    return {"msg": "Request created"}


# =========================
# 📋 GET ALL REQUESTS
# =========================
@app.get("/request/all")
def get_requests():
    return read_data(REQUEST_FILE)


# =========================
# ✅ FULFILL REQUEST
# =========================
@app.put("/request/fulfill/{req_id}")
def fulfill(req_id: int):
    requests = read_data(REQUEST_FILE)
    blood = read_data(BLOOD_FILE)

    for r in requests:
        if r["id"] == req_id and r["status"] == "Pending":

            needed = r["units"]
            grp = r["blood_group"]

            total = sum(b["units"] for b in blood if b["blood_group"] == grp)

            if total < needed:
                return {"msg": "Not enough blood"}

            for b in blood:
                if b["blood_group"] == grp and needed > 0:

                    if b["units"] <= needed:
                        needed -= b["units"]
                        b["units"] = 0
                    else:
                        b["units"] -= needed
                        needed = 0

            r["status"] = "Fulfilled"

    write_data(BLOOD_FILE, blood)
    write_data(REQUEST_FILE, requests)

    return {"msg": "Request fulfilled"}