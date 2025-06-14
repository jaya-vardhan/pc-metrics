from pc_metrics import PcMetrics
from dotenv import load_dotenv

def get_metrics():
    pc = PcMetrics()
    res = pc.get_metrics()
    print(res)


def create_app():
    load_dotenv()

def init():
    create_app()
    get_metrics()

if __name__ == '__main__':
    init()
