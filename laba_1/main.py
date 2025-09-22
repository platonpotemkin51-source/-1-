def two_sum(nums, target):
    if type(nums) != type([]): # прописываем ошибки
        raise ValueError('Ошибка! Неверный тип данных.')
    if type(target) != type(1):
        raise ValueError('Ошибка! Неверный тип данных.')
    for i in range(len(nums)):
        if type(nums[i]) != type(1):
            raise ValueError('Ошибка! Неверный тип данных.')
    if len(nums) < 2:
        raise ValueError('Ошибка! Недостаточно чисел в nums.')

    for i in range(len(nums) - 1): # сама функция
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                res = [i, j]
                return res
