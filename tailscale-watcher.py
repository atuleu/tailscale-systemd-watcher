#!/usr/bin/env python3
import json
import subprocess
from typing import Dict


def get_tailscale_node_status():
    completed = subprocess.run(["/usr/bin/tailscale","status","--json"],capture_output=True)
    completed.check_returncode()
    status = json.loads(completed.stdout)
    res = {}
    for node in status["Peer"].values():
        res[node["HostName"]] =node["Online"]
    return res

state_filepath = '/tmp/tailscale-watcher.json'

def get_previous_state():
    try:
        with open(state_filepath) as f:
            return json.load(f)
    except:
        return {}

def save_state(status: Dict[str,bool]):
    try:
        with open(state_filepath,'w') as f:
            json.dump(status,f)
    except:
        pass


def main():
    status = get_tailscale_node_status()
    previous_state = get_previous_state()
    save_state(status)
    for node,current in status.items():
        if current == previous_state.get(node,False):
            # no state change
            continue
        service_name = "tailscale-node-online@" + node + ".target"
        if current == True:
            #node went online
            subprocess.run(["/usr/bin/systemctl","start",service_name])
        else:
            #node went offline
            subprocess.run(["/usr/bin/systemctl","stop",service_name])

if __name__ == "__main__":
    main()
