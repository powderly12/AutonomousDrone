
"""
Simple example that connects to the first Crazyflie found, logs the Stabilizer
and prints it to the console. After 10s the application disconnects and exits.

This example utilizes the SyncCrazyflie and SyncLogger classes.
"""
import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.utils import uri_helper


uri = uri_helper.uri_from_env(default='radio://0/6/2M/EE5C21CF05')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='motion', period_in_ms=100)
    lg_stab.add_variable('motion.min Raw', 'float')


    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(uri, cf=cf) as scf:
        # Note: it is possible to add more than one log config using an
        # array.
        # with SyncLogger(scf, [lg_stab, other_conf]) as logger:
        with SyncLogger(scf, lg_stab) as logger:
            endTime = time.time() + 10

            for log_entry in logger:
                timestamp = log_entry[0]
                data = log_entry[1]
                logconf_name = log_entry[2]

                print('[%d][%s]: %s' % (timestamp, logconf_name, data))

                if time.time() > endTime:
                    break