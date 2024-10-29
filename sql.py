def min_weight_for_balance(masses, max_diff):
    # Разворачиваем массив масс, чтобы проще было обращаться по именам
    A, B, C = masses

    # Создаем все возможные парные комбинации детей
    possible_combinations = [
        ((A + B), C),  # Комбинация: Аня и Боря против Саши
        ((A + C), B),  # Комбинация: Аня и Саша против Боря
        ((B + C), A),  # Комбинация: Боря и Саша против Ани
    ]

    # Инициализируем переменную для хранения минимального веса камня
    # Устанавливаем начальное значение для минимального камня как "бесконечность"
    min_stone_weight = float('inf')

    # Проверяем каждую комбинацию
    for left_weight, right_weight in possible_combinations:
        # Чтобы держать баланс, разница масс не должна превышать max_diff.
        # Если разница > max_diff, рассчитываем необходимый вес камня.
        if abs(left_weight - right_weight) <= max_diff:
            # Качели уже сбалансированы, камень не нужен
            return 0
        else:
            # Рассчитываем необходимый вес камня для балансировки
            stone_weight = abs(left_weight - right_weight) - max_diff
            # Обновляем минимальный вес камня, если найден меньший
            min_stone_weight = min(min_stone_weight, stone_weight)

    return min_stone_weight


A = int(input())
B = int(input())
C = int(input())
D = int(input())
# Вызываем функцию
result = min_weight_for_balance([A, B, C], D)
print(f"Минимальный вес камня: {result} кг")