from openpyxl.workbook import Workbook


def write_file(packs: list[dict], file_path: str, value_set: list[str]|tuple[str]):
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()

    ws.append(value_set)

    for row in (row for pack in packs for row in zip(*(pack.values()))):
        ws.append(values for section in row for values in section)

    wb.save(file_path)