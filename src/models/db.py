from schemas.cars import Car, Color

CARS = {
    1: Car(id=1, name="BMW", color=Color.blue),
    2: Car(id=2, name="Mercedes", color=Color.blue),
    3: Car(id=3, name="Audi", color=Color.white, details="awesome car"),
}
