from db.db import Base
from db.sessions import engine
from db.tcgen.model import TcGen
from db.tcgen_block.model import TcGenBlock
from db.tcgen_file.model import TcGenFile

if __name__ == "__main__":
    print("✅ Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("🎉 DB setup complete.")