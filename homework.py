from dataclasses import dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def __repr__(self) -> str:
        return (
            'Тип тренировки: {training_type}; '
            'Длительность: {duration:.3f} ч.; '
            'Дистанция: {distance:.3f} км; '
            'Ср. скорость: {speed:.3f} км/ч; '
            'Потрачено ккал: {calories:.3f}.'
        )

    def get_message(self) -> str:
        return repr(self).format(
            training_type=self.training_type, duration=self.duration,
            distance=self.distance, speed=self.speed,
            calories=self.calories
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration  # Длительность тренировки в часах
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
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    COEFF_DIST: int = 18
    COEFF_SP_DIV_TIME: int = 20

    def get_spent_calories(self) -> float:
        return (
            (
                self.COEFF_DIST * super().get_mean_speed()
                - self.COEFF_SP_DIV_TIME
            ) * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_SP_DIV_TIME: float = 0.035
    COEFF_DIST: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:

        return (
            (
                self.COEFF_SP_DIV_TIME * self.weight
                + (super().get_mean_speed() ** 2 // self.height)
                * self.COEFF_DIST * self.weight
            ) * self.duration * self.MIN_IN_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_SPEED_CORR: float = 1.1
    COEFF_SPEED: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (
                self.get_mean_speed() + self.COEFF_SPEED_CORR
            ) * self.COEFF_SPEED * self.weight
        )


def read_package(workout_type: str, data: List) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts: Dict[str, Type] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    try:
        return workouts[workout_type](*data)
    except KeyError:
        print('Неизвестный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    try:
        info: InfoMessage = training.show_training_info()
        print(info.get_message())
    except AttributeError:
        print('', end='')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
