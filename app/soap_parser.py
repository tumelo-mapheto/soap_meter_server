from lxml import etree


def extract_msno(xml_data):
    root = etree.fromstring(xml_data)
    ns = {"soap": "http://schemas.xmlsoap.org/soap/envelope/"}
    body = root.find("soap:Body", namespaces=ns)
    msno_elem = body.xpath(".//@msno")
    return msno_elem[0] if msno_elem else ""
