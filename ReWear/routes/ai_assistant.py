from flask import Blueprint, render_template, request, jsonify

from services.ai_service import analyze_bulk_donation


ai_assistant = Blueprint(
    "ai_assistant",
    __name__,
    url_prefix="/ai"
)


@ai_assistant.route("/bulk-donation")
def bulk_donation_page():
    return render_template("donor/bulk_donation.html")


@ai_assistant.route("/bulk-donation/analyze", methods=["POST"])
def analyze_donation():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No data received."
        }), 400

    description = data.get("description", "").strip()

    if not description:
        return jsonify({
            "success": False,
            "error": "Please describe your donation."
        }), 400

    try:
        result = analyze_bulk_donation(description)

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
