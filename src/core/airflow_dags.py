import datetime
from urllib.parse import urljoin

from src.core.http_requests import MakeRequest
from src.settings import settings


class AirFlowDags:

    is_subdug = False
    is_success = False
    state = 'running'

    def __init__(self, app=None, db=None):
        self.app = app
        self.config = settings
        self.db = db
        self.auth = (
            self.config.airflow.login,
            self.config.airflow.password.get_secret_value(),
        )

    @property
    def _prepare_url(self) -> str:
        return urljoin(self.config.airflow.url, 'api/v1/dags/')

    async def get_list_dags(self) -> dict:
        # use default core url to fetch all dags
        request = MakeRequest(uri=self._prepare_url[:-1], auth=self.auth)
        return await request.do_request()

    def get_list_dags_sync(self) -> dict:
        request = MakeRequest(uri=self._prepare_url[:-1], auth=self.auth)
        return request.do_sync_request()

    async def get_status_dag(self, dag_id: str):
        _uri = self._prepare_url + dag_id
        request = MakeRequest(uri=_uri, auth=self.auth)
        if not await self.validate_dag_id(dag_id):
            raise ValueError('dag_id should be in the list of available dags')

        response = await request.do_request()
        # set status of started DAG
        self.is_subdug = is_subdug = response['is_subdag']
        self.is_success = response['is_paused'] and is_subdug
        return response

    async def trigger_dag(self, dag_id: str, query: str, user_id) -> dict:
        _uri = self._prepare_url + f'{dag_id}/dagRuns'

        full_query = {'conf': {'query': self.validated_query(query)}}
        if not await self.validate_dag_id(dag_id):
            raise ValueError('dag_id should be in the list of available dags')

        request = MakeRequest(
            uri=_uri, method='POST', data=full_query, auth=self.auth
        )
        response = await request.do_request()
        dag_run_id = response['dag_run_id']
        await self.create_search(dag_id, query, dag_run_id, user_id)
        return await request.do_request()

    async def get_status_dagrun(self, dag_id: str, dag_run_id: str):
        _uri = self._prepare_url + f'{dag_id}/dagRuns/{dag_run_id}'
        request = MakeRequest(uri=_uri, auth=self.auth)
        response = await request.do_request()
        self.state = response['state']

        async with self.db as session:
            from src.apps.organization.models import Search

            async with session.begin():
                # take a Table instance of Search model
                search = Search.__table__
                await session.execute(
                    search.update()
                    .where(search.c.dag_run_id == dag_run_id)
                    .values(status=self.state)
                )
        return response

    @staticmethod
    def validated_query(query) -> str:
        from src.apps.organization.schemas import QueryFilterSchema

        _klass = QueryFilterSchema(query=query)
        return _klass.query

    async def validate_dag_id(self, dag_id: str) -> bool:
        dags_response = await self.get_list_dags()
        dags = dags_response.get('dags', [])
        return dag_id in [dag['dag_id'] for dag in dags]

    def validate_dag_id_sync(self, dag_id: str) -> bool:
        dags_response = self.get_list_dags_sync()
        dags = dags_response.get('dags', [])
        return dag_id in [dag['dag_id'] for dag in dags]

    async def create_search(self, dag_id, query, dag_run_id, user_id):
        from src.apps.organization.models import Search

        dag_info = await self.get_status_dag(dag_id)
        metadata = {
            'fileloc': dag_info['fileloc'],
            'file_token': dag_info['file_token'],
            'tags': dag_info['tags'],
            'description': dag_info['description']
        }

        search = Search()
        search.query = query
        search.dag_id = dag_id
        search.dag_run_id = dag_run_id
        search.status = self.state
        search.date = datetime.datetime.now().isoformat()
        search.meta_data = metadata
        search.user_id = user_id
        self.db.add(search)
        await self.db.commit()
        await self.db.refresh(search)

        return search
