"""Add queue notifications

Revision ID: 509440a9c704
Revises: 23b391f4c353
Create Date: 2022-01-20 18:51:15.122518

"""
import sqlalchemy as sa

from alembic import op
from sqlalchemy.dialects.postgresql import BIGINT

# revision identifiers, used by Alembic.
revision = "509440a9c704"
down_revision = "23b391f4c353"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "queue_notification",
        sa.Column("queue_id", sa.String(), nullable=False),
        sa.Column("player_id", BIGINT, nullable=False),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["player.id"],
            name=op.f("fk_queue_notification_player_id_player"),
        ),
        sa.ForeignKeyConstraint(
            ["queue_id"],
            ["queue.id"],
            name=op.f("fk_queue_notification_queue_id_queue"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_queue_notification")),
    )
    with op.batch_alter_table("queue_notification", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_queue_notification_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_queue_notification_player_id"),
            ["player_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_queue_notification_queue_id"),
            ["queue_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_queue_notification_size"), ["size"], unique=False
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("queue_notification", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_queue_notification_size"))
        batch_op.drop_index(batch_op.f("ix_queue_notification_queue_id"))
        batch_op.drop_index(batch_op.f("ix_queue_notification_player_id"))
        batch_op.drop_index(batch_op.f("ix_queue_notification_created_at"))

    op.drop_table("queue_notification")
    # ### end Alembic commands ###
