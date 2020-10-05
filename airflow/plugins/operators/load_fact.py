from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    """ Loading fact table into Redshift
    """
    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_stmt="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id=redshift_conn_id
        self.table=table
        self.sql_stmt=sql_stmt

    def execute(self, context):
        """ Execute loading fact table
        """
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info(f"Loading fact table {self.table}")
        insert_cmd = f"""
            INSERT INTO public.{self.table}
            {self.sql_stmt};
            commit;
        """
        redshift.run(insert_cmd)
