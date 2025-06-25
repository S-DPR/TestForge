from uuid import UUID

import grpc
import json
from dacite import from_dict, Config
from concurrent import futures
from concurrent.futures import ProcessPoolExecutor
from input_generator_service import v1_pb2, v1_pb2_grpc
from request.config_structs import TestcaseConfig
from request.executor import process
from error.exception import ConfigValueError, VariableNotFoundError

from sqlalchemy.orm import Session
from db.sessions import get_db
from db.preset import service, schema
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

from log_common import get_logger

logger = get_logger(__name__)

class TestcaseServicer(v1_pb2_grpc.TestcaseServicer):
    def __init__(self):
        self.CreateTestcaseRes = getattr(v1_pb2, 'CreateTestcaseRes', None)
        self.executor = ProcessPoolExecutor(max_workers=10)

    def CreateTestcase(self, request, context):
        logger.info('테스트케이스 생성 요청 받음')
        logger.debug(request)
        account_id = request.account_id
        format_ = request.format
        repeat_count = request.repeat_count

        logger.info("테스트케이스 설정 생성 시작")
        format_dict = json.loads(format_)
        try:
            testcase_config = from_dict(data_class=TestcaseConfig, data=format_dict)
        except Exception as e:
            logger.error("테스트케이스 설정 생성 실패", e)
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        logger.info("테스트케이스 설정 생성 성공")
        logger.debug(testcase_config)

        try:
            for _ in range(repeat_count):
                if not context.is_active():
                    break
                result = process(account_id, testcase_config)
                yield v1_pb2.CreateTestcaseRes(output=result)
        except ConfigValueError as e:
            logger.error("테스트케이스 생성 중 Value 에러 발생 : %s", e)
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, e.message)
        except VariableNotFoundError as e:
            logger.error("변수 찾기 실패 에러 발생 : %s", e)
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, e.message)
        except Exception as e:
            logger.error("알 수 없는 에러 발생 : %s", e)
            context.abort(grpc.StatusCode.INTERNAL, "서버 내부 오류")

def to_proto_timestamp(dt: datetime) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts

class PresetServicer(v1_pb2_grpc.PresetServicer):
    def __init__(self):
        pass

    def CreatePreset(self, request, context):
        logger.info("프리셋 생성 요청")
        try:
            db: Session = get_db()
            data = schema.PresetCreate(
                preset_name=request.preset_name,
                preset_type=request.preset_type,
                content=request.content,
                account_id=UUID(request.account_id) if request.account_id else None
            )
            preset = service.create_preset(db, data)
            return v1_pb2.PresetResponse(
                preset_id=str(preset.preset_id),
                preset_name=preset.preset_name,
                preset_type=preset.preset_type,
                content=preset.content,
                account_id=str(preset.account_id) if preset.account_id else "",
                create_dt=to_proto_timestamp(preset.create_dt),
                update_dt=to_proto_timestamp(preset.update_dt),
            )
        except Exception as e:
            logger.error("프리셋 생성 중 에러: %s", e)
            context.abort(grpc.StatusCode.INTERNAL, "프리셋 생성 실패")

    def GetPreset(self, request, context):
        logger.info("프리셋 단건 조회")
        try:
            db: Session = get_db()
            preset = service.get_preset(db, UUID(request.preset_id))
            if not preset:
                context.abort(grpc.StatusCode.NOT_FOUND, "Preset not found")

            return v1_pb2.PresetResponse(
                preset_id=str(preset.preset_id),
                preset_name=preset.preset_name,
                preset_type=preset.preset_type,
                content=preset.content,
                account_id=str(preset.account_id) if preset.account_id else "",
                create_dt=to_proto_timestamp(preset.create_dt),
                update_dt=to_proto_timestamp(preset.update_dt),
            )
        except Exception as e:
            logger.error("프리셋 조회 실패: %s", e)
            context.abort(grpc.StatusCode.INTERNAL, "프리셋 조회 실패")

    def GetAllPresets(self, request, context):
        logger.info("프리셋 목록 조회")
        try:
            db: Session = get_db()
            presets = service.get_all_presets(
                db=db,
                account_id=UUID(request.account_id),
                page=request.page,
                size=request.size,
            )
            return v1_pb2.PresetListResponse(
                presets=[
                    v1_pb2.PresetResponse(
                        preset_id=str(p.preset_id),
                        preset_name=p.preset_name,
                        preset_type=p.preset_type,
                        content=p.content,
                        account_id=str(p.account_id) if p.account_id else "",
                        create_dt=to_proto_timestamp(p.create_dt),
                        update_dt=to_proto_timestamp(p.update_dt),
                    )
                    for p in presets
                ]
            )
        except Exception as e:
            logger.error("프리셋 리스트 조회 실패: %s", e)
            context.abort(grpc.StatusCode.INTERNAL, "프리셋 리스트 조회 실패")

    def UpdatePreset(self, request, context):
        logger.info("프리셋 수정 요청")
        try:
            db: Session = get_db()
            data = schema.PresetUpdate(
                preset_id=UUID(request.preset_id),
                preset_name=request.preset_name,
                preset_type=request.preset_type,
                content=request.content,
                account_id=UUID(request.account_id) if request.account_id else None
            )
            preset = service.update_preset(db, data)
            if not preset:
                context.abort(grpc.StatusCode.NOT_FOUND, "Preset not found")

            return v1_pb2.PresetResponse(
                preset_id=str(preset.preset_id),
                preset_name=preset.preset_name,
                preset_type=preset.preset_type,
                content=preset.content,
                account_id=str(preset.account_id) if preset.account_id else "",
                create_dt=to_proto_timestamp(preset.create_dt),
                update_dt=to_proto_timestamp(preset.update_dt),
            )
        except Exception as e:
            logger.error("프리셋 수정 실패: %s", e)
            context.abort(grpc.StatusCode.INTERNAL, "프리셋 수정 실패")

    def DeletePreset(self, request, context):
        logger.info("프리셋 삭제 요청")
        try:
            db: Session = get_db()
            result = service.delete_preset(db, UUID(request.preset_id))
            return v1_pb2.DeletePresetResponse(success=result)
        except Exception as e:
            logger.error("프리셋 삭제 실패: %s", e)
            context.abort(grpc.StatusCode.INTERNAL, "프리셋 삭제 실패")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    v1_pb2_grpc.add_TestcaseServicer_to_server(TestcaseServicer(), server)
    v1_pb2_grpc.add_PresetServicer_to_server(PresetServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("CreateTestcase 서버 실행")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()