from sqlmodel import create_engine, SQLModel, Session, select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from config import settings

db = None

class DB:
    def __init__(self):
        conn_str = (
            "postgresql://{user}:{password}@{host}:{port}/{database}"
            .format(
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                database=settings.POSTGRES_DB,
            )
        )
        self._engine = create_engine(conn_str)
        SQLModel.metadata.create_all(self._engine)

    def create(self, entry):
        if entry.id != None:
            entry.id = None
        try:
            with Session(self._engine) as session:
                session.add(entry)
                session.commit()
                session.refresh(entry)
            return True, entry
        except Exception as e:
            return False, str(e)
        
    def delete(self, model, id):
        try:
            with Session(self._engine) as session:
                stmt = select(model).where(model.id == id)
                res = session.exec(stmt)
                entry = res.one()
                session.delete(entry)
                session.commit()
            return True, 1
        except MultipleResultsFound:
            return False, f"Multiple results found for ID {id}"
        except NoResultFound:
            return True, 0
        
    def update(self, model, id, content):
        if content.id != None:
            content.id = None
        try:
            with Session(self._engine) as session:
                stmt = select(model).where(model.id == id)
                res = session.exec(stmt)
                entry = res.one()

                d_content = dict(content)
                for key, val in d_content.items():
                    if val != None:
                        setattr(entry, key, val)

                session.add(entry)
                session.commit()
                session.refresh(entry)

            return True, entry
        except MultipleResultsFound:
            return False, f"Multiple results found for ID {id}"
        except NoResultFound:
            return True, None
        
    def retrieve(self, model, id):
        try:
            with Session(self._engine) as session:
                stmt = select(model).where(model.id == id)
                res = session.exec(stmt)
                entry = res.one()
            return True, entry
        except MultipleResultsFound:
            return False, f"Multiple results found for ID {id}"
        except NoResultFound:
            return False, None
        
    def enumerate(self, model):
        with Session(self._engine) as session:
            stmt = select(model)
            res = session.exec(stmt)
            entries = res.all()
        return True, entries

    def retrieve_link(self, model, cart_id, item_id):
        try:
            with Session(self._engine) as session:
                stmt = select(model).where(model.cart_id == cart_id, model.item_id == item_id)
                res = session.exec(stmt)
                entry = res.one()
            return True, entry
        except MultipleResultsFound:
            return False, f"Multiple results found for ID {id}"
        except NoResultFound:
            return True, None
        

    def retrieve_cart_items(self, model, cart_id = None, item_id = None):
        with Session(self._engine) as session:
            stmt = select(model)
            if cart_id != None:
                stmt = stmt.where(model.cart_id == cart_id)
            if item_id != None:
                stmt = stmt.where(model.item_id == item_id)
            res = session.exec(stmt)
            entries = res.all()
        return True, entries
    

    def clear_cart(self, model, cart_id):
        with Session(self._engine) as session:
            stmt = select(model).where(model.cart_id == cart_id)
            res = session.exec(stmt)
            entries = res.all()
            for entry in entries:
                session.delete(entry)
            session.commit()

def sc_database():
    global db
    if not db:
        db = DB()
    return db