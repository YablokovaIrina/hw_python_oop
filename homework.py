from dataclasses import asdict, dataclass
from typing import Callable, List, ClassVar, Dict


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
    action - количество совершённых действий
    duration_hour - длительность тренировки
    weight_kg - вес спортсмена
    LEN_STEP - длина шага
    M_IN_KM - константа для перевода значений из метров в километры
    MIN_IN_H - константа для перевода значений из часа в минуты
    """

    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_H: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Необходимо определить get_spent_calories()")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    RUN_coeff_1: ClassVar[int] = 18
    RUN_coeff_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.RUN_coeff_1 * self.get_mean_speed() - self.RUN_coeff_2)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба.
    height_cm - рост спортсмена.
    """

    height: float

    WLK_coeff_1: ClassVar[float] = 0.035
    WLK_coeff_2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        return (
            self.WLK_coeff_1 * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * self.WLK_coeff_2
            * self.weight
        ) * (self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """
    Тренировка: плавание.
    LEN_STEP - длина гребка
    length_pool - длина бассейна (в метрах)
    count_pool - сколько раз пользователь переплыл бассейн
    """

    length_pool: float
    count_pool: float

    SWM_coeff_1: ClassVar[float] = 1.1
    SWM_coeff_2: ClassVar[float] = 2
    LEN_STEP: ClassVar[float] = 1.38

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавании."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.SWM_coeff_1)
            * self.SWM_coeff_2
            * self.weight
        )


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training: Dict[str, Callable] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    return training[workout_type](*data)


def main(training: Training) -> None:
    print(training.show_training_info().get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
