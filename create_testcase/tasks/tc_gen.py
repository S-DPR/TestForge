from create_testcase.celery_app import celery_app
from request.config_structs import TestcaseConfig
from dacite import from_dict
from request.executor import process


@celery_app.task(name='tc_gen.tc_raw')
def tc_gen_raw_from_cfg_dict(cfg: dict):
    return tc_gen_raw(**cfg)

def tc_gen_raw(testcaseConfig: dict):
    return process(from_dict(data_class=TestcaseConfig, data=testcaseConfig))

@celery_app.task(name='tc_gen.tc_upload')
def tc_gen_upload_from_cfg_dict(cfg: dict):
    return tc_gen_upload(**cfg)

def tc_gen_upload(folder: str, testcaseConfig: dict, ext: str):
    return {
        "folder": folder,
        "content": process(from_dict(data_class=TestcaseConfig, data=testcaseConfig)),
        "ext": ext
    }
