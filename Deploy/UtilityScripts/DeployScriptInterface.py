# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployScriptInterface
#   Type: Interface
#   Author: David Mehoves
#   Copyright: Aspire Digital
#   Purpose: An interface to ensure standards od Deploy Scripts
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import abc


class DeployScriptInterface(abc.ABC):

    @abc.abstractclassmethod
    def run():
        pass

    @abc.abstractclassmethod
    def __str__():
        pass

    @abc.abstractclassmethod
    def __init__():
        pass
