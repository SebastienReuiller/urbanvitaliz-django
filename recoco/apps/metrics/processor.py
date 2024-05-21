from pathlib import Path
from django.db.backends.utils import CursorWrapper
from django.contrib.sites.models import Site
import importlib
from django.db.models import QuerySet
from typing import Any
from django.conf import settings
from dataclasses import dataclass

from recoco.utils import make_site_slug


class MaterializedViewSpecError(Exception):
    pass


@dataclass
class MaterializedViewSqlQuery:
    sql: str
    params: tuple[Any] | None = None

    def __post_init__(self):
        self.sql = self.sql.replace("\n", "").strip()
        if self.sql.endswith(";"):
            self.sql = self.sql[:-1]


class MaterializedView:
    site: Site
    name: str
    cursor: CursorWrapper
    indexes: list[str]
    unique_indexes: list[str]

    def __init__(
        self,
        site: Site,
        name: str,
        indexes: list[str] = None,
        unique_indexes: list[str] = None,
    ):
        self.site = site
        self.name = name
        self.cursor = None
        self.indexes = indexes or []
        self.unique_indexes = unique_indexes or []

    @classmethod
    def create_for_site(
        cls, site: Site, spec: dict[str, Any], check_sql_query: bool = True
    ) -> "MaterializedView":
        try:
            materialized_view = MaterializedView(site, **spec)
        except TypeError:
            raise MaterializedViewSpecError(
                f"Invalid materialized view specification '{spec}'"
            )

        if check_sql_query and materialized_view.get_sql_query() is None:
            raise MaterializedViewSpecError(
                f"SQL query for materialized view '{materialized_view.name}' is not found"
            )

        return materialized_view

    @property
    def db_view_name(self) -> str:
        return f"{settings.MATERIALIZED_VIEWS_PREFIX}_{self.name}"

    @property
    def db_schema_name(self) -> str:
        site_slug = make_site_slug(site=self.site)
        return f"metrics_{site_slug}"

    def set_cursor(self, cursor: CursorWrapper | None) -> None:
        self.cursor = cursor

    def get_django_sql_query(self) -> MaterializedViewSqlQuery | None:
        module_name = "{}.{}".format(
            str(
                Path(settings.MATERIALIZED_VIEWS_SQL_DIR).relative_to(
                    settings.BASE_DIR.parent
                )
            ).replace("/", "."),
            self.name,
        )
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            return None

        try:
            queryset = module.get_queryset(site_id=self.site.id)
        except AttributeError as e:
            raise e

        if isinstance(queryset, QuerySet):
            sql, params = queryset.query.sql_with_params()
            return MaterializedViewSqlQuery(sql=sql, params=params)

    def get_raw_sql_query(self) -> MaterializedViewSqlQuery | None:
        sql_file = settings.MATERIALIZED_VIEWS_SQL_DIR / f"{self.name}.sql"
        if not sql_file.exists():
            return None

        with open(sql_file, "r") as f:
            return MaterializedViewSqlQuery(sql=f.read(), params=(self.site.id,))

    def get_sql_query(self) -> MaterializedViewSqlQuery | None:
        return self.get_django_sql_query() or self.get_raw_sql_query()

    def create(self) -> None:
        sql_query = self.get_sql_query()
        if sql_query is None:
            return

        # Create the schema if it does not exist
        self.cursor.execute(sql=f"CREATE SCHEMA IF NOT EXISTS {self.db_schema_name};")

        # Create the materialized view
        self.cursor.execute(
            sql=f"CREATE MATERIALIZED VIEW {self.db_schema_name}.{self.db_view_name} AS ( {sql_query.sql} ) WITH NO DATA;",
            params=sql_query.params,
        )

        # Create indexes if any
        for index in self.indexes:
            self.cursor.execute(
                sql=f"CREATE INDEX ON {self.db_schema_name}.{self.db_view_name} ({index});"
            )

        # Create unique indexes if any
        for index in self.unique_indexes:
            self.cursor.execute(
                sql=f"CREATE UNIQUE INDEX ON {self.db_schema_name}.{self.db_view_name} ({index});"
            )

    def drop(self) -> None:
        self.cursor.execute(
            sql=f"DROP MATERIALIZED VIEW IF EXISTS {self.db_schema_name}.{self.db_view_name};"
        )

    def refresh(self) -> None:
        self.cursor.execute(
            sql=f"REFRESH MATERIALIZED VIEW {self.db_schema_name}.{self.db_view_name};"
        )
