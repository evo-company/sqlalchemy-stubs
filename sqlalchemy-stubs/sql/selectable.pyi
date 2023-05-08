from typing import Any, Optional, Union, TypeVar, List, Iterable, Sequence, Mapping, Set, Tuple, Type
from .elements import (
    ClauseElement as ClauseElement, Grouping as Grouping, UnaryExpression as UnaryExpression, ColumnElement, ColumnClause,
    TextClause, Label, BindParameter
)
from .base import Immutable as Immutable, Executable as Executable, Generative as Generative, ImmutableColumnCollection, ColumnSet
from .annotation import Annotated as Annotated
from ..engine import Engine, Connection
from .schema import ForeignKey, Table
from .functions import Function
from .dml import Insert, Update, Delete
from .type_api import TypeEngine
from .visitors import Visitable
from .. import util

_T = TypeVar('_T')

def subquery(alias: str, *args: Any, **kwargs: Any) -> Alias: ...
def alias(selectable: FromClause, name: Optional[Any] = ..., flat: bool = ...) -> Alias: ...
def lateral(selectable: FromClause, name: Optional[Any] = ...) -> Lateral: ...
def tablesample(selectable: FromClause, sampling: float, name: Optional[str] = ..., seed: Optional[Any] = ...) -> TableSample: ...

_S = TypeVar('_S', bound=Selectable)

class Selectable(ClauseElement):
    __visit_name__: str = ...
    is_selectable: bool = ...
    @property
    def selectable(self: _S) -> _S: ...

_HP = TypeVar('_HP', bound=HasPrefixes)

class HasPrefixes(object):
    def prefix_with(self: _HP, *expr: Union[str, ClauseElement], **kw: Any) -> _HP: ...

_HS = TypeVar('_HS', bound=HasSuffixes)

class HasSuffixes(object):
    def suffix_with(self: _HS, *expr: Union[str, ClauseElement], **kw: Any) -> _HS: ...

class FromClause(Selectable):
    __visit_name__: str = ...
    named_with_column: bool = ...
    schema: Optional[str] = ...
    def count(self, whereclause: Optional[Union[str, bool, Visitable]] = ..., **params: Any) -> Select: ...
    def select(self, whereclause: Optional[Union[str, bool, Visitable]] = ..., **params: Any) -> Select: ...
    def join(self, right: FromClause, onclause: Optional[ClauseElement] = ..., isouter: bool = ..., full: bool = ...) -> Join: ...
    def outerjoin(self, right: FromClause, onclause: Optional[ClauseElement] = ..., full: bool = ...) -> Join: ...
    def alias(self, name: Optional[str] = ..., flat: bool = ...) -> Alias: ...
    def lateral(self, name: Optional[str] = ...) -> Lateral: ...
    def tablesample(self, sampling: Union[float, Function[float]], name: Optional[str] = ...,
                    seed: Optional[Any] = ...) -> TableSample: ...
    def is_derived_from(self, fromclause: FromClause) -> bool: ...
    def replace_selectable(self, old: FromClause, alias: Alias) -> FromClause: ...
    def correspond_on_equivalents(self, column: ColumnElement[Any],
                                  equivalents: Mapping[Any, Any]) -> Optional[ColumnElement[Any]]: ...
    def corresponding_column(self, column: ColumnElement[Any], require_embedded: bool = ...) -> ColumnElement[Any]: ...
    @property
    def description(self) -> str: ...
    @property
    def columns(self) -> ImmutableColumnCollection: ...
    @property
    def primary_key(self) -> ColumnSet: ...
    @property
    def foreign_keys(self) -> Set[ForeignKey]: ...
    c: ImmutableColumnCollection = ...

_J = TypeVar('_J', bound=Join)

class Join(FromClause):
    __visit_name__: str = ...
    left: FromClause = ...
    right: FromClause = ...
    onclause: ClauseElement = ...
    isouter: bool = ...
    full: bool = ...
    def __init__(self, left: FromClause, right: FromClause, onclause: Optional[ClauseElement] = ...,
                 isouter: bool = ..., full: bool = ...) -> None: ...
    @property
    def description(self) -> str: ...
    def is_derived_from(self, fromclause: FromClause) -> bool: ...
    def self_group(self, against: Optional[Any] = ...) -> FromGrouping: ...
    def get_children(self, **kwargs: Any) -> Tuple[FromClause, FromClause, ClauseElement]: ...
    def select(self, whereclause: Optional[Union[str, bool, Visitable]] = ..., **kwargs: Any) -> Select: ...
    def where(self: _SE, whereclause: Union[str, bool, Visitable]) -> _SE: ...
    @property
    def bind(self) -> Optional[Union[Engine, Connection]]: ...
    # Return type of "alias" incompatible with supertype "FromClause"
    def alias(self, name: Optional[str] = ..., flat: bool = ...) -> Union[Alias, Join]: ...  # type: ignore
    @classmethod
    def _create_outerjoin(cls: Type[_J], left: FromClause, right: FromClause, onclause: Optional[ClauseElement] = ...,
                          full: bool = ...) -> _J: ...
    @classmethod
    def _create_join(cls: Type[_J], left: FromClause, right: FromClause, onclause: Optional[ClauseElement] = ...,
                     isouter: bool = ..., full: bool = ...) -> _J: ...

_A = TypeVar('_A', bound=Alias)

class Alias(FromClause):
    __visit_name__: str = ...
    named_with_column: bool = ...
    original: Selectable = ...
    supports_execution: bool = ...
    element: Selectable = ...
    name: Optional[str] = ...
    def __init__(self, selectable: Selectable, name: Optional[str] = ...) -> None: ...
    def self_group(self: _A, against: Optional[Any] = ...) -> Union[FromGrouping, _A]: ...
    @property
    def description(self) -> str: ...
    def as_scalar(self) -> Any: ...
    def is_derived_from(self, fromclause: FromClause) -> bool: ...
    def get_children(self, column_collections: bool = ..., **kw: Any) -> Iterable[Union[ColumnElement[Any], Selectable]]: ...
    @property
    def bind(self) -> Optional[Union[Engine, Connection]]: ...

class Lateral(Alias):
    __visit_name__: str = ...

class TableSample(Alias):
    __visit_name__: str = ...
    sampling: Any = ...
    seed: Any = ...
    def __init__(self, selectable: FromClause, sampling: Union[float, Function[float]], name: Optional[str] = ...,
                 seed: Optional[Any] = ...) -> None: ...

class CTE(Generative, HasPrefixes, HasSuffixes, Alias):
    __visit_name__: str = ...
    recursive: bool = ...
    def __init__(self, selectable: Select, name: Optional[str] = ..., recursive: bool = ...,
                 _cte_alias: Optional[Any] = ..., _restates: Any = ..., _prefixes: Optional[Any] = ...,
                 _suffixes: Optional[Any] = ...) -> None: ...
    def alias(self, name: Optional[str] = ..., flat: bool = ...) -> CTE: ...
    def union(self, other: Select) -> CTE: ...
    def union_all(self, other: Select) -> CTE: ...

class HasCTE(object):
    def cte(self, name: Optional[str] = ..., recursive: bool = ...) -> CTE: ...

class FromGrouping(FromClause):
    __visit_name__: str = ...
    element: FromClause = ...
    def __init__(self, element: FromClause) -> None: ...
    @property
    def columns(self) -> ImmutableColumnCollection: ...
    @property
    def primary_key(self) -> ColumnSet: ...
    @property
    def foreign_keys(self) -> Set[ForeignKey]: ...
    def is_derived_from(self, element: FromClause) -> bool: ...
    # Return type of "alias" incompatible with supertype "FromClause"
    def alias(self, name: Optional[str] = ..., flat: bool = ...) -> FromGrouping: ...  # type: ignore
    def get_children(self, **kwargs: Any) -> Tuple[FromClause]: ...
    def __getattr__(self, attr: str) -> Any: ...

class TableClause(Immutable, FromClause):
    __visit_name__: str = ...
    named_with_column: bool = ...
    implicit_returning: bool = ...
    name: str = ...
    primary_key: ColumnSet = ...
    foreign_keys: Set[ForeignKey] = ...
    def __init__(self, name: str, *columns: ColumnClause[Any]) -> None: ...
    @property
    def description(self) -> str: ...
    def append_column(self, c: ColumnClause[Any]): ...
    def get_children(self, column_collections: bool = ..., **kwargs: Any) -> List[ColumnClause[Any]]: ...
    # `values` should be Mapping[Union[ColumnClause[Any], str]] but because Mapping is invariant in the key type,
    # we must use Mapping[Any, Any] or list all subclasses of ColumnClause in the Union
    def insert(self, values: Union[Mapping[Any, Any], Sequence[Any]] = ..., inline: bool = ..., **kwargs: Any) -> Insert: ...
    def update(self, whereclause: Optional[Union[str, bool, Visitable]] = ...,
               values: Union[Mapping[Any, Any], Sequence[Any]] = ...,
               inline: bool = ..., **kwargs: Any) -> Update: ...
    def delete(self, whereclause: Optional[Union[str, bool, Visitable]] = ..., **kwargs: Any) -> Delete: ...

class ForUpdateArg(ClauseElement):
    @classmethod
    def parse_legacy_select(self, arg: Optional[str]) -> Optional[ForUpdateArg]: ...
    @property
    def legacy_for_update_value(self) -> Union[str, bool]: ...
    nowait: bool = ...
    read: bool = ...
    skip_locked: bool = ...
    key_share: bool = ...
    of: Any = ...
    def __init__(self, nowait: bool = ..., read: bool = ..., of: Optional[Union[TextClause, Sequence[ColumnClause[Any]]]] = ...,
                 skip_locked: bool = ..., key_share: bool = ...) -> None: ...

_SB = TypeVar('_SB', bound=SelectBase)

class SelectBase(HasCTE, Executable, FromClause):
    def as_scalar(self) -> ScalarSelect[Any]: ...
    def label(self, name: str) -> Label: ...
    def autocommit(self: _SB) -> _SB: ...

_GS = TypeVar('_GS', bound=GenerativeSelect)

class GenerativeSelect(SelectBase):
    use_labels: bool = ...
    for_update: Union[str, bool] = ...
    def __init__(self, use_labels: bool = ..., for_update: bool = ..., limit: Optional[int] = ...,
                 offset: Optional[int] = ...,
                 order_by: Optional[Union[int, str, Visitable, Iterable[Union[int, str, Visitable]]]] = ...,
                 group_by: Optional[Union[int, str, Visitable, Iterable[Union[int, str, Visitable]]]] = ...,
                 bind: Optional[Union[Engine, Connection]] = ...,
                 autocommit: Optional[bool] = ...) -> None: ...
    def with_for_update(self: _GS, nowait: bool = ..., read: bool = ...,
                        of: Optional[Union[TextClause, Sequence[ColumnClause[Any]], TableClause, Sequence[TableClause]]] = ...,
                        skip_locked: bool = ..., key_share: bool = ...) -> _GS: ...
    def apply_labels(self: _GS) -> _GS: ...
    def limit(self: _GS, limit: Optional[Union[int, str, Visitable]]) -> _GS: ...
    def offset(self: _GS, offset: Optional[Union[int, str, Visitable]]) -> _GS: ...
    def order_by(self: _GS, *clauses: Optional[Union[str, bool, Visitable]]) -> _GS: ...
    def group_by(self: _GS, *clauses: Optional[Union[str, bool, Visitable]]) -> _GS: ...
    def append_order_by(self, *clauses: Optional[Union[str, bool, Visitable]]): ...
    def append_group_by(self, *clauses: Optional[Union[str, bool, Visitable]]): ...

class CompoundSelect(GenerativeSelect):
    __visit_name__: str = ...
    UNION: util.symbol = ...
    UNION_ALL: util.symbol = ...
    EXCEPT: util.symbol = ...
    EXCEPT_ALL: util.symbol = ...
    INTERSECT: util.symbol = ...
    INTERSECT_ALL: util.symbol = ...
    keyword: util.symbol = ...
    selects: List[Selectable] = ...
    def __init__(self, keyword: util.symbol, *selects: Selectable, **kwargs: Any) -> None: ...
    def self_group(self, against: Optional[Any] = ...) -> FromGrouping: ...
    def is_derived_from(self, fromclause: FromClause): ...
    def get_children(self, column_collections: bool = ...,
                     **kwargs: Any) -> List[Union[ColumnClause[Any], ClauseElement, Selectable]]: ...
    def bind(self) -> Optional[Union[Engine, Connection]]: ...
    @classmethod
    def _create_union(cls, *selects: Selectable, **kwargs: Any) -> CompoundSelect: ...
    @classmethod
    def _create_union_all(cls, *selects: Selectable, **kwargs: Any) -> CompoundSelect: ...
    @classmethod
    def _create_except(cls, *selects: Selectable, **kwargs: Any) -> CompoundSelect: ...
    @classmethod
    def _create_except_all(cls, *selects: Selectable, **kwargs: Any) -> CompoundSelect: ...
    @classmethod
    def _create_intersect(cls, *selects: Selectable, **kwargs: Any) -> CompoundSelect: ...
    @classmethod
    def _create_intersect_all(cls, *selects: Selectable, **kwargs: Any) -> CompoundSelect: ...

_SE = TypeVar('_SE', bound=Select)

class Select(HasPrefixes, HasSuffixes, GenerativeSelect):
    __visit_name__: str = ...
    def __init__(self, columns: Optional[Iterable[Union[ColumnElement[Any], FromClause, int]]] = ...,
                 whereclause: Optional[Union[str, bool, Visitable]] = ...,
                 from_obj: Optional[Union[str, Selectable, Iterable[Union[str, Selectable]]]] = ...,
                 group_by: Optional[Union[int, str, Visitable, Iterable[Union[int, str, Visitable]]]] = ...,
                 having: Optional[Union[str, bool, Visitable]] = ...,
                 order_by: Optional[Union[int, str, Visitable, Iterable[Union[int, str, Visitable]]]] = ...,
                 distinct: bool = ..., correlate: bool = ..., limit: Optional[int] = ..., offset: Optional[int] = ...,
                 use_labels: bool = ..., autocommit: bool = ..., bind: Union[Engine, Connection] = ...,
                 prefixes: Optional[Any] = ..., suffixes: Optional[Any] = ...,
                 **kwargs: Any) -> None: ...
    @property
    def froms(self) -> List[FromClause]: ...
    def with_statement_hint(self: _SE, text: str, dialect_name: str = ...) -> _SE: ...
    def with_hint(self: _SE, selectable: Union[Table, Alias], text: str, dialect_name: str = ...) -> _SE: ...
    @property
    def type(self) -> Any: ...
    @property
    def locate_all_froms(self) -> List[FromClause]: ...
    @property
    def inner_columns(self) -> Iterable[ColumnElement[Any]]: ...
    def is_derived_from(self, fromclause: FromClause) -> bool: ...
    def get_children(self, column_collections: bool = ..., **kwargs: Any) -> List[ClauseElement]: ...
    def column(self: _SE, column: ColumnElement[Any]) -> _SE: ...
    def reduce_columns(self: _SE, only_synonyms: bool = ...) -> _SE: ...
    def with_only_columns(self: _SE, columns: Iterable[ColumnElement[Any]]) -> _SE: ...
    def where(self: _SE, whereclause: Union[str, bool, Visitable]) -> _SE: ...
    def having(self: _SE, having: Union[str, bool, Visitable]) -> _SE: ...
    def distinct(self: _SE, *expr: ColumnElement[Any]) -> _SE: ...
    def select_from(self: _SE, fromclause: FromClause) -> _SE: ...
    def correlate(self: _SE, *fromclauses: FromClause) -> _SE: ...
    def correlate_except(self: _SE, *fromclauses: FromClause) -> _SE: ...
    def append_correlation(self, fromclause: FromClause) -> None: ...
    def append_column(self, column: ColumnElement[Any]) -> None: ...
    def append_prefix(self, clause) -> None: ...
    def append_whereclause(self, whereclause: Union[str, bool, Visitable]) -> None: ...
    def append_having(self, having: Union[str, bool, Visitable]) -> None: ...
    def append_from(self, fromclause: FromClause) -> None: ...
    def self_group(self: _SE, against: Optional[Any] = ...) -> Union[_SE, FromGrouping]: ...
    def union(self, other: Selectable, **kwargs: Any) -> CompoundSelect: ...
    def union_all(self, other: Selectable, **kwargs: Any) -> CompoundSelect: ...
    def except_(self, other: Selectable, **kwargs: Any) -> CompoundSelect: ...
    def except_all(self, other: Selectable, **kwargs: Any) -> CompoundSelect: ...
    def intersect(self, other: Selectable, **kwargs: Any) -> CompoundSelect: ...
    def intersect_all(self, other: Selectable, **kwargs: Any) -> CompoundSelect: ...
    def bind(self) -> Optional[Union[Engine, Connection]]: ...

_SS = TypeVar('_SS', bound=ScalarSelect)

class ScalarSelect(Generative, Grouping[_T]):
    element: ClauseElement = ...
    type: TypeEngine[_T] = ...
    def __init__(self, element: ClauseElement) -> None: ...
    @property
    def columns(self): ...
    c: Any = ...
    def where(self: _SS, crit: ClauseElement) -> _SS: ...
    def self_group(self: _SS, **kwargs: Any) -> _SS: ...  # type: ignore  # return type incompatible with all supertypes

class Exists(UnaryExpression):
    __visit_name__: Any = ...
    def __init__(self, *args: Union[Select, str], **kwargs: Any) -> None: ...
    def select(self, whereclause: Optional[Union[str, bool, Visitable]] = ..., **params: Any) -> Select: ...
    def correlate(self, *fromclause: FromClause) -> Exists: ...
    def correlate_except(self, *fromclause: FromClause) -> Exists: ...
    def select_from(self, clause: FromClause) -> Exists: ...
    def where(self, clause: ClauseElement) -> Exists: ...

_TAF = TypeVar('_TAF', bound=TextAsFrom)

class TextAsFrom(SelectBase):
    __visit_name__: str = ...
    element: TextClause = ...
    column_args: Any = ...
    positional: Any = ...
    def __init__(self, text: TextClause, columns: ColumnClause[Any], positional: bool = ...) -> None: ...
    def bindparams(self: _TAF, *binds: BindParameter[Any], **bind_as_values: Any) -> _TAF: ...

class AnnotatedFromClause(Annotated[FromClause]):
    def __init__(self, element: FromClause, values: Any) -> None: ...
