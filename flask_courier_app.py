from app import app_instance

from app import enums, models, db

if models.NumerPaczki.query.first() is None:
    db.session.add(models.NumerPaczki(numerPaczki=1))
    db.session.commit()

if models.NumerZamowienia.query.first() is None:
    db.session.add(models.NumerZamowienia(numerZamowienia=1))
    db.session.commit()

for name, member in enums.PackageState.__members__.items():
    state = models.StanPaczki.query.get(member.value)
    if state is None:
        db.session.add(models.StanPaczki(stanPaczki=member.value, stanPaczkiOpis=name))
        db.session.commit()
    elif state.stanPaczkiOpis != name:
        db.session.delete(state)
        db.session.add(models.StanPaczki(stanPaczki=member.value, stanPaczkiOpis=name))
        db.session.commit()