from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Literal

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from fastapi.responses import FileResponse

# from google.cloud import storage

router = APIRouter()

PYTEST_REPORT_PATH = "Reports/latest/pytest_report.html"


@router.post(
    "/run-tests",
    tags=["Automation"],
    summary="To run smoke/sanity/regression",
)
async def run_tests(
    env: Literal["stage", "dev"] = Query(
        default="stage",
        title=" Environment Argument",
        description="Environment in which you want to run the test.",
        example="stage",
    ),
    suite: Literal["smoke", "sanity", "regression"] = Query(
        "smoke",
        title="Pytest suites",
        description="Group of test cases grouped "
        "by the keyword using pytest marker",
    ),
    pytest_args: str = Query(
        None,
        title="Pytest Arguments",
        description="Additional pytest arguments "
        "to customize the test run.",
        examples=[
            "-k session",
        ],
    ),
):
    try:
        pytest_command = [
            "pytest",
            "-v",
            f"--env={env}",
            f"tests/{suite}",
        ]
        if pytest_args:
            del pytest_command
            pytest_command = [
                "pytest",
                "-v",
                f"--env={env}",
            ]
            pytest_command.append(pytest_args)

        print("Pytest path is : ", os.getcwd())
        print("Running command:", " ".join(pytest_command))
        # Run pytest asynchronously
        process = await asyncio.create_subprocess_exec(
            *pytest_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # Read the output and error streams asynchronously
        stdout, stderr = await process.communicate()

        result = {
            "status": "success" if process.returncode == 0 else "failure",
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "returncode": process.returncode,
            "command": " ".join(pytest_command),
        }
        pretty_json = json.dumps(result, indent=4)

        return pretty_json
    except Exception as e:
        result = {"status": "error", "message": str(e)}

        return json.dumps(result, indent=4)


@router.get(
    "/pytest-report",
    tags=["Automation"],
    summary="To view the pytest-html report",
)
async def get_pytest_report():
    """
    Serve the pytest HTML report.
    """
    if os.path.exists(Path.home() / PYTEST_REPORT_PATH):
        return FileResponse(Path.home() / PYTEST_REPORT_PATH)
    else:
        raise HTTPException(
            status_code=404,
            detail="Report not found, Rerun pytest to view report",
        )
