# WICHTIG:
# - Der Dateiname der Migration muss mit der `revision`-ID beginnen, z.B. `4c8d3fea0cbb_create_documents_table.py`.
# - Ersetze `<previous_revision_id>` durch die tatsächliche Vorgänger-Revision (steht im Ordner `migrations/versions`).
# - Achte darauf, dass `revision` und `down_revision` korrekt gesetzt sind.

# Revision identifiers, used by Alembic.
revision = '4c8d3fea0cbb'
down_revision = None  # erste Migration oder wenn Vorgänger gelöscht wurde
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Create the new documents table without altering the organizations table
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('document_id', sa.String(), nullable=False),
        sa.Column('org_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('file_data', sa.LargeBinary(), nullable=False),
        sa.Column('mime_type', sa.String(), nullable=False)
    )
    op.create_index('ix_documents_org_doc', 'documents', ['org_id', 'document_id'])

    # Hinweis: Es werden keine Änderungen an `organizations` vorgenommen, daher kein ALTER COLUMN nötig.


def downgrade():
    op.drop_index('ix_documents_org_doc', table_name='documents')
    op.drop_table('documents')