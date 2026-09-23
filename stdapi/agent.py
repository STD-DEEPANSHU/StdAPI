"""
========================================================================
StdAPI 2.1.0 — Autonomous Agent Module (Thin Client)
Protected Client Interface for STD AI OS & Central Brain
Copyright (c) 2026 STD DEEPANSHU (github.com/STD-DEEPANSHU)
All Rights Reserved • Protected under Apache-2.0
========================================================================
"""
import os
import sys
import asyncio
import subprocess
import webbrowser
from pathlib import Path
from typing import Dict, Any, List, Optional
from .client import StdAPIClient
from .results import Result

try:
    import psutil
except ImportError:
    psutil = None


class AgentModule:
    """
    Thin, public-safe client for the STD-AI Master Agentic Brain.
    Executes tasks locally using instructions from StdApiBackend without exposing
    proprietary planning algorithms, prompt engineering, or model heuristics.
    """
    def __init__(self, client: StdAPIClient):
        self.client = client

    async def handshake(self, client_id: str = "default_pc") -> Result:
        """Authenticates with central brain and retrieves signed session token."""
        hostname = os.environ.get("COMPUTERNAME", "unknown-host")
        payload = {
            "client_id": client_id,
            "hostname": hostname,
            "platform": "windows",
            "version": "2.1.0"
        }
        return await self.client._request("POST", "/v1/agent/handshake", json=payload)

    async def recommend_models(self, ram_gb: Optional[float] = None, gpu_name: Optional[str] = None) -> Result:
        """Queries central brain for optimal free local models matching system specs."""
        if ram_gb is None and psutil:
            ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 1)
        elif ram_gb is None:
            ram_gb = 8.0

        payload = {
            "ram_gb": ram_gb,
            "gpu_name": gpu_name or "Integrated"
        }
        return await self.client._request("POST", "/v1/agent/recommend-models", json=payload)

    async def plan(self, prompt: str, project_dir: Optional[str] = None) -> Result:
        """Fetches atomic execution graph from central brain for a user mission."""
        payload = {
            "prompt": prompt,
            "os_name": "windows",
            "project_dir": project_dir
        }
        return await self.client._request("POST", "/v1/agent/plan", json=payload)

    async def self_heal(self, command: str, error_output: str) -> Result:
        """Diagnoses execution errors and retrieves corrective repair steps."""
        payload = {
            "command": command,
            "error_output": error_output
        }
        return await self.client._request("POST", "/v1/agent/self-heal", json=payload)

    async def resolve_software(self, query: str) -> Result:
        """Resolves common software names to official Windows WinGet package IDs."""
        return await self.client._request("GET", "/v1/agent/resolve-software", params={"q": query})

    async def run_mission(self, prompt: str) -> Dict[str, Any]:
        """
        End-to-end execution of user mission:
        1. Handshake with brain
        2. Fetch execution plan
        3. Execute atomic steps locally on Windows (Shell, Files, WinGet, Browser)
        4. Auto self-heal on errors
        """
        print(f"\n[*] [STD-API] Dispatching mission to brain: '{prompt}'...")
        plan_res = await self.plan(prompt)

        intent = plan_res.intent
        voice_ack = plan_res.voice_ack
        steps = plan_res.plan_steps or []

        print(f"[✓] Brain Intent : {intent}")
        print(f"[✓] Voice Reply  : {voice_ack}")
        print(f"[*] Execution Steps : {len(steps)}")

        results = []
        for step in steps:
            s_id = step.get("step_id")
            action = step.get("action")
            desc = step.get("description")
            params = step.get("params", {})

            print(f"\n  [Step {s_id}] {desc}...")

            step_res = self._execute_step(action, params)
            results.append(step_res)

            # Auto self-healing on failure
            if not step_res.get("success", True):
                print(f"  [!] Step failed: {step_res.get('error')}. Requesting self-heal patch...")
                heal_res = await self.self_heal(command=params.get("command", ""), error_output=str(step_res.get("error")))
                if heal_res.can_heal:
                    print(f"  [✓] Diagnosis: {heal_res.diagnosis}")
                    for c_step in heal_res.corrective_steps:
                        print(f"  [Self-Heal] {c_step.get('description')}...")
                        self._execute_step(c_step.get("action"), c_step.get("params", {}))

        return {
            "intent": intent,
            "voice_ack": voice_ack,
            "steps_completed": len(results),
            "summary": plan_res.summary
        }

    def _execute_step(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Local Windows execution engine."""
        try:
            if action == "shell.exec":
                cmd = params.get("command", "")
                timeout = params.get("timeout", 60)
                res = subprocess.run(
                    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                return {"success": res.returncode == 0, "output": res.stdout.strip(), "error": res.stderr.strip()}

            elif action == "shell.exec_background":
                cmd = params.get("command", "")
                cwd = params.get("cwd")
                subprocess.Popen(["cmd.exe", "/c", cmd], cwd=cwd, shell=True)
                return {"success": True, "message": f"Background process spawned: {cmd}"}

            elif action == "fs.mkdir":
                target_dir = Path(params.get("directory", "std_workspace"))
                target_dir.mkdir(parents=True, exist_ok=True)
                return {"success": True, "path": str(target_dir)}

            elif action == "fs.write":
                fpath = Path(params.get("path", "output.txt"))
                fpath.parent.mkdir(parents=True, exist_ok=True)
                fpath.write_text(params.get("content", ""), encoding="utf-8")
                return {"success": True, "path": str(fpath)}

            elif action == "system.open_browser":
                url = params.get("url") or params.get("path")
                if url:
                    if not url.startswith("http") and not Path(url).is_absolute():
                        url = f"file://{Path(url).resolve()}"
                    webbrowser.open(url)
                return {"success": True, "opened": url}

            elif action == "system.notify":
                print(f"  [STD-AI NOTIFICATION] {params.get('message')}")
                return {"success": True}

            else:
                return {"success": True, "action": action}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def launch_hud(self):
        """Launches the native Virtual Desktop HUD application."""
        hud_script = Path(__file__).resolve().parent.parent.parent / "StdAi" / "std_desktop_hud.py"
        if hud_script.exists():
            print(f"[*] Launching STD AI Virtual Desktop HUD from {hud_script}...")
            subprocess.Popen([sys.executable, str(hud_script)])
        else:
            print("[!] HUD script not found locally. Please ensure 'StdAi' repository is cloned.")


class StdAgent:
    """
    High-level user-friendly wrapper for STD AI Agent.
    Usage:
        from stdapi import StdAgent

        agent = StdAgent()
        agent.run("Next.js aur FastAPI ka crypto app bana")
    """
    def __init__(self, base_url: Optional[str] = None):
        self.client = StdAPIClient(base_url=base_url)
        self.module = AgentModule(self.client)

    def run(self, prompt: str):
        """Synchronous wrapper to run agent missions directly."""
        return asyncio.run(self.module.run_mission(prompt))

    def launch_hud(self):
        """Launches native Virtual Desktop HUD."""
        self.module.launch_hud()
