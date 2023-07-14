import xml.etree.ElementTree as ET
from openpyxl import Workbook

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    data = []

    for trade in root.findall(".//{http://www.fixprotocol.org/FIXML-4-4}TrdCaptRpt"):
        quantity = trade.find(".//{http://www.fixprotocol.org/FIXML-4-4}Quantity").text
        cfi = trade.find(".//{http://www.fixprotocol.org/FIXML-4-4}Instrmt").get("CFI")
        side = trade.find(".//{http://www.fixprotocol.org/FIXML-4-4}RptSide").get("Side")
        pty_id = trade.find(".//{http://www.fixprotocol.org/FIXML-4-4}RptSide/{http://www.fixprotocol.org/FIXML-4-4}Pty").get("ID")
        pty_r = trade.find(".//{http://www.fixprotocol.org/FIXML-4-4}RptSide/{http://www.fixprotocol.org/FIXML-4-4}Pty").get("R")
        customer_type = trade.find(".//{http://www.fixprotocol.org/FIXML-4-4}RptSide/{http://www.fixprotocol.org/FIXML-4-4}Pty").get("AR")

        data.append((quantity, cfi, side, pty_id, pty_r, customer_type))

    return data

def summarize_data(data):
    summary = {}

    for row in data:
        quantity, cfi, side, pty_id, pty_r, customer_type = row

        if customer_type == "C":
            if pty_r == "14":
                key = (cfi, side, "Ultimate Clearing Firm")
                if key in summary:
                    summary[key].append(pty_id)
                else:
                    summary[key] = [pty_id]
            elif pty_r == "18":
                key = (cfi, side, "Ultimate Clearing Firm")
                if key not in summary:
                    summary[key] = [pty_id]
            elif pty_r == "1":
                key = (cfi, side, "Ultimate Clearing Firm")
                if key not in summary:
                    summary[key] = [pty_id]

            if pty_r == "2":
                key = (cfi, side, "Entering Firm")
                if key in summary:
                    summary[key].append(pty_id)
                else:
                    summary[key] = [pty_id]
            elif pty_r == "18":
                key = (cfi, side, "Entering Firm")
                if key not in summary:
                    summary[key] = [pty_id]
            elif pty_r == "1":
                key = (cfi, side, "Entering Firm")
                if key not in summary:
                    summary[key] = [pty_id]

        if customer_type == "F":
            if pty_r == "2":
                key = (cfi, side, "Entering Firm")
                if key in summary:
                    summary[key].append(pty_id)
                else:
                    summary[key] = [pty_id]
            elif pty_r == "18":
                key = (cfi, side, "Entering Firm")
                if key not in summary:
                    summary[key] = [pty_id]
            elif pty_r == "1":
                key = (cfi, side, "Entering Firm")
                if key not in summary:
                    summary[key] = [pty_id]

        if customer_type == "M":
            if pty_r == "2":
                key = (cfi, side, "Entering Firm")
                if key in summary:
                    summary[key].append(pty_id)
                else:
                    summary[key] = [pty_id]
            elif pty_r == "18":
                key = (cfi, side, "Entering Firm")
                if key not in summary:
                    summary[key] = [pty_id]
            elif pty_r == "1":
                key = (cfi, side, "Entering Firm")
                if key not in summary:
                    summary[key] = [pty_id]

    return summary

def write_to_excel(summary, output_file):
    wb = Workbook()
    ws = wb.active

    headers = ["Customer / Market Maker", "Side", "Ultimate Clearing Firm (OCC#)", "Total Qty"]
    ws.append(headers)

    for key, values in summary.items():
        cfi, side, customer_type = key
        total_qty = len(values)
        row_data = [customer_type, side, ",".join(values), total_qty]
        ws.append(row_data)

    wb.save(output_file)
    print("Excel file saved successfully.")

# Main execution
xml_file = "input.xml"  # Path to your XML file
output_file = "output.xlsx"  # Output Excel file path

data = parse_xml(xml_file)
summary = summarize_data(data)
write_to_excel(summary, output_file)
