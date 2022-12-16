"""Block header store.

"""
import abc
from typing import Tuple

import pandas as pd
from pyparsing import Optional


class BlockDataStore(abc.ABC):
    """Persistent storage interface to store aby processed data from blockchains.

    Store any block data that is block oriented

    - Input is indexed by the block number

    - Input and output as py:class:`pd.DataFrame`

    - Append writes with chain reorganisation support

    - Partial tail reads

    Used for

    - Cache downlaoded block headers and timestamps,
      so you do not need to fetch them again over JSON-RPC when restarting an application.

    - Cache downlaoded trades

    The input data

    - Must be py:class:`pd.DataFrame`

    - Must have key `block_number`

    - Must have key `partition` if the storage implementation does partitioning.
      This can be the block number rounded down to the nearest partition chunk.
    """

    def load(self, since_block_number: int = 0) -> pd.DataFrame:
        """Load data from the store.

        :param since_block_number:
            Return only blocks after this (inclusive).

            The actual read datasets may contain more blocks
            due to partition boundaries.

        :return:
            Data read from the store.
        """

    def save(self, data: pd.DataFrame):
        """Save to the store."""

    def save_incremental(self, data: pd.DataFrame) -> Tuple[int, int]:
        """Save the latest data to the store.

        Write the minimum amount of data to the disk we think is

        - Valid

        - Needs to be written to keep partitions intact

        Usually this is data worth of two partitions.

        :param data:
            Must have column 'block_number'. Must have
            column `partition` if partitioning is supported.

        :return:
            Block range written (inclusive).
        """

    def peak_last_block(self) -> Optional[int]:
        """Get the block number of the last data entry stored.

        :return:
            None if the store is empty.
        """