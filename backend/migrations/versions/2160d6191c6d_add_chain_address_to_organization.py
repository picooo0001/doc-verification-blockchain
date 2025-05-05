"""Add chain_address to Organization

Revision ID: 2160d6191c6d
Revises: 24f35ff7b7ad
Create Date: 2025-04-30 15:16:49.630534
"""

# Alembic‐Revision‐Metadaten:
revision = '2160d6191c6d'
down_revision = '24f35ff7b7ad'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    # 1) Spalte zuerst NULLABLE anlegen
    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chain_address', sa.String(length=42), nullable=True))

    # 2) Bestehende Zeilen mit einem Default füllen (hier leerer String)
    op.execute("UPDATE organizations SET chain_address = '' WHERE chain_address IS NULL;")

    # 3) NOT NULL‐Constraint aktivieren
    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.alter_column('chain_address', nullable=False)

def downgrade():
    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.drop_column('chain_address')
