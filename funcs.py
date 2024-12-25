def design_buttons(buttons, names_per_row=2):
    """
    Функция группирует кнопки в списки по заданному количеству.

    Args:
      buttons: Список кнопок.
      names_per_row: Количество кнопок в одной строке.

    Returns:
      Список списков с кнопками, сгруппированными по заданному количеству.
    """
    grouped_names = []
    current_row = []
    for i, name in enumerate(buttons):
        current_row.append(name)
        if (i + 1) % names_per_row == 0 or i == len(buttons) - 1:
            grouped_names.append(current_row)
            current_row = []

    return grouped_names