from sqlalchemy import Integer, String, Boolean, TIMESTAMP, Column

from src.database import Base


class Operation(Base):
    __tablename__="operation"
    id = Column(Integer, primary_key=True)
    quantity = Column(String)
    figi = Column(String)
    instriment_type = Column(String, nullable=True)
    date = Column(TIMESTAMP)
    operation_type = Column(String)

    
    
    
     
