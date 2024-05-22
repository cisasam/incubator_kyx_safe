from incubator.config.config import config_logger, load_config
from incubator.physical_twin.controller_from_kyx import ControllerSafeKyx
from incubator.physical_twin.low_level_driver_server import CTRL_EXEC_INTERVAL



def start_controller_from_kyx(ok_queue=None):
    config_logger("logging.conf")
    config = load_config("startup.conf")
    controller = ControllerSafeKyx(rabbit_config=config["rabbitmq"])
    controller.setup(step_size=CTRL_EXEC_INTERVAL, std_dev=0.001,
                  Theater_covariance_init=0.001, T_covariance_init=0.001,
                  **(config["digital_twin"]["models"]["plant"]["param4"]))

    if ok_queue is not None:
        ok_queue.put("OK")

    controller.start_control()


if __name__ == '__main__':
    start_controller_from_kyx()