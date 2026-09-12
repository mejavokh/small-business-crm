from aiogram.fsm.state import State, StatesGroup

class BookingState(StatesGroup):
    choosing_employee = State()
    choosing_date = State()
    choosing_time = State()