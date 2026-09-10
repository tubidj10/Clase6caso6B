"""Cliente mínimo de Responses API; no guarda ni imprime credenciales."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request

MODEL = "gpt-5-mini-2025-08-07"
INPUT_PRICE = 0.25 / 1_000_000
CACHED_PRICE = 0.025 / 1_000_000
OUTPUT_PRICE = 2.0 / 1_000_000
MAX_OUTPUT = 2500


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def call_api(payload):
    # El límite es por esta preparación, independiente del límite de la cuenta.
    # El ledger se mantiene fuera del repositorio y las invocaciones son secuenciales.
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    ledger_path = Path(os.environ.get("UCEMA_BUDGET_LEDGER", ".budget-ledger.json"))
    limit = min(float(os.environ.get("UCEMA_BUDGET_USD", "1.00")), 1.00)
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {"reserved_usd": 0, "calls": []}
    # Una cota conservadora: un token por byte más margen de envoltura y máximo de salida.
    reservation = (len(raw) + 4096) * INPUT_PRICE + MAX_OUTPUT * OUTPUT_PRICE
    if ledger["reserved_usd"] + reservation > limit:
        raise RuntimeError("Se alcanzó el presupuesto de preparación; no se realiza otra llamada")
    ledger["reserved_usd"] += reservation
    ledger["calls"].append({"reserved_usd": reservation, "status": "reserved"})
    write_json(ledger_path, ledger)
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY no está configurada; no se simula una ejecución")
    request = urllib.request.Request("https://api.openai.com/v1/responses", data=raw,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key}, method="POST")
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            result = json.loads(response.read())
    except urllib.error.HTTPError as error:
        # No imprimir headers ni cuerpos de error que pudieran contener credenciales.
        raise RuntimeError("La API devolvió HTTP " + str(error.code)) from None
    usage = result.get("usage", {})
    cached = usage.get("input_tokens_details", {}).get("cached_tokens", 0)
    cost = (usage.get("input_tokens", 0) - cached) * INPUT_PRICE + cached * CACHED_PRICE + usage.get("output_tokens", 0) * OUTPUT_PRICE
    ledger["calls"][-1].update({"status": result.get("status"), "estimated_actual_usd": cost,
        "input_tokens": usage.get("input_tokens", 0), "output_tokens": usage.get("output_tokens", 0)})
    # Se conserva la reserva completa: es un techo acumulado aun si no se obtiene uso.
    write_json(ledger_path, ledger)
    return result, cost, time.perf_counter() - start


def run(project, tool_spec, tool_handler, output_schema, validate):
    base = Path(__file__).resolve().parent.parent
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python3 src/main.py entradas/solicitud_01.json corridas/nueva_corrida")
    entry_path = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve()
    if output_dir.exists():
        raise SystemExit("La carpeta de salida ya existe; usar otra para conservar la corrida anterior")
    entry = json.loads(entry_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True)
    write_json(output_dir / "entrada.json", entry)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (output_dir / "fecha.txt").write_text(timestamp + "\n")
    instructions = (base / "prompts/system_prompt.md").read_text(encoding="utf-8")
    user_template = (base / "prompts/user_prompt.md").read_text(encoding="utf-8")
    conversation = [{"role": "user", "content": user_template + "\n\n" + json.dumps(entry, ensure_ascii=False)}]
    common = {"model": MODEL, "instructions": instructions, "store": False,
        "reasoning": {"effort": "minimal"}, "max_output_tokens": MAX_OUTPUT}
    requests, responses, tool_events, costs, elapsed = [], [], [], [], []
    try:
        first_request = {**common, "input": conversation, "tools": [tool_spec],
            "tool_choice": {"type": "function", "name": tool_spec["name"]}, "parallel_tool_calls": False}
        requests.append(first_request)
        first, cost, seconds = call_api(first_request)
        responses.append(first); costs.append(cost); elapsed.append(seconds)
        write_json(output_dir / "respuesta_api_01.json", first)
        if first.get("status") != "completed":
            raise RuntimeError("Primera respuesta incompleta; se conserva como fallo")
        calls = [item for item in first.get("output", []) if item.get("type") == "function_call"]
        if len(calls) != 1 or calls[0]["name"] != tool_spec["name"]:
            raise RuntimeError("La respuesta no invocó exactamente la herramienta requerida")
        call = calls[0]
        arguments = json.loads(call["arguments"])
        if arguments.get("scenario") != entry["scenario"]:
            raise RuntimeError("La herramienta no corresponde al escenario solicitado")
        observation = tool_handler(base, arguments["scenario"])
        tool_events.append({"name": call["name"], "arguments": arguments, "observation": observation})
        write_json(output_dir / "herramientas.json", tool_events)
        conversation = conversation + first["output"] + [{"type": "function_call_output", "call_id": call["call_id"], "output": json.dumps(observation, ensure_ascii=False)}]
        second_request = {**common, "input": conversation,
            "text": {"format": {"type": "json_schema", "name": project, "schema": output_schema, "strict": True}}}
        requests.append(second_request)
        second, cost, seconds = call_api(second_request)
        responses.append(second); costs.append(cost); elapsed.append(seconds)
        write_json(output_dir / "respuesta_api_02.json", second)
        if second.get("status") != "completed":
            raise RuntimeError("Respuesta final incompleta; se conserva como fallo")
        text = "".join(part["text"] for item in second.get("output", []) if item.get("type") == "message"
            for part in item.get("content", []) if part.get("type") == "output_text")
        (output_dir / "salida_original.txt").write_text(text, encoding="utf-8")
        output = json.loads(text)
        write_json(output_dir / "salida.json", output)
        problems = validate(output, observation)
        write_json(output_dir / "validacion.json", {"ok": not problems, "problems": problems})
        status = "validated" if not problems else "needs_review"
    except Exception as error:
        status = "failed"
        write_json(output_dir / "error.json", {"type": type(error).__name__, "message": str(error)})
    finally:
        write_json(output_dir / "solicitudes_api.json", requests)
        fingerprints = {p.relative_to(base).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for directory in ["src", "prompts", "datos"] for p in sorted((base/directory).rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts}
        write_json(output_dir / "metadata.json", {"timestamp_utc": timestamp, "requested_model": MODEL,
            "returned_models": [r.get("model") for r in responses], "api_calls": len(responses),
            "input_tokens": sum(r.get("usage", {}).get("input_tokens", 0) for r in responses),
            "output_tokens": sum(r.get("usage", {}).get("output_tokens", 0) for r in responses),
            "cost_usd": sum(costs), "latency_seconds": sum(elapsed), "status": status,
            "source_sha256": fingerprints, "pricing": {"input_per_million_usd": 0.25,
            "cached_input_per_million_usd": 0.025, "output_per_million_usd": 2.0,
            "source": "https://developers.openai.com/api/docs/models/gpt-5-mini", "checked_date": "2026-09-09"}})
    print(json.dumps({"status": status, "run": str(output_dir), "cost_usd": sum(costs)}, ensure_ascii=False))
    if status != "validated": raise SystemExit(2)
