from db.db import Base
from db.sessions import engine
from db.code_file.model import CodeFile
from db.code_res.model import CodeRes

if __name__ == "__main__":
    print("✅ Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("🎉 DB setup complete.")