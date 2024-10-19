from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship,mapped_column,Mapped

from . import Base

class weather(Base):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    temperature: Mapped[int]
    pressure: Mapped[int]
    wind_speed: Mapped[int]
    date: Mapped[str]

    city: Mapped["city"] = relationship(back_populates="weather")

    def __repr__(self):
        return f"Weather(id={self.id!r}, city_id={self.city_id!r}, temperature={self.temperature!r}, pressure={self.pressure!r}, wind_speed={self.wind_speed!r}, date={self.date!r})"