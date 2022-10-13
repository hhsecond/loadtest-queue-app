from pathlib import Path
from typing import Optional
import subprocess

from lightning.app import LightningFlow, LightningApp, LightningWork
from lightning.app.structures import List
from lightning.app import CloudCompute


class LocustWork(LightningWork):
    def __init__(self, work_id: int, compute_config: CloudCompute, is_master: Optional[bool] = False):
        super().__init__(cloud_compute=compute_config, parallel=True)
        self.work_id = work_id
        self.is_master = is_master

    def run(self, master_ip: Optional[str] = None, master_port: Optional[str] = None):

        if not self.is_master and (master_ip is None or master_port is None):
            raise ValueError("master_ip is required for slave nodes")

        if self.is_master:
            command = ["locust", "--web-host", "0.0.0.0", "--web-port", str(self.port), "--master"]
        else:
            command = ["locust", "--worker", "--master-host", master_ip, "--master-port", master_port]

        subprocess.run(command, cwd=Path(__file__).parent, check=True)


class Root(LightningFlow):
    def __init__(self):
        super().__init__()
        self.slaves = List()
        self.compute = CloudCompute()
        self.master = LocustWork(0, self.compute, is_master=True)

    def run(self):
        self.master.run()

        num_workers = 1

        for i in range(1, num_workers + 1):
            self.slaves.append(LocustWork(i, self.compute))

        for w in self.slaves:
            w.run(master_ip=self.master.internal_ip, master_port=self.master.port)

    def configure_layout(self):
        return {"name": "Dashboard", "content": self.master.url}


app = LightningApp(Root())
