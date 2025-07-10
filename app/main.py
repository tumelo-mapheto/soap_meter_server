from flask import Flask, request, Response
from .soap_parser import extract_msno
from .soap_responses import (
    generate_fault_response,
    generate_not_found_response,
    generate_success_response,
    generate_invalid_format_response,
)

app = Flask(__name__)


@app.route("/meter/confirm/", methods=["POST"])
def confirm_meter():
    try:
        xml_data = request.data
        msno = extract_msno(xml_data)

        if msno == "01234567891":
            response = generate_fault_response()
        elif msno == "01234567892":
            response = generate_not_found_response()
        elif msno.isdigit() and len(msno) == 11:
            response = generate_success_response(msno)
        else:
            response = generate_invalid_format_response()

        return Response(response, mimetype="text/xml")

    except Exception:
        return Response(
            generate_invalid_format_response(), mimetype="text/xml", status=500
        )
