from dataclasses import asdict, dataclass

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = (
        "Тип тренировки: {training_type};"
        " Длительность: {duration:.3f} ч.;"
        " Дистанция: {distance:.3f} км;"
        " Ср. скорость: {speed:.3f} км/ч;"
        " Потрачено ккал: {calories:.3f}."
    )

    def get_message(self) -> str:
        return self.message.format(**asdict(self))

@dataclass
class Training:
    """
    Базовый класс тренировки.
    Хранит в себе основные методы тренировок и свойства.
    action - количество совершённых действий (число шагов при ходьбе и беге либо гребков — при плавании)
    duration_hour - длительность тренировки
    weight_kg - вес спортсмена
    """

    action: int 
    duration_hour: float
    weight_kg: float

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_hour

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Необходимо определить get_spent_calories()')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration_hour,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    RUN_coeff_1: int = 18
    RUN_coeff_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
               (self.RUN_coeff_1 * self.get_mean_speed()
                - self.RUN_coeff_2) * self.weight_kg
            / self.M_IN_KM * self.duration_hour * self.MIN_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int 
    duration_hour: float
    weight_kg: float
    height_cm: float

    WLK_coeff_1: float = 0.035
    WLK_coeff_2: float = 0.029


    def get_spent_calories(self) -> float:
        return (self.WLK_coeff_1 * self.weight_kg
                + (self.get_mean_speed() ** 2 // self.height_cm)
                * self.WLK_coeff_2
                * self.weight_kg) * (self.duration_hour * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    SWM_coeff_1: float = 1.1
    SWM_coeff_2: float = 2
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
                / self.M_IN_KM / self.duration_hour)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.SWM_coeff_1)
                * self.SWM_coeff_2 * self.weight_kg)


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
