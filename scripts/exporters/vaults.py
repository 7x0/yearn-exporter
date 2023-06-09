import logging
from datetime import datetime, timezone
from time import time

import sentry_sdk
from brownie import chain
from yearn.networks import Network
from yearn.snapshot_range_helper import (start_bidirectional_export,
                                         time_tracking)
from yearn.utils import closest_block_after_timestamp

sentry_sdk.set_tag('script','vaults_exporter')

logger = logging.getLogger('yearn.vaults_exporter')

def main():
    if Network(chain.id) == Network.Fantom:
        # end: 2021-04-30 first possible date after the Fantom network upgrade
        start = datetime(2021, 4, 30, tzinfo=timezone.utc)
        # ironbank first product deployed on Fantom
        data_query = 'ironbank{network="FTM"}'
    elif Network(chain.id) == Network.Gnosis:
        # end: yvUSDC vault January-20-2022 06:10:45 AM +-6 UTC
        start = datetime(2022, 1, 20, tzinfo=timezone.utc)
        data_query = 'yearn_vault{network="GNO"}'
    elif Network(chain.id) == Network.Arbitrum:
        # end: yvUSDC 4.3 Sep-05-2021 09:05:50 PM +UTC
        start = datetime(2021, 9, 5, tzinfo=timezone.utc)
        data_query = 'yearn_vault{network="ARBB"}'
    elif Network(chain.id) == Network.Optimism:
        # end: yvDAI Aug-06-2022 10:50:49 PM +UTC block 18111485
        start = datetime(2022, 8, 6, tzinfo=timezone.utc)
        data_query = 'yearn_vault{network="OPT"}'
    elif Network(chain.id) == Network.Mainnet:
        # end: 2020-02-12 first iearn deployment
        start = datetime(2020, 2, 12, 0, 1, tzinfo=timezone.utc)
        data_query = 'iearn{network="ETH"}'
    else:
        raise NotImplementedError()

    start_bidirectional_export(start, export_snapshot, data_query)


@time_tracking
def export_snapshot(snapshot, ts):
    start = time()
    from yearn.yearn import _yearn
    block = closest_block_after_timestamp(ts, wait_for=True)
    assert block is not None, "no block after timestamp found"
    _yearn().export(block, ts)
    logger.info("exported vaults snapshot %s took %.3fs", snapshot, time() - start)
