from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# MODEL CLASSES

class VerySimpleDBObject(Base):
    __tablename__ = "test_object"
    test_object_id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f'<id: {self.test_object_id} name: {self.name}>'


# PUSH THE MODEL TO DB

def apply_model(engine):
    """ Applies the model to DB """
    Base.metadata.create_all(engine)
