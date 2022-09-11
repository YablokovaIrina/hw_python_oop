class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        # Имя класса тренировки.
        self.training_type = training_type
        # Длительность тренировки в часах.
        self.duration = duration
        # Дистанция в километрах, которую преодолел пользователь
        # за время тренировки.
        self.distance = distance
        # Средняя скорость, с которой двигался пользователь.
        self.speed = speed
        # Количество килокалорий, которое израсходовал пользователь
        # за время тренировки.
        self.calories = calories

    # Числовые значения должны округляться при выводе
    # до тысячных долей (до третьего знака после запятой).
    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""

    # Расстояние, которое спортсмен преодолевает за один шаг.
    LEN_STEP: float = 0.65
    # Константа для перевода значений из метров в километры.
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        # Количество совершённых действий
        # (число шагов при ходьбе и беге либо гребков — при плавании).
        self.action = action
        # Длительность тренировки.
        self.duration = duration
        # Вес спортсмена.
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    coeff_calorie_RUN_1: int = 18
    coeff_calorie_RUN_2: int = 20
    # Время тренировки в минутах.
    TIME_IN_MIN: int = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
               (self.coeff_calorie_RUN_1 * self.get_mean_speed()
                - self.coeff_calorie_RUN_2) * self.weight
            / self.M_IN_KM * self.duration * self.TIME_IN_MIN
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_calorie_WLK_1: float = 0.035
    coeff_calorie_WLK_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # Рост спортсмена.

    def get_spent_calories(self) -> float:
        return (self.coeff_calorie_WLK_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.coeff_calorie_WLK_2
                * self.weight) * (self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""

    coeff_calorie_SWM_1: float = 1.1
    coeff_calorie_SWM_2: float = 2
    # Расстояние, которое спортсмен преодолевает за один гребок.
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        # Длина бассейна в метрах.
        self.length_pool = length_pool
        # Сколько раз пользователь переплыл бассейн.
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавании."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.coeff_calorie_SWM_1)
                * self.coeff_calorie_SWM_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training: dict = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}
    return training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
