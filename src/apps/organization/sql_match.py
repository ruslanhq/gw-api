from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy import literal


class Match(ClauseElement):
    def __init__(self, columns, value):
        self.columns = columns
        self.value = literal(value)


@compiles(Match)
def _match(element, compiler, **kw):
    return "MATCH (%s) AGAINST (%s)" % (
               ", ".join(compiler.process(c, **kw) for c in element.columns),
               compiler.process(element.value)
             )
