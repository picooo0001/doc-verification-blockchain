# --- migrations/versions/0077712aa980_add_wallet_address_and_nonce.py ---
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0077712aa980'
down_revision = '2160d6191c6d'
branch_labels = None
depends_on = None


def upgrade():
    # Neue Spalte für Wallet-Adresse
    op.add_column(
        'users',
        sa.Column('wallet_address', sa.String(length=42), unique=True, nullable=True)
    )
    # Neue Spalte für den Login-Nonce
    op.add_column(
        'users',
        sa.Column('login_nonce', sa.String(length=32), nullable=True)
    )


def downgrade():
    # Im Downgrade wieder entfernen (in umgekehrter Reihenfolge)
    op.drop_column('users', 'login_nonce')
    op.drop_column('users', 'wallet_address')
