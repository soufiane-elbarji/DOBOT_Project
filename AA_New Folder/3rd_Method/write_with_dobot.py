# write_with_dobot.py – Python 3.5 only

from __future__ import print_function
import json, argparse
import DobotDllType as dType

# ── CLI ARGUMENTS ───────────────────────────────
ap = argparse.ArgumentParser()
ap.add_argument("--json", required=True)
ap.add_argument("--upZ",   type=float, default=-40)
ap.add_argument("--downZ", type=float, default=-59)
args = ap.parse_args()

SAFE_Z  = args.upZ
DRAW_Z  = args.downZ
START_X = 200
START_Y =   0

# ── LOAD STROKES ────────────────────────────────
with open(args.json, "r") as f:
    strokes = json.load(f)

# ── CONNECT DOBOT ───────────────────────────────
api = dType.load()
state = dType.ConnectDobot(api, "COM3", 115200)[0]
if state != dType.DobotConnect.DobotConnect_NoError:
    print("Dobot connection failed.")
    exit()

dType.SetQueuedCmdClear(api)
dType.SetHOMEParams(api, 250, 0, 50, 0)
dType.SetPTPJointParams(api, 200,200,200,200,200,200,200,200)
dType.SetPTPCommonParams(api, 100, 100)
dType.SetHOMECmd(api, 0)

def mov(x, y, z, wait=True):
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, 0)
    if wait: dType.dSleep(10)

# ── DRAW STROKES ────────────────────────────────
for stroke in strokes:
    if not stroke: continue
    sx = START_X + stroke[0][0]
    sy = START_Y + stroke[0][1]
    mov(sx, sy, SAFE_Z)
    mov(sx, sy, DRAW_Z)
    for (px, py) in stroke[1:]:
        mov(START_X + px, START_Y + py, DRAW_Z)
    mov(START_X + stroke[-1][0], START_Y + stroke[-1][1], SAFE_Z)

# ── FINISH ──────────────────────────────────────
dType.SetQueuedCmdStartExec(api)
while dType.GetQueuedCmdCurrentIndex(api)[0] < dType.GetQueuedCmdTotal(api)[0] - 1:
    dType.dSleep(100)
dType.SetQueuedCmdStopExec(api)
dType.DisconnectDobot(api)
print("Poem written.")
