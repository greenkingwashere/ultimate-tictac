import enum



class square(enum.Enum):
    """Enum used to represent squares on boards and winners."""


    none = '*'
    x = 'x'
    o = 'o'
    draw = '_'