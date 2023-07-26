# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployScriptInterface
#   Type: Interface
#   Author: David Mehoves
#   Copyright: Aspire Digital
#   Purpose: An interface to ensure standards of Deploy Scripts
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import abc


class DeployScriptInterface(abc.ABC):

    @abc.abstractclassmethod
    def run():
        pass
