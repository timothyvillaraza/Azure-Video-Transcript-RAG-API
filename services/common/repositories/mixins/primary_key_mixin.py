class PrimaryKeyMixin:
    @classmethod
    def get_primary_key_with_table(cls):
        if not hasattr(cls, '__tablename__') or not hasattr(cls, '__table__'):
            raise AttributeError(f"Class {cls.__name__} does not have a __tablename__ or __table__ attribute.")
        
        primary_key_columns = list(cls.__table__.primary_key)
        
        if not primary_key_columns:
            raise AttributeError(f"Class {cls.__name__} does not have a primary key defined.")
        
        if len(primary_key_columns) > 1:
            raise AttributeError(f"Class {cls.__name__} has a composite primary key, which is not supported by this method.")
        
        primary_key_column = primary_key_columns[0]
        primary_key_name = primary_key_column.name
        return f"{cls.__tablename__}.{primary_key_name}"