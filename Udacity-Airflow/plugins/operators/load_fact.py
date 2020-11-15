from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'
    
    insert_sql = """
        INSERT INTO {}
        {}
        ;
    """

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id="",
                 table="",
                 select_sql="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.conn_id = redshift_conn_id
        self.table = table
        self.select_sql = select_sql

    def execute(self, context):
        self.log.info('LoadFactOperator not implemented yet')
        
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Truncating Redshift table")
        redshift.run("DELETE FROM {}".format(self.table))

        formatted_sql = LoadFactOperator.insert_sql.format(
            self.table,
            self.sql_source
        )
        self.log.info(f"Executing {formatted_sql} ...")
        redshift.run(formatted_sql)
