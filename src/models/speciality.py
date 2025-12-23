from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.enums import EducationLevel

if TYPE_CHECKING:
    from src.models.student_group import Group


class Speciality(Base):
    __tablename__ = "specialties"

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(String(10), index=True)
    full_name: Mapped[str] = mapped_column(String(350), unique=True)
    clean_name: Mapped[str] = mapped_column(String(256))
    level: Mapped[EducationLevel | None] = mapped_column(nullable=True)

    groups: Mapped[list["Group"]] = relationship(
        back_populates="speciality", lazy="selectin", cascade="all, delete-orphan"
    )
