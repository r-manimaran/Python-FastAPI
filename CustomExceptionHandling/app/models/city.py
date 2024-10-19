from sqlalchemy.orm import mapped_column, Mapped, relationship
from . import Base
from sqlalchemy import ForeignKey

class city(base):
    __tablename__ = "city"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    state_id: Mapped[int] = mapped_column(ForeignKey("state.id"))
    state: Mapped["state"] = relationship(back_populates="city") 