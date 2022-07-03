from typing import Any, Optional, Union, TypeVar, Generic, List, Iterator
from . import interfaces
from .base import InspectionAttr
from ..sql.selectable import ForUpdateArg, Alias, CTE
from ..sql.elements import Label
from .session import Session


_T = TypeVar('_T')
_Q = TypeVar('_Q', bound="Query")


class Query(Generic[_T]):
    session: Session = ...
    _limit_clause: Any = ...
    _offset_clause: Any = ...
    _group_by_clauses: Any = ...

    def __init__(self, entities, session: Optional[Session] = ...) -> None: ...
    def __next__(self): ...
    # TODO: is "statement" always of type sqlalchemy.sql.selectable.Select ?
    @property
    def statement(self): ...
    def subquery(self, name: Optional[str] = ..., with_labels: bool = ..., reduce_columns: bool = ...) -> Alias: ...
    def cte(self, name: Optional[str] = ..., recursive: bool = ...) -> CTE: ...
    def label(self, name: str) -> Label: ...
    def as_scalar(self): ...
    @property
    def selectable(self): ...
    def __clause_element__(self): ...
    def _compile_state(self):...
    def enable_eagerloads(self: _Q, value: bool) -> _Q: ...
    def with_labels(self: _Q) -> _Q: ...
    def enable_assertions(self: _Q, value: bool) -> _Q: ...
    @property
    def whereclause(self): ...
    def with_polymorphic(self, cls_or_mappers, selectable: Optional[Any] = ...,
                         polymorphic_on: Optional[Any] = ...): ...
    def yield_per(self: _Q, count: int) -> _Q: ...
    def get(self, ident) -> Optional[_T]: ...
    def correlate(self, *args): ...
    def autoflush(self: _Q, setting: bool) -> _Q: ...
    def populate_existing(self: _Q) -> _Q: ...
    def with_parent(self, instance, property: Optional[Any] = ...): ...
    def add_entity(self, entity, alias: Optional[Any] = ...): ...
    def with_session(self: _Q, session: Optional[Session]) -> _Q: ...
    def from_self(self, *entities): ...
    def values(self, *columns): ...
    def value(self, column): ...
    def with_entities(self, *entities): ...
    def add_columns(self, *column): ...
    def add_column(self, column): ...
    def options(self, *args): ...
    def with_transformation(self, fn): ...
    def with_hint(self, selectable, text, dialect_name: str = ...): ...
    def with_statement_hint(self, text, dialect_name: str = ...): ...
    def execution_options(self, **kwargs): ...
    def with_lockmode(self, mode): ...
    def with_for_update(self: _Q, read: bool = ..., nowait: bool = ..., of: Optional[Any] = ...,
                        skip_locked: bool = ..., key_share: bool = ...) -> _Q: ...
    def params(self: _Q, *args, **kwargs) -> _Q: ...
    def filter(self: _Q, *criterion) -> _Q: ...
    def filter_by(self: _Q, **kwargs) -> _Q: ...
    def order_by(self: _Q, *criterion) -> _Q: ...
    def group_by(self: _Q, *criterion) -> _Q: ...
    def having(self: _Q, criterion) -> _Q: ...
    def union(self, *q): ...
    def union_all(self, *q): ...
    def intersect(self, *q): ...
    def intersect_all(self, *q): ...
    def except_(self, *q): ...
    def except_all(self, *q): ...
    def join(self, *props, **kwargs): ...
    def outerjoin(self, *props, **kwargs): ...
    def reset_joinpoint(self): ...
    def select_from(self, *from_obj): ...
    def select_entity_from(self, from_obj): ...
    def __getitem__(self, item): ...
    def slice(self: _Q, start: Optional[int], stop: Optional[int]) -> _Q: ...
    def limit(self: _Q, limit: Optional[int]) -> _Q: ...
    def offset(self: _Q, offset: Optional[int]) -> _Q: ...
    def distinct(self, *criterion): ...
    def prefix_with(self, *prefixes): ...
    def suffix_with(self, *suffixes): ...
    def all(self) -> List[_T]: ...
    def from_statement(self, statement): ...
    def first(self) -> Optional[_T]: ...
    def one_or_none(self) -> Optional[_T]: ...
    def one(self) -> _T: ...
    def scalar(self): ...
    def __iter__(self) -> Iterator[_T]: ...
    @property
    def column_descriptions(self): ...
    def instances(self, cursor, __context: Optional[Any] = ...): ...
    def merge_result(self, iterator, load: bool = ...): ...
    def exists(self): ...
    def count(self) -> int: ...
    def delete(self, synchronize_session: Union[bool, str] = ...) -> int: ...
    def update(self, values, synchronize_session: Union[bool, str] = ..., update_args: Optional[Any] = ...): ...

class LockmodeArg(ForUpdateArg):
    @classmethod
    def parse_legacy_query(self, mode): ...

class _QueryEntity(object):
    def __new__(cls, *args, **kwargs): ...

class _MapperEntity(_QueryEntity):
    entities: Any = ...
    expr: Any = ...
    def __init__(self, query, entity) -> None: ...
    supports_single_entity: bool = ...
    use_id_for_hash: bool = ...
    mapper: Any = ...
    aliased_adapter: Any = ...
    selectable: Any = ...
    is_aliased_class: Any = ...
    entity_zero: Any = ...
    path: Any = ...
    def setup_entity(self, ext_info, aliased_adapter): ...
    def set_with_polymorphic(self, query, cls_or_mappers, selectable, polymorphic_on): ...
    @property
    def type(self): ...
    @property
    def entity_zero_or_selectable(self): ...
    def corresponds_to(self, entity): ...
    def adapt_to_selectable(self, query, sel): ...
    def row_processor(self, query, context, result): ...
    def setup_context(self, query, context): ...

class Bundle(InspectionAttr):
    single_entity: bool = ...
    is_clause_element: bool = ...
    is_mapper: bool = ...
    is_aliased_class: bool = ...
    name: str = ...
    exprs: Any = ...
    c: Any = ...
    def __init__(self, name, *exprs, **kw) -> None: ...
    columns: Any = ...
    def __clause_element__(self): ...
    @property
    def clauses(self): ...
    def label(self, name): ...
    def create_row_processor(self, query, procs, labels): ...

class _BundleEntity(_QueryEntity):
    use_id_for_hash: bool = ...
    bundle: Any = ...
    type: Any = ...
    supports_single_entity: Any = ...
    def __init__(self, query, bundle, setup_entities: bool = ...) -> None: ...
    @property
    def entities(self): ...
    @property
    def entity_zero(self): ...
    def corresponds_to(self, entity): ...
    @property
    def entity_zero_or_selectable(self): ...
    def adapt_to_selectable(self, query, sel): ...
    def setup_entity(self, ext_info, aliased_adapter): ...
    def setup_context(self, query, context): ...
    def row_processor(self, query, context, result): ...

class _ColumnEntity(_QueryEntity):
    expr: Any = ...
    namespace: Any = ...
    type: Any = ...
    use_id_for_hash: Any = ...
    column: Any = ...
    froms: Any = ...
    actual_froms: Any = ...
    entity_zero: Any = ...
    entities: Any = ...
    mapper: Any = ...
    def __init__(self, query, column, namespace: Optional[Any] = ...) -> None: ...
    supports_single_entity: bool = ...
    @property
    def entity_zero_or_selectable(self): ...
    def adapt_to_selectable(self, query, sel): ...
    selectable: Any = ...
    def setup_entity(self, ext_info, aliased_adapter): ...
    def corresponds_to(self, entity): ...
    def row_processor(self, query, context, result): ...
    def setup_context(self, query, context): ...

class QueryContext(object):
    statement: Any = ...
    from_clause: Any = ...
    whereclause: Any = ...
    order_by: Any = ...
    multi_row_eager_loaders: bool = ...
    adapter: Any = ...
    froms: Any = ...
    for_update: Any = ...
    query: Any = ...
    session: Any = ...
    autoflush: Any = ...
    populate_existing: Any = ...
    invoke_all_eagers: Any = ...
    version_check: Any = ...
    refresh_state: Any = ...
    primary_columns: Any = ...
    secondary_columns: Any = ...
    eager_order_by: Any = ...
    eager_joins: Any = ...
    create_eager_joins: Any = ...
    propagate_options: Any = ...
    attributes: Any = ...
    def __init__(self, query) -> None: ...

class AliasOption(interfaces.MapperOption):
    alias: Any = ...
    def __init__(self, alias) -> None: ...
    def process_query(self, query): ...
