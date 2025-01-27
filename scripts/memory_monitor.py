# scripts/memory_monitor.py
import time
import torch

class GPUMemoryMonitor:
    def __init__(self, interval=5):
        self.interval = interval  # 监控间隔（秒）
        self._running = False

    def start(self):
        """启动显存监控"""
        self._running = True
        print("GPU Memory Monitor Started")
        while self._running:
            if torch.cuda.is_available():
                allocated = torch.cuda.memory_allocated() / 1024**3
                reserved = torch.cuda.memory_reserved() / 1024**3
                print(f"[Memory Monitor] Allocated: {allocated:.2f}GB | Reserved: {reserved:.2f}GB")
            time.sleep(self.interval)

    def stop(self):
        """停止监控"""
        self._running = False
        print("GPU Memory Monitor Stopped")

if __name__ == "__main__":
    monitor = GPUMemoryMonitor(interval=3)
    try:
        monitor.start()
    except KeyboardInterrupt:
        monitor.stop()