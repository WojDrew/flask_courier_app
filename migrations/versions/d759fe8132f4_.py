"""empty message

Revision ID: d759fe8132f4
Revises: 1ecc3bbb4cd5
Create Date: 2020-11-07 18:44:30.938266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd759fe8132f4'
down_revision = '1ecc3bbb4cd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stanPaczki',
    sa.Column('stanPaczki', sa.Integer(), nullable=False),
    sa.Column('stanPaczkiOpis', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('stanPaczki')
    )
    op.create_table('zamowienie',
    sa.Column('idZamowienie', sa.Integer(), nullable=False),
    sa.Column('idKurier', sa.Integer(), nullable=True),
    sa.Column('idKlient', sa.Integer(), nullable=True),
    sa.Column('adresDostawcy', sa.String(length=256), nullable=True),
    sa.Column('adresNadawcy', sa.String(length=256), nullable=True),
    sa.Column('calkowityKosztDostawy', sa.Float(precision=8), nullable=True),
    sa.Column('dataDostawy', sa.Date(), nullable=True),
    sa.Column('dataZaplaty', sa.DateTime(), nullable=True),
    sa.Column('przewidywanaGodzinaDostawy', sa.DateTime(), nullable=True),
    sa.Column('zrealizowana', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['idKlient'], ['klient.id'], ),
    sa.ForeignKeyConstraint(['idKurier'], ['kurier.id'], ),
    sa.PrimaryKeyConstraint('idZamowienie')
    )
    op.create_table('paczka',
    sa.Column('idPaczka', sa.Integer(), nullable=False),
    sa.Column('idZamowienie', sa.Integer(), nullable=True),
    sa.Column('dataOdbioru', sa.DateTime(), nullable=True),
    sa.Column('kod', sa.String(length=128), nullable=True),
    sa.Column('waga', sa.Float(precision=8), nullable=True),
    sa.Column('stanPaczki', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['idZamowienie'], ['zamowienie.idZamowienie'], ),
    sa.ForeignKeyConstraint(['stanPaczki'], ['stanPaczki.stanPaczki'], ),
    sa.PrimaryKeyConstraint('idPaczka')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('paczka')
    op.drop_table('zamowienie')
    op.drop_table('stanPaczki')
    # ### end Alembic commands ###
