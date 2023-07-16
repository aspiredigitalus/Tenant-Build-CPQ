# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployScriptInterface
#   Type: Interface
#   Copyright: Aspire Digital
#   Purpose: An interface to ensure standards od Deploy Scripts
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import abc


class DeployScriptInterface(abc.ABC):

    @abc.abstractclassmethod
    def run():
        pass
