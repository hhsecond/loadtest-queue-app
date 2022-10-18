from pathlib import Path
from typing import Optional
import subprocess

from lightning.app import LightningFlow, LightningApp, LightningWork
from lightning.app import CloudCompute


class LocustWork(LightningWork):
    def __init__(self, work_id: int, is_master: Optional[bool] = False):
        super().__init__(parallel=True)
        self.work_id = work_id
        self.is_master = is_master

    def run(self, master_ip: Optional[str] = None, master_port: Optional[int] = None):

        if not self.is_master and (master_ip is None or master_port is None):
            raise ValueError("master_ip is required for slave nodes")

        if self.is_master:
            command = ["locust", "--web-host", "0.0.0.0", "--web-port", str(self.port), "--master"]
        else:
            command = ["locust", "--worker", "--master-host", master_ip]

        subprocess.run(command, cwd=Path(__file__).parent, check=True)


class Root(LightningFlow):
    def __init__(self):
        super().__init__()
        compute = CloudCompute()
        self.master = LocustWork(0, is_master=True)
        self.master.cloud_compute = compute

        self.slave1 = LocustWork(1)
        self.slave1.cloud_compute = compute

        self.slave2 = LocustWork(1)
        self.slave2.cloud_compute = compute

        self.slave3 = LocustWork(1)
        self.slave3.cloud_compute = compute

        self.slave4 = LocustWork(1)
        self.slave4.cloud_compute = compute

        self.slave5 = LocustWork(1)
        self.slave5.cloud_compute = compute

        self.slave6 = LocustWork(1)
        self.slave6.cloud_compute = compute

        self.slave7 = LocustWork(1)
        self.slave7.cloud_compute = compute

        self.slave8 = LocustWork(1)
        self.slave8.cloud_compute = compute

        self.slave9 = LocustWork(1)
        self.slave9.cloud_compute = compute

        self.slave10 = LocustWork(1)
        self.slave10.cloud_compute = compute

    def run(self):
        self.master.run()
        print(self.master.internal_ip, self.master.port)
        if self.master.is_running and self.master.internal_ip:
            self.slave1.run(master_ip=self.master.internal_ip, master_port=self.master.port)
            self.slave2.run(master_ip=self.master.internal_ip, master_port=self.master.port)
            self.slave3.run(master_ip=self.master.internal_ip, master_port=self.master.port)
            self.slave4.run(master_ip=self.master.internal_ip, master_port=self.master.port)
            self.slave5.run(master_ip=self.master.internal_ip, master_port=self.master.port)
            self.slave6.run(master_ip=self.master.internal_ip, master_port=self.master.port)
            self.slave7.run(master_ip=self.master.internal_ip, master_port=self.master.port)
            self.slave8.run(master_ip=self.master.internal_ip, master_port=self.master.port)
            self.slave9.run(master_ip=self.master.internal_ip, master_port=self.master.port)
            self.slave10.run(master_ip=self.master.internal_ip, master_port=self.master.port)

    def configure_layout(self):
        return {"name": "Dashboard", "content": self.master.url}


app = LightningApp(Root())

