import psycopg2
import pandas as pd
from psycopg2 import sql
from psycopg2.extensions import connection


def insert_new_row(conn: connection, new_a_id: int, similarities_df: pd.DataFrame):
    """
    Inserts a new row into the sim_matrix table using a DataFrame.

    :param conn: PostgreSQL database connection object
    :param new_a_id: ID of the new A element
    :param similarities_df: DataFrame with single row containing similarity scores to each B element
    """
    with conn.cursor() as cursor:
        # Get B column names (excluding a_id)
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'sim_matrix' 
            AND column_name != 'id'
            ORDER BY ordinal_position;
        """)
        b_columns = [row[0] for row in cursor.fetchall()]

        # Validate DataFrame structure
        if len(similarities_df) != 1:
            raise ValueError("DataFrame must contain exactly one row")

        if list(similarities_df.columns) != b_columns:
            raise ValueError(f"DataFrame columns must match B columns in order: {b_columns}")

        # Prepare values
        values = [new_a_id] + similarities_df.iloc[0].tolist()
        columns_str = ', '.join(['id'] + b_columns)
        placeholders = ', '.join(['%s'] * (len(b_columns) + 1))

        # Create and execute INSERT query
        insert_query = f"""
            INSERT INTO sim_matrix ({columns_str})
            VALUES ({placeholders})
        """
        cursor.execute(insert_query, values)
    conn.commit()


def insert_new_column(conn: connection, new_b_id: str, similarities_df: pd.DataFrame):
    """
    Inserts a new column into the sim_matrix table using a DataFrame.

    :param conn: PostgreSQL database connection object
    :param new_b_id: Name/ID of the new B element (column name)
    :param similarities_df: DataFrame with single row containing similarity scores to each A element
    """
    with conn.cursor() as cursor:
        # Basic column name validation
        if not new_b_id.isidentifier():
            raise ValueError("Invalid column name")

        # Get existing A element IDs in order
        cursor.execute("SELECT a_id FROM sim_matrix ORDER BY a_id;")
        a_ids = [row[0] for row in cursor.fetchall()]

        # Validate DataFrame structure
        if len(similarities_df) != 1:
            raise ValueError("DataFrame must contain exactly one row")

        if len(similarities_df.columns) != len(a_ids):
            raise ValueError(f"Need {len(a_ids)} similarity scores, got {len(similarities_df.columns)}")

        # Add new column
        cursor.execute(
            sql.SQL("ALTER TABLE sim_matrix ADD COLUMN {} REAL").format(
                sql.Identifier(new_b_id)
            )
        )

        # Prepare UPDATE statements
        similarities = similarities_df.iloc[0].tolist()
        update_template = """
            UPDATE sim_matrix 
            SET {} = %s 
            WHERE a_id = %s;
        """

        # Update each row with corresponding similarity score
        for a_id, similarity in zip(a_ids, similarities):
            cursor.execute(
                sql.SQL(update_template).format(sql.Identifier(new_b_id)),
                (similarity, a_id)
            )
    conn.commit()