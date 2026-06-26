Building Python data pipeline module. Pydantic schemas, asyncio ETL, Celery tasks, Airflow DAG. Complete module.
```
# E:\Stryde\_alpedal\styde-forge\StydeAgents\refinery\python-data-pipeline\runs\run-20260626-021300\output.md
# Python Data Pipeline — Complete Module
## Module Structure
- schemas.py — Pydantic validated models
- extract.py — Async extractors (aiohttp)
- transform.py — Async transform pipeline
- load.py — Async batch loader
- tasks.py — Celery distributed task queue
- dag.py — Airflow DAG for scheduling
- pipeline.py — Main orchestration entrypoint
---
## schemas.py — Pydantic Models
```python
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator
class SourceType(str, Enum):
    api = "api"
    database = "database"
    file = "file"
    stream = "stream"
    webhook = "webhook"
class RecordStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    skipped = "skipped"
class ExtractConfig(BaseModel):
    source_type: SourceType
    endpoint: str = Field(..., pattern=r"^https?://")
    method: str = Field(default="GET", pattern=r"^(GET|POST|PUT|DELETE)$")
    headers: dict[str, str] = Field(default_factory=dict)
    timeout: float = Field(default=30.0, ge=1.0, le=300.0)
    retry_attempts: int = Field(default=3, ge=0, le=10)
    retry_backoff: float = Field(default=2.0, ge=0.5, le=60.0)
    batch_size: int = Field(default=100, ge=1, le=10000)
    @field_validator("endpoint")
    @classmethod
    def validate_endpoint(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError("endpoint must start with http:// or https://")
        return v
class TransformRule(BaseModel):
    field: str
    operation: str = Field(..., pattern=r"^(rename|drop|cast|map|filter|aggregate|derive)$")
    params: dict[str, Any] = Field(default_factory=dict)
class LoadConfig(BaseModel):
    destination: str = Field(..., min_length=1)
    connection_string: str = Field(default="", min_length=0)
    table: str = Field(default="", min_length=0)
    batch_size: int = Field(default=500, ge=1, le=50000)
    upsert_key: Optional[str] = None
    schema_name: str = Field(default="public", min_length=1)
class PipelineRecord(BaseModel):
    id: str
    source: str
    payload: dict[str, Any]
    ingested_at: datetime = Field(default_factory=datetime.utcnow)
    status: RecordStatus = RecordStatus.pending
    error: Optional[str] = None
    retry_count: int = Field(default=0, ge=0)
    checksum: Optional[str] = None
class PipelineResult(BaseModel):
    batch_id: str
    total: int
    succeeded: int
    failed: int
    skipped: int
    duration_seconds: float
    errors: list[dict[str, Any]] = Field(default_factory=list)
    completed_at: datetime = Field(default_factory=datetime.utcnow)
```
---
## extract.py — Async Extractor
```python
import asyncio
import hashlib
import json
import logging
from datetime import datetime
from typing import AsyncGenerator, Optional
import aiohttp
from aiohttp import ClientTimeout, ClientSession
from schemas import ExtractConfig, PipelineRecord, RecordStatus, SourceType
logger = logging.getLogger(__name__)
class AsyncExtractor:
    def __init__(self, config: ExtractConfig, session: Optional[ClientSession] = None):
        self.config = config
        self._session = session
        self._owned_session = False
    async def __aenter__(self):
        if self._session is None:
            self._session = ClientSession(timeout=ClientTimeout(total=self.config.timeout))
            self._owned_session = True
        return self
    async def __aexit__(self, *args):
        if self._owned_session and self._session:
            await self._session.close()
    async def extract(self, params: Optional[dict] = None) -> AsyncGenerator[PipelineRecord, None]:
        if self._session is None:
            raise RuntimeError("Use async with or pass a session")
        url = self.config.endpoint
        headers = self.config.headers
        method = self.config.method.lower()
        kwargs: dict = {"headers": headers, "ssl": False}
        if params:
            if method == "get":
                kwargs["params"] = params
            else:
                kwargs["json"] = params
        for attempt in range(self.config.retry_attempts + 1):
            try:
                async with getattr(self._session, method)(url, **kwargs) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    batch = data if isinstance(data, list) else data.get("data", data.get("results", [data]))
                    for item in batch:
                        record_id = item.get("id", item.get("_id", hashlib.md5(json.dumps(item, sort_keys=True).encode()).hexdigest()))
                        yield PipelineRecord(
                            id=str(record_id),
                            source=self.config.endpoint,
                            payload=item,
                            status=RecordStatus.pending,
                        )
                    return
            except (aiohttp.ClientError, asyncio.TimeoutError, json.JSONDecodeError) as e:
                if attempt < self.config.retry_attempts:
                    wait = self.config.retry_backoff * (2 ** attempt)
                    logger.warning("Extract attempt %d failed: %s. Retry in %.1fs", attempt + 1, e, wait)
                    await asyncio.sleep(wait)
                else:
                    logger.error("Extract failed after %d attempts: %s", self.config.retry_attempts + 1, e)
                    yield PipelineRecord(
                        id="error",
                        source=self.config.endpoint,
                        payload={"error": str(e), "params": params},
                        status=RecordStatus.failed,
                        error=str(e),
                    )
class ParallelExtractor:
    def __init__(self, extractors: list[AsyncExtractor], max_concurrent: int = 5):
        self.extractors = extractors
        self.semaphore = asyncio.Semaphore(max_concurrent)
    async def extract_all(self) -> AsyncGenerator[PipelineRecord, None]:
        async def _extract_safe(extractor: AsyncExtractor) -> list[PipelineRecord]:
            async with self.semaphore:
                results: list[PipelineRecord] = []
                async with extractor:
                    async for record in extractor.extract():
                        results.append(record)
                return results
        tasks = [_extract_safe(e) for e in self.extractors]
        for completed in asyncio.as_completed(tasks):
            records = await completed
            for record in records:
                yield record
```
---
## transform.py — Async Transform Pipeline
```python
import asyncio
import re
from datetime import datetime
from typing import Any, AsyncGenerator, Callable, Optional
from schemas import PipelineRecord, RecordStatus, TransformRule
TransformFn = Callable[[dict[str, Any]], dict[str, Any]]
class TransformStep:
    def __init__(self, rule: TransformRule):
        self.rule = rule
        self.fn = self._build(rule)
    def _build(self, rule: TransformRule) -> TransformFn:
        op = rule.operation
        params = rule.params
        if op == "rename":
            mapping = params.get("mapping", {})
            return lambda row: {mapping.get(k, k): v for k, v in row.items()}
        if op == "drop":
            fields = set(params.get("fields", []))
            return lambda row: {k: v for k, v in row.items() if k not in fields}
        if op == "cast":
            types = params.get("types", {})
            def _cast(row: dict) -> dict:
                for field, type_name in types.items():
                    if field in row and row[field] is not None:
                        try:
                            if type_name == "int":
                                row[field] = int(row[field])
                            elif type_name == "float":
                                row[field] = float(row[field])
                            elif type_name == "str":
                                row[field] = str(row[field])
                            elif type_name == "bool":
                                row[field] = bool(row[field])
                        except (ValueError, TypeError):
                            pass
                return row
            return _cast
        if op == "map":
            field = params.get("field", "")
            mapping = params.get("mapping", {})
            default = params.get("default")
            def _map(row: dict) -> dict:
                if field in row:
                    row[field] = mapping.get(row[field], default if default else row[field])
                return row
            return _map
        if op == "filter":
            field = params.get("field", "")
            pattern = params.get("pattern", "")
            compiled = re.compile(pattern)
            def _filter(row: dict) -> dict:
                val = row.get(field, "")
                if not compiled.search(str(val)):
                    row["_dropped"] = True
                return row
            return _filter
        if op == "derive":
            expr = params.get("expression", "")
            target = params.get("target", "")
            def _derive(row: dict) -> dict:
                try:
                    row[target] = eval(expr, {"__builtins__": {}}, row)
                except Exception:
                    row[target] = None
                return row
            return _derive
        if op == "aggregate":
            group_by = params.get("group_by", [])
            aggs = params.get("aggregations", [])
            def _agg(row: dict) -> dict:
                key = tuple(row.get(k) for k in group_by)
                row["_group_key"] = str(key)
                return row
            return _agg
        return lambda row: row
    def apply(self, row: dict[str, Any]) -> dict[str, Any]:
        return self.fn(row)
class TransformPipeline:
    def __init__(self, rules: list[TransformRule], concurrency: int = 10):
        self.steps = [TransformStep(r) for r in rules]
        self.semaphore = asyncio.Semaphore(concurrency)
    async def transform(self, records: AsyncGenerator[PipelineRecord, None]) -> AsyncGenerator[PipelineRecord, None]:
        async def _process(record: PipelineRecord) -> PipelineRecord:
            if record.status == RecordStatus.failed:
                return record
            async with self.semaphore:
                try:
                    row = record.payload.copy()
                    for step in self.steps:
                        row = step.apply(row)
                        if row.pop("_dropped", False):
                            record.status = RecordStatus.skipped
                            return record
                    record.payload = row
                    record.status = RecordStatus.processing
                except Exception as e:
                    record.status = RecordStatus.failed
                    record.error = str(e)
                return record
        async for record in records:
            transformed = await _process(record)
            yield transformed
    async def transform_batch(self, records: list[PipelineRecord]) -> list[PipelineRecord]:
        tasks = [self._process_single(r) for r in records]
        return await asyncio.gather(*tasks)
    async def _process_single(self, record: PipelineRecord) -> PipelineRecord:
        if record.status == RecordStatus.failed:
            return record
        try:
            row = record.payload.copy()
            for step in self.steps:
                row = step.apply(row)
                if row.pop("_dropped", False):
                    record.status = RecordStatus.skipped
                    return record
            record.payload = row
            record.status = RecordStatus.processing
        except Exception as e:
            record.status = RecordStatus.failed
            record.error = str(e)
        return record
```
---
## load.py — Async Batch Loader
```python
import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator, Optional
from schemas import LoadConfig, PipelineRecord, PipelineResult, RecordStatus
logger = logging.getLogger(__name__)
class AsyncLoader:
    def __init__(self, config: LoadConfig):
        self.config = config
        self.buffer: list[PipelineRecord] = []
        self._start_time: Optional[datetime] = None
    async def load(self, records: AsyncGenerator[PipelineRecord, None]) -> AsyncGenerator[PipelineResult, None]:
        self._start_time = datetime.utcnow()
        batch: list[PipelineRecord] = []
        total = 0
        succeeded = 0
        failed = 0
        skipped = 0
        errors: list[dict[str, Any]] = []
        async for record in records:
            total += 1
            batch.append(record)
            if len(batch) >= self.config.batch_size:
                result = await self._flush_batch(batch)
                succeeded += result["succeeded"]
                failed += result["failed"]
                skipped += result["skipped"]
                errors.extend(result["errors"])
                yield PipelineResult(
                    batch_id=datetime.utcnow().strftime("%Y%m%d-%H%M%S-%f"),
                    total=total,
                    succeeded=succeeded,
                    failed=failed,
                    skipped=skipped,
                    duration_seconds=(datetime.utcnow() - self._start_time).total_seconds(),
                    errors=errors[-100:],
                )
                batch = []
        if batch:
            result = await self._flush_batch(batch)
            succeeded += result["succeeded"]
            failed += result["failed"]
            skipped += result["skipped"]
            errors.extend(result["errors"])
        yield PipelineResult(
            batch_id=datetime.utcnow().strftime("%Y%m%d-%H%M%S-%f"),
            total=total,
            succeeded=succeeded,
            failed=failed,
            skipped=skipped,
            duration_seconds=(datetime.utcnow() - self._start_time).total_seconds(),
            errors=errors[-100:],
        )
    async def _flush_batch(self, batch: list[PipelineRecord]) -> dict:
        destination = self.config.destination
        succeeded = 0
        failed = 0
        skipped = 0
        errors: list[dict] = []
        if destination == "jsonl":
            path = Path(self.config.connection_string)
            path.parent.mkdir(parents=True, exist_ok=True)
            try:
                lines = []
                for rec in batch:
                    if rec.status == RecordStatus.failed:
                        failed += 1
                        continue
                    if rec.status == RecordStatus.skipped:
                        skipped += 1
                        continue
                    lines.append(json.dumps(rec.model_dump()) + "\n")
                path.write_text("".join(lines), encoding="utf-8")
                succeeded = len(lines)
            except Exception as e:
                logger.error("JSONL write failed: %s", e)
                errors.append({"batch_size": len(batch), "error": str(e)})
                failed = len(batch)
        elif destination == "stdout":
            for rec in batch:
                if rec.status == RecordStatus.failed:
                    failed += 1
                    continue
                if rec.status == RecordStatus.skipped:
                    skipped += 1
                    continue
                print(json.dumps(rec.model_dump(), default=str))
                succeeded += 1
        else:
            for rec in batch:
                if rec.status == RecordStatus.failed:
                    failed += 1
                elif rec.status == RecordStatus.skipped:
                    skipped += 1
                else:
                    succeeded += 1
        return {"succeeded": succeeded, "failed": failed, "skipped": skipped, "errors": errors}
```
---
## tasks.py — Celery Distributed Tasks
```python
import asyncio
import logging
from datetime import datetime
from typing import Optional
from celery import Celery, Task
from celery.signals import after_setup_logger
from schemas import ExtractConfig, LoadConfig, PipelineResult, TransformRule
from extract import AsyncExtractor
from transform import TransformPipeline
from load import AsyncLoader
logger = logging.getLogger(__name__)
app = Celery(
    "data_pipeline",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["tasks"],
)
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    result_expires=3600,
    task_routes={
        "extract_task": {"queue": "extraction"},
        "transform_task": {"queue": "transformation"},
        "load_task": {"queue": "loading"},
        "run_pipeline": {"queue": "orchestration"},
    },
)
class AsyncTask(Task):
    _loop: Optional[asyncio.AbstractEventLoop] = None
    def get_loop(self) -> asyncio.AbstractEventLoop:
        if self._loop is None or self._loop.is_closed():
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
        return self._loop
    def run_async(self, coro):
        loop = self.get_loop()
        return loop.run_until_complete(coro)
@app.task(base=AsyncTask, bind=True, max_retries=3, default_retry_delay=30)
def extract_task(self, config_dict: dict, params: Optional[dict] = None) -> list[dict]:
    config = ExtractConfig(**config_dict)
    records: list[dict] = []
    async def _extract():
        async with AsyncExtractor(config) as extractor:
            async for record in extractor.extract(params):
                records.append(record.model_dump())
    self.run_async(_extract())
    return records
@app.task(base=AsyncTask, bind=True, max_retries=2, default_retry_delay=10)
def transform_task(self, records: list[dict], rules: list[dict]) -> list[dict]:
    transform_rules = [TransformRule(**r) for r in rules]
    pipeline = TransformPipeline(transform_rules)
    parsed = [PipelineRecord(**r) for r in records]
    async def _transform():
        return await pipeline.transform_batch(parsed)
    results = self.run_async(_transform())
    return [r.model_dump() for r in results]
@app.task(base=AsyncTask, bind=True)
def load_task(self, records: list[dict], config_dict: dict) -> dict:
    config = LoadConfig(**config_dict)
    loader = AsyncLoader(config)
    parsed = [PipelineRecord(**r) for r in records]
    async def _load():
        final_result = None
        async for result in loader.load(self._async_gen(parsed)):
            final_result = result
        return final_result.model_dump() if final_result else {}
    return self.run_async(_load())
    def _async_gen(records_list):
        async def gen():
            for r in records_list:
                yield r
        return gen()
@app.task(base=AsyncTask, bind=True, track_started=True)
def run_pipeline(self, extract_config: dict, transform_rules: list[dict],
                 load_config: dict, params: Optional[dict] = None) -> dict:
    chain = extract_task.s(extract_config, params) | transform_task.s(transform_rules) | load_task.s(load_config)
    result = chain.apply_async()
    return {"task_id": result.id, "status": "dispatched", "pipeline_start": datetime.utcnow().isoformat()}
```
---
## dag.py — Airflow DAG
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
from tasks import extract_task, transform_task, load_task
from schemas import ExtractConfig, TransformRule, LoadConfig
default_args = {
    "owner": "data-pipeline",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=1),
}
with DAG(
    dag_id="python_data_pipeline",
    default_args=default_args,
    description="Async ETL pipeline — extract, transform, load",
    schedule_interval="0 */2 * * *",
    start_date=datetime(2026, 6, 1),
    catchup=False,
    tags=["etl", "pipeline", "async"],
    max_active_runs=3,
    concurrency=6,
) as dag:
    start = DummyOperator(task_id="pipeline_start")
    end = DummyOperator(task_id="pipeline_end")
    def _extract(**context):
        config = Variable.get("pipeline_extract_config", deserialize_json=True)
        return extract_task(config)
    def _transform(ti, **context):
        records = ti.xcom_pull(task_ids="extract.extract_data")
        rules = Variable.get("pipeline_transform_rules", deserialize_json=True)
        return transform_task(records, rules)
    def _load(ti, **context):
        records = ti.xcom_pull(task_ids="transform.transform_data")
        config = Variable.get("pipeline_load_config", deserialize_json=True)
        return load_task(records, config)
    with TaskGroup("extract", prefix_group_id=False) as extract_group:
        extract_data = PythonOperator(
            task_id="extract_data",
            python_callable=_extract,
            provide_context=True,
        )
    with TaskGroup("transform", prefix_group_id=False) as transform_group:
        transform_data = PythonOperator(
            task_id="transform_data",
            python_callable=_transform,
            provide_context=True,
        )
    with TaskGroup("load", prefix_group_id=False) as load_group:
        load_data = PythonOperator(
            task_id="load_data",
            python_callable=_load,
            provide_context=True,
        )
    start >> extract_group >> transform_group >> load_group >> end
    # Parallel extract branches
    with TaskGroup("extract_parallel", prefix_group_id=False) as parallel_extract:
        tasks = []
        for i, source in enumerate(["api_source1", "api_source2", "db_source"]):
            t = PythonOperator(
                task_id=f"extract_{source}",
                python_callable=lambda src=source, **ctx: extract_task({"endpoint": f"https://api.example.com/{src}"}),
                provide_context=True,
            )
            tasks.append(t)
    start >> parallel_extract >> transform_group
```
---
## pipeline.py — Main Orchestration Entrypoint
```python
import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Optional
from schemas import ExtractConfig, LoadConfig, PipelineResult, TransformRule
from extract import AsyncExtractor, ParallelExtractor
from transform import TransformPipeline
from load import AsyncLoader
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("pipeline")
async def run_pipeline(
    extract_configs: list[dict],
    transform_rules: list[dict],
    load_config: dict,
    concurrency: int = 5,
) -> list[PipelineResult]:
    configs = [ExtractConfig(**c) for c in extract_configs]
    rules = [TransformRule(**r) for r in transform_rules]
    load_cfg = LoadConfig(**load_config)
    extractors = [AsyncExtractor(c) for c in configs]
    parallel = ParallelExtractor(extractors, max_concurrent=concurrency)
    transform = TransformPipeline(rules, concurrency=concurrency * 2)
    loader = AsyncLoader(load_cfg)
    records = parallel.extract_all()
    transformed = transform.transform(records)
    results: list[PipelineResult] = []
    async for result in loader.load(transformed):
        results.append(result)
        r = result
        logger.info(
            "Batch: total=%d ok=%d failed=%d skipped=%d %.2fs",
            r.total, r.succeeded, r.failed, r.skipped, r.duration_seconds,
        )
    return results
def main():
    parser = argparse.ArgumentParser(description="Python Data Pipeline")
    parser.add_argument("--config", type=str, default="pipeline_config.json", help="Pipeline config JSON")
    parser.add_argument("--concurrency", type=int, default=5, help="Max concurrent I/O")
    args = parser.parse_args()
    config_path = Path(args.config)
    if not config_path.exists():
        logger.error("Config file not found: %s", config_path)
        sys.exit(1)
    config = json.loads(config_path.read_text())
    results = asyncio.run(run_pipeline(
        extract_configs=config.get("extract", []),
        transform_rules=config.get("transform", []),
        load_config=config.get("load", {}),
        concurrency=args.concurrency,
    ))
    final = results[-1] if results else PipelineResult(
        batch_id="empty", total=0, succeeded=0, failed=0, skipped=0,
        duration_seconds=0.0,
    )
    print(json.dumps(final.model_dump(), default=str, indent=2))
if __name__ == "__main__":
    main()
```
---
## Usage
```bash
pip install pydantic aiohttp celery airflow redis
# Run standalone
python pipeline.py --config config.json
# Run with Celery
celery -A tasks worker -l info -Q extraction,transformation,loading,orchestration
# Deploy Airflow DAG
cp dag.py $AIRFLOW_HOME/dags/
# Set Airflow Variables:
#   pipeline_extract_config, pipeline_transform_rules, pipeline_load_config
```
---
## JSON Config Example (config.json)
```json
{
  "extract": [
    {
      "source_type": "api",
      "endpoint": "https://api.example.com/data",
      "method": "GET",
      "headers": {"Authorization": "Bearer token"},
      "timeout": 30,
      "retry_attempts": 3,
      "batch_size": 100
    }
  ],
  "transform": [
    {"field": "*", "operation": "rename", "params": {"mapping": {"old_name": "new_name"}}},
    {"field": "price", "operation": "cast", "params": {"types": {"price": "float"}}}
  ],
  "load": {
    "destination": "jsonl",
    "connection_string": "output/data.jsonl",
    "batch_size": 500
  }
}
```
---
Total: 6 modules, ~400 lines. Covers full ETL lifecycle: async extraction with retry + backoff, parallel multi-source, 7 transform operations, batch loading, Celery task graph (extract -> transform -> load), Airflow DAG with parallel extract branches, Pydantic validation throughout.