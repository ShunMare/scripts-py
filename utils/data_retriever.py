def get_flag(excel_handler, first_row_index, column_indices):
    """フラグを取得する"""
    flag_value = excel_handler.ws.cell(
        row=first_row_index, column=column_indices["flag"]
    ).value
    print(f"Raw flag value: {flag_value}")
    if not excel_handler.is_cell_empty_or_match(
        first_row_index, column_indices["flag"], 1.0
    ):
        return flag_value
    return ""


def get_theme(excel_handler, first_row_index, column_indices):
    """テーマを取得する"""
    theme_value = excel_handler.ws.cell(
        row=first_row_index, column=column_indices["theme"]
    ).value
    print(f"Raw theme value: {theme_value}")
    if not excel_handler.is_cell_empty_or_match(
        first_row_index, column_indices["theme"]
    ):
        return str(theme_value)
    return ""


def get_heading(excel_handler, first_row_index, column_indices):
    """見出しを取得する"""
    heading_value = excel_handler.ws.cell(
        row=first_row_index, column=column_indices["heading"]
    ).value
    print(f"Raw heading value: {heading_value}")
    if not excel_handler.is_cell_empty_or_match(
        first_row_index, column_indices["heading"]
    ):
        return str(heading_value)
    return ""


def get_evidences(excel_handler, column_indices, group):
    """エビデンスを取得する"""
    evidences = []
    for row_index in range(group.index[0] + 2, group.index[-1] + 3):
        evidence_value = excel_handler.ws.cell(
            row=row_index, column=column_indices["evidence"]
        ).value
        print(f"Raw evidence value: {evidence_value}")
        if not excel_handler.is_cell_empty_or_match(
            row_index, column_indices["evidence"]
        ):
            evidences.append(str(evidence_value))
    return evidences


def check_flag_and_evidences(flag, evidences, first_row_index):
    """フラグとエビデンスの両方をチェックし、条件を満たさない場合は処理をスキップする"""
    if flag == "":
        print(f"Skipping group: No valid flag found. First row: {first_row_index}")
        return False
    if len(evidences) == 0:
        print(f"Skipping group: No evidences found. First row: {first_row_index}")
        return False
    print("Flag and evidences are valid.")
    return True
