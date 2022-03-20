"""Add queue waitlist table

Revision ID: 23862e11bc0c
Revises: 1fb046cac8b6
Create Date: 2021-12-31 16:03:26.339898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "23862e11bc0c"
down_revision = "1fb046cac8b6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "queue_waitlist",
        sa.Column("channel_id", sa.Integer(), nullable=False),
        sa.Column("finished_game_id", sa.String(255), nullable=False),
        sa.Column("guild_id", sa.Integer(), nullable=False),
        sa.Column("queue_id", sa.String(255), nullable=False),
        sa.Column("end_waitlist_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.String(255), nullable=False),
        sa.ForeignKeyConstraint(
            ["finished_game_id"],
            ["finished_game.id"],
            name=op.f("fk_queue_waitlist_finished_game_id_finished_game"),
        ),
        sa.ForeignKeyConstraint(
            ["queue_id"],
            ["queue.id"],
            name=op.f("fk_queue_waitlist_queue_id_queue"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_queue_waitlist")),
        sa.UniqueConstraint(
            "finished_game_id",
            "queue_id",
            name=op.f("uq_queue_waitlist_finished_game_id"),
        ),
    )
    with op.batch_alter_table("queue_waitlist", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_queue_waitlist_end_waitlist_at"),
            ["end_waitlist_at"],
            unique=False,
        )


    with op.batch_alter_table(
        "queue_player", schema=None
    ) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("uq_queue_player_queue_id"), type_="unique"
        )
        batch_op.create_unique_constraint(
            batch_op.f("uq_queue_player_queue_id"), ["queue_id", "player_id"]
        )

    with op.batch_alter_table(
        "queue_waitlist_player", schema=None
    ) as batch_op:
        batch_op.add_column(
            sa.Column("queue_waitlist_id", sa.String(255), nullable=False)
        )
        batch_op.drop_index("ix_queue_waitlist_player_finished_game_id")
        batch_op.create_index(
            batch_op.f("ix_queue_waitlist_player_queue_waitlist_id"),
            ["queue_waitlist_id"],
            unique=False,
        )
        batch_op.create_unique_constraint(
            batch_op.f("uq_queue_waitlist_player_queue_waitlist_id"),
            ["queue_waitlist_id", "player_id"],
        )
        batch_op.create_foreign_key(
            batch_op.f(
                "fk_queue_waitlist_player_queue_waitlist_id_queue_waitlist"
            ),
            "queue_waitlist",
            ["queue_waitlist_id"],
            ["id"],
        )
        batch_op.drop_constraint(
            batch_op.f("uq_queue_waitlist_player_finished_game_id"), type_="unique"
        )
        batch_op.drop_column("finished_game_id")
        batch_op.drop_column("queue_id")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table(
        "queue_waitlist_player", schema=None
    ) as batch_op:
        batch_op.add_column(
            sa.Column("queue_id", sa.VARCHAR(), nullable=False)
        )
        batch_op.add_column(
            sa.Column("finished_game_id", sa.VARCHAR(), nullable=False)
        )
        batch_op.drop_constraint(
            batch_op.f(
                "fk_queue_waitlist_player_queue_waitlist_id_queue_waitlist"
            ),
            type_="foreignkey",
        )
        batch_op.create_foreign_key(None, "queue", ["queue_id"], ["id"])
        batch_op.create_foreign_key(
            None, "finished_game", ["finished_game_id"], ["id"]
        )
        batch_op.drop_constraint(
            batch_op.f("uq_queue_waitlist_player_queue_waitlist_id"),
            type_="unique",
        )
        batch_op.drop_index(
            batch_op.f("ix_queue_waitlist_player_queue_waitlist_id")
        )
        batch_op.create_index(
            "ix_queue_waitlist_player_finished_game_id",
            ["finished_game_id"],
            unique=False,
        )
        batch_op.drop_column("queue_waitlist_id")

    with op.batch_alter_table("queue_player", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("uq_queue_player_queue_id"), type_="unique"
        )

    with op.batch_alter_table("queue_waitlist", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_queue_waitlist_end_waitlist_at"))

    op.drop_table("queue_waitlist")
    # ### end Alembic commands ###
