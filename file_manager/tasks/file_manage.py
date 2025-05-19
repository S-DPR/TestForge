import uuid

from celery_app import celery_app

@celery_app.task(name='file_manager.save')
def save_file_from_cfg_dict(cfg: dict):
    return save_file(**cfg)

def save_file(filepath: str, content: str, ext: str = ".txt") -> dict[str, str]:
    filename = str(uuid.uuid4())
    p = f"{filepath}/{filename}.{ext}"
    with open(p, "w") as f:
        f.write(content)
    return {
        "filepath": p
    }
