# =========================================================================================================
#
#     Name: StandardLogging
#     Type: Class
#     Author: David Mehoves
#     Copyright: Aspire Digital
#     Purpose:  Standard Logging Class for Error,
#               Custom Tables, and Quotes
#
# =========================================================================================================

import sys


class StandardLogging:

    @staticmethod
    def start(script_name, msg=""):
        """
        To be called at the enterance to a module or class
        Args:
            script_name (str): name of script being called
            explanation (str): purpose of script
        """

        title = script_name + ",  Script Start:"
        message = "Message:  " + msg
        Log.Info(title, message)

    @staticmethod
    def info(script_name, msg):
        """
        Displays a formatted message to the logs
        Args:
            message (str): Custom message to display
        """
        title = script_name + ", Info:"
        message = """
        Script Name:  {}
        Message:  {}
        """.format(
            script_name,
            msg
        )
        Log.Info(title, message)

    @staticmethod
    def error(script_name, msg=""):
        '''
        To be called when there is a error
        case in the code.
        Args:
            customMessage (str): Display more info to the user
        '''
        title = script_name + ",  Error:"
        message = """
        Script Name:  {}
        Message:  {}
        """.format(
            script_name,
            msg
        )
        Log.Error(title, message)

    @staticmethod
    def exception(script_name, msg=""):
        '''
        Method to be caleld directly under the
        'except' in a try/except block.
        Args:
            customMessage (str): Display more info to the user
        '''
        title = script_name + ",  Exception:"
        exc_info = sys.exc_info()
        message = """
        Script Name:  {}
        Message:  {}
        Line:  {}
        Error:  {}
        """.format(
            script_name,
            msg,
            exc_info[2].tb_lineno,
            exc_info[1]
        )
        Log.Error(title, message)
        return sys.argv[0]

    @staticmethod
    def table(script_name, query, response=""):
        '''
        Method to be called inside a script whenever a table is accessed.
        Args:
            query (str): query string
            response (str): response from the query
        '''
        # extract name
        try:
            query_list = query.split(' ')
            query_list_lower = [q.lower() for q in query_list]
            tablename_index = query_list_lower.index('from') + 1
            table_name = query_list[tablename_index]
        except Exception as e:
            Log.Error(
                "StandardLogging Script:",
                """
                Error extracting table name from query
                Error: {}
                """.format(str(e))
            )
            table_name = "unknown"
        title = table_name + ",  Table:"
        message = """
        Script Name:  {}
        Table Name:  {}
        Query:  {}
        Response:  {}
        """.format(
            script_name,
            table_name,
            query,
            str(response)
        )
        Log.Info(title, message)

    @staticmethod
    def quote(script_name, quote, msg=""):
        '''
        Method to be called at the top of any
        script that adjusts or accesses a quote.
        Args:
            quote (context.Quote): reference to the quote
            msg (str): to include what is accessed / modified
        '''
        title = str(quote.QuoteNumber) + ",  Quote:"
        message = """
        Script Name:  {}
        Message:  {}
        Quote Status:  {}
        Quote Owner ID:  {}
        Quote ID:  {}
        Quote Number:  {}
        Created:  {}
        Modified:  {}
        """.format(
            script_name,
            msg,
            quote.StatusName,
            str(quote.OwnerId),
            str(quote.Id),
            str(quote.QuoteNumber),
            str(quote.DateCreated),
            str(quote.DateModified),
        )
        Log.Info(title, message)