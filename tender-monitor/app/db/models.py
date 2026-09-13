from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Tender(Base):

    __tablename__ = "tenders"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    law: Mapped[str] = mapped_column(
        String(20),
        default="223-ФЗ",
        nullable=False,
    )

    notice_number: Mapped[str | None] = mapped_column(
        String(255),
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    customer_name: Mapped[str | None] = mapped_column(
        Text,
    )

    customer_inn: Mapped[str | None] = mapped_column(
        String(32),
    )

    okpd_code: Mapped[str | None] = mapped_column(
        String(64),
    )

    okpd_name: Mapped[str | None] = mapped_column(
        Text,
    )

    price: Mapped[float | None] = mapped_column(
        Numeric(20, 2),
    )

    currency: Mapped[str | None] = mapped_column(
        String(16),
    )

    region: Mapped[str | None] = mapped_column(
        String(255),
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    status: Mapped[str | None] = mapped_column(
        String(255),
    )

    match_type: Mapped[str | None] = mapped_column(
        String(64),
    )

    canonical_url: Mapped[str | None] = mapped_column(
        Text,
    )

    fingerprint: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    sources = relationship(
        "TenderSource",
        back_populates="tender",
        cascade="all, delete-orphan",
    )

    documents = relationship(
        "Document",
        back_populates="tender",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index(
            "ix_tenders_notice",
            "notice_number",
        ),
        Index(
            "ix_tenders_okpd",
            "okpd_code",
        ),
        Index(
            "ix_tenders_deadline",
            "deadline",
        ),
    )


class TenderSource(Base):

    __tablename__ = "tender_sources"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    tender_id: Mapped[int] = mapped_column(
        ForeignKey("tenders.id", ondelete="CASCADE"),
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    external_id: Mapped[str | None] = mapped_column(
        String(255),
    )

    url: Mapped[str | None] = mapped_column(
        Text,
    )

    first_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    tender = relationship(
        "Tender",
        back_populates="sources",
    )

    __table_args__ = (
        UniqueConstraint(
            "source",
            "external_id",
            name="uq_source_external",
        ),
    )


class RawTender(Base):

    __tablename__ = "raw_tenders"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    source: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    external_id: Mapped[str | None] = mapped_column(
        String(255),
    )

    payload: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    payload_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )


class CollectorRun(Base):

    __tablename__ = "collector_runs"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    source: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    received_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    new_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    error_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    status: Mapped[str] = mapped_column(
        String(32),
        default="RUNNING",
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
    )


class Document(Base):

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    tender_id: Mapped[int] = mapped_column(
        ForeignKey("tenders.id", ondelete="CASCADE"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    local_path: Mapped[str | None] = mapped_column(
        Text,
    )

    mime_type: Mapped[str | None] = mapped_column(
        String(255),
    )

    sha256: Mapped[str | None] = mapped_column(
        String(64),
    )

    extracted_text: Mapped[str | None] = mapped_column(
        Text,
    )

    downloaded: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    tender = relationship(
        "Tender",
        back_populates="documents",
    )
