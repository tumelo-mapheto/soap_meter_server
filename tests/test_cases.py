import requests


def run_test(file_path, label):
    with open(file_path, "rb") as f:
        response = requests.post(
            "http://localhost:5000/meter/confirm/",
            data=f.read(),
            headers={"Content-Type": "text/xml"},
        )
        print(f"--- {label} ---")
        print(response.text)
        print()


if __name__ == "__main__":
    run_test("tests/payloads/success.xml", "Test: Success (01234567890)")
    run_test("tests/payloads/fault.xml", "Test: Fault (01234567891)")
    run_test("tests/payloads/not_found.xml", "Test: Not Found (01234567892)")
    run_test("tests/payloads/invalid.xml", "Test: Invalid Format")
