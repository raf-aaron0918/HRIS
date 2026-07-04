from sqlalchemy.orm import Session

from app.models.payroll import PayrollRun


def list_payroll_runs(db: Session) -> list[PayrollRun]:
    return db.query(PayrollRun).order_by(PayrollRun.cutoff_end.desc(), PayrollRun.id.desc()).all()


def get_payroll_run_by_id(db: Session, payroll_run_id: str) -> PayrollRun | None:
    return db.query(PayrollRun).filter(PayrollRun.payroll_run_id == payroll_run_id).first()


def create_payroll_run(db: Session, payload: dict) -> PayrollRun:
    record = PayrollRun(**payload)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_payroll_run(db: Session, record: PayrollRun, payload: dict) -> PayrollRun:
    for field, value in payload.items():
        setattr(record, field, value)

    db.add(record)
    db.commit()
    db.refresh(record)
    return record
