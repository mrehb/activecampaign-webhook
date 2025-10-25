import os
import json

from dotenv import load_dotenv
import requests
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)


# Define ActiveCampaign API key, event key, domain, and list ID
load_dotenv()
ACTIVE_CAMPAIGN_API_KEY = os.environ.get('ACTIVE_CAMPAIGN_API_KEY')
TRACKING_KEY = os.environ.get('TRACKING_KEY')
API_URL = os.environ.get("API_URL")
LIST_ID = os.environ.get('LIST_ID')
TRACKING_ACTID = os.environ.get('TRACKING_ACTID')

headers = {
        "Api-Token": ACTIVE_CAMPAIGN_API_KEY,
        "Content-Type": "application/json",
    }

def find_contact(email):
    url = f"{API_URL}/api/3/contacts?email={email}"

    response = requests.get(url, headers=headers)

    return response.json()

# def update_contact(data, list_id, extra_fields):
#     url = f"{API_URL}/api/3/contact/sync"

#     payload = {
#         "contact": {
#             "email": data["email"],
            # "firstName": data.get("firstName", ""),
            # "lastName": data.get("surname", ""),
            # "address1": data.get("address1", ""),
            # "address2": data.get("address2", ""),
            # "city": data.get("city", ""),
            # "country": data.get("country", ""),
            # "postCode": data.get("postCode", ""),
            # "phone": data.get("phone", ""),
            # "state": data.get("state", ""),
            # "timezone": data.get("timezone", ""),
            # "locale": data.get("locale", ""),
            # "tags": data.get("tags", []),
            # "custom_fields": data.get("custom_fields", {}),
            # "listid": list_id,
            # "Age": extra_fields.get("Age", ""),
            # "HCP": extra_fields.get("HCP", ""),
            # "RoundsperYear": extra_fields.get("RoundsperYear", "")
#         }
#     }

#     print(f"sending request to {url}")
#     response = requests.post(url, json=payload, headers=headers)

#     if response.text.strip() == "":
#         print("Warning: Empty response received. No JSON data to parse.")
#         return None
#     return response.json()

def update_contact(customer_data, ac_id, list_id, extra_fields):
    url = f"{API_URL}/api/3/contacts/{ac_id}"
    print("AC_ID", ac_id)
    address1 = customer_data.get("address1", "")
    address2 = customer_data.get("address2", "")
    country = customer_data.get("country", "")
    city = customer_data.get("city", "")
    state = customer_data.get("state", "")
    postcode = customer_data.get("postCode", "")

    data = [
        {"field": 1, "value": extra_fields.get("Age", "")},
        {"field": 2, "value": customer_data.get("locale", "")},
        {"field": 3, "value": extra_fields.get("RoundsperYear", "")},
        {"field": 4, "value": extra_fields.get("HCP", "")},
        {"field": 7, "value": f"{address1},{address2} {city},{state} {postcode}"},
        {"field": 8, "value": country},
        {"field": 9, "value": city},
        {"field": 10, "value": postcode},
        {"field": 12, "value": address1}
    ]
    print(data)
    payload = {
        "contact": {
            "firstName": customer_data.get("firstName", ""),
            "lastName": customer_data.get("surname", ""),
            "phone": customer_data.get("phone", ""),
            "state": customer_data.get("state", ""),
            "fieldValues": data
        }
    }
    print("PAYLOAD", payload)

    print(f"sending request to {url}")
    response = requests.put(url, headers=headers, json=payload)

    if response.text.strip() == "":
        print("Warning: Empty response received. No JSON data to parse.")
        return None
    print("Update response", response.json())
    return response.json()


def track_event(contact_data, event_data, event_region):
    url = "https://trackcmp.net/event"

    if not contact_data or "email" not in contact_data:
        print("Error: Invalid contact data provided. Skipping event tracking.")
        return None
    if event_region:
        event = f"Warranty registration - {event_region}"
    else:
        event = "Warranty registration"
    payload = {
        "actid": TRACKING_ACTID,
        "key": TRACKING_KEY,
        "event": event,
        "eventdata": event_data,
        "visit": json.dumps({"email": contact_data["email"]}),
    }

    response = requests.post(url, data=payload)

    if response.text.strip() == "":
        print(f"Warning: Empty response received. No JSON data to parse. Status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
    else:
        print(response.json())
        return response.json()

def create_contact(customer_data, extra_fields, list_id):
    url = f"{API_URL}/api/3/contacts"
    customer_data["Age"] = extra_fields.get("Age", "")
    customer_data["HCP"]: extra_fields.get("HCP", "")
    customer_data["RoundsperYear"]: extra_fields.get("RoundsperYear", "")
    customer_data["listid"]: list_id
    address1 = customer_data.get("address1", "")
    address2 = customer_data.get("address2", "")
    country = customer_data.get("country", "")
    city = customer_data.get("city", "")
    state = customer_data.get("state", "")
    postcode = customer_data.get("postCode", "")

    data = [
        {"field": 1, "value": extra_fields.get("Age", "")},
        {"field": 2, "value": customer_data.get("locale", "")},
        {"field": 3, "value": extra_fields.get("RoundsperYear", "")},
        {"field": 4, "value": extra_fields.get("HCP", "")},
        {"field": 7, "value": f"{address1},{address2} {city},{state} {postcode}"},
        {"field": 8, "value": country},
        {"field": 9, "value": city},
        {"field": 10, "value": postcode},
        {"field": 12, "value": address1}
    ]
    print(data)
    payload = {
        "contact": {
            "email": customer_data.get("email", ""),
            "firstName": customer_data.get("firstName", ""),
            "lastName": customer_data.get("surname", ""),
            "phone": customer_data.get("phone", ""),
            "state": customer_data.get("state", ""),
            "fieldValues": data
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.json())

def update_contact_list(list_id, ac_id):
    url = f"{API_URL}/api/3/contactLists"

    payload = {
        "contactList": {
            "contact": ac_id,
            "list": list_id,
            "status": 1
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.json())

def create_or_update_contact(customer_data, extra_fields, list_id):
    ac_id = ""
    print(customer_data["email"])
    data = find_contact(customer_data["email"])
    if "contacts" in data and data["contacts"]:
        ac_id = data["contacts"][0]["id"]
        print(ac_id)
    if not ac_id:
        "creating contact"
        create_contact(customer_data, extra_fields, list_id)
        # Ага
    else:
        print("updating contact")
        update_contact(customer_data, ac_id, list_id, extra_fields)
        update_contact_list(list_id, ac_id)

@app.route("/webhook", methods=["POST"])
def process_webhook():
    data = request.json
    customer_data = data["customer"]
    items_data = data["items"]
    list_id = request.args.get('list_id')
    event_region = request.args.get('event_region')

    extra_fields = {}
    if items_data[0]["Age"]:
        extra_fields["Age"] = items_data[0]["Age"]
    if items_data[0]["HCP"]:
        extra_fields["HCP"] = items_data[0]["HCP"]
    if items_data[0]["RoundsperYear"]:
        extra_fields["RoundsperYear"] = items_data[0]["RoundsperYear"]

    create_or_update_contact(customer_data, extra_fields, list_id)

    for item in items_data:
        event_data = item["product"]["title"]
        track_event(customer_data, event_data, event_region)


    return jsonify({
        "status": "success",
        })


if __name__ == "__main__":
    # For development only - Railway will use Gunicorn in production
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)


# {
#     "payload": {
#         "customer": {
#             "firstName": "Test name",
#             "surname": "Test Name",
#             "email": "test@test.com",
#             "address1": "Osv",
#             "address2": "",
#             "city": "City",
#             "country": "UA",
#             "postCode": "123123",
#             "phone": "1233211221",
#             "acceptMarketingOnAccountCreation": true,
#             "state": "Kyiv City",
#             "timezone": "Europe/Kiev",
#             "locale": "uk"
#         },
#         "sendEmails": true,
#         "items": [
#             {
#                 "product": {
#                     "imageUrl": "https://cdn.shopify.com/s/files/1/0712/7469/2920/products/BM_Aqua_Eight_WBO_2560_2560_Main.jpg?v=1682093190",
#                     "id": 8094986043704,
#                     "title": "AQUA Eight",
#                     "handle": "aqua-eight"
#                 },
#                 "serialNumbers": [
#                     "Test"
#                 ],
#                 "purchaseDate": "2023-05-10",
#                 "serialNumbers1": [
#                     "123321"
#                 ],
#                 "InvoiceUpload": "https://product-reg.varify.xyz/files/serve/bigmax-warranty/big-max-golf-eu/qmbjvHCM6Y_1683793548864_chrome_uofx6csCYA.png",
#                 "Age": "18-24",
#                 "HCP": "0-10",
#                 "RoundsperYear": "1-5",
#                 "Iwouldliketosupportyouinproductdevelopmentandamhappytotakepartinsurveys": "",
#                 "MarektingInformation": "I agree to receive marketing information in accordance with the Golf Tech Terms and Conditions.",
#                 "PrivacyPolicy": "I agree to the Golf Tech privacy policy. ",
#                 "TermsandConditions": "I agree to the Golf Tech Terms and Conditions."
#             }
#         ]
#     },
#     "freeFormSlug": "product-registration"
# }