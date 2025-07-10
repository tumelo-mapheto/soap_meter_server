# SOAP Meter Confirmation Server

A Python-based SOAP web service that processes meter confirmation requests and returns dynamic SOAP/XML responses based on the meter number (`msno`).

---

## Features

- Exposes a `/meter/confirm/` HTTP POST endpoint accepting SOAP/XML requests.
- Parses incoming SOAP requests to extract the meter number (`msno`).
- Returns different SOAP responses based on the `msno` value:
  - **01234567890**: Returns a SOAP response with `(success)`.
  - **01234567891**: Returns a SOAP response with `(specified fault)`.
  - **01234567892**: Returns a SOAP response with `("Meter not Found" response)`.
  - **123** (not exactly 11 digits): Returns a SOAP response with `(invalid format fault)`.

---

## Tech Stack

- Python 3.11+
- Flask 2.3.3
- lxml 6.0.0

---

## Getting Started

### Prerequisites

- Python 3.11 or later
- `pip` package manager

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/soap-meter-server.git
   cd soap-meter-server
   ```

2. Create and activate a virtual environment:

   - On Windows:

     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Server

```bash
python run.py
```

Server runs on:
**[http://localhost:5000/meter/confirm/](http://localhost:5000/meter/confirm/)**

---

## Testing

### Using `curl`

---

#### ✅ Success – `msno=01234567890`

```bash
curl -X POST http://localhost:5000/meter/confirm/ -H "Content-Type: text/xml" --data-binary @tests/payloads/success.xml
```

**Expected:**

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <confirmMeterResp xmlns:b0="http://www.nrs.eskom.co.za/xmlvend/base/2.1/schema"
        xmlns:r0="http://www.nrs.eskom.co.za/xmlvend/revenue/2.1/schema"
        xmlns="http://www.nrs.eskom.co.za/xmlvend/meter/2.1/schema">
      <b0:clientID xsi:type="b0:GenericDeviceID" id="6004708000090"/>
      <b0:serverID xsi:type="b0:EANDeviceID" ean="0123123456789"/>
      <b0:terminalID xsi:type="b0:GenericDeviceID" id="6004708000090"/>
      <b0:reqMsgID dateTime="22222222222222222" uniqueNumber="2222222"/>
      <b0:respDateTime>2025-07-10T02:39:06.951608</b0:respDateTime>
      <b0:dispHeader>Confirm Meter Details</b0:dispHeader>
      <confirmMeterResult>
        <meterDetail xsi:type="b0:ExtMeterDetail" msno="01234567890" sgc="100836" krn="2" ti="07">
          <b0:meterType at="07" tt="02"/>
        </meterDetail>
      </confirmMeterResult>
    </confirmMeterResp>
  </soap:Body>
</soap:Envelope>
```

---

#### ❌ Fault – `msno=01234567891`

```bash
curl -X POST http://localhost:5000/meter/confirm/ -H "Content-Type: text/xml" --data-binary @tests/payloads/fault.xml
```

**Expected:**

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <soap:Fault>
      <faultcode>soap:Server</faultcode>
      <faultstring>010038 Meter information not found</faultstring>
      <faultactor>http://onlinevending.eskom.co.za/OVS/WS/Actaris.WSNRS21EskomFull/WSActaris.asmx</faultactor>
      <detail>
        <b0:xmlvendFaultResp xmlns:r0="http://www.nrs.eskom.co.za/xmlvend/revenue/2.1/schema"
            xmlns:b0="http://www.nrs.eskom.co.za/xmlvend/base/2.1/schema">
          <b0:clientID d3p1:type="b0:GenericDeviceID" id="6004708000090"
              xmlns:d3p1="http://www.w3.org/2001/XMLSchema-instance"/>
          <b0:serverID d3p1:type="b0:EANDeviceID" ean="0123123456789"
              xmlns:d3p1="http://www.w3.org/2001/XMLSchema-instance"/>
          <b0:terminalID d3p1:type="b0:GenericDeviceID" id="6004708000090"
              xmlns:d3p1="http://www.w3.org/2001/XMLSchema-instance"/>
          <b0:reqMsgID dateTime="22222222222222222" uniqueNumber="2222222"/>
          <b0:respDateTime>2025-07-10T02:39:45.736627</b0:respDateTime>
          <b0:dispHeader>ONLINE ERROR</b0:dispHeader>
          <b0:operatorMsg>Meter information not found,cannot process request. Contact Eskom to register meter</b0:operatorMsg>
          <b0:custMsg>Meter not found.Contact Eskom to register meter</b0:custMsg>
          <b0:fault d3p1:type="b0:UnknownMeterEx"
              xmlns:d3p1="http://www.w3.org/2001/XMLSchema-instance">
            <b0:desc>010038 Meter information not found</b0:desc>
          </b0:fault>
        </b0:xmlvendFaultResp>
      </detail>
    </soap:Fault>
  </soap:Body>
</soap:Envelope>
```

---

#### ⚠️ Not Found – `msno=01234567892`

```bash
curl -X POST http://localhost:5000/meter/confirm/ -H "Content-Type: text/xml" --data-binary @tests/payloads/not_found.xml
```

**Expected:**

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <confirmMeterResp>
      <message>Meter not Found</message>
    </confirmMeterResp>
  </soap:Body>
</soap:Envelope>
```

---

#### 🚫 Invalid Format – `msno=123`

```bash
curl -X POST http://localhost:5000/meter/confirm/ -H "Content-Type: text/xml" --data-binary @tests/payloads/invalid.xml
```

**Expected:**

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <soap:Fault>
      <faultcode>soap:Client</faultcode>
      <faultstring>Invalid meter number format</faultstring>
    </soap:Fault>
  </soap:Body>
</soap:Envelope>
```

---

### Using Python Test Script

```bash
python tests/test_cases.py
```

Runs all defined cases and prints responses to console.

---

## Project Structure

```
soap-meter-server/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # Flask app and endpoint
│   ├── soap_parser.py       # XML parsing utilities
│   ├── soap_responses.py    # SOAP response templates
│   └── utils.py             # Helpers (e.g. timestamp)
│
├── tests/
│   ├── test_cases.py        # Automated test runner
│   └── payloads/
│       ├── success.xml
│       ├── fault.xml
│       ├── not_found.xml
│       └── invalid.xml
│
├── run.py
├── requirements.txt
└── README.md
```

---

## Notes

- All responses are fully SOAP 1.1-compliant.
- XMLs are generated dynamically via `lxml`.
- Input validation and fault handling are consistent with Eskom’s schema expectations.

---

## License

MIT License
